""" Miscellaneous methods for directory and file names processing


    """

import sys

import os

from api.Texts import *



class PathNames ( Texts ) :


    """ Miscellaneous methods for directory and file names processing

        """


    # headers of URLs
    
    httpHeader = "http://"

    webHeader = "www."

    # header of links to files
    
    fileHeader = "file:///"
    
    # extensions recognized as images

    imageExtensionList = [ "bmp", "gif", "jpg", "png", "tif", "tiff" ]

    def fileNameSplit (

        self,
        text = None
        ) :
        
        """ Sentence format: words (1st capitalized) separated by spaces
            Splits words using uppercase letters, digits and separators
            
            """

        if text is None : return None

        index = text.find( "-" )
        
        if index >= 0 : text = text[ index + 1 : ]
                        
        return self.split( text, first = "upper" )


    

    def isAbsolutePath (

        self,
        path = None
        ) :

        """ Returns True iff path is absolute,

            absolute paths start with "/" ( os.sep ) or with their drive

            """

        if self.isEmpty( path ) : return False

        # particular cases: curdir, pardir, user's dir are considered absolute

        osPath = self.osPath( path ).upper()

        # normal cases : /xxx and C:/xxx

        if osPath.startswith( os.sep ) : return True

        if osPath.startswith( self.pathDrive( osPath ) ) : return True

        # special cases : parent current and user directory : ~, ~/, ., ./, .., ../

        if osPath.startswith( os.pardir ) :

            if len( osPath ) == len( os.pardir ) : return True

            elif osPath[ len( os.pardir ) ] == os.sep : return True

            else : return False

        # CURDIR ( . ) AFTER PARDIR ( .. )
        
        if osPath.startswith( os.curdir ) :

            if len( osPath ) == len( os.curdir ) : return True

            elif osPath[ len( os.curdir ) ] == os.sep : return True

            else : return False
            
        if osPath.startswith( "~" ) :

            if len( osPath ) == 1 : return True

            elif osPath[ 1 ] == os.sep : return True

            else : return False
            
        return False



    def isUrl (

        self,
        path = None
        ) :

        """ True iff the path starts with http:// or www. """

        if self.isEmpty( path ) : return False

        if path.startswith( self.httpHeader ) : return True

        if path.startswith( self.webHeader ) : return True

        if path.startswith( self.httpHeader.upper() ) : return True

        if path.startswith( self.webHeader.upper() ) : return True

        return False

    
    


    def matchPattern (

        self,
        path = None,
        namePrefix = None,
        nameSuffix = None,
        extensionPrefix = None,
        extensionSuffix = None
        ) :

        """ Matches a file name with a 4-uple pattern composed of prefixes and suffixes """

        name = self.pathName( path )

        extension = self.pathExtension( path )

        if not self.isEmpty( namePrefix ) :

            if self.isEmpty( name ) : return False

            if not name.startswith( namePrefix ) : return False

        if not self.isEmpty( nameSuffix ) :

            if self.isEmpty( name ) : return False

            if not name.endswith( nameSuffix ) : return False

        if not self.isEmpty( extensionPrefix ) :

            if self.isEmpty( extension ) : return False

            if not extension.startswith( extensionPrefix ) : return False

        if not self.isEmpty( extensionSuffix ) :

            if self.isEmpty( extension ) : return False

            if not extension.endswith( extensionSuffix ) : return False

        return True

    
    

    def normalizeDrive (

        self,
        path = None
        ) :

        """ Normalizes the drive of the path to upper case. Does NOT normalize the path """

        if self.isEmpty( path ) : return path

        # looks for :
        
        index = path.find( ":" )

        if index < 0 : return path

        return path[ : index ].upper() + path[ index : ]
    
        
    def normalizePath (

        self,
        path = None,
        normalize = 1
        ) :

        """ Normalizes a path ( absolute ) """

        if not type( path ) == str : return None

        # this is an URL
        
        if self.isUrl( path ) :

            if ( ( not path.startswith( self.httpHeader ) ) and ( not path.startswith( self.httpHeader.upper() ) ) ) :

                 path = self.httpHeader + path

            return path
            
        # removes the file prefix for browser

        if ( ( path.startswith( self.fileHeader ) ) or ( path.startswith( self.fileHeader.upper() ) ) ) :

            path = path[ len( self.fileHeader ) : ]

        # replaces \\ and // by os.sep

        path = self.osPath( path )
        
        # keeps track of final "\"
        
        isDirectory = ( ( path.endswith( os.sep ) ) or
                        ( path == os.curdir ) or
                        ( path == os.pardir ) or
                        ( path == "" ) )

        # normalizes the path and removes final "\"
        
        path = os.path.abspath( os.path.expanduser( path ) )

        # normalizes the name ( not the directory ) if required

        if normalize == 1 :

            directory, name = os.path.split( path )

            name = self.string( name, format = "path" )

            path = os.path.join( directory, name )
            
            
        # normalizes the name ( not the directory ) if required

        elif normalize == 2 :

            directory, name = os.path.split( path )

            # for directories, normalizes last name

            if isDirectory :

                name = self.string( name, format = "strictIdentifier" )

            # for files, normalizes separately name and extension

            else :

                name, extension = os.path.splitext( name )

                name = self.string( name, format = "strictIdentifier" )

                if not self.isEmpty( extension ) :

                    extension = extension[ 0 ] + self.string( extension[ 1 : ], format = "strictIdentifier" )

                name = name + extension

            path = os.path.join( directory, name )
            

        # adds final "\" again

        if ( ( isDirectory ) and ( not path.endswith( os.sep ) ) ) : path = path + os.sep

        # normalizes the drive to upper case

        path = self.normalizeDrive( path )

        return path

         

    def osPath (

        self,
        path = None
        ) :

        """ Normalizes a path with os.sep (e.g. \\) instead of /, \\, etc.

            Returns the normalized path or None if problem

            """

        if self.isEmpty( path ) : return path

        # replaces / and \ by / (one of the two may be useless) and removes doubles, removes tabs and cr lf
        
        path = path.replace( "\\", os.sep )\
                   .replace( "/", os.sep )\
                   .replace( os.sep + os.sep , os.sep )\
                   .replace( "\t", "")\
                   .replace( "\n", "")

        return path




    def path (

        self,
        path = None,
        normalize = 1
        ) :

        """ Normalizes a path ( absolute ) - alias for normalizePath """

        return self.normalizePath( path, normalize )


    
    def pathDate (

        self,
        path = None,
        format = None
        ) :

        """ Alias for pathNameDate - returns the date that appears at the end of a path's name """

        return self.pathNameDate( path, format = format )




    def pathDescription (

        self,
        path = None,
        format = "title"
        ) :

        """ returns a standard description of the file, i.e., the name without extension

            under the form of a title, in which the dates have been extracted

            """

        text = self.pathNameWithoutDate( path )

        return self.string( text, format = format, default = "" )

         
        
        

    def pathDirectory (
        
        self,
        path = None
	) :

        """ Returns the directory of the path, under the form of absolute path  """

        path = self.normalizePath( path, normalize = False )

        if self.isEmpty( path ) : return ""

        # removes trailing // to find the name
        
        if path.endswith( os.sep ) : path = path[ : -1 ]

        directory, dummy = os.path.split( path )

        if not directory.endswith( os.sep ) : return directory + os.sep

        else : return directory




    def pathDirectoryName (
        
        self,
        path = None
        ) :

        """ Returns the path withtout extension  """

        path = self.normalizePath( path, normalize = False )

        if path is None : return ""

        # removes trailing // to find the name

        if path.endswith( os.sep ) : return path

        path, extension = os.path.splitext( path )

        return path




    def pathDrive (
            
        self,
        path = None
        ) :

        """ Returns the drive of the path """

        path = self.normalizePath( path, normalize = False )

        if self.isEmpty( path ) : return ""

        if sys.platform.startswith( "win" ) : drive, dummy = os.path.splitdrive( path )

        else : drive = os.sep

        return drive




    def pathExtension (
        
        self,
        path = None
        ) :

        """ Returns the extension of the path,  does not include a ".", e.g. "txt" """

        path = self.normalizePath( path, normalize = False )

        if self.isEmpty( path ) : return ""

        dummy, extension = os.path.splitext( path )

        if len( extension ) <= 0 : return ""

        return extension.strip( "." )


    def pathFirstName (
        
        self,
        path = None
        ) :

        """ Returns the first name of a path, (after the drive, if there is one)

            DOES NOT normalize the path, except if it is ""

            """

        if path is None : return ""

        if len( path ) <= 0 : path = self.normalizePath( path, normalize = False )

        drive = self.pathDrive( path )

        if path.startswith( drive ) : first = len( drive )
        
        else : first = 0

        # contains no separator : returns the remainder
        
        first = path.find( os.sep, first )

        if first < 0 : return path
        
        first = first + len( os.sep )

        # no 2nd separator, returns the remainder after the first one
        
        last = path.find( os.sep, first )

        if last < 0 : return path [ first : ]

        return path[ first : last ]



    def pathLastName (

        self,
        path = None
        ) :

        """ Alias for pathLastNameWithoutExtension. Returns the name of the path, with no extension """


        return self.pathLastNameWithoutExtension( path )
    


    def pathLastNameWithExtension (
        
        self,
        path = None
        ) :

        """ Returns the file name or the last name of the path, extension is included  """

        path = self.normalizePath( path, normalize = False )

        if path is None : return ""

        # removes trailing // to find the name
        
        if path.endswith( os.sep ) : path = path[ : -1 ]

        dummy, name = os.path.split( path )

        return name



    def pathLastNameWithoutExtension (
        
        self,
        path = None
        ) :

        """ Returns the file name or the last name of the path, without extension  """

        path = self.normalizePath( path, normalize = False )

        if path is None : return ""

        # removes trailing // to find the name

        isDirectory = path.endswith( os.sep )
        
        if isDirectory : path = path[ : -1 ]

        dummy, name = os.path.split( path )

        if len( name ) <= 0 : return ""

        # directory : this is the last name, no extension
        
        if isDirectory : return name

        # file : splits to find extension
        
        
        name, dummy = os.path.splitext( name )

        return name


    def pathName (

        self,
        path = None
        ) :

        """ Alias for pathLastNameWithoutExtension - name of a path """

        return self.pathLastNameWithoutExtension( path )


    def pathNameExtension (

        self,
        path = None
        ) :

        """ Alias for pathLastNameWithExtension - name of a path with its extension """

        return self.pathLastNameWithExtension( path )



    def pathNameWithoutDate (

        self,
        path = None,
        ) :

        """ Returns the name of the path without extension and final date """

        name = self.pathName( path )

        if self.isEmpty( name ) : return None

        elif self.isEmpty( self.pathDate( name ) ) : return name

        # end of name = date and time
        
        elif name[ -1 ].isdigit() : return name.strip( "0123456789_ -" )

        # there is a version at the end
        
        else : return name[ : -1 ].strip( "0123456789_ -" ) + name[ -1 ].upper()


        
    

        
    def pathNameDate (

        self,
        path = None,
        format = None
        ) :

        """ Returns the date contained at the end of the file/directory name """

        text = self.pathLastName( path ).replace( "_", "" ).replace( "-", "" ).replace( " ", "" )

        if self.isEmpty( text ) : return None

        # ends with date and time 
        
        if ( ( len( text ) >= 14 ) and ( text[ -14 : ].isdigit() ) ) : date = text[ -14 :  ]

        # ends with date and time + version
        
        elif ( ( len( text ) >= 15 ) and ( text[ -15 : -1 ].isdigit() ) ) : date = text[ -15 : -1 ]

        # ends with date no time

        elif ( ( len( text ) >= 8 ) and ( text[ -8 : ].isdigit() ) ) : date = text[ -8 : ] + "000000"
            
        # ends with date and version 

        elif ( ( len( text ) >= 9 ) and ( text[ -9 : -1 ].isdigit() ) ) : date = text[ -9 : -1 ] + "000000"

        # ends with year-month takes 1st of month by default

        elif ( ( len( text ) >= 6 ) and ( text[ -6 : ].isdigit() ) ) : date = text[ -6 : ] + "01000000"
            
        # ends with year, takes january first by default

        elif ( ( len( text ) >= 4 ) and ( text[ -4 : ].isdigit() ) ) : date = text[ -4 : ] + "0101000000"
        
        # nothing like date or time

        else : return None

        # normalizes : year month day hour min sec

        date = date[ : 4 ] + " " + \
               date[ 4 : 6 ] + " " + \
               date[ 6 : 8 ] + " " + \
               date[ 8 : 10 ] + " " + \
               date[ 10 : 12 ] + " " + \
               date[ 12 : 14 ]

        return self.string( date, format = format )
        


         
        

    def pathNameFollowing (

        self,
        path = None,
        prefix = None
        ) :

        """ Returns the first name of a path after the prefix

            DOES NOT normalize the prefix

            Normalizes the path

            """

        path = self.normalizePath( path, normalize = False )
        
        if prefix is None : prefix = ""

        if not path.startswith( prefix ) : return self.pathFirstName( path )

        return self.pathFirstName( path[ len( prefix ) : ] )


    def pathSplit (
        
        self,
        path = None
        ) :

        """ Splits a path into component. Unlike os.path.split, this is a COMPLETE split

            Does NOT normalize the path
            
            Returns a list of words (empty in case of problems)
            
            """

        if self.isEmpty( path ) : return [ ]

        # normalizes separators to \\ or //,  removes last one, splits *EF 2009 04 18
        
        return self.osPath( path ).rstrip( os.sep ).split( os.sep )

