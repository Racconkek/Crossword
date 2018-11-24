import wx

class Editor(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(parent, title = title, size = (500, 500))
