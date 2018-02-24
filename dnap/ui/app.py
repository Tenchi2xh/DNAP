import wx
import sys

from .tray import DnapTaskBarIcon
from ..util import add_cron


class Dnap(wx.App):
    def OnInit(self):
        frame = wx.Frame(None)
        self.SetTopWindow(frame)
        self.tray = DnapTaskBarIcon(frame)
        return True


def start(scheduler):
    app = Dnap(False)

    if sys.platform == "darwin":
        from .platforms import macos
        add_cron(scheduler, macos.update_icon, {"second": "*"}, args=[app.tray])

    app.MainLoop()
