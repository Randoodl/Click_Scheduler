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

import pyautogui as Gui, keyboard as Keys

from time import sleep
from tkinter import filedialog, END

from src import TextContent


#Will be populated with a proper values from main
#Dumb way of doing it? Yes, but I am not known for elegant code
InputTable = []
MainDialog = []


def UpdateDialogBox(Message):
    #Chuck a message on screen
    
    MainDialog.config(state="normal")
    MainDialog.delete('1.0', END)
    MainDialog.insert(END, Message)
    MainDialog.config(state="disabled")


def SaveSequence():
    #Just dump all the instructions (correct or not) into a file to export

    ExportRules = []

    #Go through all instructions
    for n_Command in range(len(InputTable.Cells)):
        EvaluatedCommand = InputTable.Cells[n_Command]
            
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


def LoadSequence():
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

            InputTable.UpdateCells(Instructions)

        except:
            UpdateDialogBox(TextContent.SEQ_LOADERROR)


def ExecuteSequence(PassedListOfActions):
    #Continues the sequence by executing it
        
    #Verbosely for indexing and all that jazz
    for Instruction in PassedListOfActions:
    
        #Force a way to break a loop, only triggers after the delay
        if Keys.is_pressed('esc'):
            UpdateDialogBox(TextContent.SEQ_INTERRUPT)
            return

        #Move cursor    
        Gui.moveTo(Instruction[1], Instruction[2], 0)

        #Fun, but ultimately obtuse way to determine left or right click event. But _funi_
        if Instruction[0] != "Idle":
            Gui.click(button=["left", "right"][["Left Click", "Right Click"].index(Instruction[0])])
        
        #Delays after clicks allow for laggy systems to register what the fuck just happened   
        sleep(Instruction[3])
        
    #Loop the same action back, until ESC is pressed
    #This in no way, shape or form will cause issues. Surely.
    ExecuteSequence(PassedListOfActions)


def StartSequence():
    #Kicks off reading the sequence and executing the clicking actions
    #First constructs a list of actions to be carried out
    #READ and EXECUTE phase are split as to not run into issues mid-sequence

    ListOfActions = []

    for n_Command in range(len(InputTable.Cells)):

        #Doing this verbosely to have both the object and its index
        EvaluatedCommand = InputTable.Cells[n_Command]
        
        #Empty actions will not be evaluated
        if len(EvaluatedCommand[0].get()) != 0:
            
            #Make sure all values are actionable numbers
            try:
                ScreenX = int(EvaluatedCommand[1].get())
                ScreenY = int(EvaluatedCommand[2].get())
                Delay   = float(EvaluatedCommand[3].get()) / 1000
                
                #Do some screen bounds checking
                if(ScreenX > Gui.size().width or ScreenY > Gui.size().height):
                    InputTable.MarkInputCells(n_Command, "#de525e")
                    UpdateDialogBox(TextContent.TABLE_COORD)
                    return

                #Dumb way to reset cell colour
                InputTable.MarkInputCells(n_Command, "white")

                #This is now a cleaned up set of instructions
                ListOfActions.append([EvaluatedCommand[0].get(), ScreenX, ScreenY, Delay])

            except:
                InputTable.MarkInputCells(n_Command, "#de525e")
                UpdateDialogBox(TextContent.TABLE_FAULT)
                return
    
    #Wait a few seconds before launching the sequence
    #This is so you can minimize the program or something
    sleep(3)
    
    if len(ListOfActions):
        #Catches recursion if started with an empty sequence
        ExecuteSequence(ListOfActions)