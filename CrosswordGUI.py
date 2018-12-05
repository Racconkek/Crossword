import wx

from CrosswordEditorGUI import CrosswordEditor


class CrosswordApp(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(200, 200))
        self.init_widgets()
        self.Centre()
        self.Show()

    def init_widgets(self):
        panel = wx.Panel(self)
        sizer = wx.GridSizer(3,2, 1, 1)
        self.width_value = wx.TextCtrl(panel, style=wx.TE_LEFT)
        self.height_value = wx.TextCtrl(panel, style=wx.TE_LEFT)
        width_text =  wx.StaticText(panel, label='Width')
        height_text =  wx.StaticText(panel, label='Height')
        open_button = wx.Button(panel, label = "Open Editor")
        open_button.Bind(wx.EVT_BUTTON, self.open_editor)
        sizer.AddMany([(width_text, 1, wx.EXPAND), (self.width_value, 1, wx.EXPAND),
                       (height_text, 1, wx.EXPAND), (self.height_value, 1, wx.EXPAND),
                       (open_button, 1, wx.EXPAND)])
        panel.SetSizer(sizer)

    def open_editor(self, event):
        try:
            width = int(self.width_value.GetValue())
            height = int(self.height_value.GetValue())
            if width >= 100 or height >= 100:
                raise Exception("Too big crossword")
            cr = CrosswordEditor(None, "Geometry Creator", width, height)
        except Exception:
            dial = wx.MessageDialog(None, "Incorrect crossword size.\n", 'Exception', wx.OK)
            dial.ShowModal()


def main():
    app = wx.App()
    a = CrosswordApp(None, "GUI")
    app.MainLoop()


if __name__ == '__main__':
    main()