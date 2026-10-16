"""
Copyright (c) 2026, Dylan Ooijevaar

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


"""
A GUI application to set up a mouse clicking sequence and looping through it
Because sometimes the API is so goddamn esoteric it's easier to just automate mouse clicks
"""

import tkinter as Tk

from src import Tables, ButtonActions as Actions


def CreateFunctionPanel(PassedWindow, PanelWidth, PanelHeight):
    #Create the Canvas that holds all the buttons and gizmos and whatizzits

    FunctionCanvas = Tk.Canvas(PassedWindow, bg="red", width=PanelWidth, height=PanelHeight)
    FunctionCanvasFrame = Tk.Frame(FunctionCanvas)
    FunctionCanvas.create_window((0,0), window=FunctionCanvasFrame, anchor="nw")
    
    return FunctionCanvas
    
    
def CreateTablePanel(PassedWindow):
    #Create the panel to hold the faux-Table for input scheduling

    TableCanvas = Tk.Canvas(PassedWindow, bg="green", width=560)
    TableScroll = Tk.Scrollbar(PassedWindow, orient="vertical", command=TableCanvas.yview)
    TableScrollFrame = Tk.Frame(TableCanvas)
    TableScrollFrame.bind("<Configure>", lambda x: TableCanvas.configure(scrollregion=TableCanvas.bbox("all")))
    TableCanvas.create_window((0,0), window=TableScrollFrame, anchor="nw")
    TableCanvas.configure(yscrollcommand=TableScroll.set)
    TableCanvas.grid(column=1, row=1, sticky='nesw')
    TableScroll.grid(column=2, row=1, sticky='nesw')

    return TableScrollFrame


def CreateTableHeaders(PassedWindow):
    #Populates the first row of the table with labels to indicate field function
    
    Headers = ["Row", "Action", "Mouse X", "Mouse Y", "Delay (ms)"]

    for n_Header in range(len(Headers)):
        HeaderLabel = Tk.Label(PassedWindow, text=Headers[n_Header])
        HeaderLabel.grid(row=0, column=1 + n_Header)


def main():
    #Create the main window
    MainWindow = Tk.Tk()
    MainWindow.title("Click Scheduler")

    #Create the sections for buttons and whatnot
    FunctionPanel = CreateFunctionPanel(MainWindow, 100, 10)
    FunctionPanel.grid(column=0, row=1, sticky='nesw')
    
    #Create the """Table"""
    TableSection = CreateTablePanel(MainWindow)
    InputTable = Tables.Table(TableSection, 50, 1)
    Actions.InputTable = InputTable

    #Create the headers for the table
    CreateTableHeaders(TableSection)

    #Create a bunch of Buttons

    #SAVE
    SaveSequenceButton = Tk.Button(FunctionPanel, text="Save Sequence", command=Actions.SaveSequence, width=20)
    SaveSequenceButton.grid(row=3, column=0, sticky="ew")

    #LOAD
    LoadSequenceButton = Tk.Button(FunctionPanel, text="Load Sequence", command=Actions.LoadSequence, width=20)
    LoadSequenceButton.grid(row=3, column=1, sticky="ew")

    #START
    StartSequenceButton = Tk.Button(FunctionPanel, text="Start", command=Actions.StartSequence, width=20)
    StartSequenceButton.grid(row=4, column=0, columnspan=2, sticky="ew")

    #Create a dialog box to chuck some messages on screen if need be
    StatusBox = Tk.Text(FunctionPanel, width= 40, height=5, wrap="word")
    StatusBox.grid(row=6, column=0, columnspan=2, sticky="ew")
    StatusBox.config(state='disabled')
    Actions.MainDialog = StatusBox

    #Create a instruction card for general use info
    HelpCard = Tk.Label(FunctionPanel, width= 40, height=8, text=Actions.TextContent.HELP_CARD, wraplength=310, justify='left')
    HelpCard.grid(row=7, column=0, rowspan=5, columnspan=2, sticky="ew")

    #And a lil' dev note
    AboutCard = Tk.Label(FunctionPanel, height=2, text=Actions.TextContent.VERSION, justify='left', fg='grey')
    AboutCard.grid(row=12, column=0, rowspan=2, columnspan=2, sticky="ew")
    
    MainWindow.mainloop()


if __name__ == "__main__":
    main()