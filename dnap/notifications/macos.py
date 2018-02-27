from AppKit import NSImage, NSUserNotification, NSUserNotificationCenter


def notify(title, subtitle, message, icon=None):
    notification = NSUserNotification.alloc().init()
    notification.setTitle_(title)
    notification.setSubtitle_(subtitle)
    notification.setInformativeText_(message)
    if icon:
        notification.setValue_forKey_(NSImage.alloc().initWithContentsOfFile_(icon), "_identityImage")

    NSUserNotificationCenter.defaultUserNotificationCenter().deliverNotification_(notification)
