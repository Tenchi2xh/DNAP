from AppKit import NSUserDefaults
from ..tray import TRAY_ICON_BLACK, TRAY_ICON_WHITE

def is_dark():
    return NSUserDefaults.standardUserDefaults().stringForKey_("AppleInterfaceStyle") == "Dark"

dark = None

def update_icon(tray):
    global dark
    if dark != is_dark():
        dark = not dark
        if dark:
            tray.set_icon(TRAY_ICON_WHITE)
        else:
            tray.set_icon(TRAY_ICON_BLACK)
