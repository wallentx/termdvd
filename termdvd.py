#!/usr/bin/env python3
version = "2.2-development" #The program's version number is stored here.

import argparse #Argument parsing is the first thing that runs when this program is executed.
ap = argparse.ArgumentParser(description="A program that simulates the bouncing DVD screensaver in the terminal.")

#Adding arguments.
ap.add_argument("rows",nargs="?",help="Number of rows the DVD screen has. Minimum is 3.",type=int)
ap.add_argument("columns",nargs="?",help="Number of columns the DVD screen has. Minimum is 5.",type=int)
ap.add_argument("-v","--version",help="Display the version number and exit",action="store_true")
ap.add_argument("-c","--no_color",help="Makes the DVD logo just colored white.",action="store_true")

args = ap.parse_args()

if(args.version): #If the version flag is given, display the version name and quit.
    print("termdvd, version " + version)
    print("written by MrCatFace8885") #I'm too much of a coward to use my real name, so I'll just use my online alias.
    exit()

#If the rows or columns weren't given, fill them in with a default value.
if(args.rows == None):
    args.rows,args.columns = 20,40
elif(args.columns == None):
    args.columns = 40

#Checking to see if the arguments given are big enough, and if they aren't then give an error and terminate.
if(args.rows < 3):
    print("error: There must be at least 3 rows!",file=stderr)
    exit()

if(args.columns < 5):
    print("error: There must be at least 5 columns!",file=stderr)
    exit()

#Argument parsing ends here

from os import system,name #os.system is used in the cls() function, and os.name is used to occasionally determine what OS is being used.
from time import sleep #I don't feel like explaining why I need this, because I don't know what I'll use it for yet.
from random import randint,uniform #Using randint for randomizing DVD color, and uniform for randomizing the DVD's velocity vecor.
from sys import stderr #This should allow me to print to stderr, so I can write custom error messages.
from platform import win32_ver #Need this function to check what version of Windows is being run.
from shutil import get_terminal_size #Used for getting the rows and columns of the terminal emulator.

if(name == "nt" and win32_ver()[0] != "10"): #If the computer is runnnig an older version of Windows, attempt to import the colorama module. This module makes ANSI escape codes work on Windows.
    try:
        import colorama

    except ImportError: #If importing colorama failed, then print an error message telling the user to install the module, and terminate.
        print("error: colorama module not found! Please install it by typing:\npip install colorama",file=stderr)
        exit()

    colorama.init() #Starts colorama, so it can start doing its work.



def colorud(): #Chooses colors for the DVD logo.
    if(args.no_color): #If the no-color flag is given, return white, otherwise, pick a random color and return that.
        return 7
    else:
        return randint(1,7)

def spriteud(): #Updates the DVD logo when bounce() is run. I probably should have this function inside main(), but I have some things that call for this function outside of it.
    dvd["sprite"] = "\033[30;10" + str(dvd["color"]) + "mDVD\033[0m" #Apply said color to the logo.



screen = {"rows":args.rows,"columns":args.columns} #This dictionary is used for rendering the DVD box/screen and for the physics system. This variable exists so the DVD screen can adapt to terminal resizes.

#This dictionary below contains all data relavent to the DVD, like its velocity, position, and color. Maybe I should stop using global variables.
dvd = {"x_vel":uniform(0.2,0.5),"y_vel":uniform(0.1,0.25),"x_pos":1.0,"y_pos":1.0,"color":colorud(),"sprite":"","x_rend":1,"y_rend":1}
spriteud()

def render(): #re-draw the DVD logo.
    print("\033[{0};{1}H   ".format(dvd["y_rend"] + 2,dvd["x_rend"] + 3),end="") #Erases the DVD, so it can re-draw it somewhere else.

    dvd["x_rend"] = int(round(dvd["x_pos"],0)) #These are only used for rendering the DVD, and nothing else.
    dvd["y_rend"] = int(round(dvd["y_pos"],0))

    print("\033[{0};{1}H{2}\033[{3};1H".format(dvd["y_rend"] + 2,dvd["x_rend"] + 3,dvd["sprite"],screen["rows"] + 3),end="",flush=True) #This makes the cursor jump to the spot it needs to be at and then prints the DVD logo.



def render_box(): #Clears the screen and then draws the DVD screen. It doesn't actually display the DVD logo itself.
    if(get_terminal_size()[0] < args.columns + 4): #Checks if the terminal is wide enough for the DVD screen, and if it isn't, then make the screen adapt to the terminal.
        screen["columns"] = get_terminal_size()[0] - 4
    else:
        screen["columns"] = args.columns

    if(get_terminal_size()[1] < args.rows + 3): #Does the same thing as the last if statement, but it affects height instead of width.
        screen["rows"] = get_terminal_size()[1] - 3
    else:
        screen["rows"] = args.rows


    if(name == "nt"): #This stuff clears the screen.
        system("cls")
    else:
        system("clear")

    #This stuff draws the box.
    print("\033[47m    " + " " * screen["columns"]) #Prints the top of the box.

    for row_num in range (screen["rows"]): #Prints the sides of the box. (each one)
        print("  \033[0m" + " " * screen["columns"] + "\033[47m  ")

    print("\033[47m    " + " " * screen["columns"] + "\033[0m") #Prints the bottom of the box.



def main(): #The engine of the DVD physics.
    def bounce(axis): #This function is run whenever the DVD logo hits a side, or if you're lucky, a corner.
        dvd[axis + "_vel"] *= -1 #Reverses the velocity of the axis.

        dvd["color"] = colorud() #Choose a new color for the DVD logo.
        spriteud() #Apply said color to the logo.

    old_term = get_terminal_size() #This variable is compared to the actual size of the terminal, to see if it has changed or not.
    try:
        while(True):
            for counter in range (3): #Standard physics code is run 5 times, and then the program will check if the terminal's rows and columns changed.
                render()

                sleep(0.03)

                dvd["x_pos"] += dvd["x_vel"] #Changing the position of the DVD logo according to the X and Y velocities.
                dvd["y_pos"] += dvd["y_vel"]

                if(dvd["x_pos"] >= screen["columns"] - 3 or dvd["x_pos"] <= 0): #Collision detection for the DVD logo.
                    bounce("x")
                if(dvd["y_pos"] >= screen["rows"] - 1 or dvd["y_pos"] <= 0):
                    bounce("y")

            if(old_term != get_terminal_size()): #If the size of the terminal has changed, then...
                old_term = get_terminal_size() #Reset old term
                render_box() #Re-render the DVD screen

    except KeyboardInterrupt: #If ^C is pressed, then...
        print("\033[{0};1HGoodbye. \033[31m<3\033[0m".format(screen["rows"] + 3)) #Print a message saying "goodbye" with a little love heart at the end.



render_box()
main()
