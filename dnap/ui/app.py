import wx
import sys

from .tray import DnapTaskBarIcon


class Dnap(wx.App):
    def OnInit(self):
        frame = wx.Frame(None)
        self.SetTopWindow(frame)
        self.tray = DnapTaskBarIcon(frame)
        return True


def start():
    app = Dnap(False)

    if sys.platform == "darwin":
        from .platforms import macos
        timer = wx.Timer(app)
        app.Bind(wx.EVT_TIMER, lambda _: macos.update_icon(app.tray), timer)
        timer.Start(1000)

    app.MainLoop()
