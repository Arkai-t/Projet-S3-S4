""" tool for ftk sid. Builds the python and C blocks

    takes the sources in source_blocks, compiles C into dynamic libraries (DLL, SO) and copies to directory configuration/

    uses templates for the C.
    
    """

import sys

import os

import library

from api.Utilities import *



def build (
    
    path = None,
    compilerScript = None
    ) :

    """ Builds C dll wrappers.

        takes the sources in configuration/ compiles C into dynamic libraries (DLL, SO) 

        uses templates from tools/templates/ and C compiler (TCC) from tools/tcc/.
        
        """

    # sources = current directory

    sources = utilities.normalizePath( os.curdir + os.sep, normalize = False )

    # no argument : builds the entire sources directory

    if utilities.isEmpty( path ) :

        result = True

        items = utilities.directoryContent( os.curdir, annotate = True )

        for item in items :

            if item.startswith( "_" ) : continue

            if item.startswith( "~" ) : continue

            if item.startswith( "." ) : continue

            if not item.endswith( ".c" ) : continue

            ok = build(
                item,
                compilerScript
                )

            if not ok : result = False

        return result

    # otherwise, processes (here there is control on path, could come from elsewhere)

    path = utilities.normalizePath( path, normalize = False )

    directory = utilities.pathDirectory( path )

    name = utilities.pathName( path )

    extension = utilities.pathExtension( path )

    if utilities.isEmpty( extension ) : extension = "c"

    # controls

    if not directory == sources :

        print "misplaced file", directory + os.sep + name + "." + extension, " must be in ", sources

        return False


    if not extension == "c" :

        print "invalid extension", name, ".", extension, "sources must be .c files"

        return False

    # looks for the file in current directory
    
    if not utilities.filePresent( name + ".c" ) :

        print "missing file ", sources + name + ".c"

        return False


    # copies the file in a temporary

    utilities.fileCopy( name + ".c", "_" + name + ".c" )


    # writes the file completed with header and footer, replaces call by _call (naming conflict otherwise)

    try :

        templatePath = sys.rootPath + "tools" + os.sep + "templates" + os.sep

    except Exception, exception :

        templatePath = os.curdir + os.sep

    header = utilities.fileRead( templatePath + "c_header_" + sys.platform + ".h" )

    text = utilities.fileRead( name + ".c" ).replace( "int call", "int _call" )

    footer = utilities.fileRead( templatePath + "c_footer_" + sys.platform + ".h" )

    utilities.fileWrite( name + ".c", header + text + footer )

    # compiles

##    os.system( compilerDirectory + "tcc" + " " + "-shared" + " " + name + ".c" )
##

    os.system( compilerScript.replace( "(1)", name ) )


    # renames

    utilities.fileCopy( "_" + name + ".c", name + ".c" )

    utilities.fileDelete( "_" + name + ".c" )

    print "compiled : ", name + ".c"



def main (

    name = None

    ) :

    """ compiles a file configuration/name.c or if name is undefined all configuration/*.c """


    # root and subdirectories

    try :

        directory = sys.configurationPath

    except Exception, exception :

        directory = os.curdir + os.sep

    if sys.platform == "linux2" : compilerScript = "tcc -c (1).c -o (1).o ; gcc -shared (1).o -o (1).so"

    elif sys.platform == "win32" : compilerScript = "..\\tools\\tcc\\tcc.exe -shared (1).c"

    else :

        print "only for Linux & Win os, sorry"

        sys.exit( 0 )
    
    # goes to sources

    utilities.gotoDirectory( directory )

    # path is void or a file

    if utilities.isEmpty( name ) : path = ""

    else : path = directory + name + ".c"

    # builds library(ies)

    build(
        path,
        compilerScript
        )



    


    

if __name__ == "__main__" :

    print "compile name == main"

    # normalizes argument

    if len( sys.argv ) < 2 : name = ""

    elif utilities.isEmpty( sys.argv[ 1 ] ) :  name = ""

    else : name = utilities.pathName( sys.argv[ 1 ] )

    main( name )

