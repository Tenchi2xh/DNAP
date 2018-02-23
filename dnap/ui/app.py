import wx
import sys

from .tray import DnapTaskBarIcon


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
        scheduler.add_job(macos.update_icon, trigger="cron", args=[app.tray], second="*")

    app.MainLoop()
