
""" Utilities for wiki text format

    See on wikipedia for information on  Wiki format
   
 
    """


from api.Utilities import *


class Wiki :
    
    """ Utilities for wiki text format

        See on wikipedia for information on  Wiki format

        """

    

    # bold and bold + italic

    boldCode = "'''"

    boldItalicCode = "''''"

    # end of link definitiopn

    closeLinkCode = "]"

    # list of format tags (codes)

    codeStartList = None

    # list of format tags (codes)

    codeStopList = None

    # code for subform

    formCode = "form"

    # list of formats ( identifiers )

    formatList = None

    # main heading
    
    headingCode = "=="

    # insert horizontal line
    
    horizontalLineCode = "----"

    # extensions recognized as images

    imageExtensionList = [
        "bmp",
        "gif",
        "jpg",
        "png",
        "tif",
        "tiff"
        ]

    # keyword to include a form / printable subdocument

    includeCode = "include"
    
    # index of current subform

    indexForm = None

    # index of formatted zone, during parsing ( a string line.column )

    indexFormat = None

    # italics
    
    italicCode = "''"

    # levels of heading subheadings etc.

    heading2Code = "==="

    heading3Code = "===="

    heading4Code = "====="

    heading5Code = "======"

    # end of line

    newLineCode = "\n"

    # tag 'notes' for subforms

    notesCode = "notes"
    
    # tag to set the required rights  for links

    noRightsStartCode = "<norights"

    # tag to set the required rights  for links

    noRightsStopCode = "</norights>"

    # tag for suspending wiki syntax analysis

    noWikiStartCode = "<nowiki>"

    # tags for resuming wiki syntax analysis

    noWikiStopCode = "</nowiki>"

    # starts a link

    openLinkCode = "["

    # printable subdocument

    printCode = "print"
    
    # tags to manage required rights

    rightsCloseCode = ">"

    rightsStartCode = "<rights"

    rightsStopCode = "</rights>"

    # code for text subdocument

    viewCode = "view"

    # fields (xwiki format) - prefixes recognized as fields in links

    widgetPrefixList = [
##        "box",          # sub-box, containing anything else
        "button",       # simple button, pressure is detected by .pressed() method
        "check",        # check box with 2 options, ok or error
##        "choice",       # box containing choices or radio buttons
        "directory",    # box containing one directory
        "entry",        # a text entry, one line. Free entry, with eventually a popup list
        "file",         # a text box to open a file
        "float",        # float number entry
        "image",        # box with image and link
        "integer",      # integer number entry
        "label",        # simple text
        "level",        # VAS done with characters
        "menu",         # text selected from popup list
        "password",     # password entry
        "path",         # path selector with popup browser
        "progress",     # progress bar
        "radio",        # radio button
        "scale",        # slider, 0-100
        "text",         # text window with scroll bar
        "tooltip",      # tooltip label       
        ]
        



    def __init__ ( self ) :

        """ Constructor. Does absolutely nothing
           
            """


        self.initLists()



        
        
    def appendText (

        self,
        lineList = None,
        stateList = None,
        text = None,
        state = None,
        new = None
        ) :

        """ appends a text to a list of lines.

            If no change in state, appends to last line otherwise create new line

            If new is True, always appends a new line
            
            """

        # lists of texts and states are indefined
        
        if ( ( not type( lineList ) == list ) or ( not type( stateList ) == list ) ) : return False

##        # removes tags, crlf and rigth spaces
##        
##        text = self.removeTags( text ).replace( "\n", " " )

        # except for forced fields, does not add empty fields
        
        if ( ( utilities.isEmpty( text ) ) and ( not bool( new ) ) ) : return False

        # empty lists or change of state, or new is forced
        
        if ( ( bool( new ) ) or
             ( utilities.isEmpty( lineList ) ) or
             ( utilities.isEmpty( stateList ) ) or
             ( not stateList[ -1 ] == state )
             ) :
            

            stateList.append( state )

            lineList.append( text )

        # same state than last line : appends text to last line

        else :

            lineList[ -1 ] = lineList[ -1 ] + text


        return True




    def asciiToList (

        self,
        text = None,
        path = None
        ) :

        """ converts a wiki text into 2 lists of text + state """


        if utilities.isEmpty( text ) : return None, None

        # normalizes the new lines ( remove additional "-" )

        text = self.normalizeHorizontalLines( text )
        
        # normalizes the titles( remove additional "-" )

        text = self.normalizeTitles( text )

        

        size = len( text )
        
        iStart = 0

        iTag = 0

        lineList = [ ]

        tagList = [ ]

        if utilities.isEmpty( path ) : directory = ""

        else : directory = utilities.pathDirectory( path )

        while iStart < size :

            # looks for next tag
            
            tag = None

            for iTag in range( iStart, size ) :

                iClose, tag = self.getTag( text, iTag )

                if not tag is None : break

