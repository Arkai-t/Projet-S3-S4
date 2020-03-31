
""" Utilities to convert files from text/special wiki into Wiki (standard) HTML, PDF...

    See on wikipedia for information on  Wiki format
   
 
    """


from api.Utilities import *

from api.BibFile import *

from api.Clock import *

from api.Html import *

from api.PdfFile import *

from api.TableFile import *

from api.Wiki import *



class Converter :
    
    """ Utilities to convert files from text/special wiki into Wiki (standard) HTML, PDF...

        See on wikipedia for information on  Wiki format
        
        """

   
    # output ( text buffer )

    output = None

    # source file

    source = None

    # target file

    target = None
    
    # input template (text buffer)

    template = None


    def __init__ ( self ) :

        """ Constructor. Does absolutely nothing
           
            """

        None



        
        
    def convertFormatWikiToHtml (

        self,
        text = None,
        format = None
        ) :

        """ converts the tag of 'format' ( bold, italics...) from wimi to html

            returns a text ( empty if problem )

            """

        if utilities.isEmpty( text ) : return ""
        
        index = utilities.index( wiki.formatList, format )

        if index < 0 : return text

        wikiStartCode = wiki.codeStartList[ index ]

        wikiStopCode = wiki.codeStopList[ index ]

        index = utilities.index( html.formatList, format )

        if index < 0 : return text

        htmlStartCode = html.codeStartList[ index ]

        htmlStopCode = html.codeStopList[ index ]

        iStart= 0

        while True :

            iStart = text.find( wikiStartCode, iStart )

            if iStart < 0 : break

            iStop = text.find( wikiStopCode, iStart + len( wikiStartCode) )

            if iStop < 0 : break

            old = text[ iStart : iStop + len( wikiStopCode ) ]

            new = htmlStartCode + text[ iStart + len( wikiStartCode ) : iStop ] + htmlStopCode

            text = text.replace( old, new )

            iStart = iStart + len( new )

        return text




    def convertLinksWikiToHtml (

        self,
        text = None
        ) :

        """ converts the links from wiki format ( wiki-like, in fact) to html, and copies locally the files


            """


        if utilities.isEmpty( text ) : return ""
        

        iStart = 0

        while True :

            iStart = text.find( wiki.openLinkCode, iStart )

            if iStart < 0 : break

            iLink, address, description = wiki.getLink( text, iStart )

            if iLink < 0 : break

            old = text[ iStart : iLink ]

            # normalizes description: removes quotes

            description = description.replace( '"', ' ' ).replace( "'", " " ) 

            # for urls, just inserts

            if utilities.isUrl( address ) :

                new = html.link( address, description )

            # for files, makes a copy in local directory

            else :

                if utilities.isAbsolutePath( address ) : path = address

                else : path = utilities.pathDirectory( self.source ) + address

                directory = utilities.pathDirectory( self.target )

                local = utilities.localDirectory( self.target )

                if not path.startswith( local ) :

                    address = local + utilities.pathLastNameWithExtension( path )

                    utilities.pathCopy( path, address )

                # link or image, will take relative address
                
                if utilities.pathExtension( address ) in wiki.imageExtensionList :

                    new = html.image( address, description, directory )

                else :

                    new = html.link( address, description, directory )

            text = text.replace( old, new )

            iStart = iStart + len( new )

        return text
        




    def convertLinksWikiToWiki (

        self,
        text = None,
        normalize = False
        ) :

        """ normalizes the links in wiki format i.e. copies locally the files

            if normalize is True, performs strict conversion,i.e., removes local links
            

            """

        
        if utilities.isEmpty( text ) : return ""
        

        iStart = 0

        while True :

            iStart = text.find( wiki.openLinkCode, iStart )

            if iStart < 0 : break

            iLink, address, description = wiki.getLink( text, iStart )

            if iLink < 0 : break

            old = text[ iStart : iLink ]

            # normalizes description: removes quotes

            description = description.replace( '"', ' ' ).replace( "'", " " )

            # url : skips

            if utilities.isUrl( address ) :

                new = old.replace( utilities.featureDelimiter, " " )

                text = text.replace( old, new )

                iStart = iStart + len( new )


            # strict normalization : removes files

            elif bool( normalize ) :

                text = text.replace( old, "" )
            
            # for files, makes a copy in local directory

            else :

                if utilities.isAbsolutePath( address ) : path = address

                else : path = utilities.pathDirectory( self.source ) + address

                directory = utilities.pathDirectory( self.target )

                local = utilities.localDirectory( self.target )

                if not path.startswith( local ) :

                    address = local + utilities.pathLastNameWithExtension( path )

                    utilities.pathCopy( path, address )

                address = address[ len( directory ) : ]

                new = wiki.openLinkCode + address + utilities.featureDelimiter + description + wiki.closeLinkCode

                text = text.replace( old, new )

                iStart = iStart + len( new )


        return text
        

    def convertTextWikiToHtml (

        self,
        text = None,
        normalize = False
        
        ) :

        """ converts a text from wiki to html, does not handle protection tags <nowiki>

            
            """

        if utilities.isEmpty( text ) : return False       

        # replaces horizontal lines

        text = text.replace( wiki.horizontalLineCode, html.horizontalLine() )

        # processes the wiki tags in order (otherwise there is ambiguity in wiki syntax)

        for format in wiki.formatList : text = self.convertFormatWikiToHtml( text, format )

        # processes links

        text = self.convertLinksWikiToHtml( text )

        return text



    def convertTextWikiToWiki (

        self,
        text = None,
        normalize = False,
        ) :

        """ converts a text from wiki to STANDARD wiki, does not handle protection tags <nowiki>

            if normalize is True, performs strict conversion, so that the page can be loaded on w Wiki
            

            """

        if utilities.isEmpty( text ) : return ""      

        # processes starting spaces

        # removes starting spaces and processes links

        text = wiki.normalizeHeadingSpaces( text )
        
        text = self.convertLinksWikiToWiki( text, normalize )

        return text





    def convertWikiToHtml (

        self,
        text = None

        ) :

        """ converts a text (default = self.template ) from wiki format to html format """

        if utilities.isEmpty( text ) : text = self.template

        if utilities.isEmpty( text ) : return ""

        # parses the wiki text according to <nowiki> tags

        textList = wiki.split( text, normalize = True )

        if utilities.isEmpty( textList ) : return ""

        result = ""

        for text in textList :

            if text.startswith( wiki.noWikiStartCode ) :

                result = result + text[ len( wiki.noWikiStartCode ) : - len( wiki.noWikiStopCode ) ]

            else :

                result = result + self.convertTextWikiToHtml( text )

        # replaces end of lines
        
        result = result.replace( "\n", html.newLineCode )

        return result


        

    def convertWikiToWiki (

        self,
        text = None,
        normalize = False

        ) :

        """ converts a text (default = self.template ) from wiki format to expanded wiki format

            if normalize is True, performs strict conversion, so that the page can be loaded on w Wiki
            

            """

        if utilities.isEmpty( text ) : text = self.template

        if utilities.isEmpty( text ) : return ""

        # parses the wiki text according to <nowiki> tags

        textList = wiki.split( text, normalize = True )

        if utilities.isEmpty( textList ) : return ""

        result = ""

        for text in textList :

            if text.startswith( wiki.noWikiStartCode ) :

                result = result + text[ len( wiki.noWikiStartCode ) : - len( wiki.noWikiStopCode ) ]

            else :

                result = result + self.convertTextWikiToWiki( text, normalize = normalize )


        return result



    def create (

        self,
        source = None,
        target = None,
        instantiate = True,
        copy = True
        ) :

        """ creates a target file from a source file.

            Source is a .txt containing special wiki text.

            Target is a PDF or a HTML file, or a .txt file that contains standard wiki.

            if Instantiate is True, the source file is instantiated before processing

            """

        # target & source 

        target = utilities.normalizePath( target, normalize = False )

        if utilities.isEmpty( target ) : return False

        source = utilities.normalizePath( source, normalize = False )

        if not utilities.filePresent( source ) : return False

        self.targetPath = target

        self.sourcePath = source

        # same file

        if self.sourcePath == self.targetPath : return True

        # local directory of target, NOT DELETED (may be referenced in source)
        
        localTarget = utilities.localDirectory( self.targetPath )

        # local directory of source

        localSource = utilities.localDirectory( self.sourcePath )

        if not utilities.directoryPresent( localSource ) : localSource = None

        elif localSource == localTarget : localSource = None
        
        # reads source into lists of texts-tags

        ok = self.read( self.sourcePath, instantiate )

