

""" Miscellaneous methods on files and directories """

import sys

import os

import glob

import time

import dircache

import stat

from api.Clock import *

from api.PathNames import *

from api.Texts import *



class Files ( PathNames, Texts ) :

    """ Miscellaneous methods on files and directories """


##    # bookcase drive
##
##    bookcase = None



    # parentheses and ! in html when coded in unicode

    htmlOpen = "%28"

    htmlClose = "%29"

    htmlQuote = "%21"

               
    # reserved prefixes

    reservedPrefixList = None
    
##    # directory of items to classify
##
##    toClassify = None


    
    def chdir (

        self,
        path = None
        ) :

        """ Aliasing for gotoDirectory. Changes dir.

            Returns True if possible False otherwise

            Captures exception

            """

        return self.gotoDirectory( self.string( path ) )
        

    def closestDirectory (

        self,
        path = None
        ) :

        """ returns the largest directory of path that exists. Used to find a directory in command lines """
        
        items = self.pathSplit( path )

        if self.isEmpty( items ) : return ""

        directory = ""

        for item in items :
            
            if not item.endswith( os.sep ) : item = item + os.sep

            subdirectory = directory + item

            if not self.directoryPresent( subdirectory ) : break

            directory = subdirectory

        return directory      
    
        
    def currentDirectory ( self ) :
        
        """ Returns current directory or None if problem.

            Captures exception

            """

        # goes to source directory
        
        try :
            
            path = self.normalizeDrive( os.getcwd() )

            # normalizes drive to upper case

            
            
            return path + os.sep    # not put by system

        except Exception, exception :

            self.error = str( exception )
            
            return None




    def directoryClear (
        
        self,
        path = None,
        ) :
            
            
        """ Deletes recursively the special files from the content of directory "path" ( start with . or ~ )
        
            leaves the empty directory in place.

            Returns True if OK, False otherwise
            
            Throws no exception (return False instead)
            
            """

        ok = self.directoryPurge( path, mode = "other" )

        return ok
        


    def directoryContent (
        
        self,
        path = None,
        annotate = None
        ) :
        
        """ Returns the content of the directory, i.e., a list of entry names

            Removes the current directory and parent directory

            Annotate is a flag that says whether the directories have a trailing "/"
            
            Returns [] if path is not a directory
        
            """

        if not self.directoryPresent( path ) : return [ ]

        path = self.normalizePath( path, normalize = False )
       
        try :
            
            entries = dircache.listdir( path )
            
        except Exception, exception :
            
            self.error = str( exception )
            
            return []

        # filters the entries to remove the current directory and parent directory
        
        content = [ ]
        
        for entry in entries :
            
            if entry == os.curdir : continue
            
            if entry == os.pardir : continue

            content.append( entry )

        # annotate ?

        if bool( annotate ) :

            dircache.annotate( path, content )

            # normalizes, annotate appends a "/" instead of os.sep
            
            for index in range( len( content ) ) :

                if content[ index ][ -1 ] == "/" : content[ index ] = content[ index ][ : -1 ] + os.sep
          
        return content


            
    def directoryCopy (
        
        self,
        source = None,
        target = None,
        overwrite = True,
        instantiate = None,
        filter = None,
        link = None,
        empty = False,
        ) :
            
        """ Copies a directory into another.

            overwrite indicates whether existing files are overwritten or not.

            instantiate indicates that the files will be instantiated when it is possible, e.g., .txt, .htm, .html, etc.

            link is a flag that indicates that the source files with extension .to will be replaced by the files they point at

            empty tells whether empty items should be copied

            Returns True if OK False otherwise

            Throws no exception (return False instead)
            
            """


        source = self.normalizePath( source, normalize = False )
        
        target = self.normalizePath( target, normalize = False )

        if ( ( source is None ) or ( target is None ) ) : return False

        # source is not a directory
        
        if not self.directoryPresent( source ) :

            self.error = "directoryCopy - source not found " + source

            return False

        # creates target now, so that it is done even when source is empty

        self.directoryCreate( target )

        # same directory

        if source == target : return True
        

        # keeps current directory
        
        currentDirectory = self.currentDirectory()
        
        if currentDirectory is None :

            self.error = "directoryCopy - current directory not found " 

            return False

        # goes to source directory
        
        if not self.gotoDirectory( source ) :

            self.error = "directoryCopy - cannot go to source directory " + source

            return False

        # recursive walk through directory
        
        walk = os.walk( os.curdir )

        # by default, anything OK
        
        result = True

        empty = True

        for root, directories, files in walk :


            # result is false ? break
            
            if not result : break

            # if copies empty subdirectories, one pass to create subdirectories

            if bool( empty ) :

                for item in directories :

                    # target path with same file name: may be modified later ( source name contains instances )
                 
                    self.directoryCreate( target + os.sep + root + os.sep + item )

                

            # copies content

            for item in files :

                # result is false ? break
                
                if not result : break

                name = self.pathName( item )

                extension = self.pathExtension( item )
                   
                # file name with path relative to sourceDirectory 
                
                sourceFilePath = self.normalizePath( root + os.sep + item, normalize = False )

                # name is special ( starts with . or ~, e.g., subversion directories, temporary files )

                if ( ( os.sep + "." in sourceFilePath ) or ( os.sep + "~" in sourceFilePath ) ) : continue                    

                # target path with same file name: may be modified later ( source name contains instances )
             
                targetFilePath = self.normalizePath( target + os.sep + root + os.sep + item, normalize = False )

                # the source file is a link ( *.to ) : will copy its content, but must change the target name
                # e.g., source = toto.txt.to -> target = toto.txt
                
                if ( ( bool( link ) ) and ( extension == "to" ) ) :

                    targetFilePath = self.normalizePath( target + os.sep + root + os.sep + name, normalize = False )

    
                # if instantiate flag is True, instantiates the target path

                if bool( instantiate ) :

                    targetFilePath = self.instantiate( targetFilePath, default = "_", format = "strictIdentifier" )
                    
                # if not overwrite and file present, does nothing
                
                if ( ( not overwrite ) and ( self.pathPresent( targetFilePath ) ) ) : continue
                
                # copies the file
                
                result = self.fileCopy(
                    sourceFilePath,
                    targetFilePath,
                    instantiate = instantiate,
                    filter = filter,
                    link = link,
                    empty = empty
                    )
                
                if not result : break

            

        # back to original directory
        
        self.gotoDirectory( currentDirectory )

        return result




    def directoryCreate (
        
        self,
        path = None
        ) :
        
        """ Aliasing for makeDirectory. Creates a directory (and intermediary subdirectories)

            Returns True if directory exists after the execution, False otherwise
            
            """

        return self.makeDirectory( path )




    def directoryDateModified (
        
        self,
        path = None,
        recursive = 2
        ) :

        """ Returns the date and time of last modification of the directory as a string """

        time = self.directoryTimeModified(
            path,
            recursive = recursive
            )

        return clock.date(
            time = time,
            format = clock.fileDateFormat
            )




    def directoryDayModified (
        
        self,
        path = None,
        recursive = 2
        ) :

        """ Returns the date of last modification of the directory as a string """

        time = self.directoryTimeModified(
            path,
            recursive = recursive
            )

        return clock.date(
            time = time,
            format = clock.fileDayFormat
            )



    def directoryDelete (
        
        self,
        path = None,
        ) :
            
            
        """ Deletes recursively the content of directory "path".
        
            removes the empty directory in place.

            Returns True if OK, False otherwise
            
            Throws no exception (return False instead)
            
            """

        ok = self.directoryPurge( path, mode = "all" )

        return ok
        






    def directoryDeleteContent (
        
        self,
        path = None,
        ) :
            

        """ Deletes the content of the directory, but not the directory itself (Useful to preserve access rights)

            Returns True if everything was deleted, false otherwise

            The path is mandatory.
            
            Returns True if OK, False otherwise
            
            Throws no exception (return False instead)
      

            """

        path = self.normalizePath( path, normalize = False )
        
        if path is None : return False
        
        entries = self.directoryContent( path, annotate = True )

        if entries is None : return False

        for entry in entries :

            # does nothing for current and parent directories
            # normally, they are not in directoryContent() but...

            if entry == os.curdir : continue
            
            if entry == os.pardir : continue

            entryPath = self.normalizePath( path + os.sep + entry, normalize = False )

            # directory

            if entry.endswith( os.sep ) : self.directoryDelete( entryPath )
                
            else : self.fileDelete( entryPath )
                
                

        # here, anything OK
        
        return True
        




    def directoryFiles (
        
        self,
        path = None,
        recursive = None,
        reserved = None
        ) :

        """ List of files contained in directory and subdirectories (recursive )

            returns list of full paths
            
            """

        return self.directoryPaths(
            path,
            mode = "files",
            recursive = recursive,
            reserved = reserved
            )





    def directoryGet ( self ) :
        
        """ Aliasing for currentDirectory. Returns current directory or None if problem.

            Captures exception

            """

        return self.currentDirectory()


    def directoryPairs (

        self,
        path = None,
        browse = None,
        pattern = None,
        drives = None,
        selfReference = None,
        sort = True
        ) :

        """ Returns a list of pairs name-path for the entries of the directory.

            The list is decorated according to "browse", i.e. a path that is the tree in which browsing is allowed
            There are : 1 blank line, a line "this", a line "parent", and a set of allowed drives

            Pattern is a pattern with wildcard * to filter the content of the directory, or a list of patterns
            separated by spaces, commas, etc.

            Drives says whether the list of drives is added to the list (True) or not ( False) or
            if  drives is a string, it is the drive to add ( e.g., "C:" )
            if  drives is a list, it is a list of drives to add  ( e.g. [ C:, D: ] )

            if Sort, the list of pairs is sorted by names

            Returns an empty list in case of error
            
            """

        # content of directory

        items = self.directoryPaths(
            path,
            recursive = False,
            reserved = 1
            )

        if type( pattern ) == str : patternList = self.textToWords( pattern )

        elif type( pattern ) == list : patternList = pattern

        else : patternList = [ ]
        

        namePrefixList = [ ]
        
        nameSuffixList = [ ]
        
        extensionPrefixList = [ ]
        
        extensionSuffixList = [ ]

        sizePattern = len( patternList )

        for pattern in patternList :

            namePrefix, nameSuffix, extensionPrefix, extensionSuffix = self.splitPattern( pattern )

            namePrefixList.append( namePrefix )
        
            nameSuffixList.append( nameSuffix )
        
            extensionPrefixList.append( extensionPrefix )
        
            extensionSuffixList.append( extensionSuffix )
        
        pairs = [ ]

        for item in items :

            name = self.pathLastNameWithExtension( item )

            if item.endswith( os.sep ) : name = name + os.sep

            # no pattern list

            if sizePattern == 0 :

                pairs.append( [ name, item ] )

                continue
                

            # checks patterns 1 by 1

            for index in range( sizePattern ) :

                if self.matchPattern(
                    name,
                    namePrefixList[ index ],
                    nameSuffixList[ index ],
                    extensionPrefixList[ index ],
                    extensionSuffixList[ index ]
                    ) :

                    pairs.append( [ name, item ] )

                    break

        # sorts pairs text - path

        if bool( sort ) : pairs.sort()


        # directory that the widget browses. If the current directory is below, adds a line to <parent>

        if self.isEmpty( browse ) : return pairs

        browse = self.instantiate( browse, default = "_" )

        browse = self.normalizePath( browse + os.sep, normalize = False )

        # inserts the allowed drives (place list in reverse order because insertions are always in position 0)

        if drives is None : driveList = self.getVariable( "drives" )

        elif self.boolean( drives, default = "None" ) == True : driveList = self.getVariable( "drives" )

        elif self.boolean( drives, default = "None" ) == False : driveList = [ ]

        # here, drives can be a list and/or a text
        
        if type( drives ) == list : driveList = list( drives )

        elif type( drives ) == str : driveList = self.textToWords( drives )

        else : driveList = [ ]

        # reverse order *EF 2009 04 18 was .sort(), .reverse()
        
        driveList.sort( reverse = True )

        for drive in driveList :

            pairs.insert( 0, [ " <" + drive + ">", drive + os.sep ] )

        # insert a line for parent directory iff. not in the outermost level of the browse tree

        if ( ( path.startswith( browse ) ) and
             ( not path == browse ) and
             ( not self.context is None )
             ) :

            pairs.insert(
                0,
                [ "  <" + self.getMessage( "parent" ) + " " + self.getMessage( "directory" ) + ">",
                  self.pathDirectory( path ) ]
                )

                

        # inserts a line for this directory iff. not in the root of the drive and self reference


        if ( ( self.boolean( selfReference, default = True ) ) and
             ( not self.isEmpty( self.pathName( path ) ) )  and
             ( not self.context is None )
             ) :

            pairs.insert(
                0,
                [ "  <" + self.getMessage( "this" ) + " " + self.getMessage( "directory" ) + ">",
                  path ] )

                

