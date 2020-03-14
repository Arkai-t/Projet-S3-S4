
""" Manages the bookcase, i.e., repository of items
   
 
    """


from api.Utilities import *

from api.Archiver import *

from api.BibFile import *

from api.TableFile import *



class Librarian :
    
    """ Manages the bookcase, i.e., repository of items


        """

    
    # address ( drive etc )

    address = None

    # bookcase ( path to a volume or directory )

    bookcaseDirectory = None

    # error

    error = None

    # list of erroneous items

    errorList = None

    # directory containing items exported from bookcase

    exportDirectory = None

    # logs

    logClassify = None

    logDownload = None
    
    logIndex = None
    
    # local directory of selected object on doc server

    local = None
   
    # current file or directory ( last uploaded or downloaded )

    path = None

    # selected item on server ( last downloaded or uploaded )

    selected = None

    # items to classiy ( path to a volume or a directory )

    classifyDirectory = None

    # lists of things to do (manually)

    todoList = None
   
    # list of uploaded items

    uploadList = None
    
    

    def __init__ ( self ) :

        """ constructor """

        self.setDefault()




    def buildIndex ( self ) :
        
        """ builds the indexes and verifies the bookcase

            
        """

        if not self.checkAccess() : return False

        if utilities.isEmpty( bibFile.typeList ) : return False

        # deletes the indexes

        items = utilities.directoryContent( self.bookcaseDirectory, annotate = True )

        for item in items :

            if item.endswith( os.sep ) : continue

            if item.startswith( "index" ) : utilities.fileDelete( self.bookcaseDirectory + item )

        
        # resets the log. After checkaccess we know that bookcase is defined and accessible
        
        utilities.fileWrite(
            self.bookcaseDirectory + os.sep + self.logIndex,
            "#date" + utilities.fieldDelimiter + \
            "name" + utilities.fieldDelimiter + \
            "link" + utilities.fieldDelimiter + \
            "problem" + "\n"
            )

        for iType in range( len(  bibFile.typeList ) ) :

            bibtex = bibFile.typeList[ iType ]

            categoryPath = self.bookcaseDirectory + os.sep + bibtex + os.sep

            if not utilities.directoryPresent( categoryPath ) : continue

            # lists of fields for general index and specific indexes

            fieldList = bibFile.fieldMatrix[ iType ]

            # paths to indexes
            
            bibtexIndex = self.bookcaseDirectory + "index" + "_" + bibtex

            # creates header if file not here

            if not utilities.filePresent( bibtexIndex ) :
                
                utilities.fileWrite(
                    bibtexIndex + ".tsv",
                    "#key" + utilities.fieldDelimiter + \
                    "bibtex" + utilities.fieldDelimiter + \
                    "link" + utilities.fieldDelimiter + \
                    utilities.wordsToText( fieldList, utilities.fieldDelimiter ) + "\n"
                    )
                          
            years = utilities.directoryContent( categoryPath, annotate = True )

            for year in years :

                if not year.endswith( os.sep ) : continue

                if not len( year ) == 5 : continue

                year = year[ : -1 ]

                if utilities.integer( year ) is None : continue                   

                # this is a date.

                # prepares index
                
                yearIndex = self.bookcaseDirectory + "index" + "_" + bibtex + "_" + year
                    
                if not utilities.filePresent( yearIndex ) :
                    
                    utilities.fileWrite(
                        yearIndex + ".tsv",
                        "#key" + utilities.fieldDelimiter + \
                        "bibtex" + utilities.fieldDelimiter + \
                        "link" + utilities.fieldDelimiter + \
                        utilities.wordsToText( fieldList, utilities.fieldDelimiter ) + "\n"
                        )


                # checks content

                yearPath = categoryPath + year + os.sep

                items = utilities.directoryContent( yearPath, annotate = True )

                for item in items :

                    if item.startswith( "_" ) : continue

                    self.indexItem(
                        yearPath + item,
                        bibtexIndex,
                        yearIndex,
                        fieldList
                        )


        return True




    def check ( self ) :

        """ Checks the connection to server

            returns True/False and sets context variable connectedValue to "true" or "false"
            
            """

        self.bookcaseDirectory = utilities.getVariable( "bookcase", default = "" )

        self.classifyDirectory = utilities.getVariable( "classify", default = "" )

        self.exportDirectory = utilities.getVariable( "export", default = "" )

        ok1 = self.checkAccess()

        ok2 = self.checkAccess( self.classifyDirectory )

        ok = ok1 and ok2
        
        if ok : utilities.setVariable( "connected", "true" )

        else : utilities.setVariable( "connected", "false" )
        
        return ok



    def checkAccess (

        self,
        directory = None

        ) :

        """ Checks the access to drive  and/or to directory( no control of access rights ) """

        # default is current bookcase

        if utilities.isEmpty( directory ) : directory = self.bookcaseDirectory
        
        # empty : no access

        if utilities.isEmpty( directory ) : return False

        # resets the cache ***FUCKING PYTHON: dircache on network drive works when it wants.

        dircache.reset()

        # there is a check file, can be detected : good
        
        if utilities.filePresent( directory + "check.txt" ) : return True

        # no drive : wrong
        
        if not utilities.directoryPresent( directory ) : return False

        # cannot read the check file, tries to create it ( users should have write - rights at least )
        
        ok = utilities.fileCreate( directory + "check.txt" )

        return ok
    


    def classify (

        self,
        path = None,
        directory = None,
        owner = None,
        ) :

        """ builds the indexes and verifies the bookcase """

        self.error = ""

        # called on the main to_classify directory

        if utilities.isEmpty( directory ) :

            # cannot access bookcase
        
            if not self.checkAccess() : 

                self.writeLogClassify(
                    self.bookcaseDirectory,
                    "cannot access bookcase"
                    )

                return False

            # prepares log file header

            utilities.fileWrite(
                self.bookcaseDirectory + os.sep + self.logClassify,
                "#date" + utilities.fieldDelimiter + \
                "directory" + utilities.fieldDelimiter + \
                "item" + utilities.fieldDelimiter + \
                "problem" + utilities.fieldDelimiter + \
                "link" + "\n"
                )

            # cannot access to classify directory

            if not self.checkAccess( self.classifyDirectory ) :

                self.writeLogClassify(
                    self.classifyDirectory,
                    "cannot access directory"
                    )

                return False

            # no bib types

            if utilities.isEmpty( bibFile.typeList ) :

                self.writeLogClassify(
                    self.bookcaseDirectory,
                    "list of types undefined (bibfile)"
                    )

                return False

        # there is a specific item to classify : uploads

        if not utilities.isEmpty( path ) :

            result = self.upload( path )

            return result


        # check content of directory to classify

        if utilities.isEmpty( directory ) : directory = self.classifyDirectory
        
        items = utilities.directoryContent( directory, annotate = True )

