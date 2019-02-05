#!/usr/bin/env python3
from os import system,name #These modules are needed to make a function that clears the screen that works on both posix and nt systems.
from time import sleep #I don't feel like explaining why I need this, because I don't know what I'll use it for yet.
from random import randint,uniform #Using randint for randomizing DVD color, and uniform for randomizing the DVD's velocity vecor.

#I should seriously consider uploading my code to a git repo soon, because some of my projects are actually really cool and should be shared.

version = "1.0" #The program's version number is stored here.

def spriteud(): #Run this function to update the DVD sprite when the DVD color changes.
    dvd["sprite"] = "\033[1;7;3" + str(dvd["color"]) + "mDVD\033[0m"



def cls(): #Clears the screen.
    if(name == "nt"):
        system("cls")
    else:
        system("clear")



screen = {"rows":None,"columns":None} #I was initially gonna use a class for this, but then I figured it would be better to use a dictionary.
#BTW, that dictionary is used to store the resolution of the DVD screensaver in rows and columns.

#This dictionary below contains all data relavent to the DVD, like its velocity, position, and color.
dvd = {"x_vel":uniform(0.2,0.5),"y_vel":uniform(0.1,0.25),"x_pos":1.0,"y_pos":1.0,"color":randint(1,7),"sprite":""}
spriteud()



def row_colInp(minimum,thing): #Used for setting how many rows and columns the screen has.
    while(True):
        print("")

        try: #Attempts to set row_col to an integer typed in by the user.
            row_col = int(input("How many " + thing + "s? (minimum is " + str(minimum) + ")\n>"))

            if(row_col >= minimum): #If row_col is at least the minimum value, move on to prompting how many columns.
                break
            else: #Else, print this error message and try again.
                print("The minimum value is " + str(minimum) + ". Try again.")

        except ValueError: #If the typed-in value isn't an integer, so try again.
            print("That's not an integer. Please type an integer.")

    return row_col #This variable can represent either the number of rows or the number of columns... if that makes sense.



def render(): #Prints one frame of the screensaver to the screen.
    print("\033[0;0H") #Resets the cursor position, so each frame gets overwritten with the next one instead of getting cleared and then having the new frame.
    print("\033[7m",end="") #God, I love ANSII escape codes. :)

    for generic_variable_name_number_297 in range (screen["columns"] + 4): #Prints the top of the screen window.
        print(" ",end="")

    print("\033[0m")

    rend_x = int(round(dvd["x_pos"],0)) #rend_x and rend_y are used for rendering the DVD icon, and are not used in the bouncing physics.
    rend_y = int(round(dvd["y_pos"],0))

    for row_num in range (screen["rows"]): #Printing left and right sides of the screen, and the DVD logo.
        print("\033[7m  \033[0m",end="")

        if(row_num == rend_y): #If the cursor is on the same row the DVD logo is, then...
            for x in range (rend_x): #...print spaces until it's time to print the DVD logo...
                print(" ",end="")
            print(dvd["sprite"],end="")

            for x in range (rend_x + 3,screen["columns"]): #...and then print spaces until there's no more columns.
                print(" ",end="")

        else: #Otherwise, as many spaces as there are columns.
            for col_num in range (screen["columns"]):
                print(" ",end="")

        print("\033[7m  \033[0m")

    print("\033[7m",end="")

    for generic_variable_name_number_297 in range (screen["columns"] + 4): #Prints the bottom of the screen window.
        print(" ",end="")
    print("\033[0m")



def main(): #The engine of the DVD physics.
    while(True):
        render()

        sleep(0.025)

        dvd["x_pos"] += dvd["x_vel"] #Changing the position of the DVD logo according to the X and Y velocities.
        dvd["y_pos"] += dvd["y_vel"]

        if(dvd["x_pos"] >= screen["columns"] - 3 or dvd["x_pos"] <= 0): #If a collision occurs on the left or right side, then...
            dvd["x_vel"] *= -1 #Reverse X velocity
            dvd["color"] = randint(1,7) #Change DVD color.
            spriteud()

        if(dvd["y_pos"] >= screen["rows"] - 1 or dvd["y_pos"] <= 0): #If a collision occurs on the top or bottom side, then...
            dvd["y_vel"] *= -1 #Reverse Y velocity
            dvd["color"] = randint(1,7) #Change DVD color.
            spriteud()



#Prints version number and a brief description of the program.
print("----Terminal DVD----\nversion " + version + '''

This program simulates the DVD video screensaver in the terminal. There's not much else
to say about it.

This program was written by Luke Farris. He's too stupid to know how to have the program
automatically get the number of rows and columns the terminal screen has, so you'll have
to type it in manually. This is totally not an excuse for him to not properly learn
Python. (it is)''') #I should SERIOUSLY learn argument parsing in Python. (It would make using the program a lot more convenient)

screen["rows"] = row_colInp(3,"row") #Yes, I know my code is awful. I'm sorry. :(
screen["columns"] = row_colInp(5,"column") #BTW, this is where I used the function that sets rows and columns.

print("\nDVD screensaver is ready. Hold Ctrl + C to exit at any time.")
sleep(3)

cls()
main()
