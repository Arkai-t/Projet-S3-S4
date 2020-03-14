#
# general information
#

import os

import sys

# copyright information

copyright = "Copyright (C) 2006-2007 Eric Fimbel , Fatronik. General Public License."

# this computer

cpu = os.environ.get( "COMPUTERNAME" )

if cpu is None : cpu = "someComputer"

# possible drives (or volumes) accessible from this computer (browsing is allowed)

if sys.platform == "win32" :

    driveList = [
        "A:",
        "B:",
        "C:",
        "D:",
        "E:",
        "F:",
        "G:",
        "H:",
        "I:",
        "J:",
        "K:",
        "L:",
        "M:",
        "N:",
        "O:",
        "P:",
        "Q:",
        "R:",
        "S:",
        "T:",
        "U:",
        "V:",
        "W:",
        "Y:",
        "Z:",
        ]

elif sys.platform == "linux2" :

    driveList = [
        "/"
        ]

else :

    driveList = [
        "/"
        ]

# contact information

email =	"efimbel@fatronik.com"

# book case and items to classify

# book case and items to classify

if sys.platform == "win32" :
    
    bookcase = "x:/bookcase/"

    classify = "x:/classify/"

    export = "x:/export/"

elif sys.platform == "linux2" :
    
    bookcase = "x:/bookcase/"

    classify = "x:/classify/"

    export = "x:/export/"
else :
    
    bookcase = "x:/bookcase/"

    classify = "x:/classify/"

    export = "x:/export/"


# organization

organization = "Fatronik"

# program

program = "FTK Doc"

# current version

version	= "Beta - 2009 04 15"

# web site

web = "http://www.fatronik.com"