##        # systematically adds this directory and a blank line
##
##        pairs.insert( 0, [ "", "" ] )

        return pairs

        
        
        

    def directoryPaths (
        
        self,
        path = None,
        mode = None,
        recursive = 1,
        reserved = 2,
        level = 0
        ) :

        """ List of files contained in directory and subdirectories (recursive )

            Recursive is
            0( False),
            1 (True default)
            2, 3 ... . N means that items up to N-1 are accepted, root = 1 etc.

            Reserved is
            2 refuses any path that have a reserved subdir,
            1 refuses paths with last name reserved),
            0 accepts reserved.
            
            returns list of full paths
            
            """

        # the level of recursivity is too high

        if ( ( recursive > 1 ) and ( level + 1 > recursive ) ) : return [ ]
        
        mode = self.string(
            mode,
            texts = [ "all", "files", "directories" ],
            default = "all"
            )

        path = self.normalizePath( path, normalize = False )
        
        items = self.directoryContent( path, annotate = True )

##        dircache.annotate( path, items )
        
        if len( items ) <= 0 : return [ ]

        paths = [ ]

        for item in items :

            # current directory and parent directory
            
            if item == os.pardir : continue
            
            if item == os.curdir : continue

            itemPath = self.normalizePath( path + os.sep + item, normalize = False )

            # checks reserved items directly ( detects presence of reserved characters, "_", "." etc. )

            if self.isReserved( itemPath, level = reserved ) : continue
           
            # sub directory, not recursive

            if itemPath.endswith( os.sep ) :

                if ( ( mode == "directories" ) or ( mode == "all" ) ) : paths.append( itemPath )

                # recursive (whatever the mode )
            
                if recursive : paths.extend(
                    self.directoryPaths(
                        path = itemPath,
                        mode = mode,
                        recursive = recursive,
                        reserved = reserved,
                        level = level + 1
                        ) )


            # file : appends in mode "all" or "files"
            
            else :

                if ( ( mode == "files" ) or ( mode == "all" ) ) : paths.append( itemPath )

        return paths


            
    def directoryPresent (

        self,
        path = None
        ) :

        """ Checks whether the directory "path" is here

            Returns True if present False if absent or any other problem

            """
        
        path = self.normalizePath( path, normalize = False )
        
        if path is None : return False
        
        else : return os.path.isdir( path ) 



    def directoryPurge (
        
        self,
        path = None,
        mode = None
        ) :
            
            
        """ Deletes recursively the content of directory "path", either all files, normal files of special files ". and "~
        
            leaves the empty directory in place.

            mode is "all", "normal" or "other" (anything else, in fact)
            
            Returns True if OK, False otherwise
            
            Throws no exception (return False instead)
            
            """

        mode = self.string(
            mode,
            texts = [ "all", "normal", "other" ],
            default = "all"
            )
       
        # not a directory

        if not self.directoryPresent( path ) : return False

        # normalizes path
        
        path = self.normalizePath( path, normalize = False )

        # checks that it is not a complete volume. In this case, there is no last name
        
        name = self.pathLastNameWithExtension( path )
        
        if self.pathDrive( path ) == path.rstrip( os.sep ) : return False

        # loop on directory content
        
        entries = self.directoryContent( path, annotate = True )

        result = True

        for entry in entries :

            item = path + os.sep + entry

            # decides whether to delete or not

            other = ( os.sep + "." in item ) or ( os.sep + "~" in item )

            delete = ( mode == "all" ) or ( ( mode == "other" ) == other )


            # file

            if not item.endswith( os.sep ) :

                if not delete : continue

                ok = self.fileDelete( item )

            # directory
            
            else :

                # must delete: deletes completely

                if delete : ok = self.directoryPurge( item, mode = "all" )

                # special directory, must only delete normal : does nothing

                elif other : continue
                
                # normal directory, must only delete others, deletes selectively

                else : ok = self.directoryPurge( item, mode = mode )
            
            if not ok : result = False

        # deletes directory itself only if there is no error and must delete all
        
        if not mode == "all" : return result

        if not result : return False

        # gets delete rights
        
        try :
            
            os.chmod( path, stat.S_IRWXU )

        except Exception, exception :

            None
        
        try :
            
            os.rmdir( path )
            
        except Exception, exception :

            self.error = str( exception )
                        
            return False

        return True

    


    def directoryRename (
        
        self,
        source = None,
        target = None
        ) :
            
        """ Alias for pathRename. Renames the source directory into the target directory.
            
            WARNING: USE FULL PATHS, OTHERWISE IT IS A COPY IN CURRENT DIRECTORY
            
            Returns True is OK, False otherwise

            Throws no exception (return False instead)
            
                
            """

        result = self.pathRename(
            source = source,
            target = target )

        return result



    def directorySize (
        
        self,
        path = os.curdir,
        ) :
            
        """ Determines recursively the size of a directory on local disk
            Returns the sum of the sizes of all files contained in the directory and its subdirectories

            In case of cancellation, or if directory does not exist, the function returns 0L

            Stops when maximal file size ( context.... is reached )
            
            Throws no exception (return False instead)
            
            """

        # not a directory
        
        if not self.directoryPresent( path ) : return 0L

        # normalizes path
        
        path = self.normalizePath( path, normalize = False )
            
        # keeps current directory
        
        currentDirectory = self.directoryGet()
        
        if currentDirectory is None : return 0L

        # goes to source directory
        
        if not self.gotoDirectory(path) : return 0L

        # recursive walk through directory
        
        walk = os.walk( os.curdir )

        size = 0.

        result = True

        maxFileSizeKb = self.integer( self.maxFileSizeKb, default = 32000 )
            
        
        for root, directories, files in walk :

            # too big

            if size >= float( maxFileSizeKb ) * 1024. : break

            if not result :  break 

            for file in files :

                # file name with path relative to sourceDirectory
                
                filePath = os.path.join( root, file )

                try :
                    
                    size = size + os.path.getsize( filePath )
                    
                except Exception, exception :

                    self.error = str( exception )

                    result = False
                    
                    break ;

        # back to original directory
        
        self.gotoDirectory( currentDirectory )

        # error returns 0
        
        if not result : size = 0.
        
        return size
            

    def directoryTimeModified (
        
        self,
        path = None,
        recursive = 2
        ) :

        """ Returns the date and time of last modification of the directory or any of its items as a long integer

            Remark : Windows does not update correctly the modification time: e.g.
              md aa             time is OK
              md aa\\bb         time of aa and bb are OK
              copy xxxx aa\\bb  time of bb is OK, time of aa is not updated

            If recursive is
            0, just takes the date of modification of the directory stored by the system
            1, takes the most recent of this date and the date of modification of the content
            2, goes recursively into the directory and finds the most recent date
            
              
            """

        if not self.directoryPresent( path ) : return 0

        lastModified = 0

        if bool( recursive ) : items = self.directoryContent( path, annotate = True )

        else : items = [ ]

