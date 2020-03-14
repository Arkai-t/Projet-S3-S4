

""" Class for archive (zip) management

 
    """


import zipfile

from api.Utilities import *


class Archiver :
    
    """ Provides methods for zipping directories and files into standard archives
    """

    # list of files in archive directory
    
    archiveList = [ ]

    # additional comment added to archive name
    
    comment = ""

    # date of archive file
    
    date = None

    # error text

    error = None

    # archive name (warning: the full name is archivePath(), e.g, ../archives/<NAME>LocalCompleted20050505.zip
    
    name = None

    # prefix for destination file

    prefix = None
    

    # remote archive directory (anywhere, and uncontrolled by archiver object, may be independent from source file name)
    
    remoteArchiveDirectory = ""


    # selected archive file (externally defined)
    
    selectedVersionName = ""
    
    # source directory
    
    sourceDirectory = ""

    # source file
    
    sourceFile = ""

    # size
    
    sourceSize = 0L

    # source type
    
    sourceType = ""

   
    # possible types of source
    
    typeList = [ "", "file", "directory" ]

    # format of backup : zip file or mere copy

    zipped = None
    
  
    



    def __init__ (
        
        self,
        master = None,
        ):
        
        """ Constructor. Initializes variables with default values

            """

        # source type = none
        
        self.sourceType = ""
        
        # source directory
        
        self.sourceDirectory = ""

        # source file
        
        self.sourceFile = ""

        # name
        
        self.name = ""

        # prefix added to archive name

        self.prefix = ""
        
        # additional comment added to archive name
        
        self.comment = ""

        # date (will be obsolete in one second...)
        
        self.date = None
        
        # content of archive directory
        
        self.archiveList = []

       
        # remote archive directory (anywhere, but not on station and uncontrolled by archiver)
        
        self.remoteArchiveDirectory = ""





    def archiveDirectory (

        self,
        directory = None
        ) :
        
        """ Returns the path of the archive directory corresponding to "directory", parent/_archives/

            directory overrides the archive directory

            """

        # directory is defined: gives the archive directly
        
        if not utilities.isEmpty( directory ) : return utilities.normalizePath( directory, normalize = False )


        # returns parent/_archives for the self.sourcePath()

        else : return utilities.backupsDirectory( self.sourcePath() )
    


    def backup (
        
        self,
        path = None,
        directory = None,
        target = None,
        comment = None,
        prefix = None,
        zipped = None
        ) :

        """ Backups a file or directory

            Directory overrides  the archive directory .

            target overrides the path to the backup

            prefix and comment are placed in the name

            Returns True / False

            """

        if path is None : return False

        self.zipped = utilities.boolean( zipped, default = True )

        # sets source to source directory
        
        if utilities.directoryPresent( path ) :

            result = self.initSourceDirectory(
                path = path,
                directory = directory,
                )

        # ... to source file
        
        elif utilities.filePresent( path ) :

            result = self.initSourceFile(
                path = path,
                directory = directory,
                )

        # or nothing.
        
        else :

            return False
        
        # creates the archive directory
        
        result = utilities.directoryCreate( self.archiveDirectory( directory = directory ) )
        
        if not result : return False

        # saves version in archive subdirectory
        
        result = self.saveVersion(
            directory = directory,
            prefix = prefix,
            comment = comment,
            target = target
            )
        
        if not result : return False

        return True



    def copyDirectory (
        
        self,
        directory = None,
        target = None
        ) :

        """ Copies self.sourceDirectory into the subdirectory self.versionPath()/ (removes extension, adds / )

            If the archive directory existed, it is overwritten.

            target overrides the version name
     
            Returns True if anything OK, False if problem or process cancelled
          
           """

        # by default everything is OK
        
        result = True

        utilities.error = ""
        
        # zip file handler (object)

        path = self.versionPath(
            directory = directory,
            target = target
            )

        path = utilities.pathDirectory( path ) + utilities.pathName( path ) + os.sep

        ok = utilities.directoryCopy( self.sourceDirectory, path )

        return ok


    def copyFile (
        
        self,
        directory = None,
        target = None
        ) :

        """ Copies self.sourceDirectory into the subdirectory self.versionPath()/ (removes extension, adds / )

            If the archive directory existed, it is overwritten.

            target overrides the version name
     
            Returns True if anything OK, False if problem or process cancelled
          
           """

        # by default everything is OK
        
        result = True

        utilities.error = ""

        # path to zip backup, modified to place extension

        path = self.versionPath(
            directory = directory,
            target = target
            )

        path = utilities.pathDirectory( path ) + \
               utilities.pathName( path ) + \
               "." + \
               utilities.pathExtension( self.sourceFile )

        ok = utilities.fileCopy( self.sourceFile, path )

        return ok

    



    def getSourceSize ( self ) :

        """ Returns the size of the source directory/ file


            """

        # default size
        
        size = 0
        
        # source = directory
        
        if self.sourceType == "directory" :
    
            size = directorySize( self.sourceDirectory )

        # source = file
        
        elif self.sourceType == "file" :

            size = utilities.fileSize( self.sourceFile )

            # inconsistency : size 0
            # else ...

        # no source, size 0
        # else : ...

        self.sourceSize = size
        
        return size





    def initSourceDirectory (
        
        self,
        path = "",
        directory = None
        ) :
        
        """ Aliasing for setSourceDirectory

            Initializes the source directory.

            If it is already an archived version, removes all labels 

            Returns True if directory exists, False otherwise.

            """
        
        return self.setSourceDirectory(
            path = path,
            directory = None
            ) 
            





    def initSourceFile (
        
        self,
        path = "",
        directory = None
        ) :
        
        """ Aliasing for setSourceDirectory

            Initializes the source file.

            Initializes the archive directory

            Returns True if file exists, False otherwise.

            """
        
        return self.setSourceFile(
            path = path,
            directory = directory
            ) 
    



            


    def matchText (
        
        self,
        pattern = None,
        text = None
        ) :

        """ Determines whether the text matches the "pattern".
            The pattern is either None (match is True ) or a string
            In this case, the comparison is done in lower case

            """

        if pattern is None : return True

        if text is None : return False

        return pattern.lower() == text.lower()
    
    
    

    def normalizedName (

        self,
        path = None
        ) :

        """ Returns a normalized name for zip file and/or local archive directory

            takes the last name of the path, removes "." and capitalize, e.g. test.txt -> testTxt

            """

        if path is None : return None

        name = utilities.pathLastNameWithExtension( path )

        name = utilities.string( name, format = "safe" )

        return name
        
            



    def parseVersionName (
        
        self,
        fileName = None,
        name = None
        ) :

        """ Parses fileName and returns name, comment (list of 4 elements)
        
            In case of ambiguity, leaves the element of the list as None.

            """

        comment = None
        
        date = None
        
        if fileName is None : return None, None, None

        # removes extension
        
        fileName = utilities.pathLastNameWithoutExtension( fileName )

        # too short for an archive name ( 8 = date 2 = at least  )
        
        if len( fileName ) < 8 : return None, None, None

        # tries date in format YYYYMMDDHHMMSS = 14 chars

        date = ""

        for index in range( len( fileName ) - 1 , 0, -1 ) :

            if ( ( not fileName[ index ] == "_" ) and ( not fileName[ index ].isdigit() ) ) : break

               
        date = fileName[ index + 1 : ]

        date = date.replace( "_", "" )

        fileName = fileName[ : index + 1 ]

        # date is not digital: error (accepts format yyyy mm dd or yyyy mm dd hh mm ss
        
        if len( date ) < 8 :
            
            date = None
            
            return None, None, None
            

        # if name is defined: removes at once the name 
        
        if not name is None :

            # gets the name (it is the prefix)
            
            name, fileName = self.splitPrefix( fileName, name )

            if name is None : return None, None, None
 

        # comment is the remainder
        
        comment = fileName
                   
        return  name, comment, date





    def saveVersion (
        
        self,
        name = None,
        prefix = None,
        comment = None,
        date = None,
        directory = None,
        target = None
        ) :

       
        """ Builds the archive file self.versionPath() (overriden by directory + target )
        
            For a source directory, the archive is a zip

            For a file directory, the archive is a mere copy

            The components of the file name (name, comment) are passed in arguments

            The variables of Archiver are updated accordingly
            
            The previous values are taken for each undefined parameter

            directory overrides  the archive directory

            target overrides the file name to the backup
            
            Returns True if anything OK, False if problem or process cancelled
          
           """

       
        # synchronizes variables and arguments

        # there is no target path, updates all the fields that will compose the version name

