import os
import tempfile
from PIL import Image
from win10toast import ToastNotifier

def notify(title, subtitle, message, icon=None):
    toaster = ToastNotifier()
    text = "%s\n%s" % (subtitle, message)

    if icon:
        tf = tempfile.NamedTemporaryFile(suffix=".ico", delete=False)
        tf.close()
        image = Image.open(icon)
        image.save(tf.name)
        toaster.show_toast(title, text, icon_path=tf.name, duration=10)
        os.unlink(tf.name)
    else:
        toaster.show_toast(title, text, duration=10, threaded=True)