##        print "librarian.classify( ", directory, "owner", str(owner)

        for item in items :

            if item.startswith( "_" ) : continue

            if item.endswith( ".bib" ) : continue

            if item == "check.txt" : continue

            # owner's subdirectory

            if ( ( item.endswith( os.sep ) ) and ( item.startswith( "owner" ) ) ) :

                user = item[ len( "owner" ) : ]

                user = utilities.string( user, format = "split" ).strip( " " + os.sep )

                self.classify(
                    directory = directory + item,
                    owner = user
                    )

                continue

            # user subdirectory (same as owner, for now )
            
            if ( ( item.endswith( os.sep ) ) and ( item.startswith( "user" ) ) ) :

                user = item[ len( "user" ) : ]

                user = utilities.string( user, format = "split" ).strip( " " + os.sep )

                self.classify(
                    directory = directory + item,
                    owner = user
                    )

                continue



            # here, I have a classifiable item

            path = directory + item

            local = utilities.localDirectory( path )

            backups = utilities.backupsDirectory( path )

            name = utilities.pathName( item )

            if path.endswith( os.sep ) : extension = os.sep

            else : extension = "." + utilities.pathExtension( path )

            # is there a bib directly in the to_classify directory? moves it to _local/information.bib

            bib = directory + name + ".bib"

            if utilities.filePresent ( bib ) :

                utilities.directoryCreate( local )

                utilities.fileCopy( bib, local + "information.bib" )

                utilities.fileDelete( bib )

            ok = self.upload(
                path,
                replace = False,
                owner = owner
                )

            if not ok : continue

            # writes to log (uses the bibfile information to determine path in bookcase)


            shared = utilities.pathShared(
                category = bibFile.bibtex,
                author = bibFile.author,
                description = bibFile.description,
                title = bibFile.title,
                year = bibFile.year,
                extension = extension,
                directory = self.bookcaseDirectory
                )

           
            self.writeLogClassify(
                path,
                "",
                shared
                )

            # removes the item from classifyDirectory

            utilities.pathDelete( path )

            utilities.directoryDelete( local )

            utilities.directoryDelete( backups )
        
        return True




    def createBib (

        self,
        path = None,
        bibtex = None,
        author = None,
        description = None,
        owner = None,
        title = None,
        year = None,
        initials = None
        ) :

        """ creates a bib file """

        if utilities.isEmpty( path ) : return False

        if utilities.isEmpty( bibtex ) : return False

