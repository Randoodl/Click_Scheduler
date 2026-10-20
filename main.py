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

from src import Tables, ButtonActions as Actions


def CreateFunctionPanel(PassedWindow, PassedWidth, PassedHeight):
    #Create the Canvas that holds all the buttons and gizmos and whatizzits

    FunctionCanvas = Actions.Tk.Canvas(PassedWindow, width=PassedWidth, height=PassedHeight)
    FunctionCanvasFrame = Actions.Tk.Frame(FunctionCanvas)
    FunctionCanvas.create_window((0,0), window=FunctionCanvasFrame, anchor="nw")
    
    return FunctionCanvas
    
    
def CreateTablePanel(PassedWindow, PassedWidth):
    #Create the panel to hold the faux-Table for input scheduling

    TableCanvas = Actions.Tk.Canvas(PassedWindow, width=PassedWidth)
    TableScroll = Actions.Tk.Scrollbar(PassedWindow, orient="vertical", command=TableCanvas.yview)
    TableScrollFrame = Actions.Tk.Frame(TableCanvas)
    TableScrollFrame.bind("<Configure>", lambda x : TableCanvas.configure(scrollregion=TableCanvas.bbox("all")))
    TableCanvas.create_window((0,0), window=TableScrollFrame, anchor="nw")
    TableCanvas.configure(yscrollcommand=TableScroll.set)
    TableCanvas.grid(column=1, row=1, sticky='nesw')
    TableScroll.grid(column=2, row=1, sticky='nesw')

    return TableScrollFrame


def CreateTableHeaders(PassedWindow):
    #Populates the first row of the table with labels to indicate field function
    
    Headers = ["Row", "Action", "Mouse X", "Mouse Y", "Delay (ms)"]

    for n_Header in range(len(Headers)):
        HeaderLabel = Actions.Tk.Label(PassedWindow, text=Headers[n_Header])
        HeaderLabel.grid(row=0, column=1 + n_Header)


def CreateMaxLoopCounter(PassedWindow):
    #Allows for an input value that will loop over the sequence n amount of times, then exits

    InfoLabel = Actions.Tk.Label(PassedWindow, text="Max iterations:")
    InfoLabel.grid(row=1, column=0, sticky="ew")

    MaxIterationsBox = Actions.Tk.Entry(PassedWindow, width=15)
    MaxIterationsBox.grid(row=1, column=1, sticky="nesw")

    return MaxIterationsBox


def CreateButtons(MainWindow, FunctionPanel, SequenceTable, StatusBox, MaxIterationBox):
    #All button creation calls combined into one function

    SaveSequenceButton = Actions.Tk.Button(FunctionPanel, text="Save Sequence", width=20,
    command= lambda : Actions.SaveSequence(SequenceTable))
    SaveSequenceButton.grid(row=0, column=0, sticky="ew")

    LoadSequenceButton = Actions.Tk.Button(FunctionPanel, text="Load Sequence", width=20,
    command= lambda : Actions.LoadSequence(SequenceTable))
    LoadSequenceButton.grid(row=0, column=1, sticky="ew")

    StartSequenceButton = Actions.Tk.Button(FunctionPanel, text="Start", width=20,
    command= lambda : Actions.StartSequence(MainWindow, SequenceTable, StatusBox, MaxIterationBox))
    StartSequenceButton.grid(row=2, column=1, sticky="ew")

    ShowCoordinatesButton = Actions.Tk.Button(FunctionPanel, text="Show Mouse Location", width=20,
    command= lambda : Actions.ShowCoordinates(MainWindow))
    ShowCoordinatesButton.grid(row=2, column=0, sticky="ew")


def main():
    #Create the main window
    MainWindow = Actions.Tk.Tk()
    MainWindow.title("Click Scheduler " + Actions.TextContent.VERSION)
    Actions.AppWindow = MainWindow

    #Create the sections for buttons and whatnot
    FunctionPanel = CreateFunctionPanel(MainWindow, 100, 10)
    FunctionPanel.grid(column=0, row=1, sticky='nesw')
    
    #Create the """Table"""
    TableSection = CreateTablePanel(MainWindow, 560)
    SequenceTable = Tables.Table(TableSection, 50, 1)

    #Create the headers for the table
    CreateTableHeaders(TableSection)

    #Create a field to set a max loop cap
    MaxIterationBox = CreateMaxLoopCounter(FunctionPanel)

    #Create a dialog box to chuck some messages on screen if need be
    StatusBox = Actions.Tk.Text(FunctionPanel, width= 40, height=4, wrap="word")
    StatusBox.grid(row=3, column=0, columnspan=2, sticky="ew")
    StatusBox.config(state='disabled')

    #Create a bunch of Buttons
    CreateButtons(MainWindow, FunctionPanel, SequenceTable, StatusBox, MaxIterationBox)
  
    #Create a instruction card for general use info
    HelpCard = Actions.Tk.Label(FunctionPanel, width= 40, height=8, text=Actions.TextContent.HELP_CARD, wraplength=310, justify='left')
    HelpCard.grid(row=8, column=0, rowspan=5, columnspan=2, sticky="ew")

    #And a lil' dev note
    AboutCard = Actions.Tk.Label(FunctionPanel, height=2, text=Actions.TextContent.VERSION_CARD, justify='left', fg='grey')
    AboutCard.grid(row=13, column=0, rowspan=2, columnspan=2, sticky="w")
    
    MainWindow.mainloop()


if __name__ == "__main__":
    main()