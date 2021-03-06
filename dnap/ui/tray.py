import wx
import wx.adv
import webbrowser

from .browse import BrowseFrame
from .util import create_menu_item, crop_text, get_bitmap
from ..util import resource_path, latest_scraped, last_scrape_result


# FIXME: Should remain the same color when clicked in dark mode in Mac OS
TRAY_ICON_WHITE = resource_path("resources/icon/white/128.png")
TRAY_ICON_BLACK = resource_path("resources/icon/black/128.png")
THUMB_SIZE = 128
NOP = lambda event: None


class DnapTaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame):
        super(DnapTaskBarIcon, self).__init__()
        self.frame = frame
        self.menu = None
        self.set_icon(TRAY_ICON_WHITE)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_UP, lambda _: self.PopupMenu(self.CreatePopupMenu()))

    def CreatePopupMenu(self):
        result = last_scrape_result()
        if result is not None:
            new_releases = "%d new release%s" % (result, "s" if result > 0 else "")
            last_scrape_message = "Last scrape: %s" % (new_releases if result else "no new releases")
        else:
            last_scrape_message = "Waiting for first scrape..."

        menu = wx.Menu()

        browse_menu = create_menu_item(menu, "Browse records\tCTRL+B", self.browse)
        if hasattr(self, "browse_frame") and self.browse_frame:
            browse_menu.Enable(False)
        create_menu_item(menu, "Preferences\tCTRL+,", NOP)

        menu.AppendSeparator()
        create_menu_item(menu, last_scrape_message, NOP).Enable(False)
        latest_release = latest_scraped()
        if latest_release:
            self.create_release_menu_item(menu, latest_release)

        menu.AppendSeparator()
        create_menu_item(menu, "Exit", self.on_exit)
        return menu

    def create_release_menu_item(self, menu, release):
        if not release:
            return
        menu.AppendSeparator()
        create_menu_item(menu, "Latest release:", NOP).Enable(False)
        create_menu_item(menu, crop_text(release["title"], limit=45), NOP).Enable(False)

        menu_item = wx.MenuItem(menu, -1, "%s on %s" % (release["price"], release["source"]))
        menu.Bind(wx.EVT_MENU, lambda e: webbrowser.open(release["link"]), id=menu_item.GetId())

        menu_item.SetBitmap(get_bitmap(release, resize_width=THUMB_SIZE))

        menu.Append(menu_item)


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
