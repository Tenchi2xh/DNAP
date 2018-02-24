import Foundation
from AppKit import NSImage, NSUserNotification, NSUserNotificationCenter


def notify(title, subtitle, message, icon=None):
    notification = NSUserNotification.alloc().init()
    notification.setTitle_(title)
    notification.setSubtitle_(subtitle)
    notification.setInformativeText_(message)
    if icon:
        notification.setValue_forKey_(NSImage.alloc().initWithContentsOfFile_(icon), "_identityImage")

    notification.setDeliveryDate_(Foundation.NSDate.dateWithTimeInterval_sinceDate_(0, Foundation.NSDate.date()))
    NSUserNotificationCenter.defaultUserNotificationCenter().scheduleNotification_(notification)

notify("Test", "Hello", "This is some text.", "resources/icon/black/128.png")
