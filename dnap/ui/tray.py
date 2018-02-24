import wx
import wx.adv
from io import BytesIO

from .util import create_menu_item, crop_text
from ..util import resource_path


# FIXME: Should remain the same color when clicked in dark mode
TRAY_ICON_WHITE = resource_path("resources/icon/white/128.png")
TRAY_ICON_BLACK = resource_path("resources/icon/black/128.png")
THUMB_SIZE = 128
NOP = lambda event: None


# FIXME
import os
import json
import requests
def latest_scraped():
    with open(os.path.expanduser("~/.dnap"), "r") as f:
        releases = json.load(f)
    #return [r for r in releases if r["title"] == "MOTHER 2"][0]
    return max(releases, key=lambda r: r["first_seen"])


class DnapTaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame):
        super(DnapTaskBarIcon, self).__init__()
        self.frame = frame
        self.set_icon(TRAY_ICON_WHITE)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, "Browse records\tCTRL+B", NOP)
        create_menu_item(menu, "Preferences\tCTRL+,", NOP)
        self.create_release_menu_item(menu, latest_scraped())
        menu.AppendSeparator()
        create_menu_item(menu, "Exit", self.on_exit)
        return menu

    # FIXME: in case of no releases
    def create_release_menu_item(self, menu, release):
        menu.AppendSeparator()
        create_menu_item(menu, "Latest release:", NOP).Enable(False)
        create_menu_item(menu, crop_text(release["title"], limit=45), NOP).Enable(False)

        menu_item = wx.MenuItem(menu, -1, "%s on %s" % (release["price"], release["source"]))
        menu.Bind(wx.EVT_MENU, NOP, id=menu_item.GetId())

        # FIXME: cache manager
        request = requests.get(release["picture"])
        image = wx.Image(BytesIO(request.content))
        ratio = image.Width / image.Height
        if image.Width > image.Height:
            image.Rescale(THUMB_SIZE, THUMB_SIZE / ratio, quality=wx.IMAGE_QUALITY_HIGH)
        else:
            image.Rescale(THUMB_SIZE * ratio, THUMB_SIZE, quality=wx.IMAGE_QUALITY_HIGH)
        menu_item.SetBitmap(wx.Bitmap(image))

        menu.Append(menu_item)
        return menu_item


    def set_icon(self, path):
        icon = wx.Icon(path, wx.BITMAP_TYPE_PNG)
        self.SetIcon(icon, "DNAP")

    def on_left_down(self, event):
        pass

    def on_exit(self, event):
        wx.CallAfter(self.Destroy)
        self.frame.Close()