##        if utilities.isEmpty( target ) :
        
        if name is None : name = self.name
        
        self.name = name

        if prefix is None : prefix = self.prefix

        else : self.prefix = utilities.string( prefix, format = "underscore", default = "" )
            
        if comment is None : comment = self.comment 
        
        else : self.comment = utilities.string( comment, format = "underscore", default = "" )

        if date is None : date = time.strftime("%Y_%m_%d_%H_%M_%S")
        
        self.date = date

        # for a directory, zips the source into the archive
        
        if self.sourceType == "directory" :

            if bool( self.zipped ) :

                result = self.zipDirectory(
                    directory = directory,
                    target = target
                    )

            else :

                result = self.copyDirectory(
                    directory = directory,
                    target = target
                    )

        # for a file, copies the source into the archive
        
        elif self.sourceType == "file" :

            if bool( self.zipped ) :

                result = self.zipFile(
                    directory = directory,
                    target = target
                    )

            else :

                result = self.copyFile(
                    directory = directory,
                    target = target
                    )
                

        # if problem, removes the archive file
        
        if not result :

            utilities.fileDelete(
                self.versionPath(
                    directory = directory,
                    target = target
                    )
                )
        
        return result


          
    def setSourceDirectory (
        
        self,
        path = "",
        directory = None
        ) :

        
        """ Initializes the source directory.

            If it is already an archived version, removes all labels 

            Returns True if directory exists, False otherwise.

            """

        # directory does not exist
        
        if not utilities.directoryPresent( path ) : return False


        # normalizes the source directory, leaves name intact
        
        self.sourceDirectory = utilities.normalizePath( path, normalize = False )

        # default archive directory is ..(current)/_archives
        
        if directory is None : directory = utilities.pathDirectory( path )


        # checks whether this is already an archive version 
        
        name = self.normalizedName( path )

        myList = self.parseVersionName( name )

        # name, comment, and date are instantiated
        
        if (( not myList [ 0 ] is None ) and
            ( not myList [ 1 ] is None ) and
            ( not myList [ 2 ] is None ) ) :
            
            name = myList[ 0 ]

        # name of archive file = name of directory without version information
        
        self.name = name 

        self.sourceDirectory = path

        # sets the source type *** BEFORE makeArchive, which depends on the source type
        
        self.sourceType = "directory"

        # creates the archive directory (source parent/bbb/ , archive parent/archives/)
        
        utilities.directoryCreate( self.archiveDirectory( directory = directory ) )

