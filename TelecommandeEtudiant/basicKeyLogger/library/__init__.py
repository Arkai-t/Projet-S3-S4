""" Application launcher.

    Modifies sys.path to access the library and launches the script execute.py(w) if it is found in the path

    define paths in sysPath.txt . USE RELATIVE PATHS FROM THIS DIRECTORY. Use / or \\.


    
    """

import sys  # built in

import imp  # built in

import os


def cleanPath (

    items = None,
    standalone = False

    ) :

    """ cleans sys.path from duplicates and non existing paths

        adds "" at beginning, if not already here

        if standalone is True, keeps only paths within rootPath

        """

    if items is None : items = list( sys.path )
    
    filtered = [ ]
    
    # places the previous paths. only those that exist (removes the void prefix "", not important: will be added again later)

    for item in items :

        if not type( item ) == str : continue

        if item == "" : continue

        if sys.platform =="win32" : item = item.lower()

        if item in filtered : continue

        if not os.path.exists( item ) : continue

        if ( bool( standalone ) ) and ( not item.startswith( sys.rootPath.lower() ) ) : continue

        filtered.append( item )

    sys.path = [ "" ] + filtered
    


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

    


def makePackage (

    path
    ) :

    """ makes a package from a directory.
        If does not exist creates it.
        Makes a package of it by adding __init__.py

        """
    
    if not type( path ) == str : return False

    if len( path ) <= 0 : return False

    path = path.\
           replace( "(root)", sys.rootPath ).\
           replace( "(library)", sys.libraryPath ).\
           replace( "(configuration)", sys.configurationPath ).\
           replace( os.altsep, os.sep ).\
           replace( os.sep + os.sep, os.sep ).\
           rstrip( os.sep )

    path = os.path.abspath( os.path.expanduser( path ) )

    try :
    
        if not os.path.exists( path ) : os.mkdir( path )

    except Exception, exception :

        error( "could not create " + path + "\n" + str( exception ) + "\n" )

        return False

    initPy = path + os.sep + "__init__.py"

    if not os.path.exists( initPy ) :

        try :        

            handler = file( initPy, mode = "w" )

            handler.close()


        except Exception, exception :

            error( "could not create " + initPy + "\n" + str( exception ) + "\n" )

            return False

    return True
        




def go ( ) :
    

    """ main function. called when module is directly executed ( python launch.py ) and/or manually

        sets the search paths sys.path

        if there is a local copy of python redirects search paths to it and prepares environment variables

        executes module defined in launch.txt, in command line or passed as argument
        
        """

    # path to library

    libraryPath, dummy = os.path.split( os.path.abspath( os.path.expanduser( __file__ ) ) )

    # root of python library 

    rootPath, dummy = os.path.split( libraryPath )

    # configuration directory. If exists in root directory (root/configuration/) overrides the local directory library/configuration/. 

    if os.path.isdir( rootPath + os.sep + "configuration" ) : configurationPath = rootPath + os.sep + "configuration"

    else : configurationPath = libraryPath + os.sep + "configuration"

    # writes the python library (also used as workpath for messages) and root path directly in sys, for next modules

    sys.libraryPath = libraryPath + os.sep

    sys.workPath = sys.libraryPath

    sys.rootPath = rootPath + os.sep

    sys.configurationPath = configurationPath + os.sep

    # makes a package of configuration/
    
    makePackage( configurationPath )

    # reads the list of paths to append to search path in directory library/

    readPath()

    # reads environment variables to define (temporary: during execution only )

    readEnvironment()

    # there is a local copy of python : processes its search paths and environment variables

    pythonPath =  libraryPath + os.sep + "python"

    standalone = False

    if os.path.isdir( pythonPath ) :

        readPath( pythonPath + os.sep + "sysPath.txt" )

        readEnvironment( pythonPath + os.sep + "osEnviron.txt" )

        standalone = os.path.exists( libraryPath + os.sep + "standalone.txt" )
    
    # places the current, library, and root directories in the search paths

    cleanPath(
        [ "", sys.rootPath, sys.libraryPath ] + sys.path,
        standalone
        ) 
    

    return True