##        print "converter.create read is ", ok

        # writes lists to target

        if ok : ok = self.write( copy = copy )

        # could not read or write: does a direct copy

        if not ok :

            ok = utilities.pathCopy( source, target )

            if not ok : return False

            if not localSource is None :  ok = utilities.directoryCopy( localSource, localTarget )
        
        return ok




    def formDataToList (

        self,
        text = None
        ) :

        """ converts a text that contains a table (at most 5 cols ) into a list """

        if utilities.isEmpty( text ) : return [ ], [ ]

        table = tableFile.readTable(
            text = text,
            size = 5,
            variable = True
            )

        if utilities.isEmpty( table ) : return [ ], [ ]

        textList = [ ]

        stateList = [ ]

        for line in table :

            text = ""

            for word in line :

                text = text + \
                       utilities.asciiToFlat( word, default = utilities.voidCode ) + \
                       utilities.fieldDelimiter

            textList.append( text[ : -1 ] )

            stateList.append( None )

            textList.append( " " )

            stateList.append( "line" )

        return textList, stateList

    

    def listToFormData ( 

        self,
        textList = None,
        stateList = None
        
        ) :

        """ converts a list of lines into a 5 columns ascii table """

        if ( ( utilities.isEmpty( textList ) ) or ( utilities.isEmpty( stateList ) ) ) :

            textList = self.textList

            stateList = self.stateList

            
        if ( ( utilities.isEmpty( textList ) ) or ( utilities.isEmpty( stateList ) ) ) : return ""

        text = ""

        for index in range( len( textList ) ) :

            state = stateList[ index ]

            line = textList[ index ]

            if state == "line" :

                text = text + "\n"

                continue

            if not utilities.isEmpty( state ) : continue


            # only void states, i.e., normal text
            
            words = line.split( utilities.fieldDelimiter )

            if len( words ) <= 1 : continue

            identifier = words[ 0 ]

            if utilities.isEmpty( identifier ) : continue

            category = utilities.voidCode

            value = utilities.voidCode

            description = utilities.voidCode

            date = utilities.string( clock.date() )

            if len( words ) >= 3 :

                category = words[ 1 ]

                value = words[ 2 ]

                if len( words ) >= 4 : description = words[ 3 ]

                if len( words ) >= 5 : date = words[ 4 ]
                
            else :

                category = "entry"

                value = words[ 1 ]

                description = identifier

            text = text + \
                   identifier + utilities.fieldDelimiter + \
                   category + utilities.fieldDelimiter + \
                   value + utilities.fieldDelimiter + \
                   description + utilities.fieldDelimiter + \
                   date

        return text

    

        
    def read (

        self,
        path = None,
        instantiate = None
        ) :

        """ reads a source file in different formats and converts it into a list of texts + tags """

        # resulting lists
        
        self.textList = [ ]

        self.stateList = [ ]

        # source file
        
        if not path is None : self.sourcePath = utilities.normalizePath( path, normalize = False )

        if utilities.isEmpty( self.sourcePath ) : return False

        # determines type of file

        isText = False

        isWiki = False

        isHtml = False

        isBib = False

        isData = False
        
        extensionSource = utilities.pathExtension( self.sourcePath ).lower()

        if "txt" in extensionSource : isText = True

        elif "ini" in extensionSource : isText = True

        elif "wiki" in extensionSource : isWiki = True

        elif "htm" in extensionSource : isHtml = True

        elif "bib" in extensionSource : isBib = True

        elif "csv" in extensionSource : isData = True

        elif "tsv" in extensionSource : isData = True

        # cannot be converted : will be copied directly
        
        else : return False

        # reads and removes invalid end-of-lines

        self.sourceText = utilities.fileRead( self.sourcePath ).replace( "\r", "" )

        if bool( instantiate ) : self.sourceText = utilities.instantiate( self.sourceText, default = "?" )

        if utilities.isEmpty( self.sourceText ) : return True

        # changes directory ( for file expansion )

        directory = utilities.pathDirectory( self.sourcePath )

        previousDirectory = utilities.currentDirectory()

        if not directory == previousDirectory : utilities.gotoDirectory( directory )

        # plain text or x-wiki
        
        if isText :

            self.sourceText = wiki.expand( self.sourceText, instantiate = instantiate )

            self.textList, self.stateList = wiki.asciiToList(
                self.sourceText,
                self.sourcePath
                )

        # html

        elif isHtml :

            self.textList, self.stateList = html.htmlToList(
                self.sourceText,
                self.sourcePath
                )


        # wiki

        elif isWiki :

            self.textList, self.stateList = wiki.asciiToList(
                self.sourceText,
                self.sourcePath
                )

        # bib file

        elif isBib :

            self.textList, self.stateList = bibFile.asciiToList( text = self.sourceText )


        # data table 

        elif isData :

            self.textList, self.stateList = self.formDataToList( text = self.sourceText )


        # back to original directory

        if not previousDirectory == directory : utilities.gotoDirectory( previousDirectory )

        return True
            

    def write (

        self,
        path = None,
        copy = True
        ) :

        """ writes the internal lists of texts and tags (previously read from any file) into the target file

            'copy' (default True) means that the links and subfiles are copied locally in local directory of target
            if 'copy' is false, the links are preserved
            
            """

        
        # target file
        
        if not path is None : self.targetPath = utilities.normalizePath( path, normalize = False )

        if utilities.isEmpty( self.targetPath ) : return False

       
        # copies or converts according to extensions

        # determines type of file

        isText = False

        isWiki = False

        isHtml = False

        isBib = False

        isData = False

        extensionTarget = utilities.pathExtension( self.targetPath ).lower()

        if "txt" in extensionTarget : isText = True

        elif "ini" in extensionTarget : isText = True

        elif "wiki" in extensionTarget : isWiki = True

        elif "htm" in extensionTarget : isHtml = True

        elif "bib" in extensionTarget : isBib = True

        elif "csv" in extensionTarget : isData = True

        elif "tsv" in extensionTarget : isData = True

        # cannot be converted : will be copied directly
        
        else : return False

        # changes directory ( for file expansion )

        directory = utilities.pathDirectory( self.targetPath )

        utilities.directoryCreate( directory )

        previousDirectory = utilities.currentDirectory()

        if not directory == previousDirectory : utilities.gotoDirectory( directory )

        if isText :
            
            self.targetText = wiki.listToAscii(
                self.textList,
                self.stateList,
                self.targetPath,
                split = True,
                copy = copy
                )

        elif isWiki :

            self.targetText = wiki.listToAscii(
                self.textList,
                self.stateList,
                self.targetPath,
                split = False,
                copy = copy
                )

            
        elif isHtml :

            self.targetText = html.listToHtml(
                self.textList,
                self.stateList,
                self.targetPath,
                copy = copy
                )

        elif isBib :

            self.targetText = bibFile.listToAscii(
                self.textList,
                self.stateList,
                )
            
        elif isData :

            self.targetText = self.listToFormData(
                self.textList,
                self.stateList,
                )
            
            
        ok = utilities.fileWrite( self.targetPath, self.targetText )


        # back to original directory

        if not previousDirectory == directory : utilities.gotoDirectory( previousDirectory )

        return True # not OK, must indicate that something was done


        
        

        


# -----------------------------------
# creates the global singleton object if not already here
#

if not "converter" in globals() : converter = Converter()
         
        

