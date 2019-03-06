# termdvd
A program that simulates the DVD video screensaver in the terminal.

Now even people without a display server can enjoy the thrill of watching the DVD icon hit the corner. Amazing!

# General info
This program requires at least Python version 3.3. If you attempt to run this program on Python 3.2 or lower, it will not work. In a future release, I may get support for older Python 3 versions working. However, I have no plans for getting Python 2 support.

This program should work on any OS that has Python 3.3 (or newer) ported to it. This includes Windows, macOS, Linux, and BSD.

This program has no installer, nor does it need one, because it's literally just one py file. All you have to do after downloading the program is run it from the command line.

# Command line arguments
When no arguments are given to termdvd, the region where the DVD icon bounces around is set to 20 rows and 40 columns by default.
If you want the DVD screen to be a diffrent size, it can be changed by typing the row count and then the column count as command line arguments. For example:

`termdvd.py 30 60`

will make the DVD screen be 30 rows long and 60 columns wide.

If you only want to change the row count, you only need to issue on argument. FOr example:

`termdvd.py 30`

will set the screen to 30 rows, but keep the column count at 40. However, if you want to issue a custom column count, you will need to issue both arguments.