##        # determines its content (in self.getArchives)
##        
##        self.updateVersions( directory = directory )

        return True



    def setSourceFile (
        
        self,
        path = "",
        directory = None
        ) :

        
        """ Initializes the source file.
        
            Initializes the archive directory

            Returns True if file exists, False otherwise.

            """

        # file does not exist
        
        if not utilities.filePresent( path ) : return False

        # normalizes the source file, leaves name intact
        
        self.sourceFile = utilities.normalizePath( path, normalize = False )

        # default archive directory is ..(current)/_archives
        
        if directory is None : directory = utilities.pathDirectory( path )


        # parses and remove previous version information from name

        name = self.normalizedName( path )

        myList = self.parseVersionName( name )

        # name, comment, and date are instantiated 
        
        if (( not myList[ 0 ] is None ) and
            ( not myList[ 1 ] is None ) and
            ( not myList[ 2 ] is None ) ) :
            
            name = myList[ 0 ]

        # name of archive file = name of directory without version information
        
        self.name = name

        # source path
        
        self.sourceFile = path

        # sets the source type *** BEFORE makeArchive, which depends on the source type
        
        self.sourceType = "file"

        # creates the archive directory (source parent/bbb/ , archive parent/archives/)
        
        utilities.directoryCreate( self.archiveDirectory( directory = directory ) )

