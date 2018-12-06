import wx
from CrosswordGUI import CrosswordApp


def main():
    app = wx.App()
    a = CrosswordApp(None, "GUI")
    app.MainLoop()


if __name__ == '__main__':
    main()