##        print "  createbib (",  bibtex, ",", author, ",", description, ",", title, ",", year, ",", initials, ")"

        if utilities.isEmpty( title ) : title = utilities.string( initials, format = "upper" )

        if utilities.isEmpty( title ) : title = description

        title = utilities.string( title, format = "title" )

        if utilities.isEmpty( owner ) : owner = utilities.getVariable( "organization" )

        owner = utilities.string( owner, format = "title", default =  "?" )

        table = [
            [ "bibtex", bibtex ],
            [ "author", author ],
            [ "description", description ],
            [ "title", title ],
            [ "year", year ],
            [ "owner", owner ],
            ]
        

        ok = bibFile.write( path, table )

        return ok

        
        
    def download (

        self,
        owner = None
        ) :

        """ Downloads an item from documentation server (path) and copies it into (target)

            
            """

        utilities.error = ""


        # cannot access bookcase
    
        if not self.checkAccess() : 

            self.writeLogDownload(
                owner = owner,
                path = self.bookcaseDirectory,
                text = "cannot access bookcase"
                )

            return False

        # prepares log file header

        utilities.fileWrite(
            self.bookcaseDirectory + os.sep + self.logDownload,
            "#date" + utilities.fieldDelimiter + \
            "owner" + utilities.fieldDelimiter + \
            "item" + utilities.fieldDelimiter + \
            "from" + utilities.fieldDelimiter + \
            "comment" + "\n"
            )

        # cannot access to download directory

        if not self.checkAccess( self.exportDirectory ) :

            self.writeLogDownload(
                owner = owner,
                path = self.exportDirectory,
                text = "cannot access directory"
                )

            return False

        # no bib types

        if utilities.isEmpty( bibFile.typeList ) :

            self.writeLogDownload(
                owner = owner,
                path = self.bookcaseDirectory,
                text = "list of types undefined (bibfile)"
                )

            return False

        # owner

        if utilities.isEmpty( owner ) : owner = utilities.getVariable( "user" )

        owner = utilities.string( owner, format = "strictunderscore", default = "All" )

        # makes a local directory

        directory = self.exportDirectory + "owner_" + owner + os.sep

        ok = utilities.directoryCreate( directory )

        if not ok :

            self.writeLogDownload(
                owner = owner,
                path = directory,
                text = "cannot create directory"
                )

            return False


        # loop on the indexes

        result = True

        items = utilities.directoryContent( self.bookcaseDirectory, annotate = True )

        for item in items :

            if not item.startswith( "index" ) : continue

            if not item.endswith( ".tsv" ) : continue

            # the index has bibcategory AND year, e.g., index_article_1999.tsv" : not considered
            
            if not item.count( "_" ) == 1 : continue

            ok = self.downloadIndex(
                index = self.bookcaseDirectory + item,
                directory = directory,
                owner = owner
                )

            if not ok : result = False
                
        return result





