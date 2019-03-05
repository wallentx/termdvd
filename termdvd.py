#!/usr/bin/env python3
from os import system,name #These modules are needed to make a function that clears the screen that works on both posix and nt systems.
from time import sleep #I don't feel like explaining why I need this, because I don't know what I'll use it for yet.
from random import randint,uniform #Using randint for randomizing DVD color, and uniform for randomizing the DVD's velocity vecor.
from sys import stderr #This should allow me to print to stderr, so I can write custom error messages.

version = "2.0-development" #The program's version number is stored here.

import argparse #ARGUMENT PARSING!! :D
ap = argparse.ArgumentParser(description="A program that simulates the bouncing DVD screensaver in the terminal.")

#Adding arguments.
ap.add_argument("rows",nargs="?",help="Number of rows the DVD screen has. Minimum is 3.",type=int)
ap.add_argument("columns",nargs="?",help="Number of columns the DVD screen has. Minimum is 5.",type=int)
ap.add_argument("-v","--version",help="Display the version number and exit",action="store_true")
ap.add_argument("-c","--no_color",help="Makes the DVD logo just colored white.",action="store_true")

args = ap.parse_args()

if(args.version): #If the version flag is given, display the version name and quit.
    print("termdvd, version " + version)
    print("written by MrCatFace885") #Should I use my real name here, or my online alias?
    exit()

#If the rows or columns weren't given, fill them in with a default value.
if(args.rows == None):
    args.rows,args.columns = 20,40
elif(args.columns == None):
    args.columns = 40

#Checking to see if the arguments given are big enough.
errors = False

if(args.rows < 3):
    print("error: There must be at least 3 rows!",file=stderr)
    errors = True

if(args.columns < 5):
    print("error: There must be at least 5 columns!",file=stderr)
    errors = True

if(errors):
    exit()

def spriteud(): #Run this function to update the DVD sprite when the DVD color changes.
    dvd["sprite"] = "\033[1;7;3" + str(dvd["color"]) + "mDVD\033[0m"



def colorud(): #Run this before running spriteud() to update DVD color.
    if(args.no_color): #If the no-color flag is given, return white, otherwise, pick a random color and return that.
        return 7
    else:
        return randint(1,7)



def cls(): #Clears the screen.
    if(name == "nt"):
        system("cls")
    else:
        system("clear")



screen = {"rows":args.rows,"columns":args.columns} #I was initially gonna use a class for this, but then I figured it would be better to use a dictionary.
#BTW, that dictionary is used to store the resolution of the DVD screensaver in rows and columns.

#This dictionary below contains all data relavent to the DVD, like its velocity, position, and color.
dvd = {"x_vel":uniform(0.2,0.5),"y_vel":uniform(0.1,0.25),"x_pos":1.0,"y_pos":1.0,"color":colorud(),"sprite":"","x_rend":1,"y_rend":1}
spriteud()



def render(): #re-draw the DVD logo.
    print("\033[{0};{1}H   ".format(dvd["y_rend"] + 2,dvd["x_rend"] + 3),end="") #Erases the DVD, so it can re-draw it somewhere else.

    dvd["x_rend"] = int(round(dvd["x_pos"],0)) #These are only used for rendering the DVD, and nothing else.
    dvd["y_rend"] = int(round(dvd["y_pos"],0))

    print("\033[{0};{1}H{2}\033[{3};0H".format(dvd["y_rend"] + 2,dvd["x_rend"] + 3,dvd["sprite"],screen["rows"] + 3),end="",flush=True) #This makes the cursor jump to the spot it needs to be at and then prints the DVD logo.



def render_box(): #Renders just the box the DVD bounces around in.
    print("\033[7m    " + " " * screen["columns"]) #Prints the top of the box.

    for row_num in range (screen["rows"]): #Prints the sides of the box. (each one)
        print("  \033[0m" + " " * screen["columns"] + "\033[7m  ")

    print("\033[7m    " + " " * screen["columns"] + "\033[0m") #Prints the bottom of the box.




def main(): #The engine of the DVD physics.
    try:
        while(True):
            render()

            sleep(0.03)

            dvd["x_pos"] += dvd["x_vel"] #Changing the position of the DVD logo according to the X and Y velocities.
            dvd["y_pos"] += dvd["y_vel"]

            if(dvd["x_pos"] >= screen["columns"] - 3 or dvd["x_pos"] <= 0): #If a collision occurs on the left or right side, then...
                dvd["x_vel"] *= -1 #Reverse X velocity
                dvd["color"] = colorud() #Change DVD color.
                spriteud()

            if(dvd["y_pos"] >= screen["rows"] - 1 or dvd["y_pos"] <= 0): #If a collision occurs on the top or bottom side, then...
                dvd["y_vel"] *= -1 #Reverse Y velocity
                dvd["color"] = colorud() #Change DVD color.
                spriteud()

    except KeyboardInterrupt: #If ^C is pressed, then...
        print("\033[{0};0HGoodbye. \033[31m<3\033[0m".format(screen["rows"] + 3)) #Print a message saying "goodbye" with a little love heart at the end.



cls()
render_box()
main()
