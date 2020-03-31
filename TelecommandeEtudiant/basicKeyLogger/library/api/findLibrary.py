""" Finds the python library of current application, and redirects python to the local copy

    Original file : (libraryPython)templates/findLibrary.py

    To use this script, insert instruction "import findLibrary" in your main script.

    The python library will be detected, and the path added to the environment variable sys.path.

    Then, import modules of the python library as usual ( import x.y or from x.y import * )

    in case of error, the execution aborts with a console message
    
    """

import sys  # built in

import imp  # built in

import os



def checkArguments ( ) :

    """ checks the arguments of the command line, reorders them if needed and extracts the library path if it exists """

    if len( sys.argv ) <= 1 : return None


    # splits the arguments that contain quotes
    
    wordList = [ ]

    for argument in sys.argv :

        wordList.extend( argument.split( '"' ) )


    # places all the arguments that start with "--" at the end, and joins the others into words

    noMinusList = [ ]

    minusList = [ ]

    argument = ""

    for word in wordList[ 1 : ] :

        # strips spaces and quotes
        
        word = word.strip( " \"'" ) 

        if word.startswith( "--" ) :

            minusList.append( word )

            if len( argument ) > 0 : noMinusList.append( argument )

            argument = ""

        elif argument == "" :

            argument = word

        else :

            argument = argument + " " + word

    if len( argument ) > 0 : noMinusList.append( argument )


    # library = 1st argument of the form "-- ... /" that exists

    libraryPath = None

    for argument in minusList :

        if ( ( argument.endswith( os.sep ) ) and ( os.path.exists( argument.strip( "- " ) ) ) ) :

             libraryPath = argument.strip( "-" )

             break

    # recomposes the command line
        
    sys.argv = wordList[ : 1 ] + noMinusList + minusList        

    return libraryPath

 
    
def browseDirectory ( directory ) :

    """ browses the entire directory to find the python library directory """

    library = "libraryPython"

    if not directory.endswith( os.sep ) : directory = directory + os.sep

    try :

        items = os.listdir( directory )

    except Exception, exception :

        items = [ ]

    for item in items :

        if item == library :

            if not item.endswith( os.sep ) : item = item + os.sep

            return directory + item 

        if item.startswith( "." ) : continue

        if item.startswith( "_" ) : continue

        if item.startswith( "~" ) : continue

        if not os.path.isdir( directory + item ) : continue

        found = browseDirectory( directory + item  )

        if not found is None : return found

    return None
    

    

def findDirectory ( path ) :

    """ finds a subdirectory of path "libraryPython/. Checks in the following order

        1 current path ( path == ../libraryPython)

        2 parent ( path == ../libraryPython/x )
        
        3 subdirectory path/libraryPython

        4 subdirectories path/*/libraryPython

        then iterates 1, 2, 3, 4 with parents ( path/.., path/../.., etc. )

        
        """

    if path is None : return None

    library = "libraryPython"

    if sys.platform.startswith( "win" ) :

        path = path.lower()

        library = library.lower()

    directory, dummy = os.path.split( path )

    # particular cases: we are in the library, or in a subfolder of the library

    if path.endswith( os.sep + library ) : return path

    if directory.endswith( os.sep + library  ) : return directory      # **EF os.sep + ...

    # looks in subdirectories
    
    while True :

        # looks for path/libraryPython/

        libraryPath = path + os.sep + "libraryPython" 

        if os.path.exists( libraryPath ) : return libraryPath

        # looks for path/*/libraryPython/
        
        items = os.listdir( path )

        for item in items :

            libraryPath = path + os.sep + item + os.sep + "libraryPython"
            
            if os.path.exists( libraryPath ) : return libraryPath


        # goes to parent directory
    
        directory, dummy = os.path.split( path )

        # not found

        if directory == path : break

        path = directory

    return None




