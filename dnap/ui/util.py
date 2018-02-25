import wx

from ..util import get_picture


def create_menu_item(menu, title, callback):
    menu_item = wx.MenuItem(menu, -1, title)
    menu.Bind(wx.EVT_MENU, callback, id=menu_item.GetId())
    menu.Append(menu_item)
    return menu_item


def crop_text(text, limit=15, suffix="..."):
    return text if len(text) <= limit else text[:limit] + suffix


def get_bitmap(release, resize_width=None):
    image = wx.Image(get_picture(release))

    ratio = image.Width / image.Height
    if resize_width and image.Width > image.Height:
        image.Rescale(resize_width, resize_width / ratio, quality=wx.IMAGE_QUALITY_HIGH)
    elif resize_width:
        image.Rescale(resize_width * ratio, resize_width, quality=wx.IMAGE_QUALITY_HIGH)

    # Ensure it's square by adding white borders
    if resize_width and image.Width != image.Height:
        image.Resize(
            size=wx.Size(resize_width, resize_width),
            pos=wx.Point((resize_width - image.Width) / 2, (resize_width - image.Height) / 2),
            red=255, green=255, blue=255
        )

    return wx.Bitmap(image)