##    def download (
##
##        self,
##        owner = None
##        ) :
##        
##        """ downloads items belonging to owner and places them in export
##            
##        """
##
##        if not self.checkAccess() : return False
##
##        if not self.checkAccess( self.classifyDirectory ) : return False
##
##        if utilities.isEmpty( bibFile.typeList ) : return False
##
##
##        for iType in range( len(  bibFile.typeList ) ) :
##
##            bibtex = bibFile.typeList[ iType ]
##
##            categoryPath = self.bookcaseDirectory  + os.sep + bibtex + os.sep
##
##            if not utilities.directoryPresent( categoryPath ) : continue
##
##            years = utilities.directoryContent( categoryPath, annotate = True )
##
##            for year in years :
##
##                if not year.endswith( os.sep ) : continue
##
##                if not len( year ) == 5 : continue
##
##                year = year[ : -1 ]
##
##                if utilities.integer( year ) is None : continue
##
##
##                yearPath = categoryPath + year + os.sep
##                
##                items = utilities.directoryContent( yearPath, annotate = True )
##
##                for item in items :
##
##                    if item.startswith( "_" ) : continue
##
##                    name = utilities.pathName( item )
##
##                    path = yearPath + item
##
##                    local = utilities.localDirectory( path )
##
##                    backups = utilities.backupsDirectory( path )
##
##                    utilities.pathCopy( path, self.classifyDirectory + item )
##
##                    utilities.directoryCopy( local, self.classifyDirectory + "_" + name + os.sep )
##
##                    utilities.directoryCopy( backups, self.classifyDirectory + "__" + name + os.sep )
##
##
##        # loop on the indexes
##
##        result = True
##
##        items = utilities.directoryContent( self.bookcaseDirectory, annotate = True )
##
##        for item in items :
##
##            if ( ( item.startswith( "index" ) ) and ( item.endswith( ".tsv" ) ) :
##
##                ok = self.downloadIndex(
##                    index = self.bookcaseDirectory + item,
##                    directory = directory,
##                    owner = owner
##                    )
##
##                 if not ok : result = False
##
##                
##        return result
##






    def downloadIndex (

        self,
        index = None,
        directory = None,
        owner = None
        ) :

        """ downloads the content of an index that belong to some owner into directory """

        if utilities.isEmpty( directory ) : return False

        table = tableFile.readTable( index, size = 4, variable = True )

        if utilities.isEmpty( table ) : return False

        owner = utilities.string( owner, format = "title", default = None )

        # looks for items with right owner (table fields are key bibtex link owner (owner is defined in BibFile.fieldMatrix)

        for item in table :

            if ( ( not owner is None ) and ( not item[ 3 ] == owner ) ) : continue

##            print "    downloadindex found", item[ 2 ], item[ 3 ]

            # path to the _item/index.html file
            
            path = item[ 2 ]

            local = utilities.pathDirectory( path )

            name = utilities.pathName( local ).strip( "_ " )

            source = utilities.pathDirectory( local )

            # copies _item*, item.*

            items = utilities.directoryContent( source, annotate = True )

            for item in items :

                if not utilities.pathName( item ).strip( "_ " ) == name : continue

                utilities.pathCopy( source + item, directory + item )

                self.writeLogDownload(
                    path = directory + item,
                    owner = owner,
                    source = path,
                    text = ""
                    )

                
            

        return True








    def downloadPath (

        self,
        path = None,
        target = None
        ) :

        """ Downloads a file or directory from documentation server (path) and copies it into (target)

            
            """


        self.selected = path
        
        self.path = utilities.normalizePath( target, normalize = False )
        
        ok = utilities.pathCopy( path, target )

        return ok





    def indexItem (

        self,
        path = None,
        bibtexIndex = None,
        yearIndex = None,
        fieldList = None
        ) :

        """ verifies an item of the bookcase and indexes it """

        if utilities.isEmpty( path ) : return False

        if utilities.isEmpty( bibtexIndex ) : return False

        if utilities.isEmpty( yearIndex ) : return False

        if utilities.isEmpty( fieldList ) : return False

        local = utilities.localDirectory( path )
        
        bib = local  + "information.bib"