##        # determines its content (in self.getArchives)
##        
##        self.updateVersions( directory = directory )

        return True





    def sourcePath ( self ) :

        """ Returns the full name of the source (path), whether it is a file and/or a directory

        """

        if self.sourceType == "file" :
            
            return self.sourceFile

        elif self.sourceType == "directory" :
            
            return self.sourceDirectory

        else :
            
            return None
        


    def splitPrefix (
        
        self,
        fileName,
        prefix = None
        ) :

        """ Splits the filename into a prefix and a remaining.

            NEW: removes cases for comparison (full normalization)
        
            Returns a pair prefix, remaining
            
            If prefix and/or fileName are empty or None, fileName is None, returns None, None
            If fileName does not begin with prefix, idem

            """

        if prefix is None : return None, None

        if fileName is None : return None, None

        if len( prefix ) <= 0 : return None, None

        if len( fileName ) <= 0 : return None, None
        
        if not fileName.lower().startswith( prefix.lower() ) : return None, fileName

        return prefix, fileName [ len( prefix ) : ]


    def splitPrefixList (
        
        self,
        fileName,
        prefixes = [] ) :

        """ Splits the filename into a prefix and a remaining. A list of prefixes is given and the first found is chosen.
        
            NEW: removes cases for comparison (full normalization)
        
            Returns a pair prefix, remaining
            
            If prefixes or fileName are None, returns None, None
            If fileName does not begin with any prefix, idem

            """

        if prefixes is None : return None, None

        if fileName is None : return None, None
        
        if len( fileName ) <= 0 : return None, None

        emptyIsOk = False
        
        for prefix in prefixes :

            # gives priority to non empty prefixes
            
            if len( prefix ) <= 0 :
                
                emptyIsOk = True
                
                continue
    
            # found one that matches
            
            if fileName.lower().startswith( prefix.lower() ) :
                
               return prefix, fileName [ len( prefix ) : ]

        if emptyIsOk : prefix = ""
        
        else : prefix = None

        return prefix, fileName

 

    def splitSuffix (
        
        self,
        fileName,
        suffix = None ) :

        """ Splits the filename into a remaining and a suffix.
        
            NEW: removes cases for comparison (full normalization)
        
            Returns a pair remaining, suffix
            
            If suffix and/or fileName are empty or None, fileName is None, returns None, None
            If fileName does not end with suffix, idem

            """

        if suffix is None : return None, None

        if fileName is None : return None, None

        if len( suffix ) <= 0 : return None, None

        if len( fileName ) <= 0 : return None, None
        
        if not fileName.lower().endswith( suffix.lower() ) : return fileName, None

        return fileName [ : -len( suffix )], suffix






   
    def unzipDirectory (
        
        self,
        archiveDirectory = None,
        archiveFileName = None,
        targetDirectory = None,
        ) :

        """ Unzips archiveFileName in directory archivesDirectory into targetDirectory.

            By default,

            archiveDirectory, archiveFileName are self.archiveDirectory(), self.versionName()
            targetDirectory = archiveDirectory

            Returns True if anything OK, False if problem or process cancelled
          
           """
        
        utilities.error = ""

        # default values

        if archiveDirectory is None : archiveDirectory = self.archiveDirectory( )

        if archiveFileName is None : archiveFileName = self.versionName()

        if targetDirectory is None : targetDirectory = archiveDirectory

        # archive does not exist
        
        archivePath = utilities.normalizePath( archiveDirectory + os.sep + archiveFileName, normalize = False )
        
        if not utilities.filePresent( archivePath ) : return False

        # by default everything is OK
        
        result = True      

        # zip file handler (object)
        
        archiveFile = zipfile.ZipFile( archivePath, 'r' )

        archivedFiles = archiveFile.namelist()

        # temporary name
        
        temporaryName = "__archiver__"
        
        for item in archivedFiles :

            # warning NOT UTILITIES.JOIN, which removes spaces from name
            
            targetPath = os.path.join( targetDirectory, item )

                
            # unzips in temporary file
            
            try :

                # opens temporary file
                
                targetFile = file( temporaryName, "wb")

                # reads content of file in ZIP archive and writes it at once *** MEMORY ???
                
                targetFile.write( archiveFile.read( item ) )

                targetFile.close()

                # copy temporary file into definitive one
                
                utilities.fileCopy( temporaryName, targetPath )
                
            except Exception, exception :

                utilities.error = str( exception )

                result = False
                
                break 
            
        # saves the zip file only if not cancelled
        
        try :
            
            archiveFile.close()

        except Exception, exception :

            utilities.error = str( exception )
                       
            result = False
    
        # deletes temporary file
        
        utilities.fileDelete(temporaryName)
        
        return result



    def unzipFile (
        
        self,
        archivePath = None,
        targetPath = None
        ) :

        """ Unzips archivePath (zip file) into targetPath

            If archive (zip) contains several files, takes 1st one
    
            Returns True/False
          
            """

        utilities.error = ""
        
        if archivePath is None : return False

        # archive does not exist
        
        if not utilities.filePresent( archivePath ) : return False
        
        if targetPath is None : return False

        
        # by default everything is OK
        
        result = True      

        # zip file handler (object)
        
        archiveFile = zipfile.ZipFile( archivePath ,'r')

        archivedFiles = archiveFile.namelist()
        
        if utilities.isEmpty( archivedFiles ) : return False

        # temporary name
        
        temporaryName = "__archiver__"

        # takes first archived file
        
        item = archivedFiles [ 0 ]

        # unzips in temporary file
        
        try :

            # opens temporary file
            
            targetFile = file( temporaryName, "wb")

            # reads content of file in ZIP archive and writes it at once *** MEMORY ???
            
            targetFile.write( archiveFile.read( item ) )

            targetFile.close()

            # copy temporary file into definitive one (works only is unzip was OK)
            
            utilities.fileCopy( temporaryName, targetPath )
                
        except Exception, exception :

            utilities.error = str( exception )

            result = False
            
        # closes zip file
        
        try :
            
            archiveFile.close()

        except Exception, exception :
            
            result = False
    
        # deletes temporary file
        
        utilities.fileDelete( temporaryName )
        
        return result