def localPython ( localPath ) :

    """ replaces the standard python library ( exists or not ) by the local one (when exists) """

    if not type( localPath ) == str : return

    if not localPath.endswith( os.sep ) : localPath = localPath + os.sep

    # reads the paths to add to sys.path
    
    try :

        handler = open( localPath + "sysPath.txt", "r" )

        text = handler.read()

        handler.close()

        items = text.splitlines()

    except Exception, exception :

        items = [ ]


    # places the local paths before the previous search paths. only those that exist

    sysPath = [ ]

    for item in items :

        item = item.strip().replace( "\\", os.sep ).replace( "/", os.sep )

        if len( item ) == 0 : continue

        item = item.strip( os.sep )

        item = localPath + item

        if item in sysPath : continue

        if not os.path.exists( item ) : continue

        sysPath.append( item )

    # places the previous paths. only those that exist


    for item in sys.path :

        if item in sysPath : continue

        if not os.path.exists( item ) : continue

        sysPath.append( item )

    sys.path = sysPath

    
##    
##    # sets the environment variable for TKinter dynamic loading ( otherwise, sublibraries of Tkinter are searched in standard installation )
##    
##    if sys.platform == "linux2" :
## 
##        os.environ[ "TCL_LIBRARY" ] = localPath + os.sep + "lib" + os.sep + "tcl84" + os.sep

    




def main ( ) :
    

    """ main function executed every time that the module is included """

    # checks the command line

    libraryPath = checkArguments()

    # checks whether the library path is defined in a file pythonLibrary.txt

    if libraryPath is None : libraryPath = readLink()

    # checks for current directory

    if libraryPath is None : libraryPath = findDirectory( os.getcwd() )

    # checks whether the current execution prefix ( the directory where we are running python ) contains libraryPython

    if libraryPath is None : libraryPath = findDirectory( sys.exec_prefix )

    # not found

    if libraryPath is None :

        raw_input( sys.argv[ 0 ] + " - fatal error : library not found. Press any key" )

        sys.exit( 1 )

    # adds final / if required

    libraryPath = libraryPath.rstrip( "\\/" ) + os.sep

    # writes the link file (contains library path, speeds up next execution)

    writeLink( libraryPath )

    # appends library and root to search path

    if not libraryPath in sys.path : sys.path = [ libraryPath ] + sys.path

    # appends library and the local copy of python to the system search path so that local python modules have priority

    if os.path.exists( libraryPath + os.sep + sys.platform ) : localPath = libraryPath + os.sep + sys.platform + os.sep

    elif os.path.exists( libraryPath + os.sep + "python" ) : localPath = libraryPath + os.sep + "python" + os.sep

    else : localPath = None

    if not localPath is None : localPython( localPath )

    # writes the python library directly in sys, for next modules

    sys.libraryPath = libraryPath

    # writes the root of python library in sys, for next modules

    rootPath, dummy = os.path.split( libraryPath.rstrip( "\\/" ) )

    rootPath = rootPath + os.sep

    sys.rootPath = rootPath

    if not rootPath in sys.path : sys.path = [ rootPath ] + sys.path

    # sets the environment variables (session) for GUIs

    if not localPath is None : setEnvironment( localPath )



def readLink ( ) :

    """ reads the file findLibrary.txt, if exists, and checks whether the content exists """

    path = os.curdir + os.sep + "findLibrary.txt"

    if not os.path.isfile( path ) : return None

    handler = file( path )

    text = handler.read().strip()

    handler.close()

    if not text.endswith( os.sep ) : text = text + os.sep

    if not os.path.isdir( text ) : return None

    return text




def setEnvironment ( localPath ) :

    """ sets the environment variables for the graphical toolkits """

    gtkPath = localPath + "GTK" + os.sep + "bin"

    tclPath = localPath + "tcl"

    os.environ[ "PATH" ] = os.environ[ "PATH" ] + ";" + gtkPath + ";" + tclPath + ";"

    os.environ[ "TCL_LIBRARY" ] = tclPath + os.sep + "tcl8.4"

    os.environ[ "TK_LIBRARY" ] = tclPath + os.sep + "tk8.4"

    os.environ[ "TIX_LIBRARY" ] = tclPath + os.sep + "tix8.1"



    
def writeLink ( text ) :

    """ writes the file findLibrary.txt in library """

    if not type( text ) == str : return False

    text = text.strip()

    if not text.endswith( os.sep ) : text = text + os.sep

    text = os.path.abspath( text )

    text = os.path.expanduser( text )

    if not text.endswith( os.sep ) : text = text + os.sep

    try :
    
        handler = file( text + "findLibrary.txt", mode = "w" )

        handler.write( text )

        handler.close()

    except Exception, exception :

        return False
        
    return True

    

    




# here we go...

main()