##        backups = utilities.backupsDirectory( path ) 
##
##        backup = backups + "backup.zip"

        # checks bib file and backup

        if not utilities.filePresent( bib ) :

            self.writeLogIndex( path, "missing bib file" )

            return False

##        # no backup : creates it
##
##        if not utilities.filePresent( backup ) :
##
##            # creates a zip that contains the item with no date or other information in name.
##
##            ok = archiver.backup(
##                path = path,
##                target = "backup.zip",
##                directory = backups
##                )
##
##            if not ok :
##
##                self.writeLogIndex( path, "missing backup file - could not create it" )
##
##                return False
##            
##            # backups the local directory in the same backup
##
##            ok = archiver.backup(
##                path = local,
##                target = "backup.zip",
##                directory = backups
##                )
##
##            if not ok :
##
##                self.writeLogIndex( path, "missing backup file - could not complete it" )
##
##                return False
##
##            # notifies creation
##
##            self.writeLogIndex( path, "create backup file" )

            

        # checks content of .bib

        bibFile.read( bib )

        if utilities.isEmpty( bibFile.bibtex ) :

            self.writeLogIndex( path, "invalid bib file" )

            return False

        if not bibFile.checkComplete() :

            self.writeLogIndex( path, "missing in bibtex file: " + utilities.wordsToText( bibFile.missingList ) )

            return False

##        if not bibFile.checkComplete( [ "file", "bib", "zip" ] ) :

        if not bibFile.checkComplete( [ "file", "bib" ] ) :

            self.writeLogIndex( path, "missing in bibtex file: " + utilities.wordsToText( bibFile.missingList ) )

            return False

            
        # check the place according to content of bib file

        if path.endswith( os.sep ) : extension = os.sep

        else : extension = "." + utilities.pathExtension( path )

        shared = utilities.pathShared(
            category = bibFile.bibtex,
            author = bibFile.author,
            description = bibFile.description,
            title = bibFile.title,
            year = bibFile.year,
            extension = extension,
            directory = self.bookcaseDirectory
            )

        if not shared == utilities.slashPath( path ) :

            self.writeLogIndex(
                path,
                "incorrect place (correct location: " + shared + ") - move back to : " + self.classifyDirectory
                )

            return False

        # rewrites the access html file, information.html

        createFlag = not utilities.filePresent( local + "information.html" ) 

        ok = self.writeHtml( path )

        if not ok :

            self.writeLogIndex( path, "could not update information.html" )

            return False

        elif createFlag :

            self.writeLogIndex( path, "create information.html file" )
        
        # places current item in indexes, uses bibfile information

        self.indexPath(
            path,
            bibtexIndex + ".tsv",
            yearIndex + ".tsv",
            fieldList
            )

        # appends to the bib files

        text = os.linesep + bibFile.text.strip( " \n\t\r," ).replace( "\n", os.linesep ) + os.linesep
        
        utilities.fileAppend( bibtexIndex + ".bib", text )
        
        utilities.fileAppend( yearIndex + ".bib", text )
        

        return True
       
        

        

    def indexPath (

        self,
        path = None,
        bibtexPath = None,
        yearPath = None,
        fieldList = None,
        ) :

        """ adds an item to the indexes, uses bibfile information.

            no control of correctness
            
            """

        # bibtex type
        
        bibtex = utilities.string( bibFile.bibtex, default = "" )

        # key to control duplicates
        
        key = utilities.string( bibFile.title, format = "initials", default = "" )

        # path to the information.html file that contains links

        local = utilities.localDirectory( path )

        html = "file:///" + utilities.slashPath( local + "information.html" )

        # texts for general and specific indexes

        text = key + utilities.fieldDelimiter + bibtex + utilities.fieldDelimiter + html + utilities.fieldDelimiter

        for item in fieldList :

            item = "reference" + item.capitalize()

            index = utilities.index( bibFile.attributeList, item )

            if index < 0 :

                text = text + utilities.voidCode + utilities.fieldDelimiter

                continue

            value = bibFile.valueList[ index ].replace( "{", "" ).replace( "}", "" )