##            print "wiki.asciitoList", utilities.pathName( path ), tag, iTag, iClose, text[ iTag : iTag + 20 ]

            # no more tags : appends final normal text

            if tag is None :
                
                self.appendText( lineList, tagList, text[ iStart : ], None )

                break

            # appends the normal text that is before the tag
            
            if iTag > iStart :

                self.appendText( lineList, tagList, text[ iStart : iTag ], None )

                iStart = iTag


            # no wiki

            if tag == "nowiki" :

                iClose = text.find( self.noWikiStopCode, iTag )

                if iClose < 0 : iClose = size

                else : iClose = iClose + len( self.noWikiStopCode )
                
                self.appendText( lineList, tagList, text[ iStart : iClose ], "special" )
                    

            # x-wiki tag, copied as it

            elif tag == "special" :
                
                iClose = text.find( ">", iTag )

                if iClose < 0 : iClose = size

                else : iClose = iClose + 1
                
                self.appendText( lineList, tagList, text[ iTag : iClose ], "special" )

            # horizontal line

            elif tag == "horizontal" :

                self.appendText( lineList, tagList, " ", "horizontal", new = True )

            # new line

            elif tag == "line" :

                self.appendText( lineList, tagList, " ", "line", new = True )

            # bold + italic

            elif tag == "boldItalic" :
                
                iClose, field = self.textBetweenTags( text, iTag, self.boldItalicCode ) 

                self.appendText( lineList, tagList, field, tag )

            # bold

            elif tag == "bold" :
                
                iClose, field = self.textBetweenTags( text, iTag, self.boldCode ) 

                self.appendText( lineList, tagList, field, tag )
                                   
            # italic

            elif tag == "italic" :
                
                iClose, field = self.textBetweenTags( text, iTag, self.italicCode ) 

                self.appendText( lineList, tagList, field, tag )
                    
            # titles start and stop

            elif "heading" in tag :

                iClose, field, level = self.parseTitle( text, iTag )

                self.appendText( lineList, tagList, field, tag )

            # link

            elif tag == "link" :

                iClose, link, label = self.getLink( text, iTag )

                if utilities.isEmpty( link ) :

                    iStart = max( iClose, iStart + 1 )

                    continue

##                print "wiki.asciitolist getlibk", iClose, link, label

                # field of the form type | or type dimensions |

                if " " in link : prefix, dummy = link.split( " ", 1 )

                else : prefix = link

                prefix = prefix.strip().lower()               

                isUrl = utilities.isUrl( link )

                isWidget = prefix in self.widgetPrefixList

                isImage = utilities.pathExtension( link ).lower() in self.imageExtensionList

                if isUrl : None

                elif isWidget : None

                elif link.startswith( utilities.fileHeader ) : link = utilities.normalizePath( link, normalize = False )

                elif utilities.isAbsolutePath( link ) : link = utilities.normalizePath( link, normalize = False )

                else : link = utilities.normalizePath( directory + link, normalize = False )

                line = link + utilities.featureDelimiter + label

                # url : appends link
                
                if isUrl : self.appendText( lineList, tagList, line, "link", new = True )

                # widget : appends widget

                elif isWidget : self.appendText( lineList, tagList, line, "widget", new = True )
        
                # image : appends image

                elif isImage : self.appendText( lineList, tagList, line, "image", new = True )

                # any other case : appends link

                else : self.appendText( lineList, tagList, line, "link", new = True )


            # skips the tag

            iStart = max( iClose, iStart + 1 )

        return lineList, tagList




    def expand (

        self,
        text = None,
        instantiate = None,
        ) :

        """ expands the links to text files. If they contain wiki syntax, increases level of headings and titles

            if 'instantiate', variables are instantiated before and after expansion
            
            """

##        print "wikiexpand"

        if utilities.isEmpty( text ) : return ""

        result = ""

        level = 0

        index = 0

        iStart = 0

        self.indexForm = 1

        size = len( text )

        while index < size :

            # there is a heading: adjusts the level

            next, title, newLevel = self.parseTitle( text, index )

            if next > index :

                index = next

                level = newLevel

                continue


