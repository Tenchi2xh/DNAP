import wx
import sys
import time
import webbrowser
from threading import Thread
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin

from .util import get_bitmap
from ..util import get_releases, get_picture


THUMB_SIZE = 100
LOOK_AHEAD = 30

class BrowseFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1,
            title="DNAP",
            style=wx.RESIZE_BORDER | wx.CLOSE_BOX | wx.CAPTION | wx.CLIP_CHILDREN | wx.STAY_ON_TOP
        )

        self.adding_items = False
        self.thread = None

        self.releases = sorted(get_releases(), key=lambda release: -release["first_seen"])
        self.labels = ["all"] + sorted(list(set([release["source"] for release in self.releases])))
        self.current_label = None

        self.init_position(435, 730)
        self.init_content()
        self.show_releases("all")

    def init_position(self, width, height):
        # FIXME: Find current display id
        display_area = wx.Display(0).GetClientArea()
        display_width, display_height = display_area.GetWidth(), display_area.GetHeight()

        self.SetSize((width, height))

        if sys.platform == "darwin":
            # Top-right
            title_bar_height = self.GetRect().height - self.GetClientRect().height
            position = (display_width - width, title_bar_height)
        else:
            # Bottom-right
            position = (display_width - width, display_height - height)

        self.SetPosition(position)

    def init_content(self):
        sizer = wx.BoxSizer(wx.VERTICAL)

        combo = wx.Choice(self, -1, choices=self.labels)
        combo.SetSelection(0)
        self.Bind(wx.EVT_CHOICE, lambda e: self.show_releases(e.GetString()))

        self.init_list()
        self.image_list = wx.ImageList(THUMB_SIZE, THUMB_SIZE)
        self.list.SetImageList(self.image_list, wx.IMAGE_LIST_SMALL)

        sizer.Add(combo, flag=wx.EXPAND | wx.ALL, border=5)
        sizer.Add(self.list, proportion=1, flag=wx.EXPAND | wx.ALL ^ wx.TOP, border=5)

        self.SetSizer(sizer)

    def init_list(self):
        class AutoWidthListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin):
            def __init__(self, *args, **kwargs):
                wx.ListCtrl.__init__(self, *args, **kwargs)
                ListCtrlAutoWidthMixin.__init__(self)

        self.list = AutoWidthListCtrl(self, style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_NO_HEADER)
        self.list.setResizeColumn(2)
        self.list.Bind(wx.EVT_SCROLLWIN, self.handle_scroll)
        self.list.Bind(wx.EVT_MOUSEWHEEL, self.handle_scroll)
        self.list.Bind(wx.EVT_MOTION, self.handle_hover)
        self.list.Bind(wx.EVT_LEFT_UP, self.handle_click)

        cover_column = wx.ListItem()
        cover_column.SetMask(wx.LIST_MASK_TEXT)
        cover_column.SetText("Cover")
        cover_column.SetWidth(THUMB_SIZE + 8)
        self.list.InsertColumn(0, cover_column)

        album_column = wx.ListItem()
        album_column.SetMask(wx.LIST_MASK_TEXT)
        album_column.SetText("Album")
        album_column.SetWidth(210)
        self.list.InsertColumn(1, album_column)

        price_column = wx.ListItem()
        price_column.SetMask(wx.LIST_MASK_TEXT)
        price_column.SetAlign(wx.LIST_FORMAT_RIGHT)
        price_column.SetText("Price")
        price_column.SetWidth(70)
        self.list.InsertColumn(2, price_column)

        self.list.setResizeColumn(2)

    def handle_scroll(self, event):
        event.Skip()

        if self.list.GetItemCount() == len(self.current_releases):
            return

        pos = self.list.GetScrollPos(wx.VERTICAL)
        if pos >= self.list.GetItemCount() - LOOK_AHEAD:
            if self.thread and self.thread.is_alive():
                return
            self.thread = Thread(target=self.add_releases, args=(LOOK_AHEAD,))
            self.thread.start()

    def add_release(self, release, release_index):
        bmp = get_bitmap(release, resize_width=THUMB_SIZE)
        image_index = self.image_list.Add(bmp)
        index = self.list.InsertItem((1 << 31) - 1, image_index)
        self.list.SetItem(index, 1, "  %s – %s" % (release["source"], release["title"]))
        self.list.SetItem(index, 2, release["price"])
        self.list.SetItemData(index, release_index)

    def add_releases(self, count):
        if self.adding_items:
            return
        self.adding_items = True
        log.debug("Adding %d more items to list..." % count)

        start = self.list.GetItemCount()
        end = min((start + count, len(self.current_releases)))
        for i in range(start, end):
            if not self.adding_items:
                break
            get_picture(self.current_releases[i])  # Preloading the image while still in the thread
            wx.CallAfter(self.add_release, self.current_releases[i], i)  # Called on main thread
            time.sleep(0.01)

        self.adding_items = False

    def show_releases(self, label):
        if label == self.current_label:
            return

        if self.thread and self.thread.is_alive():
            self.adding_items = False
            while self.thread.is_alive():
                time.sleep(0.01)

        self.current_label = label

        if label == "all":
            self.current_releases = self.releases
        else:
            self.current_releases = [release for release in self.releases if release["source"] == label]

        self.list.DeleteAllItems()
        self.image_list.RemoveAll()

        to_load = self.list.GetCountPerPage() + LOOK_AHEAD
        self.thread = Thread(target=self.add_releases, args=(to_load,))
        self.thread.start()

    def hovered_index(self, event):
        pos = event.GetPosition()
        item = self.list.HitTest(pos)
        if item and len(item) > 0:
            index = item[0]
            if index >= 0:
                return index

    def handle_hover(self, event):
        event.Skip()
        index = self.hovered_index(event)
        if index is not None and not self.list.IsSelected(index):
            self.list.Select(index)
            self.Raise()
            self.list.SetFocus()

    def handle_click(self, event):
        event.Skip()
        index = self.hovered_index(event)
        if index is not None:
            release_index = self.list.GetItemData(index)
            release = self.current_releases[release_index]
            webbrowser.open(release["link"])