##        dircache.annotate( path, items )

        for item in items :

            # current directory and parent directory
            
            if item == os.pardir : continue
            
            if item == os.curdir : continue

            # does not consider protected subdirectories
            
            if item.startswith( "_" ) : continue

            if item.startswith( "." ) : continue

            itemPath = self.normalizePath( path + os.sep + item, normalize = False )

            # file

            if not itemPath.endswith( os.sep ) : itemModifiedTime = self.fileTimeModified( itemPath )
            
            # goes into subdirectories, window is too dumb in propagating date modified

            elif recursive <= 1 : itemModifiedTime = self.directoryTimeModified( itemPath, recursive = 0 )

            # goes into subdirectories, window is too dumb in propagating date modified

            else : itemModifiedTime = self.directoryTimeModified( itemPath, recursive = recursive )

            lastModified = max( lastModified, itemModifiedTime )

        # if directory is empty, gets its own time of creation or modification

        thisModified = self.integer( os.stat( path ).st_mtime, default = 0 )
        
        return max( lastModified, thisModified )



##    def driveList (
##
##        self,
##        annotate = False
##        ) :
##
##        """ List of valid drives """
##
##
##        try :
##
##            items = self.driveList
##
##            networkDrive = self.pathDrive( self.network )
##
##        except Exception, exception :
##
##            items = None
##
##            networkDrive = None
##
##        if items is None :
##
##            items = [ "A:", "B:", "C:", "D:", "E:", "F:", "G:", "H:", "I:", "J:",
##                       "K:", "L:", "M:", "N:", "O:", "P:", "Q:", "R:", "S:", "T:",
##                       "U:", "V:", "W:", "X:", "Y:", "Z:"
##                       ]
##
##        if network is None : networkDrive = None
##
##        currentDrive = self.pathDrive( os.curdir )
##        
##        drives = [ ]
##
##        for drive in items :
##
##            if not self.pathPresent( drive ) : continue
##
##            drive = self.pathDrive( drive )
##
##            text = drive
##
##            if bool( annotate ) : 
##
##                if drive == currentDrive : text = text + " current"
##
##                elif drive == networkDrive : text = text + " network"
##
##            if not text in drives : drives.append( text )
##
##        return drives



    
        
    def fileClose (

        self,
        fileHandler = None
        ) :
        

        """ Version of file.close() that throws no exception
        
            """

        if fileHandler is None : return True
        
        try :

            fileHandler.close()

        except Exception, exception :

            self.error = str( exception )
                        
            return False

        return True






    def fileCopy (
        
        self,
        source = None,
        target = None,
        first = None,
        last = None,
        overwrite = True,
        instantiate = False,
        filter = False,
        link = False,
        empty = False,

        ) :
            
        """ Copies the source file into the target file.

            first and last are optional, they represent the first index to copy, and the last index + 1, respectively.
            
            Returns True is OK, False otherwise

            overwrite indicates whether the target file is overwritten or not

            instantiate indicates that the file will be instantiated when it is possible, e.g., .txt, .htm, .html, etc.

            link is a flag that indicates that the source file with extension .to will be replaced by the file it points at

            empty tells whether empty items should be copied
        


            Throws no exception (return False instead)
            
                
            """

        source = self.normalizePath( source, normalize = False )
        
        target = self.normalizePath( target, normalize = False  )

        if ( ( source is None ) or ( target is None ) ) : return False

        if not self.filePresent( source ) :

            self.error = "fileCopy - source not found " + source

            return False

        # same file
        
        if source == target : return True

        # defines source & target handlers, useful if exception occurs before the open (= file) instructions.
        
        sourceFile = None
        
        targetFile = None
            
        # by default result OK
        
        result = True

        # target file exists and does not overwrite
        
        if ( ( not overwrite ) and ( self.pathPresent( target ) ) ) : return True

        # makes target directory
            
        targetDirectory = self.pathDirectory( target  )

        name = self.pathLastNameWithExtension( target  )

        # the name starts with "!" : don't instantiate

        if name.startswith( "!" ) :

            instantiate = False

            name = name[ 1 : ]

            target = self.normalizePath( targetDirectory + os.sep + name, normalize = False )
            
            
        self.directoryCreate( targetDirectory )

        extension = self.pathExtension( source )

        # the file is a link ( *.to ), and must be replaced by the file or directory pointed at

        if ( ( bool( link ) ) and ( extension in self.linkExtensionList ) ) :

            link = self.fileLinkedPath( source )

            if not self.pathPresent( link ) :

                self.error = "fileCopy - linked source not found " + source

                return False

            source = link

            extension = self.pathExtension( source )


        if not extension in self.instantiateExtensionList :

            filter = False

            instantiate = False

        # the 'file' is  a directory

        isDirectory = source.endswith( os.sep )

        if isDirectory :

            result = self.directoryCopy(
                source = source,
                target = target,
                overwrite = overwrite,
                instantiate = instantiate,
                link = link,
                empty = empty
                )

        elif ( ( not filter ) and ( not instantiate ) ) :

            result = self.fileDuplicate(
                source = source,
                target = target,
                first = first,
                last = last
                )

        else :

            if ( ( filter ) and ( instantiate ) ) : text = self.instantiate( self.fileRead( source ).replace( "\r", "" ) )

            elif filter : text = self.fileRead( source ).replace( "\r", "" )

            else : text = self.instantiate( self.fileRead( source ) )   # instantiate and not filter )

            # html : instantiates also patterns with "(" ")" "!" coded in unicode (this occurs in links )
            
            if ( ( instantiate ) and ( "htm" in extension ) ) :

                text = self.instantiate(
                    text,
                    openCode = self.htmlOpen,
                    closeCode = self.htmlClose,
                    quoteCode = self.htmlQuote,
                    slashCode = "/"
                    )

            result = self.fileWrite( target, text )

        if not result : return False

        # sets permissions

        if isDirectory : mode = stat.S_IREAD + stat.S_IWRITE 

        elif extension in self.executeExtensionList : mode = stat.S_IREAD + stat.S_IWRITE + stat.S_IEXEC

        else : mode = stat.S_IREAD + stat.S_IWRITE

        try :
            
            os.chmod( target, mode )

            result = True

        except Exception, exception :

            result = False

        return result

    
        

               
    def fileCreate (

        self,
        path = None
        ) :
        
        """ Creates an empty file (creates its directory if needed)

            Returns True if file exists after the execution, False otherwise

            """

        path = self.normalizePath( path, normalize = False )

        if path is None : return False

        directory = self.pathDirectory( path )

        name = self.pathLastNameWithExtension( path )

        result = self.directoryCreate( directory )
        
        if not result : return False

        fileHandler = self.fileOpen( path, "w" )
        
        if fileHandler is None : return False

        result = self.fileClose( fileHandler )
        
        if not result : return False

        return True



    def fileDateModified (
        
        self,
        path = None
        ) :

        """ Returns the date and time of last modification of the file as a string """

        return clock.date(
            time = self.fileTimeModified( path ),
            format = clock.fileDateFormat
            )


    def fileDayModified (
        
        self,
        path = None
        ) :

        """ Returns the date of last modification of the file as a string """

        return clock.date(
            time = self.fileTimeModified( path ),
            format = clock.fileDayFormat
            )


     


        
    def fileDelete (
        
        self,
        path = None
        ) :
            
        """ Deletes the file "path"

            Returns True if file does not exist after execution, False otherwise

            Throws no exception (return False instead)
            
            """

        # not a file
        
        if not self.filePresent( path ) : return True

        # normalizes path
        
        path = self.normalizePath( path, normalize = False  )

        # gets delete rights
        
        try :
            
            os.chmod( path, stat.S_IRWXU )

        except Exception, exception :

            None

        # tries to delete           

        try :

            os.remove( path )

        except Exception, exception :

            self.error = str( exception )
            
            return False

        # everything OK:
        
        return True





    def fileDuplicate (

        self,
        source = None,
        target = None,
        first = None,
        last = None
        ) :

        """ duplicates a file between indexes first and last (low level copy ) """

        
        ioBufferSize = 16384

        result = True

        sourceFile = None

        targetFile = None
        
        try :
            
            targetFile = file( target, "wb" )
            
            sourceFile = file( source, "rb" )

            # first position defined
            
            if ( ( not first is None ) and ( first > 0 ) ) : sourceFile.seek( first )
            
            else : first = 0
            
            # reads by blocks of 16k

            position = first 

            while True :

                # reads and writes one buffer
                
                if last is None : size = ioBufferSize

                elif last - position < ioBufferSize :  size = last - position
                
                else : size = ioBufferSize
                
                buffer = sourceFile.read( size )

                # end of file reached
                
                size = len( buffer )
                
                if size <= 0 : break

                targetFile.write( buffer )

          
        except Exception, exception :

            self.error = "fileCopy - exception " + str( exception )
    
            result = False            

        # closes
        
        if not sourceFile is None : sourceFile.close()
        
        if not targetFile is None : targetFile.close()
       
        return result

    
        

    def fileLinkedPath (

        self,
        path = None,
        ) :

        """ Returns the path to which the file "path" links.

            "path" is a .go or .to file, e.g. ../A/B/toto.go

            reads path P from the file.

            searches first for P/toto, and if it does not exist, returns P

            Returns None in case of problem


            """

        if self.isEmpty( path ) : return None

        path = self.normalizePath( path, normalize = False )

        # reads and strips weird characters

        containedPath = self.fileRead( path ).strip( " \r\n\t" )

        if self.isEmpty( containedPath ) : return None

        

        # instantiates variables in the content of the file
        
        containedPath = self.normalizePath( self.instantiate( containedPath, default = "_" ), normalize = False )

        # tries the directory PLUS the name of the link, e.g. /lesia/../toto/

        # the path inside is NOT a directory : returns it directly

        if not containedPath.endswith( os.sep ) : return containedPath

        # otherwise ( it is a directory ) tries to find containedPath/myOwnName        

        completedPath = self.normalizePath( containedPath + self.pathLastNameWithoutExtension( path ), normalize = False )

        # exists
        
        if self.directoryPresent( completedPath ) : return completedPath

        # does not exist : returns the directory contained in the file

        return containedPath



    def fileOpen (
        
        self,
        path = None,
        mode = None
        ) :
        
        """ Version of file() or open() that throws no exception

            In write mode (mode contains "w"), creates directory if needed
            
        """

        path = self.normalizePath( path, normalize = False  )
        
        if path is None : return None
        
        if mode is None : mode = "r"

        # write mode: creates path
        
        if mode.lower().find( "w" ) >= 0 :
            
             directory = self.pathDirectory( path )
             
             result = self.directoryCreate( directory )
             
             if not result : return None
             
        try :

            fileHandler = file( path, mode )

        except Exception, exception :
            
            self.error = str( exception )
            
            return None

        return fileHandler


        
        
    def filePresent (
        
        self,
        path = None
        ) :

        """ Checks whether the file "path" is here

            Returns True if present False if absent or any other problem

            """

        path = self.normalizePath( path, normalize = False  )
        
        if path is None : return False
        
        else : return os.path.isfile( path )





    def fileRead (

        self,
        path = None,
        mode = None
        ) :

        """ Reads an entire file into a string """


        path = self.normalizePath( path, normalize = False  )

        if path is None : return ""

        
        handler = self.fileOpen( path, mode )

        if handler is None : return ""

        try :
            
            text = handler.read()

        except Exception, exception :

            self.error = "fileRead - exception " + str( exception ) + " : " + path

            text = ""
        
        self.fileClose( handler )

        return text


    def fileRename (
        
        self,
        source = None,
        target = None
        ) :
            
        """ Alias for pathRename. Renames the source file into the target file.
            
            WARNING: USE FULL PATHS, OTHERWISE IT IS A COPY IN CURRENT DIRECTORY
            
            Returns True is OK, False otherwise

            Throws no exception (return False instead)
            
                
            """

        result = self.pathRename(
            source = source,
            target = target )

        return result

    



    def files (
        
        self,
        pattern = None
        ) :

        """ Returns the list of files or directories that match the pattern.

            Pattern is a path with wildcards.

            Wildcards allowed anywhere, e.g. \\*toto\\a*.*xt
            
            "*" matches with end of current identifier (subdirectory, file name, extension )
            "?" matches any single character
            [ sequence of chars ] matches 1 character if it is in sequence
            [ ! sequence of chars ] matches 1 character if it is NOT in sequence

            RECOMMENDED: only use *, if possible.
            
            """

        if pattern is None : return [ ]

            
        return glob.glob( pattern )

        

    def fileSize (
        
        self,
        path = None
        ) :

        """ Returns the size of the file


            """

        path = self.normalizePath( path, normalize = False  )
        
        if path is None : return 0L 
               
        # if the source is really a file, gets its size
        
        if os.path.isfile(path) : size = os.path.getsize( path )

        else : size = 0.

          
        return float( size )


    def fileTimeModified (
        
        self,
        path = None
        ) :

        """ Returns the date and time of last modification of the file as a long integer """

        if not self.filePresent( path ) : return 0

        path = self.normalizePath( path, normalize = False  )

        thisModified = self.integer( os.stat( path ).st_mtime, default = 0 )

        return thisModified



        
           

    def fileAppend (
        
        self,
        path = None,
        text = None,
        mode = None,
        ) :

        """ Appends a text to a file. Creates if absent """

        # file does not exist creates the file (and intermediary directories first)
            
        if not self.filePresent( path ) :
                
            result = self.fileCreate( path )
                
            if not result : return False

        if mode is None : mode = ""

        else : mode = str( mode ).lower()

        handler = self.fileOpen( path, mode = "a" + mode )

        if handler is None : return False

        try :
            
            handler.write( self.string( text ) )
            
            result = True
            
        except Exception, exception :

            self.error = str( exception )
            
            result = False
        
        self.fileClose( handler )

        return result
            
           





        

    def fileWrite (
        
        self,
        path = None,
        text = None,
        mode = None
        ) :

        """ Writes a text into a file """

        if mode is None : mode = "w"

        handler = self.fileOpen( path, mode = mode )

        if handler is None : return False

        try :
            
            handler.write( self.string( text ) )
            
            result = True
            
        except Exception, exception :

            self.error = "fileWrite - exception " + str( exception ) + " : " + path

            result = False
        
        self.fileClose( handler )

        return result
            
           
            


    def getcwd ( self ) :

        """ Aliasing for currentDirectory. Returns current directory or None if problem.

            Captures exception

            """

        return self.currentDirectory()
        

        
    def gotoDirectory (
        
        self,
        path = None
        ) :
        
        """ Changes dir.

            Returns True if possible False otherwise

            Captures exception

            """

        path = self.normalizePath( path, normalize = False  )
        
        if self.isEmpty( path ) : return True
       
        # goes to source directory
        
        try :
            
            os.chdir( path )
            
            return True

        except Exception, exception :
            
            self.error = str( exception )
            
            return False


    def isReserved (

        self,
        path = None,
        level = 1
        ) :

        """ Checks whether the item is reserved, i.e., starts with a reserved prefix

            Level = 2 : checks any subdirectory
            Level = 1 : checks last name
            Level = 0 : does not check

            NOTE: For speed, does NOT normalizes path.

            """

        # no path : not reserved
        
        if self.isEmpty( path ) : return False

        # nothing to check
        
        if self.isEmpty( self.reservedPrefixList ) : return False

        # control only on name

        if level == 1 : 

            name = self.pathLastNameWithExtension( path )

            # looks for reserved prefix at beginning of name

            for prefix in self.reservedPrefixList :

                if name.startswith( prefix  ) : return True

        elif level == 2 : 

            # looks for /x, where x is reserved

            for prefix in self.reservedPrefixList :

                if path.find( os.sep + prefix ) > 0 : return True
                
        return False

            
        
    def isSubdirectory (
        
        self,
        path = None,
        root = None
        ) :

        """ Checks whether the directory path is a subdirectory of the root """

        root = self.normalizePath( root, normalize = False  )

        path = self.normalizePath( path, normalize = False  )
        
        if ( (  root is None ) or ( path is None ) ) : return False

        return path.startswith( root ) 




    def listdir (
        
        self,
        path = None
        ) :
        
        """ Aliasing for directory content. Returns the content of the directory, i.e., a list of entry names

            Removes the current directory and parent directory

            Returns none if path is not a directory

        
            """

        return self.directoryContent( path )





    def makeDirectory (

        self,
        path = None
        ) :

        """ Creates a directory (and intermediary subdirectories).
        
            Returns True if directory exists after the execution, False otherwise

            Captures exception

            """

        path = self.normalizePath( path, normalize = False  )
        
        if self.isEmpty( path ) : return True
       
        # makes directory
        
        try :
            
            os.makedirs( path )

        except Exception, exception :
            
            None


        return ( self.directoryPresent( path ) )

     



    def makedirs (
        
        self,
        path = None
        ) :

        """ Aliasing for makeDirectory. Creates a directory (and intermediary subdirectories)

            Returns True if  directory exists after the execution , False otherwise
            
            """

        return self.makeDirectory( path )




    def normalizeDirectory (
        
        self,
        path = None,
        normalize = True
        ) :

        """ Alias for normalizePath """

        return self.normalizePath( path, normalize = normalize )


    def pathCopy (

        self,
        source = None,
        target = None,
        overwrite = True,
        instantiate = False,
        filter = False,
        link = False,
        empty = False
        ) :

        """ Copies a file and/or a directory. See fileCopy for arguments """

        if source is None : return False

        # file
        
        elif ( ( not source.endswith( "\\" ) ) and ( not source.endswith( "/" ) ) ) :

            ok = self.fileCopy(
                source = source,
                target = target,
                overwrite = overwrite,
                instantiate = instantiate,
                filter = filter,
                link = link,
                empty = empty
                )

        # directory
        
        else :

            ok = self.directoryCopy(
                source = source,
                target = target,
                overwrite = overwrite,
                instantiate = instantiate,
                filter = filter,
                link = link,
                empty = empty
                )

        return ok


        
    def pathCreate (

        self,
        path = None
        ) :
        
        """ Creates an empty path, file or directory.

            Uses the final os.sep to determine what it is

            Returns True if path exists after the execution, False otherwise

            """

        if self.isEmpty( path ) : return False

        path = self.normalizePath( path, normalize = False )

        # this is a directory
        
        if ( ( path.endswith( "\\" ) ) or ( path.endswith( "/" ) ) ) :
        
            result = self.directoryCreate( path )

            return result

        # this is a file

        else :

            directory = self.pathDirectory( path )

            name = self.pathLastNameWithExtension( path )

            result = self.directoryCreate( directory )
        
            if not result : return False

            fileHandler = self.fileOpen( path, "w" )
        
            if fileHandler is None : return False

            result = self.fileClose( fileHandler )
        
            return result

        
    def pathDateModified (
        
        self,
        path = None,
        recursive = 2
        ) :

        """ Returns the date and time of last modification of the directory as a string """


        if path is None : return ""
        
        elif ( ( not path.endswith( "\\" ) ) and ( not path.endswith( "/" ) ) ) : return self.fileDateModified( path )

        else : return self.directoryDateModified( path, recursive = recursive )

        

    def pathDayModified (
        
        self,
        path = None,
        recursive = 2
        ) :

        """ Returns the date of last modification of the directory as a string """

        if path is None : return ""

        elif ( ( not path.endswith( "\\" ) ) and ( not path.endswith( "/" ) ) ) : return self.fileDayModified( path )

        else : return self.directoryDayModified( path, recursive = recursive )



    def pathDelete (

        self,
        path = None
        ) :

        """ Deletes a path, file or directory.

           Returns True iff path is not present after deletion

           """

        if self.filePresent( path ) : result = self.fileDelete( path )

        elif self.directoryPresent( path ) : result = self.directoryDelete( path )

        else : result = True

        return result



    def pathFind (

        self,
        path = None
        ) :

        """ Returns the path to the file defined by path, or None if the path does not exist

            When the path contains a windosynchrasy like toto~2.txt, finds the real path are removes this scrap

            """

        if not self.pathPresent( path ) : return None

        path = self.normalizePath( path, normalize = False )

        # for a normal system, path itself
        
        if not sys.platform.startswith( "win" ) : return path

        # for silly windows only.

        directory = self.pathDirectory( path )

        name = self.pathLastNameWithoutExtension( path ).lower()

        extension = self.pathExtension( path ).lower()

        # we are on a drive C:\\
        
        if self.isEmpty( name ) : return directory

        # gets the true directory

        directory = self.pathFind( directory )

        # not found

        if self.isEmpty( directory ) : return None

        iTilde = name.find( "~" )

        # gets the true name
            
        items = self.directoryContent( directory, annotate = True  )

        # there is a pattern tttt~1

        iTilde = name.rfind( "~" )

        matchFlag = ( iTilde > 0 ) and ( iTilde + 1 < len( name ) ) and ( name[ iTilde + 1 : ].isdigit() )

        # there is a tilde pattern is the first character , e.g., ART3E3~5 -> A ( remainder of letters is whatever )
        
        if matchFlag :

            pattern = name[ 0 ]

        # no pattern, for directories, adds again the final \ to the name
        
        else :

            if path.endswith( os.sep ) : name = name + os.sep

            pattern = ""
            
        count = 0

        found = None

        statistics = os.stat( path )    # used for matching items 

        for item in items :

            itemName = self.pathLastNameWithoutExtension( item ).lower()

            if item.endswith( os.sep ) : itemName = itemName + os.sep

            itemExtension = self.pathExtension( item ).lower()