##            # there is a link ?
##
##            iLink, address, description = self.getLink( text, index )
##
##            # otherwise, there is a reference to a subform ?
##
##            isLink = ( iLink > index )
##
##            if isLink :
##
##                isForm = False
##
##            else :
##                
##                iLink, address, description = self.getForm( text, index )
##
##                isForm = ( iLink > index )
##
##
##            # no link, no form
##            
##            if ( ( not isLink ) and ( not isForm ) ) :
##
##                index = index + 1
##
##                continue

            iLink, address, description = self.getInclude( text, index )

            if iLink < 0 :

                index = index + 1

                continue

            # adds the text that was before the include

            if bool( instantiate ) : result = result + utilities.instantiate( text[ iStart : index ], default = "_" )

            else : result = result + text[ iStart : index ]

            iStart = iLink

            index = iLink
            
            # inserts tag with origin of expansion

            separator = self.horizontalLineCode

            if result.endswith( separator + "\n" ) : result = result + description + "\n"

            elif result.endswith( separator ) : result = result + "\n" + description + "\n"

            else : result = result + "\n" + separator + "\n" + description + "\n"

            # gets the text to include, increases level of titles and expands recursively

            path = utilities.normalizePath( utilities.instantiate( address ), normalize = False )

            inclusion = utilities.fileRead( path ).replace( "\r", "" )  # to remove invalid EOL

            if bool( instantiate ) : inclusion = utilities.instantiate( inclusion, default = "_" )

            inclusion = self.increaseLevel( inclusion, level )

            inclusion = self.expand( inclusion, instantiate )

            # adds to result
            
            result = result + inclusion + "\n"

            if utilities.startswith( text, separator + "\n" + separator, iStart ) : None

            elif utilities.startswith( text, separator, iStart ) : result = result + separator + "\n"

            else : result = result + separator + "\n" + separator + "\n"

            # increments index of subform WARNING: does not work with recursive subforms

            self.indexForm = self.indexForm + 1


        # adds end of text

        if bool( instantiate ) :

            result = result + utilities.instantiate( text[ iStart : ], default = "_" )

        else :

            result = result + text[ iStart : ]

        return result
            





    def getInclude (

        self,
        text = None,
        position = None
        ) :

        """ parses a reference to a form (subdocument, horizontal line + form definition and returns the position after the closing ] a link and a text, or -1 None

           
            """


        """ parses a link to a form, defined after a horizontal line """

        # horizontal line

        if not utilities.startswith( text, self.horizontalLineCode, position ) : return -1, None, None
        
        # end of the horizontal line
        
        iStart = text.find( "\n", position )

        if iStart < 0 : return -1, None, None

        # next line must start with 'print' or 'form'

        iStart = iStart + 1       

        # next horizontal line

        iEnd = text.find( "\n", iStart )
        
        if iEnd <= iStart : iEnd = len( text )

        if iEnd <= iStart : return -1, None, None

        # parses the next line must contain 'print' or 'form'

        address, description = self.parseInclude(
            text[ iStart : iEnd ],
            include = True
            )

        if address is None : return -1, None, None

        return iEnd + 1, address, description


        

    def getLink (

        self,
        text = None,
        position = None
        ) :

        """ parses a link [... ] and returns the position after the closing ] a link and a text, or -1 None

            accepts space as internal separator if cannot find a |
            
            """

        position = self.parseOpenLink( text, position )

        if position < 0 : return -1, None, None

##        print "wiki.getlink", position, text[ position : position + 32 ],

        # looks for a closing ]
        
        position, text = self.textBeforeTag( text, position, self.closeLinkCode )

        if position < 0 : return -1, None, None

        text = text.strip( " |" )

        link = ""

        
        # parses the content of the link

        if utilities.isEmpty( text ) :

            link = ""

            text = ""

        # starts with a quote ( delimits the path )

        elif text[ 0 ] == '"' :

            iLink = text.find( '"', 1 )

            if iLink >= 0 :

                link = text[ : iLink ]

                text = text[ iLink : ]

        # simple quote
        
        elif text[ 0 ] == "'" :

            iLink = text.find( "'", 1 )

            if iLink >= 0 :

                link = text[ : iLink ]

                text = text[ iLink : ]
            

        # no quote: searches the separator | or by default, a space
        
        else :

            iLink = text.find( utilities.featureDelimiter )

            if iLink >= 0 :

                link = text[ : iLink ]

                text = text[ iLink : ]

        link = link.strip( " \"'|" )
        
        text = text.strip( " \"'|" )

        if utilities.isEmpty( link ) :

            link = text

            text = ""



        # the link is composed of an URL + something else

        words = link.split()

