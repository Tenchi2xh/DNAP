import notify2


def notify(title, subtitle, message, icon=""):
	notification = notify2.Notification(title,
		message="%s\n%s" % (subtitle, message),
		icon=icon
	)
	notification.show()
