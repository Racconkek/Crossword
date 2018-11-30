import wx
from Parser import Parser
from main import Crossword
import os

class CrosswordApp(wx.Frame):
    def __init__(self, parent, title, width, height):
        wx.Frame.__init__(self, parent, title = title, size = (500 + 5 * width, 500 + 5 * height))
        self.width = width
        self.height = height
        self.vocabulary = ""
        self.solution = None
        self.init_widgets()
        self.init_menu()
        self.Centre()
        self.Show()

    def init_menu(self):
        menu_bar = wx.MenuBar()
        saveMenu = wx.Menu()
        applyItem = saveMenu.Append(wx.ID_APPLY, 'Apply geometry', 'Saves created crossword geometry')
        solveItem = saveMenu.Append(wx.ID_CONVERT, 'Solve', 'Makes crossword solution')
        showItem = saveMenu.Append(wx.ID_PASTE, 'Show', 'Shows crossword solution')
        clearItem = saveMenu.Append(wx.ID_CLEAR, 'Clear board', 'Clears the board')
        chooseVocItem = saveMenu.Append(wx.ID_EDIT, 'Choose vocabulary', 'Chooses vocabulary')
        helpItem = saveMenu.Append(wx.ID_HELP, 'Help', 'Gives instructions')
        menu_bar.Append(saveMenu, '&Actions')
        self.SetMenuBar(menu_bar)
        self.Bind(wx.EVT_MENU, self.save_geometry, applyItem)
        self.Bind(wx.EVT_MENU, self.get_help, helpItem)
        self.Bind(wx.EVT_MENU, self.solve_cross, solveItem)
        self.Bind(wx.EVT_MENU, self.show_solution, showItem)
        self.Bind(wx.EVT_MENU, self.clear_board, clearItem)
        self.Bind(wx.EVT_MENU, self.choose_voc, chooseVocItem)

    def save_geometry(self, event):
        values = []
        for i in range(len(self.buttons)):
            values.append([])
            for j in range(len(self.buttons[0])):
                values[i].append(self.buttons[i][j].GetLabel())
        with open("current_geom.txt", 'w') as file:
            result = ""
            for i in range(len(values)):
                result += "".join(values[i]) + '\n'
            file.write(result)

    def get_help(self, event):
        text = "Push o buttons, where should be letters,\n" \
               "0 - for horizontal words\n" \
               "1 - for vertical words\n" \
               "2 - for intersections of words."
        dial = wx.MessageDialog(None, text, 'Help', wx.OK)
        dial.ShowModal()

    def solve_cross(self, event):
        parser = Parser()
        try:
            geometry = parser.parse_from_txt("current_geom.txt")
            graph = parser.parse_to_graf(geometry)
            self.solution = Crossword.solve(graph, "ruwords.txt")
        except Exception:
            dial = wx.MessageDialog(None, "Incorrect geometry", 'Exception', wx.OK)
            dial.ShowModal()

    def show_solution(self, event):
        if self.solution is None:
            text = "There is No solution"
        else:
            vertical = ""
            horizontal = ""
            for node, word in self.solution.items():
                if node.is_horizontal:
                    horizontal += word + '\n'
                else:
                    vertical += word + '\n'
            text = "\tVertical words:\n" + vertical + "\tHorizontal words:\n" + horizontal
        dial = wx.MessageDialog(None, text, 'Solution', wx.OK)
        dial.ShowModal()

    def clear_board(self, event):
        for i in range(len(self.buttons)):
            for j in range(len(self.buttons[0])):
                self.buttons[i][j].SetLabel("-")

    def choose_voc(self, event):
        wildcard = "TXT file (*.txt) | *.txt"
        dial = wx.FileDialog(self, message="Choose a vocabulary file",
            defaultDir=os.getcwd(),
            defaultFile="ruwords.txt",
            wildcard=wildcard)
        result = dial.ShowModal()
        if result == wx.ID_CANCEL or wx.ID_EXIT:
            self.vocabulary = 'rewords.txt'
        else:
            self.vocabulary = str(dial.GetPaths())

    def init_widgets(self):
        self.buttons = []
        panel = wx.Panel(self)
        hbox = wx.BoxSizer(wx.VERTICAL)
        cells = []
        fgs = wx.FlexGridSizer(self.width, self.height, 2, 2)
        for i in range(self.height):
            self.buttons.append([])
            for j in range(self.width):
                crossword_cell = wx.Button(panel, size=(500/self.width, 500/self.height))
                crossword_cell.SetLabel("-")
                crossword_cell.Bind(wx.EVT_BUTTON, self.increase_value)
                self.buttons[i].append(crossword_cell)
                cells.append((crossword_cell, 1, wx.EXPAND))
        for i in range(self.height):
            fgs.AddGrowableCol(i, 1)
        for i in range(self.width):
            fgs.AddGrowableRow(i, 0)
        fgs.AddMany(cells)
        hbox.Add(fgs, proportion=1, flag=wx.EXPAND, border=2)
        panel.SetSizer(hbox)

    def increase_value(self, event):
        button = event.GetEventObject()
        label = button.GetLabel()
        if label == '-':
            label = 0
        else:
            label = (int(label) + 1) % 3
        button.SetLabel(str(label))


def main():
    app = wx.App()
    cr = CrosswordApp(None, "Geometry Creator", 10, 10)
    app.MainLoop()


if __name__ == '__main__':
    main()