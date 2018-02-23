#!/usr/bin/env python3

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
        from AppKit import NSUserDefaults
        from apscheduler.schedulers.background import BackgroundScheduler
        from .tray import TRAY_ICON_BLACK, TRAY_ICON_WHITE

        def is_dark():
            return NSUserDefaults.standardUserDefaults().stringForKey_("AppleInterfaceStyle") == "Dark"

        dark = None

        def update_icon():
            nonlocal dark
            if dark != is_dark():
                dark = not dark
                if dark:
                    app.tray.set_icon(TRAY_ICON_WHITE)
                else:
                    app.tray.set_icon(TRAY_ICON_BLACK)

        scheduler = BackgroundScheduler()
        scheduler.start()
        scheduler.add_job(update_icon, trigger="cron", second="*")

    app.MainLoop()


if __name__ == "__main__":
    start()
