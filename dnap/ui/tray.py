import wx
import os
import json
import wx.adv
import requests
import webbrowser
from io import BytesIO

from .browse import BrowseFrame
from .util import create_menu_item, crop_text, get_bitmap
from ..util import resource_path, get_picture, latest_scraped, last_scrape_result
from .. import cache_releases_path, cache_result_path


# FIXME: Should remain the same color when clicked in dark mode in Mac OS
TRAY_ICON_WHITE = resource_path("resources/icon/white/128.png")
TRAY_ICON_BLACK = resource_path("resources/icon/black/128.png")
THUMB_SIZE = 128
NOP = lambda event: None


class DnapTaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame):
        super(DnapTaskBarIcon, self).__init__()
        self.frame = frame
        self.set_icon(TRAY_ICON_WHITE)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

    def CreatePopupMenu(self):
        result = last_scrape_result()
        new_releases = "%d new release%s" % (result, "s" if result > 0 else "")
        last_scrape_message = "Last scrape: %s" % (new_releases if result else "no new releases")

        menu = wx.Menu()

        browse_menu = create_menu_item(menu, "Browse records\tCTRL+B", self.browse)
        if hasattr(self, "browse_frame") and self.browse_frame:
            browse_menu.Enable(False)
        create_menu_item(menu, "Preferences\tCTRL+,", NOP)

        menu.AppendSeparator()
        create_menu_item(menu, last_scrape_message, NOP).Enable(False)
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
        menu.Bind(wx.EVT_MENU, lambda e: webbrowser.open(release["link"]), id=menu_item.GetId())

        menu_item.SetBitmap(get_bitmap(release, resize_width=THUMB_SIZE))

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

    def browse(self, event=None):
        self.browse_frame = BrowseFrame(self.frame)
        self.browse_frame.Bind(wx.EVT_CLOSE, lambda _: self.browse_frame.Destroy())
        self.browse_frame.Show()