##            if ( ( item == "referenceFile" ) or ( item == "referenceBib" ) or ( item == "referenceZip" ) ) :
##
            if ( ( item == "referenceFile" ) or ( item == "referenceBib" ) ) :

                value = "file:///" + utilities.slashPath( self.bookcaseDirectory + value )

            text = text + utilities.asciiToFlat( value, default = utilities.voidCode ) + utilities.fieldDelimiter

        text = text + "\n"
            
        utilities.fileAppend( bibtexPath, text )

        utilities.fileAppend( yearPath, text )

        return True




    def setDefault ( self ) :

        """ sets default attributes"""
    
        self.bookcaseDirectory = utilities.getVariable( "bookcase", default = "" )

        self.classifyDirectory = utilities.getVariable( "classify", default = "" )

        self.logClassify  = "log_classify.tsv"

        self.logDownload = "log_download.tsv"
        
        self.logIndex = "log_index.tsv"


            

        


    def setTarget (

        self,
        path = None,
        directory = None,
        ) :

        """ Determines the source path self.path and the target self.selected when something is uploaded on a drive """

        # atribute that keeps track of the current source
        
        self.path = utilities.normalizePath( path, normalize = False )

        # target's name (includes extension)

        address = self.bookcaseDirectory

        prefix = utilities.getVariable( "type", default = "" )

        year = utilities.getVariable( "year", default = "" )

        target = utilities.normalizePath( address + os.sep + prefix + os.sep + year + os.sep, normalize = False )

        if utilities.isEmpty( target ) :

            utilities.error = "upload - no folder available"

            return False

        # there is a subdirectory

        directory = utilities.string( directory, default = "" )

        # uploads the object

        name = utilities.pathLastNameWithExtension( path )

        target = utilities.normalizePath( target + os.sep + directory + os.sep + name, normalize = False )

        self.selected = target

        return True


        
        
        
    def upload (

        self,
        path = None,
        complete = True,
        replace = True,
        owner = None,
        ) :

        """ Uploads a file or directory on documentation server.

            Name is the new name ( directory and extension are conserved )


            Owner is the owner or none. If it is defined, overrides the field of bibtex

            if complete is True, uploads the local directory too

            if replace is true, can replace previous doc in bookcase, otherwise error.
            
            """

        utilities.error = ""

        if not utilities.pathPresent( path ) : return False

        # source (old)
        
        oldPath = utilities.normalizePath( path, normalize = False )

        oldDirectory = utilities.pathDirectory( path )
        
        oldName = utilities.pathNameExtension( path )

        if oldPath.endswith( os.sep ) : oldExtension = os.sep

        else : oldExtension = "." + utilities.pathExtension( oldPath )

        oldLocal = utilities.localDirectory( path )

        oldBackups = utilities.backupsDirectory( path )
        
        # parses the file name

        bibtex, author, description, year, initials = utilities.parseShared( path )

        # undefined author is unknown, and date is 9999

        if utilities.isEmpty( year ) : year = "9999"

        if utilities.isEmpty( author ) : author = "unknown"

        # keeps the description from name, to complete bib file

        defaultDescription = description
        