##    def updateVersions (
##        
##        self,
##        directory = None
##        ) :
##
##        """ Initializes self.archiveList with the content of archiveDirectory()
##
##            directory overrides the archive directory
##
##            Removes directories, only keeps files
##
##            """
##
##
##        self.archiveList = [ ]
##
##        archivesDirectory = self.archiveDirectory( directory = directory )
##
##        if utilities.isEmpty( archivesDirectory ) : return
##
##        entries = utilities.directoryFiles(
##            archivesDirectory,
##            recursive = False )
##
##        for entry in entries :
##            
##            self.archiveList.append( utilities.pathLastNameWithExtension( entry ) )





    def versionName (
        
        self,
        name = None,
        prefix = None,
        comment = None,
        date = None,
        extension = None
        ) :
        
        """ Initializes a fileName <name><comment><date YYYYMMDD>. <extension>
        
            Example: myFileUserCompleted20050921, myFileUserCompleted20050921a,
            
            If some fields are missing (None) they are leaved in blank in the name

            Returns a string with the complete name
            
          """

        # sets default values of parameters with current values of the archiver

        if prefix is None : prefix = self.prefix

        # takes the words composing "prefix" one by one and capitalizes them (removes spaces)
        
        prefix = utilities.string( prefix, format = "strictUnderscore", default = "" )

        if name is None : name = self.name

        if date is None : date = self.date
        
        if date is None : date = time.strftime("%Y_%m_%d_%H_%M_%S")
            
        if comment is None : comment = self.comment

        # takes the words composing "comment" one by one and capitalizes them (removes spaces)
        
        comment = utilities.string( comment, format = "strictUnderscore", default = "" )

        # default extension is zip
        
        if extension is None : extension = ".zip" 

        fileName = ""

        # prefix

        if not utilities.isEmpty( prefix ) : fileName = prefix + "_"

        # name
        
        if not utilities.isEmpty( name ) : fileName = fileName + name

        # comment must be defined and purely alpha numeric
        
        if not utilities.isEmpty( comment ) : fileName = fileName + "_" + comment

        # gets a string with current date in format YYYYMMDDHHMMSS - WARNING: THIS IS LOCAL TIME. Version gives the ordre
        
        fileName = fileName + "_" + date

        # adds extension
        
        if not extension is None :

            # adds extension only if not empty
            
            if len ( extension ) <= 0 : None

            # does not add dot if present
            
            elif extension[ 0 ] is '.' : fileName = fileName + extension

            else : fileName = fileName + '.' + extension
        
        return fileName


 


    def versionNumber ( self ) :

        """ Returns the numerical value of the version

            This value is the position of the first occurrence of self.version in self.versionList

            Returns -1 if not present in the list

            """

        if self.version is None : return -1

        return utilities.index( self.versionList, self.version )

