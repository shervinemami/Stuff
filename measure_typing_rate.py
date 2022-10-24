#!/usr/bin/env python
# A tool for measuring typing rate, in cps and wpm.
# By Shervin Emami 2019, "http://shervinemami.com/".
# Tested on Ubuntu 22.04 using python 3.10.

# Python 2/3 compatibility
from __future__ import print_function

import sys
import random
import time
import operator


#---------------------------------------
# Keyboard input code, taken from "https://github.com/akkana/scripts/blob/master/keyreader.py" on Jan 1st 2019.
import sys
import os
import termios, fcntl
import select

class KeyReader :
    '''
    Read keypresses one at a time, without waiting for a newline.
    echo: should characters be echoed?
    block: should we block for each character, or return immediately?
           (If !block, we'll return None if nothing is available to read.)
    '''
    def __init__(self, echo=False, block=True):
        '''Put the terminal into cbreak and noecho mode.'''
        self.fd = sys.stdin.fileno()

        self.block = block

        self.oldterm = termios.tcgetattr(self.fd)
        self.oldflags = fcntl.fcntl(self.fd, fcntl.F_GETFL)

        # Sad hack: when the destructor __del__ is called,
        # the fcntl module may already be unloaded, so we can no longer
        # call fcntl.fcntl() to set the terminal back to normal.
        # So just in case, store a reference to the fcntl module,
        # and also to termios (though I haven't yet seen a case
        # where termios was gone -- for some reason it's just fnctl).
        # The idea of keeping references to the modules comes from
        # http://bugs.python.org/issue5099
        # though I don't know if it'll solve the problem completely.
        self.fcntl = fcntl
        self.termios = termios

        newattr = termios.tcgetattr(self.fd)
        # tcgetattr returns: [iflag, oflag, cflag, lflag, ispeed, ospeed, cc]
        # where cc is a list of the tty special characters (length-1 strings)
        # except for cc[termios.VMIN] and cc[termios.VTIME] which are ints.
        self.cc_save = newattr[6]
        newattr[3] = newattr[3] & ~termios.ICANON
        if not echo:
            newattr[3] = newattr[3] & ~termios.ECHO

        if block and False:
            # VMIN and VTIME are supposed to let us do blocking reads:
            # VMIN is the minimum number of characters before it will return,
            # VTIME is how long it will wait if for characters < VMIN.
            # This is documented in man termios.
            # However, it doesn't work in python!
            # In Python, read() never returns in non-canonical mode;
            # even typing a newline doesn't help.
            cc = self.cc_save[:]   # Make a copy so we can restore VMIN, VTIME
            cc[termios.VMIN] = 1
            cc[termios.VTIME] = 0
            newattr[6] = cc
        else:
            # Put stdin into non-blocking mode.
            # We need to do this even if we're blocking, see above.
            fcntl.fcntl(self.fd, fcntl.F_SETFL, self.oldflags | os.O_NONBLOCK)

        termios.tcsetattr(self.fd, termios.TCSANOW, newattr)

    def __del__(self):
        '''Reset the terminal before exiting the program.'''
        self.termios.tcsetattr(self.fd, self.termios.TCSAFLUSH, self.oldterm)
        self.fcntl.fcntl(self.fd, self.fcntl.F_SETFL, self.oldflags)

    def getch(self):
        '''Read keyboard input, returning a string.
           Note that one key may result in a string of more than one character,
           e.g. arrow keys that send escape sequences.
           There may also be multiple keystrokes queued up since the last read.
           This function, sadly, cannot read special characters like VolumeUp.
           They don't show up in ordinary CLI reads -- you have to be in
           a window system like X to get those special keycodes.
        '''
        # Since we can't use the normal cbreak read from python,
        # use select to see if there's anything there:
        if self.block:
            inp, outp, err = select.select([sys.stdin], [], [])
        try:
            return sys.stdin.read()
        except (IOError, TypeError) as e:
            return None
#--------------------------------------




print("Type lots of characters and/or words:")

keyreader = KeyReader(echo=True, block=True)
averagedSecondsChar = -1    # Initialize with the first measurement
wordsPerMinute = -1

# Dont start measuring until they've pressed the first keypress
key = keyreader.getch()
timeStartWord = time.time()
print()

while (True):

    timeStartChar = time.time()

    if key == " ":
        timeStartWord = timeStartChar

    # Wait for a new character keypress
    key = keyreader.getch()

    timeEndChar = time.time()
    rawSecondsChar = (timeEndChar - timeStartChar)

    # Perform a running average alpha filter to smoothen the result but give more priority to recent results
    if averagedSecondsChar < 0:
        averagedSecondsChar = rawSecondsChar    # Initialize first use

    alpha = 0.1    # The closer this is to 1.0, the stronger the filtering that will be applied.
    averagedSecondsChar = ((1.0 - alpha) * rawSecondsChar) + (alpha * averagedSecondsChar)

    if key == " ":
        # Convert from seconds per character -> words per minute (WPM)
        rawSecondsWord = (timeEndChar - timeStartWord)
        rawMinutesWord = rawSecondsWord / 60.0
        wordsPerMinute = 1.0 / rawMinutesWord
        print("                Speed: %.3f seconds/character, %.0f WPM" % (averagedSecondsChar, wordsPerMinute))
    else:
        print("                Speed: %.3f seconds/character." % (averagedSecondsChar))