##        words = path.split( os.sep )
##
##        path = self.osPath( path )
##        
##        # removes the last os.sep, it screws the algorithm
##
##        if path[ -1 ] == os.sep : path = path[ : -1 ]
##        
##        # constructs a list of elements backwards
##        
##        words = [ ]
##
##        while True :
##
##            path, word = os.path.split( path )
##
##            if len( word ) <= 0 :
##
##                if len( path ) > 0 : words.append( path )
##
##                break
##
##            words.append( word )
##
##        words.reverse()
##
##        return words

        

    def pathTitle (

        self,
        path = None,
        format = "title",
        default = ""
        ) :

        """ Returns a title composed from the end of the file name, after  last "-"

            For instance /x/y/screenz-aaa-biBoBo.txt --> Bi Bo Bi

            """

        name = self.pathLastNameWithoutExtension( path )

        minus = name.rfind( "-" )

        if ( ( minus >= 0 ) and ( minus + 1 < len( name ) ) ) : name = name[ minus + 1 : ]

        return self.string( name, format = format, default = default )


    def removePrefix (

        self,
        path = None,
        prefix = None
        ) :

        """ Remove one prefix from the name of the path

            prefix may be a string or a list

            """

        if self.isEmpty( path ) : return None

        if self.isEmpty( prefix ) : return path

        directory = self.pathDirectory( path )

        name = self.pathLastNameWithExtension( path )

        if type( prefix ) == str :

            if name.startswith( prefix ) : name = name[ len( prefix ) : ]

        elif type( prefix ) == list :

            for item in prefix :

                if name.startswith( item ) :

                    name = name[ len( item ) : ]

                    break

        return name
        


    def parseShared (

        self,
        path = None
        ) :

        """ parses a standard file name like if it were normalized for bookcase

            returns category author description year key """

        

        name = self.pathName( path )

        if self.isEmpty( name ) : return None, None, None, None, None

        words = self.textToWords( self.string( name, format = "split" ) )

        if self.isEmpty( words ): return None, None, None, None, None

        
        size = len( words )

        category = ""
        
        author = ""

        description = ""

        initials = ""

        year = ""

        # type is first

        iParsed = 0
        
        if self.isType( words[ 0 ] ) :

            category = words[ 0 ]

            iParsed = 1


        # checks for a year

        value = None

        for iDate in range( size - 1 , iParsed, -1 ) :

            if not len( words[ iDate ] ) == 4 : continue

            value = self.integer( words[ iDate ] )

            if not value is None : break


        # no year

        if value is None : iDate = size

        else : year = words[ iDate ]

        # supposed to have initials after the year
        
        if iDate + 2 == size : initials = words[ -1 ]

        # no room for author or description

        if iDate == iParsed : return category, author, description, year, initials

        # author = just after type, but only if there is a date or the author is "unknown"

        if words[ iParsed ] == "unknown" :

            author = words[ iParsed ]

            iParsed = iParsed + 1

        elif iDate < size :

            author = words[ iParsed ]

            iParsed = iParsed + 1

        description = self.wordsToText( words[ iParsed : iDate ] )

        return category, author, description, year, initials



        
    def pathShared (

        self,
        category = None,
        author = None,
        description = None,
        title = None,
        year = None,
        extension = None,
        directory = None
        ) :

        """ returns a normalized path directory/category_year/category_author_description_year_initials.extension

            initials are the initials of titles, they serve as collision-detector key

            """

        directory = self.string( directory, default = "" )

        if not self.isEmpty( directory ) : directory = self.slashPath( directory + os.sep )

        extension = self.string( extension, default = "" )

        category = self.string( category, format = "strictunderscore", default = "" )
        
        author = self.string( author, format = "strict", default = "" ).replace( "_", "-" )

        author = self.textToWords( author )

        if not self.isEmpty( author ) : author = author[ 0 ]

        else : author = ""

        author = self.string( author, format = "strictunderscore", default = "" ).lower()

        description = self.string( description, format = "strictunderscore", default = "" ).lower()

        year = self.string( year, format = "strictunderscore", default = "" )

        initials = self.string( title, format = "initials", default = "" ).lower()

        # name and directory
        
        name = category + "_" + author + "_" + "_" + description + "_" + year + "_" + initials

        name = name.replace( "__", "_" )

        directory = directory + category + os.sep + year + os.sep

        # the path is in direct slash convention

        path = self.slashPath( directory + name + extension ).replace( "//", "/" )

        return path


        
        
        
    def slashPath (

        self,
        path = None
        ) :
        
        """ Normalizes a path with / instead of os.sep

            Returns the normalized path or None if problem

            """

        if self.isEmpty( path ) : return path

        # removes spaces and tabs
        
        path = path.replace( " ", "" ).replace( "\t", "" )
        
        # replaces / and \ by / (one of the two may be useless)
        
        path = path.replace( "\\", "/" ).replace( os.sep, "/" ).replace( "//", "/" )

        return path


        
        
    def splitPattern (

        self,
        pattern = None
        ) :

        """ splits a pattern of file name into prefixes and suffixes.

            Returns a 4 uple namePrefix, nameSuffix, extensionPrefix, extensionPrefix

            missing values are None

            """


        pattern = self.string( pattern )

        if self.isEmpty( pattern ) : return None, None, None, None

        name = self.pathName( pattern )

        namePrefix = None

        nameSuffix = None

        if not self.isEmpty( name ) :

            if name.startswith( "*" ) :

                nameSuffix = name[ 1 : ]

            elif name.endswith( "*" ) :

                namePrefix = name[ : -1 ]

            elif "*" in name :

                namePrefix, nameSuffix = name.split( "*" )

            else :

                namePrefix = name

                nameSuffix = name
              
        extension = self.pathExtension( pattern )

        extensionPrefix = None

        extensionSuffix = None

        if not self.isEmpty( extension ) :

            if extension.startswith( "*" ) :

                extensionSuffix = extension[ 1 : ]

            elif extension.endswith( "*" ) :

                extensionPrefix = extension[ : -1 ]

            elif "*" in extension :

                extensionPrefix, extensionSuffix = extension.split( "*" )

            else :

                extensionPrefix = extension

                extensionSuffix = extension

        return namePrefix, nameSuffix, extensionPrefix, extensionSuffix                    

                
                

            
        
