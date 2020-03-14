
""" Class for building an image directory for installation, cleaning sources, etc.

    """

import imp

import pydoc

from api.Context import *


class Installer :

    """ Class for building an image directory for installation, cleaning sources, etc.

        """

    # default values

    _defaultDeliveryPath = ""

    _defaultConfigurationPath = "installer.ini"

    _defaultImagePath = "installer.txt"



    # list of commands

    commandList = [
        "archive",
        "create",
        "delete",
        "document",
        "linux",
        "mac",
        "python",
        "windows",
        ]
   
    # configuration file ( list of files and directory to install )

    configurationPath = None
    
    # delivery to install
    
    deliveryPath = None

    # end of lines for different os:  linux, windows, mac

    eolList = [ "\n", "\r\n", "\r\n" ]
    
    # error
    
    error = None

   
    # header line
    
    headerLine = "#!(libraryPython)python/python"


    # path to file containing the content of the image

    imagePath = None
    
    
    # license 

    licenseLines = [

            "",
            "# --------------------------------------------------------------------",
            "# (program) (version)",
            "# (copyright)",
            "# Contact: (email)",
            "# Web site: (web)",
            "# This program is free software; you can redistribute it and/or modify",
            "# it under the terms of the GNU General Public License as published by",
            "# the Free Software Foundation; either version 2 of the License",
            "# This program is distributed in the hope that it will be useful,",
            "# but WITHOUT ANY WARRANTY; without even the implied warranty of",
            "# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the",
            "# GNU General Public License for more details.",
            "#",
            "# You should have received a copy of the GNU General Public License along",
            "# with this program; if not, write to the Free Software Foundation, Inc.,",
            "# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.",
            "",
            ]

    # flag giving the result of an operation

    modified = None
        
    # possible types of format ( and OS )
    
    osList = [ "linux", "mac", "windows" ]
    
    # protect string:  after this line, nothing is modified
    
    protectLines = [
        "# no refactor",
        "from api.Context import *",
        "# finds the python library",
        '"""',
        "'''",
        ]

    # import lines that will be removed (redundant)
    
    uselessLines = [
        "#",       
        "import",
        "from",
        ]

    
    
    
    def __init__ (

        self,
        delivery = None,
        configuration = None,
        image = None,
        ) :

        """ Initializes 

            """

        if utilities.isEmpty( delivery ) : self.deliveryPath = utilities.pathDelivery( "" )

        else : self.deliveryPath = utilities.normalizePath( delivery, normalize = False )

        # sets the delivery variable so that it can be used in the paths

        context.deliveryValue = self.deliveryPath

        # configuration file

        if utilities.isEmpty( configuration ) : self.configurationPath = self._defaultConfigurationPath

        else : configuration = utilities.normalizePath( configuration, normalize = False )

        # file containing the content of the image

        if utilities.isEmpty( image ) : self.imagePath = self._defaultImagePath

        else : self.imagePath = utilities.normalizePath( image, normalize = False )

        # reads configuration file
        
        self.readConfigurationFile()

        # reads file containing the content of image directory

        self.readImageFile()


    def archive (

        self,
        target = None,
        pattern = None
        ) :

        """ Creates a zip file for a file, a directory or a set of files """

        if utilities.isEmpty( target ) : return False

        isFile = not target.endswith( os.sep )

        isPattern = not utilities.isEmpty( pattern )

        # deletes a file
        
        if isFile :

            result = self.fileArchive( target, comment = "Original" )
            
            print " create archive of file (...)", target[ -32 : ], "\n      ", result, "\n"

        # deletes list of files ( takes them for source, creates them in target

        elif isPattern :

            fileList = self.files( target, pattern )

            if utilities.isEmpty( fileList ) :

                result = False

                return

            result = True

            for targetItem in fileList :

                ok = self.fileArchive( targetItem, comment = "Original" )

                print " create archive of files (...)", targetItem[ -32 : ], "\n      ", ok, "\n"

                result = result and ok

        # deletes directory

        else :

            result = self.fileArchive( target, comment = "Original" )
        
            print " create archive of directory (...)", target[ -32 : ], "\n      ", result, "\n"

            
        return result



    def convert (

        self,
        target = None,
        pattern = None,
        format = None
        ) :

        """ Converts an ascii file to linux/windows format """

        if utilities.isEmpty( target ) : return False

        isFile = not target.endswith( os.sep )

        isPattern = not utilities.isEmpty( pattern )

        # format

        if utilities.isEmpty( format ) : format = "windows"

        # converts a single file
        
        if isFile :

            result = self.fileAsciiConvert( target, format = format )
            
            print " ", format, " conversion of file (...)", target[ -32 : ], "\n      ", self.modified, result, utilities.error, "\n"

        # converts list of files ( takes them for source, creates them in target

        elif isPattern :

            fileList = self.files( target, pattern )

            if utilities.isEmpty( fileList ) :

                result = False

                return

            result = True

            for targetItem in fileList :

                ok = self.fileAsciiConvert( targetItem, format = format )

                print " ", format, " conversion of files (...)", targetItem[ -32 : ], "\n      ", self.modified, ok, utilities.error, "\n"

                result = result and ok

        # converts directory: error

        else :

            print "Installer.convert - cannot convert directory"

            result = False

            
        return result


    

    def copy (

        self,
        source = None,
        target = None,
        pattern = None
        ) :

        """ Copies a file, a list of files ( with wildcards ) or a directory """

        if utilities.isEmpty( source ) : return False

        if utilities.isEmpty( target ) : return False

        isFile = not source.endswith( os.sep )

        isPattern = not utilities.isEmpty( pattern )
                
        # single file copy

        if isFile :

            result = utilities.fileCopy( source, target )

            print " copy file (...)", source[ -32 : ],"\n           (...)", target[ -32 : ], "\n      ", result, "\n"

        # pattern copy ( multiple files )

        elif isPattern :

            fileList = self.files( source, pattern )

            if utilities.isEmpty( fileList ) :

                result = False

                return

            result = True

            for sourceItem in fileList :

                targetItem = target + sourceItem[ len( source ) : ]

                ok = utilities.fileCopy( sourceItem, targetItem )

                print " copy files (...)", sourceItem[ -32 : ],"\n            (...)", targetItem[ -32 : ], "\n      ", ok, "\n"

                result = result and ok

        # directory copy

        else :

            result = utilities.directoryCopy( source, target )

            print " copy directory (...)", source[ -32 : ],"\n                (...)", target[ -32 : ], "\n      ", result, "\n"


        return result


    
    def create (

        self,
        target = None,
        pattern = None
        ) :

        """ Creates a file or a set of files """

        if utilities.isEmpty( target ) : return False

        isFile = not target.endswith( os.sep )

        isPattern = not utilities.isEmpty( pattern )

        # creates a file
        
        if isFile :

            result = utilities.fileCreate( target )
            
            print " create file (...)", target[ -32 : ], "\n      ", result, "\n"


        # creates list of files ( impossible )

        elif isPattern :

            print "Installer.create - cannot create with patterns"

            result = False


        # directory create

        else :

            result = utilities.directoryCreate( target )
        
            print " create directory (...)", target[ -32 : ], "\n      ", result, "\n"

            
        return result



    def delete (

        self,
        target = None,
        pattern = None
        ) :

        """ Deletes a file, a directory or a set of files """

        if utilities.isEmpty( target ) : return False

        isFile = not target.endswith( os.sep )

        isPattern = not utilities.isEmpty( pattern )

        # deletes a file
        
        if isFile :

            result = utilities.fileDelete( target )
            
            print " delete file (...)", target[ -32 : ], "\n      ", result, "\n"

        # deletes list of files ( takes them for source, creates them in target

        elif isPattern :

            fileList = self.files( target, pattern )

            if utilities.isEmpty( fileList ) :

                result = False

                return

            result = True

            for targetItem in fileList :

                ok = utilities.pathDelete( targetItem )

                print " delete files (...)", targetItem[ -32 : ], "\n      ", ok, "\n"

                result = result and ok

        # deletes directory

        else :

            result = utilities.directoryDelete( target )
        
            print " delete directory (...)", target[ -32 : ], "\n      ", result, "\n"

            
        return result



    def document (

        self,
        target = None,
        pattern = None
        ) :

        """ Documents a file or a set of files. These files must be python scripts. """

        if utilities.isEmpty( target ) : return False

        isFile = not target.endswith( os.sep )

        isPattern = not utilities.isEmpty( pattern )

        # documents a file
        
        if isFile :

            result = self.fileDocument( target )
            
            print " document file (...)", target[ -32 : ], "\n      ", result, "\n"


        # documents a list of files 

        elif isPattern :



            fileList = self.files( target, pattern )

            if utilities.isEmpty( fileList ) :

                result = False

                return

            result = True

            for targetItem in fileList :

                ok = self.fileDocument( targetItem )

                print " document files (...)", targetItem[ -32 : ], "\n      ", ok, "\n"

                result = result and ok


        # documents a directory ( impossible )

        else :

            result = self.fileDocument( target )
            
            print " document directory (...)", target[ -32 : ], "\n      ", result, "\n"

            
        return result


    def fileArchive (

        self,
        path = None,
        comment = None
        ) :

        """ Creates an archive copy of the file or directory, in the correct _archives/ subdirectory, with
            desired tag

            """

        if utilities.isEmpty( path ) : return False

        result = archiver.backup(
            path = path,
            prefix = ""
            comment = comment
            )

        return result

        
        

    def fileAsciiConvert (

        self,
        path = None,
        format = None
        ) :
                
        """ Converts an ASCII file to the desired OS, uses the appropiate end of line

            """

        # no modification no error

        self.modified = ""

        utilities.error = ""
        
        # unknown OS
        
        if not format in self.osList : return False

        # file is not here
        
        if not utilities.filePresent( path ) : return False

        # reads content
        
        text = self.fileRead( path )    # does NOT convert end of lines into \n automatically

   
        # for all files, converts line format towards \n (fileWrite will add the os-dependent end of lines)

        # normalizes end of lines to \n
        
        newText = text.replace( "\r\n", "\n" )      # CR-LF

        newText = newText.replace( "\n\r", "\n" )   # inverted LF-CR
        
        newText = newText.replace( "\r", "\n" )     # loose CR



        # adds the end of lines according to the system


        eol = self.eolList[ self.osList.index( format ) ]
        
        if not eol == "\n" : newText = newText.replace( "\n", eol ) 
        
        if not ( newText == text ) :

                ok = self.fileWrite( path, newText )

                self.modified = "modified"

                return ok

        return True
            


        

    def fileDocument (

        self,
        path = None,
        ) :
                
        """ Documents a file( python script ) or a package

            """

        # no error

        utilities.error = ""

        # this is a file
        
        if utilities.filePresent( path ) : module = self.loadModule( path )

        # this is a directory

        elif utilities.directoryPresent( path ) : module = self.loadPackage( path )


        # file or directory is absent

        else :

            utilities.error = "path not found"

            return False

        
        # could not load module

        if module is None :

            utilities.error = "could not load module"

            return False
        
        # saves current directory
        
        directory = utilities.currentDirectory( )

        # goes to parent                

        utilities.gotoDirectory( utilities.pathDirectory( path ) )

        name = utilities.pathLastNameWithoutExtension( path )

        try :

            pydoc.writedoc( module )

            result = True

        except Exception, exception :

            utilities.error = "could not produce documentation"

            result = False

        # back to original directory
        
        utilities.gotoDirectory( directory )

        return result
                
            

    def filePythonRefactor (

        self,
        path = None
        ) :
                
        """ Prepares a  Python source file.

            Inserts headerLine and headers and license, etc.

            """

        # for now, no modification, no error

        self.modified = ""

        utilities.error = ""


        # not here
        
        if not utilities.filePresent( path ) :

            utilities.error = "file not found " + path

            return False
        
        text = utilities.fileRead( path )   # converts end of lines into \n automatically

        # is there a line that protects the remainder ( # protected ) ?

        protected = self.protected( text )

        # removes useless lines before the protection line

        newText = self.removeLines( text, protected )

        
        # inserts headerLine if not already here
                
        newText = self.insertHeader( newText )

        # inserts copyright files ( previous copyright has been removed by removeLines )
            
        newText = self.insertLicense( newText )

        
        if not ( newText == text ) :

                ok = self.fileWrite( path, newText )

                self.modified = "modified"

                return ok

        return True


    def fileRead (

        self,
        path = None
        ) :

        """ Reads an entire file into a string. Does NOT convert end of lines into \n automatically """


       
        handler = utilities.fileOpen( path, mode = "rb" )

        if handler is None : return ""

        try :
            
            text = handler.read()

        except Exception, exception :

            text = ""
        
        utilities.fileClose( handler )

        return text


    
    def files (

        self,
        directory = None,
        pattern = None
        ) :

        """ Returns the list of files that match the desired pattern in the directory """

        if utilities.isEmpty( directory ) : return [ ]

        
        # no pattern : all files of directory
        
        if utilities.isEmpty( pattern ) :

            return utilities.directoryPaths(
                directory,
                recursive = 1,
                reserved = 0 )

 
        # pattern means extension xxx at any depth

        elif ( ( pattern.startswith( ";/" ) ) or ( pattern.startswith( "**/" ) ) ) :


            # content of directory

            items = utilities.directoryPaths(
                directory,
                recursive = 1,
                reserved = 0 )

            files = [ ]

            # gets the pattern, replaces \\ by /, pattern matching has problems with \\
            
            pattern = pattern[ pattern.find( "/" ) + 1 : ].replace( os.sep, "/" )

            for item in items :

                name = utilities.pathLastNameWithExtension( item )

                if item.endswith( os.sep ) : name = name + "/"

                if not utilities.match( pattern, name ) : continue

                files.append( item )

            return files


        # pattern is a good old style pattern that Python can manage

        else :
   
            return utilities.files( directory + pattern )
        


    def fileWrite (
        
        self,
        path = None,
        text = None
        ) :

        """ Writes a text into a file """

        handler = utilities.fileOpen( path, mode = "wb" )

        if handler is None : return False

        try :
            
            handler.write( text )
            
            result = True
            
        except Exception, exception :

            result = False

        result = utilities.fileClose( handler )
        
        return result
            
           

    
    def image ( self ) :

        """ Copies files and directories according to the configuration file


            format of configuration file :

            source file,        target file
            source directory,   target directory
            source directory,   target directory,

            pattern can be relative path, can contain *, ?
            
            COMMAND,             target file
            COMMAND,             target directory
            COMMAND,             target directory,   pattern

            command can be:
            DELETE,
            CREATE,
            LINUX (converts ascii files to linux format),
            MAC (converts ascii files to mac os format),
            WINDOWS (converts ascii files to windows format),
            PYTHON (prepares python source file)


            """

        if utilities.isEmpty( self.table ) : return False

        if utilities.isEmpty( self.deliveryPath ) : return False

        # copies the files and directories. read the content of the table ( content of installer.ini ) source, destination

        result = True
        
        for fields in self.table :

            if len( fields ) < 2 :

                print "Installer.image - incorrect line format"

                result = False

                continue

            # reads source. Relative paths are taken from current delivery. Instantiates variables (xxx) in path
            
            source = fields[ 0 ]

            if utilities.isEmpty( source ) :

                print "Installer.image - source is undefined"
                
                result = False

                continue

            # source is a command

            command = source.lower().replace( " ", "" )

            if command in self.commandList :

                isCommand = True

            else :

                isCommand = False

                source = utilities.instantiate( source, default = "_" )

                if not utilities.isAbsolutePath( source ) : source = self.deliveryPath + os.sep + source

                source = utilities.normalizePath( source, normalize = False )

            
            # reads target. Relative paths are taken from current delivery. Instantiates variables (xxx) in path


            target = fields[ 1 ]

            if utilities.isEmpty( target ) :

                print "Installer.image - target is undefined"

                result = False

                continue

            target = utilities.instantiate( target, default = "_" )

            if not utilities.isAbsolutePath( target ) : target = self.deliveryPath + os.sep + target

            target = utilities.normalizePath( target, normalize = False )

            # pattern ( optional )

            if len( fields ) >= 3 :

                pattern = fields[ 2 ]
                
                pattern = utilities.instantiate( pattern, default = "_" )

            else :

                pattern = ""



            # checks presence

            if isCommand :

                isFile = False

            elif ( ( not source.endswith( os.sep ) ) and ( utilities.filePresent( source ) ) ) :

                isFile = True

            elif utilities.directoryPresent( source ) :

                isFile = False

            else :

                print "Installer.install - source not found ", source

                result = False

                continue

                

            # incompatibility file - directory: normalizes the target and the source ( final / )

            if isFile :

                if target.endswith( os.sep ) : target = target + utilities.pathLastNameWithExtension( source )

            elif not isCommand :

                if not target.endswith( os.sep ) : target = target + os.sep

                if not source.endswith( os.sep ) : source = source + os.sep


            # there is a pattern, this can be only for directories

            isPattern = not utilities.isEmpty( pattern )

            if ( ( isFile ) and ( isPattern ) ) :

                print "Installer.image - file vs. pattern not allowed", source

                result = False

                continue


            # copies

            if not isCommand : result = self.copy( source, target, pattern )

            # other commands

            elif command == "archive" : result = self.archive( target, pattern )

            elif command == "create" : result = self.create( target, pattern )

            elif command == "delete" : result = self.delete( target, pattern )

            elif command == "document" : result = self.document( target, pattern )

            elif command == "linux" : result = self.convert( target, pattern, "linux" )

            elif command == "windows" : result = self.convert( target, pattern, "windows" )

            elif command == "mac" : result = self.convert( target, pattern, "mac" )

            elif command == "python" : result = self.python( target, pattern )

            else :

                print "Installer.image - unknown command ", command
                
                result = False

                continue


        return result

            


    def insertHeader (

            self,
            text = None
            ) :

            """ Inserts the headerLine lines in text if not already here

                    Removes obsolete headerLine lines, wherever they are
                    
                    """

            if utilities.isEmpty( text ) : text = ""

            # looks for 1st occurrence of header line
            
            position = text.find( self.headerLine + "\n" )

            # header line not at the beginning ? inserts
            
            if not position == 0 : text = self.headerLine + "\n" + text


            return text


               
            

                    
               
    def insertLicense (

            self,
            text = None
            ) :

            """ Inserts the import lines in text if not already here

                    Removes useless import lines
                    
                    """

            if utilities.isEmpty( text ) : text = ""

            # builds the text of import lines
            
            licenseText = ""
            
            for line in self.licenseLines :

                    licenseText = licenseText + line + "\n"


            # already present: this is all
            
            if text.find( licenseText ) >= 0 : return text

            # inserts import lines just after headerLine line
            
            position = text.find( "\n" ) + 1

            text = text[ : position ] + licenseText + text[ position : ]

            return text
            




    def loadPackage (
        
        self,
        path = None
        ) :

        """ Loads an entire package and imports it.
    
            Returns the module itself, or None in case of problem

            Remark. The internal name of the module is the name of the file, this is invisible from outside.
        
            Example of use :

            myModule = loadPackage( "c:\\toto\\titi" ) # titi contains __init__.py, titi1.py, etc.
        
            del ( myModule )

            """

        if not utilities.directoryPresent( path ) : return None

        currentDirectory = utilities.currentDirectory()

        directory = utilities.pathDirectory( path )

        name = utilities.pathLastName( path )

        if not directory == currentDirectory : utilities.gotoDirectory( directory )
        
        try :

            # gets the arguments of the "load_module function" : file, fileName, ( suffix, mode, type )

            arg2, arg3, arg4 = imp.find_module( name )
            
            module = imp.load_module( name, arg2, arg3, arg4 )

        except Exception, exception :

            utilities.error = str( exception )
            
            module = None

        if not directory == currentDirectory : utilities.gotoDirectory( currentDirectory )

        return module


    def loadModule (
        
        self,
        path = None
        ) :

        """ Loads a package module from a .py* file and imports it.
    
            Returns the module itself, or None in case of problem

            The module is named package.fileName.
        
            Example of use :

            myModule = loadPackageModule( "c:\\toto\\titi.py" )
        
            myModule.go() or eval ("toto.titi" ).go()

            del ( myModule )

            """

        if not utilities.filePresent( path ) : return None

        directory = utilities.pathDirectory( path )

        package = utilities.pathLastName( directory )

        name = utilities.pathLastNameWithoutExtension( path )

        extension = utilities.pathExtension( path )

        if not extension.startswith( "py" ) : return None

        try :

            module = imp.load_source( package + "." + name, path )

        except Exception, exception :

            print str( exception )
            
            return None

        return module
   


    def protected (

        self,
        text = None
        ) :

        """ Checks whether the text contains some protected line, and returns its position """

        if utilities.isEmpty( self.protectLines ) : return -1

        if utilities.isEmpty( text ) : return -1

        index = len( text )

        for line in self.protectLines :

            position = text.find( line )

            if position >= 0 : index = min( index, position )

        return index
        


    def python (

        self,
        target = None,
        pattern = None
        ) :

        """ Converts an ascii file to windows format """

        if utilities.isEmpty( target ) : return False

        isFile = not target.endswith( os.sep )

        isPattern = not utilities.isEmpty( pattern )

        # converts a single file
        
        if isFile :

            result = self.filePythonRefactor( target )
            
            print " python refactor of file (...)", target[ -32 : ], "\n      ", result, "\n"

        # converts list of files ( takes them for source, creates them in target

        elif isPattern :

            fileList = self.files( target, pattern )
            
            if utilities.isEmpty( fileList ) :

                result = False

                return

            result = True

            for targetItem in fileList :

                ok = self.filePythonRefactor( targetItem )

                print " python refactor of files (...)", targetItem[ -32 : ], "\n      ", ok, "\n"

                result = result and ok

        # converts directory: error

        else :

            print "Installer.python - cannot refactor directory "

            result = False

            
        return result


        

    def readConfigurationFile (

        self,
        path = None
        ) :

        """ Reads the configuration file """

        if path is None : path = self.configurationPath

        else : path = utilities.normalizePath( path, normalize = False )

        # because the lines may have different numbers of fields, reads values and splits afterwards

        identifiers, values = tableFile.readAttributeValueList( path, strict = False )

        if len( identifiers ) <= 0 :

            return False

        for index in range( len( identifiers ) ) :

            identifier = identifiers[ index ].lower()

            if identifier == "copyright" : context.copyrightValue = values[ index ]
            
            elif identifier == "email" : context.emailValue = values[ index ]

            elif identifier == "program" : context.programValue = values[ index ]

            elif identifier == "version" : context.versionValue = values[ index ]

            elif identifier == "web" : context.webValue = values[ index ]



        # instantiates the strings used in the sources with the variables that have been loaded

        for index in range( len( self.licenseLines ) ) :

            self.licenseLines[ index ] = utilities.instantiate( self.licenseLines[ index ], default = "_" )


        for index in range( len( self.uselessLines ) ) :

            self.uselessLines[ index ] = utilities.instantiate( self.uselessLines[ index ], default = "_" )


        self.headerLine = utilities.instantiate( self.headerLine, default = "_" )
        
        return True


            


        
            
        
    def readImageFile (

        self,
        path = None
        ) :

        """ Reads the configuration file """

        if path is None : path = self.imagePath

        else : path = utilities.normalizePath( path, normalize = False )

        # because the lines may have different numbers of fields, reads values and splits afterwards

        valueList = tableFile.readValueList( path, strict = False )

        if utilities.isEmpty( valueList ) : return False

        self.table = len( valueList ) * [ None ]

        for index in range( len( valueList ) ) :

            self.table[ index ] = utilities.textToWords( 
                text = valueList[ index ],
                delimiters = [ "\t", "=", "," ],
                number = 3,
                )

        return True




    def removeLines (

        self,
        text = None,
        protected = None
        ) :

        """ Removes useless lines from text """

        if utilities.isEmpty( text ) : return ""

        if utilities.isEmpty( self.uselessLines ) : return text

        # last position of unprotected lines

        if ( ( protected is None ) or ( protected < 0 ) ) : protected = len( text )

        # removes all useless lines

        for line in self.uselessLines :

            position = text.find( line, 0, protected )

            # removes all occurrences of the line
            
            while position >= 0 :

                nextLine = text.find( "\n", position ) + 1
                
                text = text[ : position ] + text [ nextLine : ]

                protected = protected - ( nextLine - position  )

                position = text.find( line, 0, protected )

        return text
        
            


        
            
        