##*ef 2009 04 18
##        if self.version is None : return -1
##        
##        i = 0
##        
##        while i < len( self.versionList ) :
##            
##            if self.version is self.versionList[ i ] :
##                
##                return i
##
##        return -1
    

    def versionPath (

        self,
        directory = None,
        target = None
        ) :

        """ Returns the full name of the current archive file, i.e., an absolute path """

        if utilities.isEmpty( target ) : target = self.versionName()

        if not target.endswith( ".zip" ) : target = target + ".zip"

        # remove redundant dots that may come from version name

        target = target.replace( "..", "." )

        return self.archiveDirectory( directory = directory ) + target




          
        
    def zipDirectory (
        
        self,
        directory = None,
        target = None
        ) :

        """ Zips self.sourceDirectory into the file self.versionPath().

            If the archive file existed, it is overwritten.

            target overrides the version name
     
            Returns True if anything OK, False if problem or process cancelled
          
           """

        # by default everything is OK
        
        result = True

        utilities.error = ""
        
        # zip file handler (object)

        path = self.versionPath(
            directory = directory,
            target = target
            )

        if utilities.filePresent( path ) : mode = "a"

        else : mode = "w"
        
        archiveFile = zipfile.ZipFile( path, mode, zipfile.ZIP_DEFLATED)

        # keeps current directory
        
        currentDirectory = utilities.currentDirectory()

        # goes to parent of source directory
        
        utilities.gotoDirectory( utilities.pathDirectory( self.sourceDirectory ) )

        # recursive walk through directory
        
        walk = os.walk( utilities.pathName( self.sourceDirectory ) )

        # goes back to previous

        for root, directories, files in walk :

            # error : stops

            if not result : break
           
            for file in files :

                # file name with path relative to sourceDirectory WARNING : NOT utilities.join, which removes spaces...
                
                filePath = os.path.join(root, file )
               
                try :
                    
                    archiveFile.write( filePath )

                except Exception, exception :

                    utilities.error = str( exception )
                    
                    result = False

                    break

        # back to original directory
        
        utilities.gotoDirectory( currentDirectory )
        
        # saves the zip file only if not cancelled
        
        archiveFile.close()
    
        return result





    def zipFile (
        
        self,
        directory = None,
        target = None
        ) :

        """ Zips self.sourceFile into the file self.versionPath().

            If the archive file existed, it is overwritten.

            target overrides the version name
     
            Returns True/ False
          
           """

        # by default everything is OK
        
        result = True

        utilities.error = ""
        
        # zip file handler (object)
        
        path = self.versionPath(
            directory = directory,
            target = target
            )

        if utilities.filePresent( path ) : mode = "a"

        else : mode = "w"
        
        archiveFile = zipfile.ZipFile( path, mode, zipfile.ZIP_DEFLATED)

        # keeps current directory
        
        currentDirectory = utilities.currentDirectory()

        # goes to directory of source file

        directory = utilities.pathDirectory( self.sourceFile )

        fileName = utilities.pathLastNameWithExtension( self.sourceFile )
       
        utilities.gotoDirectory( directory )

        # zips file (with no path information )
        
        try :
            
            archiveFile.write( fileName )

        except Exception, exception :

            utilities.error = str( exception )
                   
            result = False


        # back to original directory
        
        utilities.gotoDirectory( currentDirectory )

        # saves the zip file only if not cancelled
        
        archiveFile.close()
    
        return result

    

# creates a singleton if not already here

if not "archiver" in globals() :  archiver = Archiver()
         
        