##        print "->", position, "text",text,"link", link, "words", words

        if ( ( len( words ) > 1 ) and ( utilities.isUrl( words[ 0 ] ) ) ) :

             endLink = link[ len( words[ 0 ] ) : ].strip()

             if text == link : text = endLink

             else : text = endLink + " " + text

             link = words[ 0 ]


        return position, link, text



    def getNoRights (

        self,
        text = None,
        position = None
        ) :

        """ parses a tag <no rights, returns the position after the closing > and a text, or -1 None """

        position = self.parseNoRightsStart( text, position )

        # looks for a closing >

        return self.textBeforeTag( text, position, self.rightsCloseCode )





    def getRights (

        self,
        text = None,
        position = None
        ) :

        """ parses a tag <rights, returns the position after the closing > and a text, or -1 None """

        position = self.parseRightsStart( text, position )

        # looks for a closing >

        return self.textBeforeTag( text, position, self.rightsCloseCode )



    def getTag (

        self,
        text = None,
        position = None,
        ) :

        """ searches a tag in text, at the given position.

            uses self.tagList to recognize valid tags.

            if strip is true, finds the next "<" in the text otherwise searches here.

            returns a pair, position after the tag and  state corresponding to the tag ( self.stateList )

            """

        position = utilities.integer( position, default = 0 )

        if not utilities.isIndex( position, text ) : return -1, None

        # prefiltering

        if ( ( not text[ position ] == "=" ) and
             ( not text[ position ] == "'" ) and
             ( not text[ position ] == "<" ) and
             ( not text[ position ] == "[" ) and             
             ( not text[ position ] == "-" ) and
             ( not text[ position ] == "\n" )
             ) :

            return -1, None             

        # start tags

        found = None

        for index in range( len( self.tagList ) ) :

            tag = self.tagList[ index ]

            if text.startswith( tag, position ) : 

                found = self.stateList[ index ]

                iClose = position + len( tag )
               
                return iClose, found

        return -1, None

    

    
    def image (

        self,
        address = None,
        description = None,
        local = None,
        copy = None,
        ) :

        """ returns the text of a x-wiki link address / description and a local directory to copy the files """

        return self.link(
            address = address,
            description = description,
            local = local,
            copy = copy
            )






    def increaseLevel (

        self,
        text = None,
        level = None
        ) :

        """ increases the level of the titles """

        if utilities.isEmpty( text ) : return ""

        level = utilities.integer( level, default = 0 )

        if level <= 0 : return text

        # prepares new tags for headings, adding "=" to increment the level

        tagSize = len( self.heading5Code )
      
        heading4Code = min( tagSize, len( self.heading4Code ) + level ) * "."

        heading3Code = min( tagSize, len( self.heading3Code ) + level ) * "."

        heading2Code = min( tagSize, len( self.heading2Code ) + level ) * "."

        headingCode = min( tagSize, len( self.headingCode ) + level ) * "."

        result = ""

        iStart = 0

        index = 0

        size = len( text )

        while index < size :

            next, title, titleLevel = self.parseTitle( text, index )


            if next > index :

                titleLevel = min( titleLevel + level, len( self.heading4Code ) )

                result = result + text[ iStart : index ] + titleLevel * "=" + title + titleLevel * "="

                index = next

                iStart = next

                continue

            index = index + 1

        result = result + text[ iStart : ]

        return result


        

    def initLists ( self ) :

        """ creates the lists of codes """


        self.formatList = [
            "heading5",
            "heading4",
            "heading3",
            "heading2",
            "heading",
            "boldItalic",
            "bold",
            "italic"
            ]
            
            
        self.headingCodeList = [
            self.headingCode,
            self.heading2Code,
            self.heading3Code,
            self.heading4Code,
            self.heading5Code,
            ]


        self.codeStartList = [
            self.heading5Code,
            self.heading4Code,
            self.heading3Code,
            self.heading2Code,
            self.headingCode,
            self.boldItalicCode,
            self.boldCode,
            self.italicCode,
            ]


        self.codeStopList = [
            self.heading5Code,
            self.heading4Code,
            self.heading3Code,
            self.heading2Code,
            self.headingCode,
            self.boldItalicCode,
            self.boldCode,
            self.italicCode,
            ]

        self.tagList = [
            self.heading5Code,
            self.heading4Code,
            self.heading3Code,
            self.heading2Code,
            self.headingCode,
            self.boldItalicCode,
            self.boldCode,
            self.italicCode,
            self.horizontalLineCode,
            self.newLineCode,
            self.openLinkCode,
            self.noWikiStartCode,
            self.rightsStartCode,
            self.noRightsStartCode,
            self.rightsStopCode,
            self.noRightsStopCode,
            ]

        self.stateList = [
            "heading5",
            "heading4",
            "heading3",
            "heading2",
            "heading",
            "boldItalic",
            "bold",
            "italic",
            "horizontal",
            "line",
            "link",
            "nowiki",
            "special",
            "special",
            "special",
            "special",
            "special",
            "special"
            ]
            
            
            

    
        
    def link (

        self,
        address = None,
        description = None,
        local = None,
        copy = True
        ) :

        """ returns the text of a x-wiki link address / description and a local directory to copy the files """

        address = utilities.string( address, default = "" )

        addressPath = utilities.normalizePath( utilities.instantiate( address, default = "_" ), normalize = False )

        description = utilities.string( description, default = "" )

        if local is None : local = utilities.currentDirectory()

        description = description.replace( '"', ' ' ).replace( "'", " " )