##        print "librarian.upload", path
##        
##        print "     ", bibtex,author, description, year, initials

        extension = utilities.pathExtension( path )

        bibPath = oldLocal + os.sep + "information.bib"

        bibFlag = utilities.filePresent( bibPath )

        # no bib file, name allows creation, creates

        if ( ( not bibFlag ) and ( not utilities.isEmpty( bibtex ) ) ) :

            bibFlag = self.createBib(
                bibPath,
                bibtex = bibtex,
                author = author,
                description = description,
                year = year,
                owner = owner,
                initials = initials
                )


        # no way , there is no bibtex file

        if not bibFlag :

            self.writeLogClassify(
                oldPath,
                "no sufficient bibtex information (incomplete name and no file *.bib)"
                )

            return False
                

        # reads the bib file 
        
        bibFile.read( bibPath, bind = False )

        bibtex = bibFile.bibtex

        year = utilities.string( bibFile.year, default = "" )

        author = utilities.string( bibFile.author, default = "" )

        description = utilities.string( bibFile.description )

        if utilities.isEmpty( description ) : description = defaultDescription

        title = utilities.string( bibFile.title, default = "" )

        if utilities.isEmpty( bibtex ) :

            self.writeLogClassify(
                oldPath,
                "bibtex category undefined"
                )

            return False

        if utilities.isEmpty( year ) :

            self.writeLogClassify(
                oldPath,
                "year undefined"
                )

            return False

        if not bibFile.checkComplete() :

            self.writeLogClassify(
                oldPath,
                "missing in bibtex file: " + utilities.wordsToText( bibFile.missingList )
                )

            return False

        # determines the path and name in the bookcase

        newPath = utilities.pathShared(
            category = bibtex,
            author = author,
            description = description,
            title = title,
            year = year,
            extension = oldExtension,
            directory = self.bookcaseDirectory
            )
        
        newName = utilities.pathName( newPath )

        newExtension = oldExtension

        newName = newName + "." + newExtension
      
        newLocal = utilities.localDirectory( newPath )

        newBackups = utilities.backupsDirectory( newPath )

        # already present

        if ( ( not bool( replace ) ) and ( utilities.pathPresent( newPath ) ) ) :

            self.writeLogClassify(
                oldPath,
                "already present in bookcase: " + newPath
                )

            return False           

        # copies the file

        ok = utilities.pathCopy( oldPath, newPath )

        if not ok :

            self.writeLogClassify(
                oldPath,
                "could not copy in bookcase"
                )

            return False

        # copies the local directory

        ok = utilities.directoryCopy ( oldLocal, newLocal )

        if not ok :

            self.writeLogClassify(
                oldPath,
                "could not copy local directory in bookcase"
                )

            return False

##        # creates a zip that contains the item with no date or other information in name.
##
##        ok = archiver.backup(
##            path = newPath,
##            target = "backup.zip",
##            directory = newBackups
##            )
##
##        if not ok :
##
##            self.writeLogClassify( oldName, "could not create backup in bookcase"   )
##
##            return False
##        
##
##
##        # backups the local directory in the same backup
##
##        ok = archiver.backup(
##            path = newLocal,
##            target = "backup.zip",
##            directory = newBackups
##            )
##
##        if not ok :
##
##            self.writeLogClassify( oldName, "could not complete backup in bookcase" )
##
##            return False

        # writes the bib file again, with the paths to bib, item and zip

        bibFile.setAttributes(
            owner = owner,
            filePath = newPath,
            )

        ok = bibFile.write( path = newLocal + "information.bib" )

        if not ok :

            self.writeLogClassify(
                oldPath,
                "could not create bib file in bookcase"
                )

            return False
        
        # creates a html with links to document & bib

        ok = self.writeHtml( newPath )

        if not ok :

            self.writeLogClassify(
                oldPath,
                "could not create information.html file in bookcase"
                )

            return False

        return True



    def writeHtml (

        self,
        path = None
        ) :

        """ creates _local/information.html, with links to the item & the bib """

        local = utilities.localDirectory( path )

        # stores previous values of variables, initializes them to copy the template

        utilities.pushVariables( [ "shared", "author", "title", "year" ] )

        utilities.setVariable( "shared", path )

        utilities.setVariable( "author", bibFile.author.replace( "{", "" ).replace( "}", "" ).replace( "~", " " ) )
        
        utilities.setVariable( "title", bibFile.title.replace( "{", "" ).replace( "}", "" ) )
        
        utilities.setVariable( "year", bibFile.year )

        templatePath = utilities.getVariable( "procedures" ) + "_common" + os.sep + "documents" + os.sep + "information.html"

        ok = utilities.fileCopy(
            templatePath,
            local + "information.html",
            instantiate = True
            )
        

        # restores the variables

        utilities.popVariables( [ "shared", "author", "title", "year" ] )

        return ok 



    def writeLogClassify (

        self,
        path = None,
        text = None,
        target = None,
        date = None,
        
        ) :

        """ status of item "path", error and/or target in bookcase """


        if utilities.isEmpty( date ) : date = clock.date()
        
        if not utilities.isEmpty( path ) :

            directory = utilities.pathDirectory( path )

            name = utilities.pathLastNameWithExtension( path )

        else :

            directory = ""

            name = ""

        if not utilities.isEmpty( target ) :

            html = utilities.localDirectory( target ) + "information.html"

            html = "file:///" + utilities.slashPath( html )

        else :

            html = ""
        
        
        text = utilities.string( text, default = "" )

        # there is a message : sets the error

        if not utilities.isEmpty( text ) :
        
            if utilities.isEmpty( name ) : error = text

            else : error = name + "-" + text

            self.error = error

        # no access to bookcase cannot write log
        
        if not utilities.directoryPresent( self.bookcaseDirectory ) : return
        
        # there is a file : writes it in log

        if not utilities.isEmpty( name ) :

            flat = utilities.asciiToFlat( text, default = utilities.voidCode )

            utilities.fileAppend(
                self.bookcaseDirectory + os.sep + self.logClassify,
                date + utilities.fieldDelimiter +
                directory + utilities.fieldDelimiter + \
                name + utilities.fieldDelimiter + \
                flat + utilities.fieldDelimiter + \
                html + utilities.fieldDelimiter + "\n"
                )

