
""" Standard paths. Can be overridden from a configuration file


    """


import os 

import sys

from api.Utilities import *

##from api.TableFile import *


class Paths :

    """ Standard paths. Can be overridden from a configuration file """



    # defines root and library from sys (initialized formerly by findLibrary.py)

    try :

        libraryPath = sys.libraryPath

        rootPath = sys.rootPath

    except Exception, exception :

        raw_input( sys.argv[ 0 ] + " - fatal error : library not found. Press any key" )

        sys.exit( 1 )


    # python library & root directory

    libraryPath = utilities.normalizePath( libraryPath + os.sep, normalize = False )

    rootPath = utilities.normalizePath( rootPath + os.sep, normalize = False )

    # prepares configuration so that it is a package, adds parent of configuration/ to search path

    if not rootPath in sys.path : sys.path = [ rootPath ] + sys.path
           


    # loads standard, then tries the redefined file and if fails, reloads original

    from path_configuration import *

    try :

        from configuration.path_configuration import *

    except Exception, exception :

        from path_configuration import *



    # relative paths start from rootPath

    if not utilities.isAbsolutePath( configurationPath ) : configurationPath =  rootPath + configurationPath
    
    if not utilities.isAbsolutePath( notesPath ) : notesPath =  rootPath + notesPath

    if not utilities.isAbsolutePath( pendingPath ) : pendingPath =  rootPath + pendingPath

    if not utilities.isAbsolutePath( proceduresPath ) : proceduresPath =  rootPath + proceduresPath

    if not utilities.isAbsolutePath( typesPath ) : typesPath =  rootPath + typesPath

    if not utilities.isAbsolutePath( workPath ) : workPath =  rootPath + workPath


    # if configuration has changed, adds its parent to the search paths

    parentDirectory = utilities.pathDirectory( configurationPath )

    if not parentDirectory in sys.path : sys.path = [ parentDirectory ] + sys.path
       

    # if needed, converts configuration into a package (adds __init__.py) and copies all the *_configuration.py files in it
    
    if not utilities.filePresent( configurationPath + "__init__.py" ) :
        
        utilities.fileCreate( configurationPath + "__init__.py" )

        modules = utilities.directoryContent( libraryPath, annotate = True )

        for module in modules :

            if module.startswith( "_" ) : continue

            if not utilities.filePresent( libraryPath + module + "__init__.py" ) : continue

            items = utilities.directoryContent( libraryPath + module, annotate = True )

            for item in items :

                if not item.endswith( "_configuration.py" ) : continue

                utilities.fileCopy(
                    libraryPath + module + os.sep + item,
                    configurationPath + item,
                    filter = True
                    )

        



    # copies the paths in sys, so that they are directly accessible from any module

    sys.rootPath = rootPath

    sys.configurationPath = configurationPath

    sys.typesPath = typesPath
        
    sys.proceduresPath = proceduresPath     

    sys.notesPath = notesPath

    sys.pendingPath = pendingPath
        
    sys.workPath = workPath



