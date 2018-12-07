import wx
from Parser import Parser
from Solution import Crossword
import os

class CrosswordEditor(wx.Frame):
    def __init__(self, parent, title, width, height):
        wx.Frame.__init__(self, parent, title = title, size = (500, 500))
        self.width = width
        self.height = height
        self.vocabulary = "sources/ruwords.txt"
        self.solution = None
        self.coord_to_word = None
        self.current_geom = None
        self.init_widgets()
        self.init_menu()
        self.Centre()
        self.Show()

    def init_menu(self):
        menu_bar = wx.MenuBar()
        actions_menu = wx.Menu()
        help_menu = wx.Menu()
        solution_menu = wx.Menu()
        # apply_item = actions_menu.Append(wx.ID_APPLY, 'Apply geometry', 'Saves created crossword geometry')
        solve_item = actions_menu.Append(wx.ID_CONVERT, 'Solve', 'Makes crossword solution')
        show_in_cells_item = solution_menu.Append(wx.ID_PASTE, 'In cells', 'Shows crossword solution')
        show_in_list_item = solution_menu.Append(wx.ID_PASTE, 'In list', 'Shows crossword solution')
        clear_item = actions_menu.Append(wx.ID_CLEAR, 'Clear board', 'Clears the board')
        choose_voc_item = actions_menu.Append(wx.ID_EDIT, 'Choose vocabulary', 'Chooses vocabulary')
        help_item = help_menu.Append(wx.ID_HELP, 'Help', 'Gives instructions')
        menu_bar.Append(actions_menu, '&Actions')
        menu_bar.Append(solution_menu, '&Solutions')
        menu_bar.Append(help_menu, '&Help')

        self.SetMenuBar(menu_bar)
        # self.Bind(wx.EVT_MENU, self.save_geometry, apply_item)
        self.Bind(wx.EVT_MENU, self.get_help, help_item )
        self.Bind(wx.EVT_MENU, self.solve_cross, solve_item)
        self.Bind(wx.EVT_MENU, self.show_solution_in_cells, show_in_cells_item)
        self.Bind(wx.EVT_BUTTON, self.show_solution_in_list, show_in_list_item)
        self.Bind(wx.EVT_MENU, self.clear_board,  clear_item)
        self.Bind(wx.EVT_MENU, self.choose_voc, choose_voc_item)

    def save_geometry(self):
        values = []
        for i in range(len(self.buttons)):
            values.append([])
            for j in range(len(self.buttons[0])):
                values[i].append(self.buttons[i][j].GetLabel())
        self.current_geom = values

    def get_help(self, event):
        text = '''
        Push on buttons, where should be letters:
            "-" - no letter
            "*" - should be letter.
        Buttons:
            Solve - Makes crossword solution
            Show solution- Shows crossword solution
            Clear board - Clears the crossword board
            Choose vocabulary - Opens file explorer and let you choose the vocabulary file
            Help - Gives instructions
        '''
        dial = wx.MessageDialog(None, text, 'Help', wx.OK)
        dial.ShowModal()

    def solve_cross(self, event):
        self.save_geometry()
        parser = Parser()
        try:
            graph = parser.parse_to_graph(parser.parse_from_gui(self.current_geom))
            self.solution, self.coord_to_word = Crossword.make_solution(graph, self.vocabulary)
        except Exception as e:
            dial = wx.MessageDialog(None, "Incorrect geometry\n" + str(e), 'Exception', wx.OK)
            dial.ShowModal()

    def show_solution_in_cells(self, event):
        res = CrosswordResult(self, "Result", self.width, self.height, (self.solution, self.coord_to_word))

    def show_solution_in_list(self, event):
        
        dial = wx.MessageDialog(None, "Incorrect geometry\n" , 'Solution', wx.OK)
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
            label = '*'
        else:
            label = '-'
        button.SetLabel(str(label))


class CrosswordResult(wx.Frame):
    def __init__(self, parent, title, width, height, result):
        wx.Frame.__init__(self, parent, title=title, size=(500, 500))
        self.height = height
        self.width = width
        self.template_to_result = result[0]
        self.coordinates_to_template = result[1]
        self.init_widgets()
        self.Centre()
        self.Show()

    def init_widgets(self):
        self.buttons = []
        panel = wx.Panel(self)
        sizer = wx.GridSizer(self.width, self.height, 1, 1)
        cells = []
        for i in range(self.height):
            self.buttons.append([])
            for j in range(self.width):
                crossword_cell = wx.Button(panel)
                self.buttons[i].append(crossword_cell)
                cells.append((crossword_cell, 1, wx.EXPAND))
        sizer.AddMany(cells)
        panel.SetSizer(sizer)
        for i in range(self.width):
            for j in range(self.height):
                template = self.coordinates_to_template.get((i, j))
                if template is not None:
                    self.input_result(template)

    def input_result(self, template):
        y, x = template.coordinates
        if template.is_horizontal:
            counter = 0
            for i in range(x, x + template.length):
                self.buttons[y][i].SetLabel(self.template_to_result[template][counter])
                counter += 1
        else:
            counter = 0
            for i in range(y, y + template.length):
                self.buttons[i][x].SetLabel(self.template_to_result[template][counter])
                counter += 1


def main():
    app = wx.App()
    cr = CrosswordEditor(None, "Geometry Creator", 10, 10)
    app.MainLoop()


if __name__ == '__main__':
    main()