##            print "            nam [", itemName, "] ext [", itemExtension, "] vs nam [", name, "] ext [", extension, "]"

            # no match to do

            if not matchFlag :

                # no match ?
                
                if not extension == itemExtension : continue

                if not itemName == name : continue

                # here, there is a match

                found = item

                break


            # match is OK, now try to sort out the windowmanias, e.g., LABBOO~2 for the first match of labbook2005

            else :

                # no match

                if not extension[ : 3 ] == itemExtension[ : 3 ] : continue  # only 3 chars of extension are defined

                if not itemName.startswith( pattern ) : continue

                if not len( itemName ) > len( pattern ) : continue

                if not os.stat( directory + item ) == statistics : continue

                # multiple matches
                
                if count > 0 : break

                # keeps on to detect multiple matches

                found = item

                count = count + 1


        # after the loop, found nothing.
        
        if found is None : return None

        # multiple matches: could not solve ambiguity. comes back to the original path with ~ 

        if count > 1 : return path

        # normalizes final /

        if ( ( path.endswith( os.sep ) ) and ( not found.endswith( os.sep ) ) ) : found = found + os.sep

        return directory + found
        


            


    def pathLevel (

        self,
        path = None
        ) :

        """ Returns the level, i.e., the depth from the root of the volume """

        directory = self.pathDirectory( path )
        
        if directory is None : return 0

        return directory.count( os.sep )



        

            
    def pathPresent (

        self,
        path = None
        ) :

        """ Path is present on disk ( file or directory ) """


        if path is None : return False

        path = self.normalizePath( path, normalize = False  )
        
        if path is None : return False
        
        result = os.path.exists( path )

        return result



    def pathRename (
        
        self,
        source = None,
        target = None
        ) :
            
        """ Renames the source file into the target file.

            WARNING: USE FULL PATHS, OTHERWISE IT IS A COPY IN CURRENT DIRECTORY
            
            Returns True is OK, False otherwise

            Throws no exception (return False instead)
            
                
            """

        source = self.normalizePath( source, normalize = False  )

        target = self.normalizePath( target, normalize = False  )

        if ( ( source is None ) or ( target is None ) ) : return False
           
        if source == target : return True

