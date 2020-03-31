""" Application launcher.

    configures the library, then launches argument and/or content of file library/launch.txt

    
    """

import sys  # built in

import imp  # built in

import os

import __init__


def error (

    text,
    fatal = False
    ) :

    """ displays an interactive error message if there is a console.

        if error is fatal, stops execution

        """

    text = str( text )

    directory, name = os.path.split( sys.executable )

    identifier, extension = os.path.splitext( name )

    if identifier.lower() == "python" :

        if bool( fatal ) : prefix = "fatal error - "

        else : prefix = "warning - "

        text = str( text )

        if ( not text.endswith( "\n" ) ) and ( len( text ) > 60 ) : text = text + "\n"

        raw_input( prefix + " " + str( text ) + " Press any key" )

    if bool( fatal ) : sys.exit( 1 )

    


def go (

    module = None

    ) :
    

    """ main function. called when module is directly executed ( python launch.py ) and/or manually

        sets the search paths sys.path

        if there is a local copy of python redirects search paths to it and prepares environment variables

        executes module defined in launch.txt, in command line or passed as argument
        
        """



    # loads module to execute or loads it from command line

    if not module is None :

        module = module.\
                 replace( "(root)", sys.rootPath ).\
                 replace( "(library)", sys.libraryPath ).\
                 replace( "(configuration)", sys.configurationPath ).\
                 replace( os.altsep, os.sep ).\
                 replace( os.sep + os.sep, os.sep )

        path = os.path.abspath( os.path.expanduser( module ) )

    elif len( sys.argv ) >= 2 :

        path = sys.argv[ 1 ].replace( os.altsep, os.sep ).replace( os.sep + os.sep, os.sep )

        path = os.path.abspath( os.path.expanduser( path ) )

    else :

        path = readModule()

        if path is None : return True

    ok = startModule( path )

    return ok

        





def readModule (

    path = None
    ) :

    """ reads file "launch.txt" and returns a path to script to execute *.py """

    # by default, reads the file in directory of py file in execution

    if path is None :

        path = os.path.abspath( os.path.expanduser( __file__ ) )

        directory, dummy = os.path.split( path )

        name = "launch.txt"

        path = directory + os.sep + name

    # normalizes
    
    else :        

        path = os.path.abspath( os.path.expanduser( path ) )

        directory, name = os.path.split( path )

    # absent

    if not os.path.isfile( path ) : return None
    
    # changes directory to solve relative paths
    
    current = os.getcwd()

    os.chdir( directory )

    # reads

    try :
        
        handler = file( path )

        text = handler.read().strip()

        handler.close()

    except Exception, exception :

        error( "Could not read " + path + "\n  " + str( exception )+ "\n" )

        return None
        

    # gets the path (non blank line)

    text = text.\
           replace( "(root)", sys.rootPath ).\
           replace( "(library)", sys.libraryPath ).\
           replace( "(configuration)", sys.configurationPath ).\
           replace( os.altsep, os.sep ).\
           replace( os.sep + os.sep, os.sep ).\
           replace( "\t", " " ).\
           replace( "\n", " " ).\
           strip()

    text = os.path.abspath( os.path.expanduser( text ) )

    return text




def startModule (

    path
    ) :

    """ starts the module path, i.e. loads it and executes go/start/execute/run/main """

    if not type( path ) == str : return False

    path = path. \
           replace( "(root)", sys.rootPath ).\
           replace( "(library)", sys.libraryPath ).\
           replace( "(configuration)", sys.configurationPath ).\
           replace( os.altsep, os.sep ).\
           replace( os.sep + os.sep, os.sep )

    path = os.path.abspath( os.path.expanduser( path ) )
    
    if not os.path.isfile( path ) : error( "Could not find module " + path, fatal = True )

    directory, name = os.path.split( path )

    identifier, extension = os.path.splitext( name )

    if ( not extension == "" ) and ( not extension.startswith( ".py" ) ) : error( "Invalid module (not a .py* file) " + path, fatal = True  )

    # adds the current directory to the search paths

    if not directory in sys.path : sys.path.append( directory )

    try :

        module = imp.load_source( identifier, path )

    except Exception, exception :

        error( "Could not load module " + identifier + "\n  " + str( exception ) + "\n", fatal = True )

    # starts : tries methods go, execute, run, start, main.
    #
    # Note: if module executes stuff as soon as loaded (NOT recommended), this part is useless and/or redundant
    #
    

    for item in [ "go", "execute", "run", "start", "main" ] :

        if not item in dir( module ) : continue

        method = getattr( module, item )

        if not callable( method ) : continue

        try :

            method()

            return True

        except Exception, exception :

            None


        



# here we go...

if __name__ == "__main__" :

    go()

