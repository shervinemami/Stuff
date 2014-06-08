# Extremely useful features to add to your Linux .bashrc file.
# Provides colored highlighting of the shell prompt based on whether a command returned an error or not. Plus a few handy colorizations of 'ls', 'grep', etc.
# Tested on Ubuntu, Debian and Arch. By Shervin Emami, 2014.

#######################################################################
# Get the BASH command prompt to show the hostname & time & path, in a distinct color from regular text,
# and shown in red if the previous command had an error.
# eg:   "john@mypc:1 12:04:58 /etc $"

# Text display colors for Ubuntu or Debian:
RESET='\[\e[0m\]'
RED_TEXT="${RESET}\[\e[7;3;31m\]"
RED_BOLD="${RESET}\[\e[1;41;39m\]"
BLUE_TEXT="${RESET}\[\e[0;44m\]"
BLUE_BOLD="${RESET}\[\e[1;44m\]"
GREEN_TEXT="${RESET}\[\e[0;30;42m\]"
GREEN_BOLD="${RESET}\[\e[1;42;39m\]"
YELLOW_TEXT="${RESET}\[\e[0;103;30m\]"
YELLOW_BOLD="${RESET}\[\e[1;103;30m\]"
PURPLE_TEXT="${RESET}\[\e[0;45;30m\]"
PURPLE_BOLD="${RESET}\[\e[1;45;97m\]"
GREY_TEXT="${RESET}\[\e[0;100;97m\]"
GREY_BOLD="${RESET}\[\e[1;100;97m\]"

# Choose one of the text colors: blue, green, yellow, purple or grey:
TEXT="$BLUE_TEXT"
BOLD="$BLUE_BOLD"
#TEXT="$GREEN_TEXT"
#BOLD="$GREEN_BOLD"
#TEXT="$YELLOW_TEXT"
#BOLD="$YELLOW_BOLD"
#TEXT="$PURPLE_TEXT"
#BOLD="$PURPLE_BOLD"
#TEXT="$GREY_TEXT"
#BOLD="$GREY_BOLD"

# If you want to display something different to the hostname, change it from \h:
HOST="\h"               # eg: "mango"
#HOST="\u@\h:\l"        # eg: "john@mango:1"

# Choose to end with either the full username, or just the $ or # symbol:
ENDING='\$'       # Single character (eg: "$" for users or "#" for root)

# The next 3 lines cause a red background if the previous command returned an error:
PS1_OK="${BOLD}${HOST} ${TEXT}\T ${BOLD}\w ${TEXT}"
PS1_ERROR="${RED_BOLD}${HOST} ${RED_TEXT}\T ${RED_BOLD}\w ${RED_TEXT}"
PS1="\$(if [[ \$? > 0 ]]; then echo -e '$PS1_ERROR'; else echo -e '$PS1_OK'; fi)${ENDING}${RESET} "



######################################################################
# Enable color support of ls and also add handy aliases:
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    COLOR='--color=auto'
fi

# Set ls parameters:
alias ls='ls -AFh --time-style=long-iso $COLOR'
# Create shortcuts for ls:
alias l='ls -o'     # Long list format (like "ls -l" but better)
alias lt='l -tr'    # Sorted by time & date (in reverse)
alias lS='l -Sr'    # Sorted by filesize (in reverse)
# Create shortcuts for grep:
alias grep='grep $COLOR --exclude-dir=.svn'
alias fgrep='fgrep $COLOR --exclude-dir=.svn'
alias egrep='egrep $COLOR --exclude-dir=.svn'


# Create my own 'psgrep' that is basically a "ps -ef | grep" to search running processes:
alias psgrep='ps -ef | grep -v grep | grep'
# Show lots of useful info about the attached disks & storage devices:
alias lsblkf='sudo lsblk -o MODEL,NAME,LABEL,FSTYPE,SIZE,MOUNTPOINT,UUID'
