import wx
from Parser import Parser
from main import Crossword
import os

class CrosswordApp(wx.Frame):
    def __init__(self, parent, title, width, height):
        wx.Frame.__init__(self, parent, title = title, size = (500, 500))
        self.width = width
        self.height = height
        self.vocabulary = "sources/ruwords.txt"
        self.solution = None
        self.current_geom = None
        self.init_widgets()
        self.init_menu()
        self.Centre()
        self.Show()

    def init_menu(self):
        menu_bar = wx.MenuBar()
        actions_menu = wx.Menu()
        help_menu = wx.Menu()
        apply_item = actions_menu.Append(wx.ID_APPLY, 'Apply geometry', 'Saves created crossword geometry')
        solve_item = actions_menu.Append(wx.ID_CONVERT, 'Solve', 'Makes crossword solution')
        show_item = actions_menu.Append(wx.ID_PASTE, 'Show', 'Shows crossword solution')
        clear_item = actions_menu.Append(wx.ID_CLEAR, 'Clear board', 'Clears the board')
        choose_voc_item = actions_menu.Append(wx.ID_EDIT, 'Choose vocabulary', 'Chooses vocabulary')
        help_item = help_menu.Append(wx.ID_HELP, 'Help', 'Gives instructions')
        menu_bar.Append(actions_menu, '&Actions')
        menu_bar.Append(help_menu, '&Help')
        self.SetMenuBar(menu_bar)
        self.Bind(wx.EVT_MENU, self.save_geometry, apply_item)
        self.Bind(wx.EVT_MENU, self.get_help, help_item )
        self.Bind(wx.EVT_MENU, self.solve_cross, solve_item)
        self.Bind(wx.EVT_MENU, self.show_solution, show_item)
        self.Bind(wx.EVT_MENU, self.clear_board,  clear_item)
        self.Bind(wx.EVT_MENU, self.choose_voc, choose_voc_item)

    def save_geometry(self, event):
        values = []
        for i in range(len(self.buttons)):
            values.append([])
            for j in range(len(self.buttons[0])):
                values[i].append(self.buttons[i][j].GetLabel())
        self.current_geom = values
        # with open("sources/current_geom.txt", 'w') as file:
        #     result = ""
        #     for i in range(len(values)):
        #         result += "".join(values[i]) + '\n'
        #     file.write(result)

    def get_help(self, event):
        text = '''
        Push on buttons, where should be letters:
            0 - for horizontal words
            1 - for vertical words
            2 - for intersections of words.
        Buttons:
            Apply geometry - saves your current geometry
            Solve - Makes crossword solution
            Show - Shows crossword solution
            Clear board - Clears the crossword board
            Choose vocabulary - Opens file explorer and let you choose the vocabulary file
            Help - Gives instructions
        '''
        dial = wx.MessageDialog(None, text, 'Help', wx.OK)
        dial.ShowModal()

    def solve_cross(self, event):
        parser = Parser()
        try:
            graph = parser.parse_to_graf(self.current_geom)
            self.solution = Crossword.solve(graph, self.vocabulary)
        except Exception as e:
            dial = wx.MessageDialog(None, "Incorrect geometry\n" + str(e), 'Exception', wx.OK)
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
            defaultFile="sources/ruwords.txt",
            wildcard=wildcard)
        result = dial.ShowModal()
        self.vocabulary = str(dial.GetPaths())

    def init_widgets(self):
        self.buttons = []
        panel = wx.Panel(self)
        sizer = wx.GridSizer(self.width, self.height, 1, 1)
        cells = []
        for i in range(self.height):
            self.buttons.append([])
            for j in range(self.width):
                crossword_cell = wx.Button(panel)
                crossword_cell.SetLabel("-")
                crossword_cell.Bind(wx.EVT_BUTTON, self.increase_value)
                self.buttons[i].append(crossword_cell)
                cells.append((crossword_cell, 1, wx.EXPAND))
        sizer.AddMany(cells)
        panel.SetSizer(sizer)

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