##        print name, "-", text


    def writeLogDownload (

        self,
        path = None,
        text = None,
        source = None,
        date = None,
        owner = None,
        
        ) :

        """ status of item "path", error and/or target in bookcase """

        if utilities.isEmpty( date ) : date = clock.date()

        text = utilities.string( text, default = "" )

        path = utilities.string( path, default = utilities.voidCode )

        owner = utilities.string( owner, default = utilities.voidCode )

        source= utilities.string( source, default = utilities.voidCode )

        # there is a message : sets the error

        if not utilities.isEmpty( text ) :

            error = text

            self.error = error

        # no access to bookcase cannot write log
        
        if not utilities.directoryPresent( self.bookcaseDirectory ) : return
        
        # there is a file : writes it in log

        flat = utilities.asciiToFlat( text, default = "" )

        utilities.fileAppend(
            self.bookcaseDirectory + os.sep + self.logDownload,
            date + utilities.fieldDelimiter + \
            owner + utilities.fieldDelimiter + \
            path + utilities.fieldDelimiter + \
            source + utilities.fieldDelimiter + \
            flat + utilities.fieldDelimiter + "\n"
            )




        

    def writeLogIndex (

        self,
        path = None,
        text = None,
        target = None,
        date = None,
        
        ) :

        """ status of item "path", error and/or target in bookcase """

        if utilities.isEmpty( date ) : date = clock.date()
        
        if not utilities.isEmpty( path ) :

            name = utilities.pathLastNameWithExtension( path )

            html = utilities.localDirectory( path ) + "information.html"

            html = "file:///" + utilities.slashPath( html )

        else :

            name = ""

            html = ""

        text = utilities.string( text, default = "" )

        # there is a message : sets the error

        if not utilities.isEmpty( text ) :
        
            if utilities.isEmpty( name ) : error = text

            else : error = name + "-" + text

            self.error = error

        # no access to bookcase cannot write log
        
        if not utilities.directoryPresent( self.bookcaseDirectory ) : return
        
        # there is a file : writes it in log

        if not utilities.isEmpty( html ) :
            
            flat = utilities.asciiToFlat( text, default = "" )

            utilities.fileAppend(
                self.bookcaseDirectory + os.sep + self.logIndex,
                date + utilities.fieldDelimiter + \
                name + utilities.fieldDelimiter + \
                html + utilities.fieldDelimiter + \
                flat + utilities.fieldDelimiter + "\n"
                )









    
# -----------------------------------
# creates the global singleton object if not already here
#

if not "librarian" in globals() : librarian = Librarian()
