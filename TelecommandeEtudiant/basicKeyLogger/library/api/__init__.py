""" This module contains a general context manager ( singleton Context ), an API ( singleton Utilities ) and
    miscellaneous classes for communication, logs, book keeping, etc

    """


# prepares the library. uses __init__.py one level above

import sys

import os

import imp

def main( ) :

    # already initialized
    
    if "libraryPath" in dir( sys ) : return

    # current directory ( package )

    directory, module = os.path.split( os.path.abspath( os.path.expanduser( __file__ ) ) )

    # library directory

    library, package = os.path.split( directory )

    # no initialization

    if not os.path.isfile( library + os.sep + "__init__.py" ) : return
    
    # parent directory

    parent, name = os.path.split( library )

    try :

        current = os.getcwd()

        os.chdir( parent )

        module = imp.load_source( name, library + os.sep + "__init__.py" )

        os.chdir( current )

    except Exception, exception :

        pass
    

# initializes

main()
