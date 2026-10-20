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
All the commands issued whenever a button is pressed
"""

import tkinter as Tk, pyautogui as Gui, keyboard as Keys

from time import sleep
from tkinter import Toplevel, filedialog

from src import TextContent


def UpdateDialogBox(StatusBox, Message):
    #Chuck a message on screen
    
    StatusBox.config(state="normal")
    StatusBox.delete('1.0', Tk.END)
    StatusBox.insert(Tk.END, Message)
    StatusBox.config(state="disabled")


def SaveSequence(SequenceTable):
    #Just dump all the instructions (correct or not) into a file to export

    ExportRules = []

    #Go through all instructions
    for n_Command in range(len(SequenceTable.Cells)):
        EvaluatedCommand = SequenceTable.Cells[n_Command]
            
        #If there even is but one value, save it
        ContainsValue = False
        for n_Cell in range(4):
            if len(EvaluatedCommand[n_Cell].get()) != 0:
                ContainsValue = True
           
        if(ContainsValue):
            ExportRules.append(EvaluatedCommand[0].get() + "," + EvaluatedCommand[1].get() + "," + EvaluatedCommand[2].get() + "," + EvaluatedCommand[3].get() + "\n")
    
    File = filedialog.asksaveasfile(title="Save Sequence as...", defaultextension=".txt")
    
    #If action is cancelled, don't bother
    if File:
        File.writelines(ExportRules)
        File.close()


def LoadSequence(SequenceTable):
    #Load a sequence and populate all rules into what I pretend is a table
    
    FilePath = filedialog.askopenfilename(title="Open Sequence File")
    Instructions = []

    #If action is cancelled, don't bother
    if FilePath:
        try:
            with open(FilePath, 'r') as File:
                for Line in File.readlines():
                    InputCells = Line.replace("\n", "").split(",")
                    Instructions.append(InputCells)
            File.close()

            SequenceTable.UpdateCells(Instructions)

        except:
            UpdateDialogBox(TextContent.SEQ_LOADERROR)


def ExecuteSequence(PassedListOfActions):
    #Continues the sequence by executing it
        
    #Verbosely for indexing and all that jazz
    for Instruction in PassedListOfActions:
    
        #Force a way to break a loop, only triggers after the delay
        if Keys.is_pressed('esc'):
            UpdateDialogBox(TextContent.SEQ_INTERRUPT)
            AppWindow.deiconify()
            return

        #Move cursor    
        Gui.moveTo(Instruction[1], Instruction[2], 0)

        #Fun, but ultimately obtuse way to determine left or right click event. But _funi_
        if Instruction[0] != "Idle":
            Gui.click(button=["left", "right"][["Left Click", "Right Click"].index(Instruction[0])])
        
        #Delays after clicks allow for laggy systems to register what the fuck just happened   
        sleep(Instruction[3])


def StartSequence(MainWindow, SequenceTable, StatusBox, MaxIterationBox):
    #Kicks off reading the sequence and executing the clicking actions
    #First constructs a list of actions to be carried out
    #READ and EXECUTE phase are split as to not run into issues mid-sequence
    
    ListOfActions = []
    LoopMax = 0

    #Check if the max iterations is set correctly
    try:
        LoopMax = int(MaxIterationBox.get())
        MaxIterationBox.config({"background" :"white"})
        UpdateDialogBox(StatusBox, "") #lazy bastard
    except:
        MaxIterationBox.config({"background" :"#de525e"})
        UpdateDialogBox(StatusBox, TextContent.ITER_FAULT)
        return

    for n_Command in range(len(SequenceTable.Cells)):

        #Doing this verbosely to have both the object and its index
        EvaluatedCommand = SequenceTable.Cells[n_Command]
        
        #Empty actions will not be evaluated
        if len(EvaluatedCommand[0].get()) != 0:
            
            #Make sure all values are actionable numbers
            try:
                ScreenX = int(EvaluatedCommand[1].get())
                ScreenY = int(EvaluatedCommand[2].get())
                Delay   = float(EvaluatedCommand[3].get()) / 1000
                
                #Do some screen bounds checking
                if(ScreenX > Gui.size().width or ScreenY > Gui.size().height):
                    SequenceTable.MarkInputCells(n_Command, "#de525e")
                    UpdateDialogBox(StatusBox, TextContent.TABLE_COORD)
                    return

                #Dumb way to reset cell colour
                SequenceTable.MarkInputCells(n_Command, "white")

                #This is now a cleaned up set of instructions
                ListOfActions.append([EvaluatedCommand[0].get(), ScreenX, ScreenY, Delay])

            except:
                SequenceTable.MarkInputCells(n_Command, "#de525e")
                UpdateDialogBox(StatusBox, TextContent.TABLE_FAULT)
                return
    
    #Catches recursion if started with an empty sequence
    if len(ListOfActions):

        #Wait a few seconds before launching the sequence
        #It used to be here to allow window minimisation, but that's taken care of now with iconify()
        #Now it remains here to gives the impression it "does something"
        sleep(2)
        MainWindow.iconify()

        #Print this before any possible interrupt lines
        UpdateDialogBox(StatusBox, TextContent.SEQ_FINISHED)

        Iterations = 0
        while(Iterations < LoopMax):
            ExecuteSequence(ListOfActions)
            Iterations += 1

        MainWindow.deiconify()        


def CloseCoordinateScreen(PassedOverlay, PassedMainWindow):
    #Exit out of the coordinate overlay

    PassedOverlay.destroy()
    PassedMainWindow.deiconify()


def PrintCoordinatesToBox(event):
    #Print mouse location to screen

    MousePositionBox.delete('1.0', Tk.END)
    MousePositionBox.insert(Tk.END, "Width:  " + str(Gui.position().x) + "\nHeight: " + str(Gui.position().y))

   
def ShowCoordinates(MainWindow):
    #Create a full-screen overlay to show mouse coordinates

    #Making these global so other functions can access them
    #Not great, not terrible
    global ScreenOverlay, MousePositionBox

    #Minimise the Sequence gui 
    MainWindow.iconify()

    #Create a full-screen overlay
    ScreenOverlay = Tk.Tk()
    ScreenOverlay.attributes("-fullscreen", True)
    ScreenOverlay.attributes("-alpha", 0.65)

    #Create a button to exit the overlay and return to the Sequence viewer
    ExitOverlayButton = Tk.Button(ScreenOverlay, text="Return", font=("System",15), 
    command= lambda: CloseCoordinateScreen(ScreenOverlay, MainWindow))
    ExitOverlayButton.grid(row=0, column=0, sticky="ew")

    #Create a Text widget to display the position of the cursor on screen
    MousePositionBox = Tk.Text(ScreenOverlay, font=("System", 15), height=2, width=12)
    MousePositionBox.grid(row=1, column=0, sticky="nesw")

    #Bind mouse motion to the updating of shown coordinates
    ScreenOverlay.bind("<Motion>", PrintCoordinatesToBox)