##        print "wiki.link", address, "local", local,
        
        if ( ( bool( copy ) ) and
             ( not utilities.isUrl( addressPath ) ) and
             ( not utilities.isEmpty( local ) ) and
             ( not addressPath.startswith( local ) )
             ):

            target = local + utilities.pathLastNameWithExtension( addressPath )

            utilities.pathCopy( addressPath, target )

            address = target

##        print "new address", address

        return self.openLinkCode + address + utilities.featureDelimiter + description + self.closeLinkCode

        

                

    def listToAscii (

        self,
        textList = None,
        stateList = None,
        path = None,
        split = None,
        copy = None,
        ) :

        """ converts a pair of lists text + state into a flat html text """
               
        
        if utilities.isEmpty( textList ) : return ""

        if utilities.isEmpty( stateList ) : return ""

        if utilities.isEmpty( path ) : local = None

        else : local = utilities.localDirectory( path )

        size = min( len( textList ), len( stateList ) )

        body = ""

        iField = 0

        indexForm = 1

        checkInclude = False

##        print "wiki.listToAscii"

        while iField < size :

            state = stateList[ iField ]

            text = textList[ iField ].rstrip()

            # ends with a space or a line (used to insert separating spaces)

            spaceFlag = body.endswith( " " )

            lineFlag = body.endswith( self.newLineCode )

##            print "  ", state, text, iField

            iField = iField + 1

            # checks for definition of a subdocument

            if checkInclude :  address, description = self.parseInclude( text, index = indexForm )

            else : address = None


            # looks for a double horizontal line, and includes
            
            if not address is None :

