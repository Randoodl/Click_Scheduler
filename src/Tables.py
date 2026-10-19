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
Class to create a sort of table using a whole host of tkinter Entry widgets
"""

import tkinter as Tk

from tkinter import ttk


class Table:
    #Class to create a table-esque widget

    def __init__(self, PassedWindow, t_Rows, ColumnRoot):
        
        #Each individual cell is stored in a dumb nested list of
        #[Action, MouseX, MouseY, Delay(ms)]
        self.Cells = []
        
        #Construct the """"table"""""
        for n_Row in range(t_Rows):
            self.Cells.append([])
            
            #Add a row indicator
            self.Label = Tk.Label(PassedWindow, text=str(n_Row + 1), width=7)
            self.Label.grid(row=n_Row + 1, column=ColumnRoot)

            #Add a dropdown box for the Action
            Action = Tk.StringVar()
            self.Dropper = ttk.Combobox(PassedWindow, textvariable=Action, width=15)
            self.Dropper['values'] = ('', 'Idle', 'Left Click', 'Right Click')
            self.Dropper.grid(row=n_Row + 1, column=ColumnRoot + 1)
            self.Cells[-1].append(self.Dropper)
            
            #Add the Entry options for ScreenX, ScreenY, Delay(ms)
            #Starts at 1 because the dropdown box is at 0
            for n_Column in range(1, 4):
                self.Entry = Tk.Entry(PassedWindow, width=15)
                self.Entry.grid(row=n_Row + 1, column=ColumnRoot + n_Column + 1)
                self.Cells[-1].append(self.Entry)


    def MarkInputCells(self, CommandIndex, ColourString):
        #Function to quickly (de)colour the rows for Errors
        for Cell in range(4):
            self.Cells[CommandIndex][Cell].config({"background" : ColourString})


    def UpdateCells(self, Instructions):
        #Load values into cells if a Sequence is opened

        #First clear ALL cells of content
        for Row in self.Cells:
            for Cell in Row:
                Cell.delete(0, 'end')

        #Then write data to 'em
        for n_Instruction in range(len(Instructions)):
            for n_Cell in range(4):
                self.Cells[n_Instruction][n_Cell]
                self.Cells[n_Instruction][n_Cell].insert(Tk.END, Instructions[n_Instruction][n_Cell])