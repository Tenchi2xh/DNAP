import wx

def create_menu_item(menu, title, callback):
    menu_item = wx.MenuItem(menu, -1, title)
    menu.Bind(wx.EVT_MENU, callback, id=menu_item.GetId())
    menu.Append(menu_item)
    return menu_item

def crop_text(text, limit=15, suffix="..."):
    return text if len(text) <= limit else text[:limit] + suffix