##                print "parseInclude", address, description

                for iClose in range( iField, size ) :

                    if size - iField < 4 : continue

                    if not stateList[ iClose ] == "horizontal" : continue

                    if not stateList[ iClose + 1 ] == "line" : continue

                    if not stateList[ iClose + 2 ] == "horizontal" : continue

                    if not stateList[ iClose + 3 ] == "line" : continue

                    break


                # no path to copy subfiles or ...

                addressPath = utilities.normalizePath( address, normalize = False )

                if local is None : copyPath = None

                else : copyPath = addressPath

                text = self.listToAscii(
                    textList[ iField : iClose ],
                    stateList[ iField : iClose ],
                    path = copyPath,
                    split = False,
                    copy = copy
                    )

                utilities.fileWrite( addressPath, text )

                body = body + \
                       self.includeCode + \
                       " " + \
                       utilities.pathLastNameWithoutExtension( address ).replace( "_", " " ) + \
                       self.newLineCode

                indexForm = indexForm + 1
                
                iField = iClose + 2
       

            # nothing special, appends text, separates with space if needed
            
            elif state is None :

                if ( ( lineFlag ) or ( spaceFlag ) ) : body = body + text

                else : body = body + " " + text

            elif state == "line" :

                if spaceFlag : body = body.rstrip() + self.newLineCode

                else : body = body + self.newLineCode


            # horizontal line : if split mode, will check next line for definition of a subdocument
            
            elif state == "horizontal" :

                if spaceFlag : body = body.rstrip() + self.horizontalLineCode

                else : body = body + self.horizontalLineCode

            elif state.startswith( "heading" ) :

                level = utilities.integer( state[ len( "heading" ) : ], default = 1 )

                if utilities.isIndex( level - 1, self.headingCodeList ) :

                    tag = self.headingCodeList[ level - 1 ]

                    if not lineFlag : body = body.rstrip() + self.newLineCode + tag + text + tag

                    else : body = body + tag + text + tag

            elif state == "bold" :

                if ( ( lineFlag ) or ( spaceFlag ) ) : body = body + self.boldCode + text + self.boldCode

                else : body = body + " " + self.boldCode + text + self.boldCode


            elif state == "italic" :

                if ( ( lineFlag ) or ( spaceFlag ) ) : body = body + self.italicCode + text + self.italicCode

                else : body = body + " " + self.italicCode + text + self.italicCode

                
            elif state == "boldItalic" :

                if ( ( lineFlag ) or ( spaceFlag ) ) : body = body + self.boldItalicCode + text + self.boldItalicCode

                else : body = body + " " + self.boldItalicCode + text + self.boldItalicCode


            elif state == "link" :

                if utilities.featureDelimiter in text :

                    address, description = text.split( utilities.featureDelimiter, 1 )

                else :

                    address = text

                    description = ""

                if lineFlag : body = body + self.link( address, description, local, copy )

                else : body = body.strip() + self.newLineCode + self.link( address, description, local, copy )


            elif state == "image" :

                if utilities.featureDelimiter in text :

                    address, description = text.split( utilities.featureDelimiter, 1 )

                else :

                    address = text

                    description = ""

                if lineFlag : body = body + self.image( address, description, local, copy )

                else : body = body.strip() + self.newLineCode + self.image( address, description, local, copy )


            # widget : treated like a link

            elif state == "widget" :

                if lineFlag : body = body + self.widget( text )

                else : body = body.strip() + self.newLineCode + self.widget( text )

                body = body + self.widget( text )

            # wiki tag: added to text, no modification
            
            elif state == "special" :

                body = body + text # + self.newLineCode

            # unknown tag, e.g., html : skips
            
            else :

                None
                

            # updates flag to check inclusions

            if state == "horizontal" : checkInclude = bool( split )

            elif not state == "line" : checkInclude = False

        return body





    def normalize (

        self,
        text = None
        ) :

        """ normalizes a wiki text, i.e.,
            1 - expands links to text files (increases the level of subtitles if needed )
            2 - normalize remaining links to standard wiki syntax

            """

        textList = self.split( text )

        if utilities.isEmpty( textList ) : return ""

        result = ""
        
        for text in textList :

            if text.startswith( wiki.noWikiStartCode ) : result = result + text[ len( wiki.noWikiStartCode ) : ]

            else : result = result + self.asciiToWiki( text )

        return result

            

    def normalizeHeadingSpaces (

        self,
        text = None
        ) :

        """ replaces heading spaces by a dot to avoid creation of boxes """


        if utilities.isEmpty( text ) : return ""

        # first heading space

        if text.startswith( " " ) : text = "." + text[ 1 : ]

        # line return followes by heading space
        
        index = 0

        while True :

            index = text.find( "\n ", index )

            if index < 0 : break

            text = text.replace( "\n ", "\n." )

        return text
            
            
        
    def normalizeHorizontalLines (

        self,
        text = None
        ) :

        """ normalizes the horizontal lines that have too many "-" """

        if utilities.isEmpty( text ) : return ""

        index = 0

        while True :

            index = text.find( self.horizontalLineCode + "-", index )

            if index < 0 : break

            text = text.replace( self.horizontalLineCode + "-", self.horizontalLineCode )

        index = 0

        while True :

            index = text.find( " " + self.horizontalLineCode, index )

            if index < 0 : break

            text = text.replace( " " + self.horizontalLineCode, self.horizontalLineCode )
            
        return text





    def normalizeTitles (

        self,
        text = None
        ) :

        """ normalizes the titles, i.e., removes spaces in titles of any level """

        if utilities.isEmpty( text ) : return ""

        index = 0

        while True :

            index = text.find( self.headingCode + " ", index )

            if index < 0 : break

            text = text.replace( self.headingCode + " ", self.headingCode )

        index = 0

        while True :

            index = text.find( " " + self.headingCode, index )

            if index < 0 : break

            text = text.replace( " " + self.headingCode, self.headingCode )

        while True :

            index = text.find( "=" + self.heading5Code, index )

            if index < 0 : break

            text = text.replace( "=" + self.heading5Code, self.heading5Code )

            
        return text





    def parseHorizontalLine (

        self,
        text = None,
        position = None
        ) :

        """ parses a tag 'horizontal line' and returns the index after the tag, or -1

            horizontal line starts with spaces then there is one tag

            """

        return self.parseTag(
            text = text,
            position = position,
            tag = self.horizontalLineCode,
            strip = True
            )
    






    def parseInclude (

        self,
        text = None,
        index = None,
        include = False
        ) :

        """ parses a reference to a form (subdocument, horizontal line + form definition and returns the position after the closing ] a link and a text, or -1 None

            """


        """ parses a link to a form, defined after a horizontal line """

        text = text.lower()

        words = text.split()

        if len( words ) < 1 : return None, None


        # this is an inclusion (a line : include form xxx )
        
        if bool( include ) :

            if not words[ 0 ] == self.includeCode : return None, None

            if len( words ) < 3 : return None, None

            name = words[ 1 ]

            # index of file must be numerical

            index = words[ 2 ]

            if utilities.integer( index ) is None : return None, None

            # remainder of properties

            remainder = words[ 3 : ]
            
        # this is not an inclusion skips prefix 'include'

        elif words[ 0 ] == self.includeCode :

            if len( words ) < 2 : return None, None

            name = words[ 1 ]

            if index is None : index = self.indexForm

            index = utilities.string( index, default = 0 ).rjust( 2, '0' )

            remainder = words[ 2 : ]

        else :

            name = words[ 0 ]

            if index is None : index = self.indexForm

            index = utilities.string( index, default = "0" ).rjust( 2, '0' )

            remainder = words[ 1 : ]

        # type of inclusion

        if not name in [ self.viewCode, self.printCode, self.formCode ] : return None, None

        if not name == self.printCode : remainder.sort()

        description = name + " " + utilities.wordsToText( remainder )

        address = name + "_" + index + "_" + utilities.wordsToText( remainder, "_" ) + ".txt"

        address = address.strip( "_" ).replace( "__", "_" )

        return address, description


        
        
    def parseNoRightsStart (

        self,
        text = None,
        position = None
        ) :

        """ parses a tag no rights and returns the index after the tag, or -1

            """

        return self.parseTag(
            text = text,
            position = position,
            tag = self.noRightsStartCode,
            strip = False
            )


    def parseNoRightsStop (

        self,
        text = None,
        position = None
        ) :

        """ parses a tag end of NO rights and returns the index after the tag, or -1

            """

        return self.parseTag(
            text = text,
            position = position,
            tag = self.noRightsStopCode,
            strip = False
            )



    def parseNoWikiStart (

        self,
        text = None,
        position = None
        ) :

        """ parses a tag NOWIKI and returns the index after the tag, or -1

            """

        return self.parseTag(
            text = text,
            position = position,
            tag = self.noWikiStartCode,
            strip = False
            )

        

    def parseNoWikiStop (

        self,
        text = None,
        position = None
        ) :

        """ parses a tag end of NOWIKI and returns the index after the tag, or -1

            """

        return self.parseTag(
            text = text,
            position = position,
            tag = self.noWikiStopCode,
            strip = False
            )
        

    

    def parseOpenLink (

        self,
        text = None,
        position = None
        ) :

        """ parses an open link tag and returns the index after the tag, or -1

            """

        return self.parseTag(
            text = text,
            position = position,
            tag = self.openLinkCode,
            strip = False
            )
    


    def parseRightsStart (

        self,
        text = None,
        position = None
        ) :

        """ parses a tag rights and returns the index after the tag, or -1

            """

        return self.parseTag(
            text = text,
            position = position,
            tag = self.rightsStartCode,
            strip = False
            )

    


    def parseRightsStop (

        self,
        text = None,
        position = None
        ) :

        """ parses a tag end of rights and returns the index after the tag, or -1

            """

        return self.parseTag(
            text = text,
            position = position,
            tag = self.rightsStopCode,
            strip = False
            )



    def parseTag (

        self,
        text = None,
        position = None,
        tag = None,
        strip = None
        ) :

        """ parses a wiki tag in text, at the given position and returns the position after the tag or -1

            if strip is true, verifies that before the tag, the text only contains spaces

            """

        if utilities.isEmpty( tag ) : return -1
        
        position = utilities.integer( position, default = 0 )

        # not found in this position
        
        if not utilities.startswith( text, tag, position ) : return -1


        # before the tag, there must only be spaces
        
        if ( ( bool( strip ) ) and ( not text[ : position ].strip() == "" ) ) : return -1

        return position + len( tag )
        



    def parseTitle (

        self,
        text = None,
        position = None,
        strip = None
        ) :

        """ parses a wiki tag indicating a title in text, at the given position

            returns a pair = position after the tag, title and level  or -1, None, None

            if strip is true, verifies that before the tag, the text only contains spaces

            """

        iLevel, title = self.textBetweenTags( text, position, self.heading5Code, strip )

        if iLevel >= 0 : return iLevel, title, 5

        iLevel, title = self.textBetweenTags( text, position, self.heading4Code, strip )

        if iLevel >= 0 : return iLevel, title, 4

        iLevel, title = self.textBetweenTags( text, position, self.heading3Code, strip )

        if iLevel >= 0 : return iLevel, title, 3

        iLevel, title = self.textBetweenTags( text, position, self.heading2Code, strip )

        if iLevel >= 0 : return iLevel, title, 2

        iLevel, title = self.textBetweenTags( text, position, self.headingCode, strip )

        if iLevel >= 0 : return iLevel, title, 1

        return -1, None, None
    





    def removeRights (

        self,
        text = None
        ) :

        """ removes the tags with access rights """

        if utilities.isEmpty( text ) : return ""

        text = text.replace( self.rightsStopCode, "" ).replace( self.noRightsStopCode, "" )

        while True :

            iStart = text.find( self.rightsStartCode )

            if iStart < 0 : break

            iStop = text.find( self.rightsCloseCode, iStart )

            if iStop < 0 : break

            text = text[ : iStart ] + text[ iStop + len( self.rightsCloseCode ) : ]

        while True :

            iStart = text.find( self.noRightsStartCode )

            if iStart < 0 : break

            iStop = text.find( self.rightsCloseCode, iStart )

            if iStop < 0 : break

            text = text[ : iStart ] + text[ iStop + len( self.rightsCloseCode ) : ]

        return text



    def split (

        self,
        text = None,
        normalize = False
        ) :

        """ splits the text according to <nowiki> tags,

            returns a list of text chunks. Those that must not be parsed  are enclosed in <nowiki>, </nowiki>

            """

        if utilities.isEmpty( text ) : return [ ]

        textList = [ ]

        iStart = 0

        while True :

            iStop = text.find( self.noWikiStartCode, iStart )

            # no more tag <nowiki>

            if iStop < 0 :

                if bool( normalize ) : textList.append( self.asciiToWiki( text[ iStart : ] ) )

                else : textList.append( text[ iStart : ] )

                break

            # there is a tag <nowiki> parses until this tag

            if bool( normalize ) : textList.append( self.asciiToWiki( text[ iStart : iStop ] ) )

            else : textList.append( text[ iStart : iStop ] )

            iStop = iStop + len( self.noWikiStartCode )

            iStart = text.find( self.noWikiStopCode, iStop )

            if iStart < 0 :

                textList.append( self.noWikiStartCode + text[ iStop : ] + self.noWikiStopCode )

                break

            textList.append( self.noWikiStartCode + text[ iStop : iStart ]  + self.noWikiStopCode )

            iStart = iStart + len( wiki.noWikiStopCode )

        return textList




    def asciiToWiki (

        self,
        text = None
        ) :

        """ converts to standard wiki format. EXCEPT for links """

        if utilities.isEmpty( text ) : return ""

        # removes the special tags rights/ norights

        text = self.removeRights( text )

        # normalizes the new lines ( remove additional "-" )

        text = self.normalizeHorizontalLines( text )
        
        # normalizes the titles( remove additional "-" )

        text = self.normalizeTitles( text )
        
        return text
        


        
    def textBeforeTag (

        self,
        text = None,
        position = None,
        tag = None
        ) :

        """ gets the text before some tag and returns the position after the tag of -1 None """

        
        if ( ( text is None ) or ( position < 0 ) ) : return -1, None

        if utilities.isEmpty( tag ) : return -1, None

        iEnd = text.find( tag, position  )

        if iEnd < 0 : return -1, None

        return iEnd + len( tag ), text[ position : iEnd ]




    def textBetweenTags (

        self,
        text = None,
        position = None,
        tag = None,
        strip = None
        ) :

        """ gets the text between 2 identical tags and returns position after closing tag and text, or -1 None """

        position = self.parseTag(
            text = text,
            position = position,
            tag = tag,
            strip = strip
            )

        if position < 0 : return -1, None

        iEnd = text.find( tag, position  )

        if iEnd < 0 : return -1, None

        return iEnd + len( tag ), text[ position : iEnd ]



    def widget (

        self,
        text = None,
        ) :

        """ returns the text of a x-wiki widget """

        if utilities.isEmpty( text ) : return ""

        indexBar = text.find( utilities.featureDelimiter )

        if indexBar < 0 : return ""

        category = text[ : indexBar ].strip()

        definition = text[ indexBar : ].strip()

        return self.openLinkCode + category + definition + self.closeLinkCode




# -----------------------------------
# creates the global singleton object if not already here
#

if not "wiki" in globals() : wiki = Wiki()
         
        