##        print "Files.pathRename ", source, target, "\n--------"

        # by default result OK
        
        result = True      

        try :
            
            os.rename( source, target )

        except Exception, exception :
            
            self.error = str( exception )
            
            return False

        return True


    def pathProperties (

        self,
        path = None
        ) :

        """ returns a list of properties for the path. Each property is a word among:

            file, directory, drive, read (allowed), write (allowed), execute (allowed)

            file and directory are mutually exclusive, as well as file and drive

            for absent paths , the list is empty

            """


        # access rights : read, write, execute

        infos = self.pathStat( path )

        # path is absent

        if self.isEmpty( infos ) : return []

        # path present, considers the first word of statistics, and normalizes path, to detect whether it is a drive

        info = infos[ 0 ]

        path = self.normalizePath( path, normalize = False )
        
        propertyList = []

        # file 
        
        if stat.S_ISREG( info ) : propertyList.append( "file" )

        # not a drive or a directory

        elif not stat.S_ISDIR( info ) : None

        # drive

        elif len( self.pathDrive( path ) + os.sep ) == len( path ) : propertyList.extend( [ "drive", "directory" ] )

        # directory

        else : propertyList.append( "directory" )

        # access rights : read, write, execute

        if ( info & stat.S_IREAD ) : propertyList.append( "read" )

        if ( info & stat.S_IWRITE ) : propertyList.append( "write" )

        if ( ( stat.S_ISREG( info ) ) and ( info & stat.S_IEXEC ) ) : propertyList.append( "execute" )

        return propertyList

        

        

        
        
        
    def pathSize (

        self,
        path = None
        ) :

        """ Size of the path, file or directory """

        if not self.pathPresent( path ) : return 0L
        
        if self.filePresent( path ) : return self.fileSize( path )

        else : return self.directorySize( path )
        


    def pathStat (

        self,
        path = None
        ) :

        """ Returns the statistics of the path (if present) """

        try :

            return os.stat( self.normalizePath( path, normalize = False ) )

        except Exception, exception :

            return None

        

        
    def pathSubdirectory (

        self,
        directory = None,
        path = None
        ) :

        """ Finds the subdirectory of "directory" that matches best the prefix of the path """

        if self.isEmpty( path ) : return None

        # takes name and removes special characters
        
        name = self.pathLastName( path ).strip( "_.~" )
        
        # content of the directory
        
        items = self.directoryContent( directory, annotate = True )

        if self.isEmpty( items ) : return directory

        # loop on subdirectories
        
        match = ""

        length = 0
        
        for item in items :

            if not item.endswith( os.sep ) : continue

            # matches up to /
            
            if ( ( len( item ) > length + 1 ) and ( name.startswith( item[ : -1 ] ) ) ) : 

                length = len( item ) - 1

                match = item

            # matches up to 1 character before / ( e.g. article vs articles/ )

            elif ( ( len( item ) > length + 2 ) and ( name.startswith( item[ : -2 ] ) ) ) :

                length = len( item ) - 2

                match = item

        return self.normalizePath( directory + os.sep + match, normalize = False )

            
        
    def pathTimeModified (
        
        self,
        path = None,
        recursive = 2
        ) :

        """ Returns the ime of last modification of the directory as a string """

        if path is None : return 0L

        # tests both separators, in case the path is in slash convention
        
        elif ( ( not path.endswith( "\\" ) ) and ( not path.endswith( "/" ) ) ) : return self.fileTimeModified( path )

        else : return self.directoryTimeModified( path, recursive = recursive )


        

        
    def remove (
        
        self,
        path = None
        ) :

        """ Aliasing for fileDelete. Deletes the file "path"

            Returns True if file does not exist after execution, False otherwise

            Throws no exception (return False instead)
            
            """

        return self.fileDelete( path )
        

    def subDirectories (
        
        self,
        path = None,
        recursive = None
        ) :

        """ List of subdirectories contained in directory and subdirectories (recursive )

            returns list of full paths
            
            """

        return self.directoryPaths(
            path,
            mode = "directories",
            recursive = recursive,
            reserved = reserved
            )



      
    def theFile (
        
        self,
        directory = None,
        prefix = None,
        extension = None
        ) :

        """ Gets the unique file that starts with prefix, with the given extension in directory path

            In case of multiple matches, takes the 1st one and deletes the other files

            Returns a pair path, name

            """

        if directory is None : directory = os.curdir
        
        directory = self.normalizePath( directory, normalize = False  )
            
        path = None

        name = None

        # looks for name
        
        for item in self.directoryContent( directory ) :
                
            itemName = self.pathLastNameWithoutExtension( item )
            
            itemExtension = self.pathExtension( item )
            
            itemPath = self.normalizePath( directory + os.sep + item, normalize = False )
               
            if ( ( not prefix is None ) and ( not itemName.startswith( prefix ) ) ) : continue

            if ( ( not extension is None ) and ( not itemExtension == extension ) ) : continue

            # duplicate name
            
            if not path is None :
                    
                self.fileDelete( itemPath )


            # correct name
            
            else :

                path = itemPath
                    
                if prefix is None : name = itemName
                
                else : name = itemName[ len( prefix ) : ]

        return path, name
        
        