def readEnvironment (

    path = None
    ) :

    """ reads environment variables os.environ[ .. ] to modify (temporary; only during execution) and returns True/False """


    # by default, reads the file in directory of py file in execution

    if path is None :

        path = os.path.abspath( os.path.expanduser( __file__ ) )

        directory, dummy = os.path.split( path )

        name = "osEnviron.txt"

        path = directory + os.sep + name

    # normalizes
    
    else :        

        path = os.path.abspath( os.path.expanduser( path ) )

        directory, name = os.path.split( path )

    # absent

    if not os.path.isfile( path ) : return False
    
    # changes directory to solve relative paths

    current = os.getcwd()

    os.chdir( directory )

    # reads

    try :

        handler = file( path )

        text = handler.read().strip()

        handler.close()

    except Exception, exception :

        error( "Could not read " + path + "\n  " + str( exception ) + "\n" )

        return False


    # processes lines

    pathList = [ ]

    for item in text.splitlines() :

        item = item.strip( "\t=" )

        if "=" in item : variable, content = item.split( "=", 1 )

        elif "\t" in item : variable, content = item.split( "\t", 1 )

        elif " " in item : variable, content = item.split( " ", 1 )

        else : continue

        variable = variable.strip( " \t=" ).upper()

        content = content.strip( " \t=" )

        if len( variable ) <= 0 : continue

        if len( content ) <= 0 : continue

        # normalizes paths in content (warning: cannot normalize more that curdir and pardir)

        curdir = os.path.abspath( os.path.expanduser( os.curdir ) )

        pardir = os.path.abspath( os.path.expanduser( os.pardir ) )
            
        content = content.\
                  replace( os.altsep, os.sep ).\
                  replace( os.sep + os.sep, os.sep ).\
                  replace( os.pardir + os.sep, pardir + os.sep ).\
                  replace( os.curdir + os.sep, curdir + os.sep )

        # instantiates content

        if "%" in content :
            
            if not variable in os.environ : continue

            content = content.replace( "%", os.environ[ variable ] )

        # instantiates environment variable

        os.environ[ variable ] = content

    # back to original directory
    
    os.chdir( current )

    return True
                                                         
    




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
           replace( "\t", " " ).\
           replace( "\n", " " ).\
           strip()


    text = text.\
           replace( "(root)", sys.rootPath ).\
           replace( "(library)", sys.libraryPath ).\
           replace( "(configuration)", sys.configurationPath ).\
           replace( os.altsep, os.sep ).\
           replace( os.sep + os.sep, os.sep )

    text = os.path.abspath( os.path.expanduser( text ) )

    return text




def readPath (

    path = None
    ) :

    """ reads the file sysPath.txt normalizes and adds to sys.path

        all paths returned exist

        """

    # by default, reads the file in directory of py file in execution

    if path is None :

        path = os.path.abspath( os.path.expanduser( __file__ ) )

        directory, dummy = os.path.split( path )

        name = "sysPath.txt"

        path = directory + os.sep + name


    # normalizes
    
    else :        

        path = os.path.abspath( os.path.expanduser( path ) )

        directory, name = os.path.split( path )

    # absent
        
    if not os.path.isfile( path ) : return False

    # changes directory to solve relative paths
  
    current = os.getcwd()

    if not directory == current : os.chdir( directory )

    # reads

    try :

        handler = file( path )

        text = handler.read().strip()

        handler.close()

    except Exception, exception :

        error( "Could not read " + path + "\n  " + str( exception ) + "\n" )

        return False

    # processes lines

    for item in text.splitlines() :

        item = item.\
               replace( "\t", " " ).\
               replace( "\n", " " ).\
               strip()


        if len( item ) <= 0 : continue

        item = item.\
               replace( "(root)", sys.rootPath ).\
               replace( "(library)", sys.libraryPath ).\
               replace( "(configuration)", sys.configurationPath ).\
               replace( os.altsep, os.sep ).\
               replace( os.sep + os.sep, os.sep ).\
               rstrip( os.sep )

        item = os.path.abspath( os.path.expanduser( item ) )

        if not os.path.isdir( item ) : continue

        if item in sys.path : continue

        sys.path.append( item )

    # back to original directory
    
    if not directory == current : os.chdir( current )

    return True



def startModule (

    path
    ) :

    """ starts the module path, i.e. loads it and executes go/start/execute/run/main """

    if not type( path ) == str : return False

    path = path.\
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

        

# prepares the library

go()
