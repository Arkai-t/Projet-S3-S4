
""" HTML format manager.

    See on wikipedia for information on HTML format
   
 
    """


from api.Utilities import *



class Html :
    
    """ HTML format manager

        Current version HTML 4.01 transitional

        See on wikipedia for information on HTML format

        Elements accepted here (remainder is filtered)

        <head>
            <DOCTYPE>
            <title>
        <body>
            <hr with attribute style
            <label>xxx<input ></label> (only with one field inside)
                <input with attributes value, type (widget)

        Elements converted (normalized to presentation markers, remainder ignored)
        
            <big> 
            <small>
            <tt> (teletype-like)
            <strike>
            <div style...
            <span style...
            <p style...
            

            <abbr> italics
            <acronym>  italics
            <cite> italics
            <em> italics
            <code> teletype
            <kbd> teletype
            <strong> bold
            <var> italics
            <ins> italics
            <samp> teletype
            <var> italics

        Elements accepted without conversion in <body>
            <h1>..<h6>
            <i>
            <b>
            <u>
            <s>

            <br>

        Elements accepted, simplified
            <a with attribute href (link)
            <hr : horizontal line, normalized to 2 pixels
            <img with attributes alt src (image)


        Elements filtered: tag removed, content inserted in body
            <isindex>
            <noscript>
            <noframes>


        Elements ignored: tag inserted, content parsed
            <address>
            <blockquote>
            <center>

            <dir>
            <dl>
            <dt>
            <dd>
            <li>
            <menu>
            <ol>
            <ul>
            
            <form>
            
            <table>
            <caption>
            <colgroup>
            <col>
            <thead>
            <tfoot>
            <tbody>
            
            <frame>
            <frameset>
            <q>
            <iframe>

            <bdo> (direction of writing)
            

        Elements ignored completely: tag & content inserted but not parsed (there may be several lines)

            <applet>
            <del>
            <map>
            <object>
            <script>
            <sub>
            <sup>
            

            <button>
            <fillset>
            <legend>
            <select>
            <optgroup>
            <option>
            <textarea>

            <iframe>
            <noframes>
            

        Elements ignored completely, tag inserted (there is no content)
            <param>
            <col>
            
            
            <area>


        Misc

            <pre>
            <tr>

        Elements used for generation
        <html>
        <header>
            <meta>
            <title>
        <body>

        <b>
        <u>
        <i>
        <s>
        <tt>
        <small>
        <big>

        <label>
        <input>
        
        

       
     
        """

    # field of tag

    altCode = "alt"

    # tag

    bigCode = "big"

    # tag

    bodyCode = "body"

    # tag

    boldItalicCode = 'span style="font-weight: bold;font-style: italic"'

    # tag to parse (basic html syntax)

    boldSimpleCode = "b"

    # tag

    boldCode = 'span style="font-weight: bold;"'

    
    # table of special characters

    characterCodeList = [
        '&quot;',
        '&amp;',
        '&lt;',
        '&gt;',
        '&nbsp;',
        ]

    characterAsciiList = [

        '"',
        '&',
        '<',
        '>',
        ' ',
        ]

    # list of valod format tags( start + stop together )

    codeList = None

    # list of format tags (codes)

    codeStartList = None

    # list of format tags (codes)

    codeStopList = None

    # default values

    defaultCharset = None

    # div tag

    divCode = "div"

    # type of document

    doctype = '!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"'

    # emphasize (italics)

    emphasizeCode = "em"

    
    # list of formats ( identifiers )

    formatList = None
    
    # tag
    
    headCode = "head"

    # tag to parse (basic html syntax)

    headingCode = "h1"

    # tag to parse (basic html syntax)

    heading2Code = "h2"
    
    heading3Code = "h3"

    heading4Code = "h4"

    heading5Code = "h5"

    heading6Code = "h6"
    
    # horizontal line for recognition

    horizontalCode = "hr"

    # for generation
    
    horizontalLineCode = 'hr style="width: 100%; height: 2px;"'

    # field of address tags
    
    hrefCode = "href"


    # tag

    imageCode = 'img'


    # input field (only parsed within label)

    inputCode = "input"

        
    # tag to parse (basic html syntax)

    italicSimpleCode = "i"

    # tag

    italicCode = 'span style="font-style: italic;"'

    # label of input field

    labelCode = "label"
    
    # tag

    linkCode = "a"


    # end of line

    newLineCode = "br"

    # specific tags of wiki

    noRightsStartCode = "<norights"

    noWikiStartCode = "<nowiki>"


    # paragraph

    paragraphCode = "p"

    
    # specific tags of x-wiki

    rightsStartCode = "<rights"

    # field of tag

    selectedCode = "selected"

    # small code

    smallCode = "small"

    # SPAN tag

    spanCode = "span"


    # attribute of img tags

    srcCode = "src"

    # state ( parser automaton )

    state = None

    # strikethrough

    strikethroughCode = "s"

    # strong font (bold)

    strongCode = "strong"
    
    # attribute of tags

    styleCode = "style"

    # table , row cell

    tableRowCode = "tr"

    # spaces per tab

    tabSpace = 4

    # complete list of tag pairs. Those of HTML 4 STRICT, plus applet, iframes, frames

    tagPairList = None

    # complete list of single tags    
        
    tagSingleList = None

    # teletype font (constant spacing)

    teletypeCode = "tt"
    
    # tag
    
    titleCode = "title"
    
    # attribute of input tag

    typeCode = "type"

    # underline font

    underlineCode = "u"

    # attribute of input tag

    valueCode = "value"

    # prefixes recognized as widget fields

    widgetPrefixList = None




    def __init__ ( self ) :

        """ Constructor. 
           
            """

        # initializes special code lists
        
        self.initLists()

        # initializes codes from utilities
        
        self.defaultCharset = utilities.htmlFormat

        self.characterCodeList = [ ]

        self.characterAsciiList = [ ]

        for index in range( 0, len( utilities.htmlTable ), 2 ) :

            self.characterCodeList.append( utilities.htmlTable[ index ] )

            self.characterAsciiList.append( utilities.htmlTable[ index + 1  ] )

        






    def appendText (

        self,
        lineList = None,
        stateList = None,
        text = None,
        state = None,
        new = None,
        raw = None,
        split = None,
        margin = None
        ) :

        """ appends a text to a list of lines.

            If no change in state, appends to last line otherwise create new line

            If new is True, always appends a new line

            in any case, will split internal lines of the new text.

            If raw is true, does not normalize the text, otherwise removes the tags and special html codes

            If split is true,

            margin is added on the left
            
            """

        # lists of texts and states are indefined
        
        if ( ( not type( lineList ) == list ) or ( not type( stateList ) == list ) ) : return False

        # if lists are empty, forces new line

        if ( ( utilities.isEmpty( lineList ) ) or
             ( utilities.isEmpty( stateList ) ) or
             ( utilities.isEmpty( lineList[ -1 ] ) ) ) :

            new = True

        # except for forced fields, does not add empty fields
        
        if ( ( utilities.isEmpty( text ) ) and ( not bool( new ) ) ) : return False

        # if there are lines, appends line by line.

        if "\n" in text :

            textList = text.splitlines()

            result = False

            for text in textList :

                ok = self.appendText(
                    lineList,
                    stateList,
                    text = text,
                    state = state,
                    new = new,
                    raw = raw,
                    split = split,
                    margin = margin
                    )

                if ok : result = True

                new = True      # remainder of lines will be separated, never appended

            return result
                    

##        # removes tags, crlf and right spaces
##        
##        text = text.replace( "\n", "" )
            
        # splits into special tags and remainder

        if ( ( bool( split ) ) and ( self.asciiToHtml( "<" ) in text ) ) :

            lines, states = self.splitSpecial( text, state )

            result = False
            
            for iLine in range( len( lines ) ) :

                lineText = lines[ iLine ]

                lineState = states[ iLine ]

                # for tags, remains raw ( otherwise may remove the tags that have been added )

                if lineState == "special" : lineRaw = True

                else : lineRaw = raw

                ok = self.appendText(
                    lineList,
                    stateList,
                    text = lineText,
                    state = lineState,
                    new = new,
                    raw = lineRaw,
                    split = False,
                    margin = margin
                    )

                if ok : result = True

            return result

        

            
        # removes  html tags and replaces html character codes
        
        if not bool( raw ) : text = self.removeTags( text )

        # except for forced fields, does not add empty fields
        
        if ( ( utilities.isEmpty( text ) ) and ( not bool( new ) ) ) : return False


        # tabs are removed (substituded by spaces )
        
        if "\t" in text : text = text.replace( "\t", self.tabSpace * " " )

        # empty lists or change of state, or new is forced
        
        if ( ( bool( new ) ) or ( not stateList[ -1 ] == state ) ) :

            # there is a margin or tabs

            if margin is None : None

            elif utilities.isEmpty( lineList ) : text = ( margin * " " ) + text

            elif stateList[ -1 ] == "line" : text = ( margin * " " ) + text

            lineList.append( text )

            stateList.append( state )

        # same state than last line : appends text.

        else :

            lineList[ -1 ] = lineList[ -1 ] + text


        return True





    def asciiToHtml (

        self,
        text = None
        ) :

        """ converts a flat ascii into html-coded text ii.e., replaces special characters by html codes &nbsp, &gt  """

        if utilities.isEmpty( text ) : return ""

        # here, there may be some special characters

        for iCode in range( len( self.characterCodeList ) ) :

            text = text.replace( self.characterAsciiList[ iCode ], self.characterCodeList[ iCode ] )

        return text





    def asciiToList (

        self,
        text = None,
        path = None
        ) :

        """ parses a HTML text, keeps only wiki-compatible tags. Returns a pair of lists lines + tags

            path is the path of the original document, used to transform relative links into absolute
        
            the parser is a state maching with states : bold, italic, bold + italic, header (1..6 sub-headings),
            link, image ( text ), horizontal line.

            in addition, manages a hierarchy of origin files (uses a special tag written by the conversion x-wiki to html )
            so that the text can be splitted into original hierarchical files ( a whole section becomes a link )

            """

        if utilities.isEmpty( text ) : return None, None
        
        size = len( text )
        
        iStart = 0

        iTag = 0

        state = None        # default text

        spanState = None    # state determined by last span tag

        marginState = None  # left margin or tab

        margin = None       # current margin

        lineList = [ ]

        tagList = [ ]

        if utilities.isEmpty( path ) : directory = ""

        else : directory = utilities.pathDirectory( path )

        lt = self.asciiToHtml( "<" )

        gt = self.asciiToHtml( ">" )

        while iStart < size :

            iTag = text.find( "<", iStart )

            # no more tags : appends final normal text (adds a line after headings )

            if iTag < 0 :

                self.appendText( lineList, tagList, text[ iStart :  ], state, split = True, margin = margin )

                margin = None

                if ( ( not state is None ) and ( state.startswith( "heading" ) ) ) :

                    self.appendText( lineList, tagList, " ", "line", new = True )

                break

            # appends the normal text that is before the tag

            if iTag > iStart :

                self.appendText( lineList, tagList, text[ iStart : iTag ], state, split = True, margin = margin )

                margin = None

                if ( ( not state is None ) and ( state.startswith( "heading" ) ) ) :

                    self.appendText( lineList, tagList, " ", "line", new = True )

                iStart = iTag

            # gets current tag, returns it if valid, else returns none.

            iClose, identifier, tag = self.getTag(
                text,
                position = iTag,
                )

##            print "Html.asciiToList", iStart, "..", iClose, "<", identifier, "->", tag, text[ iStart: iClose ]
                

           # no valid tag found (but there is a tag: skips the sequence <tag ... </tag>
           
            if tag is None :

                iStart = max( iStart + 1, iClose )

                continue

            # this is a new line: replaces by a space

            elif tag == "line" :

                self.appendText( lineList, tagList, " ", "line", new = True )

                margin = marginState        # next text will have a margin

            # new horizontal line

            elif tag == "horizontal" :

                self.appendText( lineList, tagList, " ", "horizontal", new = True )

                self.appendText( lineList, tagList, " ", "line", new = True )

                marginState = None          # resets margins

                margin = None

            # bold, old fashioned

            elif ( ( "bold" in tag ) or ( "italic" in tag ) ) :
                
                state = self.stateStyle( state, tag )
                
            # larger or smaller size

            elif ( ( "big" in tag ) or ( "small" in tag ) ) :

                state = self.stateSize( state, tag )
                    
            # titles start and stop

            elif "heading" in tag :

                state = self.stateHeading( state, tag )

                marginState = None      # resets margins

                margin = None

            # SPAN or DIV tags may contain style information

            elif ( ( tag == "spanStart" ) or ( tag == "divStart" ) ) :

                spanState = self.getStyle( text[ iTag : iClose ] )

                left = self.getMargin( text[ iTag : iClose ] )

                if not left is None :

                    marginState = left / 8  # recall that margin is in pixels

                    margin = marginState

                state = self.stateStyle( state, spanState )

            # end formattings that were initiated with span or div

            elif ( ( tag == "spanStop" ) or ( tag == "divStop" ) ) :

                if not spanState is None : state = None

                marginState = None

                margin = None

                spanState = None

            # link

            elif tag == "linkStart" :

                index, link, label = self.getLink(
                    text,
                    position = iStart
                    )

                if index < 0 :

                    iStart = max( iStart + 1, iClose )

                    continue

                link = self.removeTags( link )

                if utilities.isUrl( link ) : None

                elif link.startswith( utilities.fileHeader ) : link = utilities.normalizePath( link, normalize = False )

                elif utilities.isAbsolutePath( link ) : link = utilities.normalizePath( link, normalize = False )

                else : link = utilities.normalizePath( directory + link, normalize = False )

                label = self.removeTags( label )

                self.appendText( lineList, tagList, link + utilities.featureDelimiter + label, "link", new = True )

                self.appendText( lineList, tagList, " ", "line", new = True )

                iClose = index


            # image

            elif tag == "imageStart" :

                index, link, label = self.getImage(
                    text,
                    position = iStart
                    )

                if index < 0 :

                    iStart = max( iStart + 1, iClose )

                    continue

                link = self.removeTags( link )

                if utilities.isUrl( link ) : None

                elif link.startswith( utilities.fileHeader ) : link = utilities.normalizePath( link, normalize = False )

                elif utilities.isAbsolutePath( link ) : link = utilities.normalizePath( link, normalize = False )

                else : link = utilities.normalizePath( directory + link, normalize = False )

                label = self.removeTags( label )

                self.appendText( lineList, tagList, link + utilities.featureDelimiter + label, "image", new = True )

                self.appendText( lineList, tagList, " ", "line", new = True )

                iClose = index


            # input field

            elif tag == "widgetStart" :

                index, category, label = self.getWidget( 
                    text,
                    position = iStart
                    )

                if index < 0 :

                    iStart = max( iStart + 1, iClose )

                    continue

                category = self.removeTags( category )

                category = category.lower()

                label = self.removeTags( label )

                if utilities.featureDelimiter in label :label, definition = label.split( utilities.featureDelimiter, 1 )

                else : definition = ""

                definition = definition.strip()

                if not utilities.isEmpty( definition ) : definition = utilities.featureDelimiter + definition

                label = label.strip()

                if category == "image" :

                    if utilities.isUrl( label ) : None

                    elif label.startswith( utilities.fileHeader ) : label = utilities.normalizePath( label, normalize = False )

                    elif utilities.isAbsolutePath( label ) : label = utilities.normalizePath( label, normalize = False )

                    else : label = utilities.normalizePath( directory + label, normalize = False )

                line = category + utilities.featureDelimiter + label + definition

                self.appendText( lineList, tagList, line, "widget", new = True )

                self.appendText( lineList, tagList, " ", "line", new = True )

                iClose = index

            # this is a tag to keep as it

            elif tag == "keep" :

                iClose = text.find( ">", iClose )

                if iClose < 0 : iClose = size

                else : iClose = iClose + 1

                self.appendText( lineList, tagList, text[ iTag : iClose ], "html", new = True, raw = True )


            # the content of the enclosing tags must be preserved

            elif tag == "protect" :

                iClose = text.find( "</" + identifier + ">", iClose )

                if iClose < 0 : iClose = size

                else : iClose = iClose + 2 + len( tag ) + 1

                self.appendText( lineList, tagList, text[ iTag : iClose ], "html", new = True, raw = True )


            # this is a wiki tag: added without modification

            elif tag == "special" :

                self.appendText( lineList, tagList, text[ iTag : iClose ], "special", new = True, raw = True )

                self.appendText( lineList, tagList, " ", "line", new = True )

            # skips the tag

            iStart = max( iStart + 1, iClose )

        return lineList, tagList



            

    def body (

        self,
        content = None
        ) :

        """ returns a body text, with the given content """

        content = utilities.string( content, default = "" )

        text = "<" + self.bodyCode + ">" + \
               content + \
               "</" + self.bodyCode + ">"

        return text


        


    def initLists ( self ) :

        """ creates the lists """

        self.tagPairList = [
            "html",
            "head",
            "script",
            "style",
            "title", 
            "body", 
            "address",
            "blockquote",
            "del",
            "div",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "ins",
            "noscript",
            "p",
            "pre",
            "dl",
            "dt",
            "dd",
            "li",
            "ol",
            "ul",
            "table",
            "caption",
            "colgroup",
            "form",
            "button",
            "fieldset",
            "legend",
            "label",
            "select",
            "optgroup",
            "option",
            "textarea",
            "a",
            "bdo",
            "map",
            "object",
            "q",
            "script",
            "span",
            "sub",
            "sup",
            "abbr",
            "acronym",
            "cite",
            "code",
            "del",
            "dfn",
            "em",
            "ins",
            "kbd",
            "samp",
            "strong",
            "var",
            "b",
            "big",
            "i",
            "s",
            "small",
            "strike",
            "tt",
            "u",
            "applet",
            "frame",
            "iframe",
            "frameset",
            "noframes",
            ]

        
        self.tagSingleList = [
            "base",
            "link",
            "meta",
            "hr",
            "col",
            "thead",
            "tfoot",
            "tbody",
            "tr",
            "td",
            "th",
            "input",
            "br",
            "img",
            "area",
            "param",
            ]
        
        
            
        self.widgetPrefixList = [
##            "box",          # sub-box, containing anything else
            "button",       # simple button, pressure is detected by .pressed() method
            "check",        # check box with 2 options, ok or error
##            "choice",       # box containing choices or radio buttons
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
        



        self.formatList = [
            "heading4",
            "heading3",
            "heading2",
            "heading",
            "boldItalic",
            "bold",
            "italic",
            "strikethrough",
            "teletype",
            "underline",
            ]

        self.codeStartList = [
            "<" + self.heading4Code + ">",
            "<" + self.heading3Code + ">",
            "<" + self.heading2Code + ">",
            "<" + self.headingCode + ">",
            "<" + self.boldItalicCode + ">",
            "<" + self.boldCode + ">",
            "<" + self.italicCode + ">",
            "<" + self.strikethroughCode + ">",
            "<" + self.teletypeCode + ">",
            "<" + self.underlineCode + ">",
            ]

        self.codeStopList = [
            "</" + self.heading4Code + ">",
            "</" + self.heading3Code + ">",
            "</" + self.heading2Code + ">",
            "</" + self.headingCode + ">",
            "</" + self.boldItalicCode + ">",
            "</" + self.boldCode + ">",
            "</" + self.italicCode + ">",
            "</" + self.strikethroughCode + ">",
            "</" + self.teletypeCode + ">",
            "</" + self.underlineCode + ">",
            ]

                        

        # keeps the tag untouched, processes content

        self.keepList = [
            "<" + "blockquote",
            "<" + "ins", 
            "<" + "pre",            
            "<" + "dl", 
            "<" + "dt", 
            "<" + "dd", 
            "<" + "li", 
            "<" + "ol", 
            "<" + "ul", 
            "<" + "table", 
            "<" + "caption", 
            "<" + "colgroup", 
            "<" + "form", 
            "<" + "q", 
            "<" + "code", 
            "<" + "sub", 
            "<" + "sup", 
            "<" + "abbr", 
            "<" + "acronym", 
            "<" + "cite", 
            "<" + "script", 
            "<" + "script", 
            "<" + "script", 
            "<" + "dfn", 
            "<" + "dfn", 
            "<" + "ins", 
            "<" + "kbd", 
            "<" + "samp", 
            "<" + "var", 
            "<" + "frameset",
            "<" + "frame",
            "</" + "blockquote",
            "</" + "ins", 
            "</" + "pre",            
            "</" + "dl", 
            "</" + "dt", 
            "</" + "dd", 
            "</" + "li", 
            "</" + "ol", 
            "</" + "ul", 
            "</" + "table", 
            "</" + "caption", 
            "</" + "colgroup", 
            "</" + "form", 
            "</" + "q", 
            "</" + "code", 
            "</" + "sub", 
            "</" + "sup", 
            "</" + "abbr", 
            "</" + "acronym", 
            "</" + "cite" , 
            "</" + "script", 
            "</" + "dfn", 
            "</" + "dfn", 
            "</" + "ins", 
            "</" + "kbd", 
            "</" + "samp", 
            "</" + "var", 
            "</" + "frameset",
            "</" + "frame",

            "<" + "base",
            "<" + "link",
            "<" + "meta",
            "<" + "col",
            "<" + "thead",
            "<" + "tfoot",
            "<" + "tbody",
            "<" + "td",
            "<" + "th",
            "<" + "input",
            "<" + "area",
            "<" + "param",
            ]

        # keep tag + content without parsing (won t be visible in other formats)
                          
        self.protectList = [
            "<" + "del",
            "<" + "noscript",
            "<" + "button",
            "<" + "fieldset",
            "<" + "legend",
            "<" + "select",
            "<" + "optgroup",
            "<" + "option",
            "<" + "textarea",
            "<" + "bdo", 
            "<" + "map", 
            "<" + "object", 
            "<" + "script", 
            "<" + "applet",
            "<" + "iframe",
            "<" + "noframes",
            "<" + "style",
            ]


        self.headingCodeList = [
            self.headingCode,
            self.heading2Code,
            self.heading3Code,
            self.heading4Code,
            self.heading5Code,
            self.heading6Code
            ]


        self.tagList = [
            "<" + self.emphasizeCode,
            "<" + self.strongCode,
            "<" + self.heading6Code,
            "<" + self.heading5Code,
            "<" + self.heading4Code,
            "<" + self.heading3Code,
            "<" + self.heading2Code,
            "<" + self.headingCode,
            "<" + self.linkCode,
            "<" + self.imageCode,
            "<" + self.boldSimpleCode,
            "<" + self.italicSimpleCode,
            "<" + self.strikethroughCode,
            "<" + self.teletypeCode,
            "<" + self.underlineCode,            
            "<" + self.bigCode,
            "<" + self.smallCode,
            "<" + self.spanCode,
            "<" + self.divCode,
            "<" + self.newLineCode,
            "<" + self.horizontalCode,
            "</" + self.paragraphCode,           
            "</" + self.tableRowCode,
            "<" + self.noRightsStartCode,
            "<" + self.noWikiStartCode,
            "<" + self.rightsStartCode,
            "</" + self.emphasizeCode,
            "</" + self.strongCode,
            "</" + self.heading6Code,
            "</" + self.heading5Code,
            "</" + self.heading4Code,
            "</" + self.heading3Code,
            "</" + self.heading2Code,
            "</" + self.headingCode,
            "</" + self.linkCode,
            "</" + self.boldSimpleCode,
            "</" + self.italicSimpleCode,
            "</" + self.strikethroughCode,
            "</" + self.teletypeCode,
            "</" + self.underlineCode,            
            "</" + self.bigCode,
            "</" + self.smallCode,
            "</" + self.spanCode,
            "</" + self.divCode,
            "</" + self.noRightsStartCode,
            "</" + self.noWikiStartCode,
            "</" + self.rightsStartCode,
            "<" + self.labelCode,
            "</" + self.labelCode,
            ]

        self.specialList = [
            self.asciiToHtml( "<" + self.noRightsStartCode ),
            self.asciiToHtml( "<" + self.noWikiStartCode ),
            self.asciiToHtml( "<" + self.rightsStartCode ),
            self.asciiToHtml( "</" + self.noRightsStartCode ),
            self.asciiToHtml( "</" + self.noWikiStartCode ),
            self.asciiToHtml( "</" + self.rightsStartCode ),
            ]
            

        self.stateList = [
            "italicStart",
            "boldStart",
            "heading6Start",
            "heading5Start",
            "heading4Start",
            "heading3Start",
            "heading2Start",
            "headingStart",
            "linkStart",
            "imageStart",
            "boldStart",
            "italicStart",
            "strikethroughStart",
            "teletypeStart",
            "underlineStart",
            "bigStart",
            "smallStart",
            "spanStart",
            "divStart",
            "line",
            "horizontal",
            "line",
            "line",
            "special",
            "special",
            "special",
            "italicStop",
            "boldStop",
            "heading6Stop",
            "heading5Stop",
            "heading4Stop",
            "heading3Stop",
            "heading2Stop",
            "headingStop",
            "linkStop",
            "boldStop",
            "italicStop",
            "strikethroughStop",
            "teletypeStop",
            "underlineStop",
            "bigStop",
            "smallStop",
            "spanStop",
            "divStop",
            "special",
            "special",
            "special",
            "widgetStart",
            "widgetStop"
            ]
            


        self.defaultCharset = "ISO-8859-1"

        

    def findTag (

        self,
        text = None,
        position = None,
        tag = None,
        skip = None
        ) :

        """ searches a wiki tag in text, at the given position and returns the position after the tag or -1, plus the tag found

            tag may be a list of tags

            if skip is true, verifies that before the tag, the text only contains spaces

            """

        if utilities.isEmpty( tag ) : return -1, None

        if utilities.isEmpty( text ) : return -1, None

        

        # lists: takes first encountered tag

        if type( tag ) == list :

            closestPosition = len( text )

            closestTag = None

            for item in tag :

                thisPosition, thisTag = self.findTag(
                    text = text,
                    position = position,
                    tag = item,
                    skip = skip
                    )

                if thisPosition < 0 : continue

                elif thisPosition >= closestPosition : continue

                closestPosition = thisPosition

                closestTag = thisTag

                if not bool( skip ) : break

            if closestTag is None : return -1, None

            else : return closestPosition, closestTag
        
        tagOpen = "<" + tag

        position = utilities.integer( position, default = 0 )

        # not found in this position

        if not bool( skip ) :
        
            if utilities.startswith( text, tag, position ) : None

            elif utilities.startswith( text, tagOpen, position ) : tag = tagOpen

            else : return -1, None

        else :

            positionTag = text.find( tag, position )

            positionTagOpen = text.find( tagOpen, position )

            if ( ( positionTag < 0 ) and ( positionTagOpen < 0 ) ) :

                return -1, None

            elif positionTag < 0 :

                position = positionTagOpen

                tag = tagOpen

            elif positionTagOpen < 0 :

                position = positionTag

            elif positionTagOpen < positionTag :

                position = positionTagOpen

                tag = tagOpen

            else :

                position = positionTag


        # finds the final ">"

        iClose = text.find( ">", position )

        if iClose <= 0 : iClose = len( text )

        else : iClose = iClose + 1

        return iClose, tag
        





    def getImage (

        self,
        text = None,
        position = None,
        skip = None,
        ) :

        """ returns the content of a link starting at desired position: label and url """

        iEnd, tag = self.findTag(
            text = text,
            position = position,
            tag = self.imageCode,
            skip = skip
            )

        if iEnd < 0 : return -1, None, None

        # start of tag

        iOpen = text.rfind( "<", 0, iEnd )

        if iOpen< 0 : return -1, None, None
        
        # finds the url, enclosed in quotes after src = ...
       
        iSrc = text.find( self.srcCode, iOpen, iEnd )

        if iSrc < 0 : return -1, None, None

        iSrcStart = text.find( '"', iSrc )

        if iSrcStart < 0 : return -1, None, None

        iSrcEnd = text.find( '"', iSrcStart + 1 )
        
        if iSrcEnd < 0 : return -1, None, None

        link = text[ iSrcStart + 1 : iSrcEnd ]

        # finds the text, enclosed in quotes after alt = ...
       
        iAlt = text.find( self.altCode, iOpen, iEnd )

        if iAlt < 0 : iAltStart = -1

        else : iAltStart = text.find( '"', iAlt )

        if iAltStart < 0 : iAltEnd = -1

        else : iAltEnd = text.find( '"', iAltStart + 1 )
        
        if ( ( iAltEnd < 0 ) or ( iAltStart < 0 ) ) : label = ""

        else : label = text[ iAltStart + 1 : iAltEnd ]

        # must filter to avoid unwanted new lines
        
        label = label.strip().replace( "\n", " " ).replace( "\t", " " ).replace( "&nbsp:", " " )
        
        return iEnd, link, label 
    
    




    def getLink (

        self,
        text = None,
        position = None,
        skip = None,
        ) :

        """ returns the content of a link starting at desired position: label and url """

        iStart, tag = self.findTag(
            text = text,
            position = position,
            tag = self.linkCode,
            skip = skip
            )

        if iStart < 0 : return -1, None, None

        closeTag = "</" + self.linkCode + ">"

        iEnd, tag = self.findTag(
            text = text,
            position = iStart,
            tag = closeTag,
            skip = True
            )
        
        if iEnd < 0 : return -1, None, None

        # gets label (between the 2 tags)

        iStartLabel = iStart

        iEndLabel = text.rfind( "<", 0, iEnd )

        label = text[ iStartLabel : iEndLabel ]

        # must filter to avoid unwanted new lines
        
        label = label.strip().replace( "\n", " " ).replace( "\t", " " ).replace( "&nbsp:", " " )

        # start of tag

        iOpen = text.rfind( "<", 0, iStart )

        if iOpen< 0 : return -1, None, None

        # finds the url, enclosed in quotes after href = ...

       
        iUrl = text.rfind( self.hrefCode, iOpen, iStart )

        if iUrl < 0 : return -1, None, None

        iUrlStart = text.find( '"', iUrl )

        if iUrlStart < 0 : return -1, None, None

        iUrlEnd = text.find( '"', iUrlStart + 1 )
        
        if iUrlEnd < 0 : return -1, None, None

        link = text[ iUrlStart + 1 : iUrlEnd ]

        
        return iEnd, link, label 
    



    def getMargin (

        self,
        text = None
        ) :

        """ gets the margin defined in a DIV or SPAN tag, e.g., style="margin-left: 40px;"

            returns aNone, or number of pixels
            
            """


        if utilities.isEmpty( text ) : return None

        iStyle = text.find( self.styleCode )

        if iStyle < 0 : return None

        # pair of quotes enclosing the style

        iStart = text.find( '"', iStyle )

        if iStart < 0 : return None

        iEnd = text.find( '"', iStart + 1 )

        if iEnd < 0 : return None

        text = text[ iStart + 1 : iEnd ]

        # margin left

        if not "margin-left" in text : return None

        items = utilities.textToWords( utilities.string( text, format = "split" ) )

        for item in items :

            margin = utilities.integer( item )

            if not margin is None : return margin

        return None
        
        

    def getSelect (

        self,
        text = None,
        position = None,
        skip = None,
        ) :

        """ returns the content of a selection field (popup menu) starting at desired position: label and url """

        iStart, tag = self.findTag(
            text = text,
            position = position,
            tag = self.selectStartCode,
            skip = skip
            )

        if iStart < 0 : return -1, None, None

        closeTag = "</" + self.selectStartCode + ">"

        iEnd, tag = self.findTag(
            text = text,
            position = iStart,
            tag = closeTag,
            skip = True
            )
        
        if iEnd < 0 : return -1, None, None

        # gets label (between the 2 tags)

        iStartLabel = iStart

        iEndLabel = text.rfind( "<", 0, iEnd )

        label = text[ iStartLabel : iEndLabel ]

        # start of tag

        iOpen = text.rfind( "<", 0, iStart )

        if iOpen< 0 : return -1, None, None

        # finds the url, enclosed in quotes after href = ...

        link = "menu"
        
        return iEnd, link, label 



    def getStyle (

        self,
        text = None
        ) :

        """ gets the style defined in a DIV or SPAN tag, i.e., bold and/or italic

            returns a state None, "bold", "italic" and/or "boldItalic"
            
            """


        if utilities.isEmpty( text ) : return None

        iStyle = text.find( self.styleCode )

        if iStyle < 0 : return None

        # pair of quotes enclosing the style

        iStart = text.find( '"', iStyle )

        if iStart < 0 : return None

        iEnd = text.find( '"', iStart + 1 )

        if iEnd < 0 : return None

        text = text[ iStart + 1 : iEnd ]

        # style fields

        bold = "bold" in text

        italic = "italic" in text

        if ( ( bold ) and ( italic ) ) : state = "boldItalicStart"

        elif bold : state = "boldStart"

        elif italic : state = "italicStart"

        else : state = None

        return state
        




    def getTag (

        self,
        text = None,
        position = None,
        ) :

        """ searches a tag in text, at the given position.

            uses self.tagList to recognize valid tags.

            if skip is true, finds the next "<" in the text otherwise searches here.

            returns a 3-uple,  position after the tag, identifier of tag (no <>),and  state corresponding to the tag ( self.stateList )

            position is -1 in case of problem

            """

        if utilities.isEmpty( text ) : return -1, None, None

        if not utilities.isIndex( position, text ) : return -1, None, None

        size = len( text )

##        position = utilities.integer( position, default = 0 )

        # searches the end of the tag : space or ">"

        iEnd = position + 64

        iBracket = text.find( ">", position, iEnd )

        if ( ( iBracket >= position ) and ( iBracket < iEnd ) ) : iEnd = iBracket

        iSpace = text.find( " ", position, iEnd )

        if ( ( iSpace >= position ) and ( iSpace < iEnd ) ) : iEnd = iSpace
        
        iLine = text.find( "\n", position, iEnd )

        if ( ( iLine >= position ) and ( iLine < iEnd ) ) : iEnd = iLine
        
        iTab = text.find( "\t", position, iEnd )

        if ( ( iTab >= position ) and ( iTab < iEnd ) ) : iEnd = iTab

        # means that did not find a tag identifier
        
        if iEnd >= position + 64 : return -1, None, None

        # the tag contains the initial "<"

        tag = text[ position : iEnd ].lower()

        # identifier does not

        identifier = tag.strip( " <>/" )

        # searches the tags that generate a state

        if tag in self.tagList : found = self.stateList[ self.tagList.index( tag ) ]

        # searches the tags to keep intact

        elif tag in self.keepList : found = "keep"

        # searches the tag to protect ( copy enclosing tags and content)

        elif tag in self.protectList : found = "protect"

        else : found = None

        iClose = text.find( ">", iEnd )

        if iClose < 0 : iClose = size

        else : iClose = iClose + 1

        return iClose, identifier, found



    def getWidget (

        self,
        text = None,
        position = None,
        skip = None,
        ) :

        """ returns the content of a widget <label>...<input></label> """

        openTag = "<" + self.labelCode + ">"
        
        iStart, tag = self.findTag(
            text = text,
            position = position,
            tag = openTag,
            skip = skip
            )

        if iStart < 0 : return -1, None, None

        # final tag. returns the final position
        
        closeTag = "</" + self.labelCode + ">"
        
        iEnd, tag = self.findTag(
            text = text,
            position = iStart,
            tag = closeTag,
            skip = True
            )
        
        if iEnd < 0 : return -1, None, None

        # searches for an intermediate <input> tag. returns the final position

        iInput = text.find( "<" + self.inputCode, iStart, iEnd )

        if iInput < 0 : return -1, None, None


        # closing bracket

        iClose = text.find( ">", iInput, iEnd )

        if iClose < 0 : return -1, None, None

        # type of widget, text & definition between <label> and <input. Must filter to avoid double lines

        label = text[ iStart : iInput ].strip().replace( "\n", " " ).replace( "\t", " " ).replace( "&nbsp:", " " )


        # label is of the form type text|definition
        
        if " " in label : prefix, label = label.split( " ", 1 )

        else : prefix = ""

        # no way of determining the type

        prefix = prefix.strip().lower()

        if not prefix in self.widgetPrefixList : return -1, None, None

##        print "getWidget", iStart, iInput, iEnd, "prefix", prefix, "label", label

        return iEnd, prefix, label
    



    def header (

        self,
        charset = None,
        title = None
        
        ) :

        """ returns a header text with a charset and a title """

        charset = utilities.string( charset, default = self.defaultCharset )

        title = utilities.string( title, default = "" )

        text = "<" + self.doctype + ">"
        
        text = text + "<" + self.headCode + ">"

        text = text + '<meta content="text/html; charset=' + charset + '" '

        text = text + 'http-equiv="content-type">'

        text = text + \
               "<" + self.titleCode + ">" + \
               title + \
               "</" + self.titleCode + ">"

        text = text + "</" + self.headCode + ">"
        
        return text




    def horizontalLine ( self ) :

        """ returns a tag for an horizontal line """

        return '<hr style="width: 100%; height: 2px;">'



    def htmlToAscii (

        self,
        text = None
        ) :

        """ converts an html-coded text into flat ascii, i.e., replaces the html codes &nbsp, &gt etc by asciis """

        if utilities.isEmpty( text ) : return ""
        
        # converts special characters if there are some

        iAmp = text.find( "&" )

        if iAmp < 0 : return text

        # here, there may be some special characters

        for iCode in range( len( self.characterCodeList ) ) :

            text = text.replace( self.characterCodeList[ iCode ], self.characterAsciiList[ iCode ] )

        return text



        
    def htmlToList (

        self,
        text = None,
        path = None
        ) :

        """ returns the content of the body of a text, enclosed between </body .. > and </body>
            Path is the original path
            
            """

        position, text, tag = self.textBetweenTags(
            text,
            tag = self.bodyCode,
            skip = True
            )

        return self.asciiToList( text, path )


    

    def image (

        self,
        address = None,
        description = None,
        directory = None,
        ) :

        """ returns an included image. If it is a file below directory, uses a relative link """

        if utilities.isEmpty( address ) : return ""

        directory = utilities.normalizePath( directory, normalize = False )

        if utilities.isUrl( address ) : return ""

        address = utilities.normalizePath( address, normalize = False )

        # relative path

        if ( ( not utilities.isEmpty( directory ) ) and ( address.startswith( directory ) ) ) :

            address = address[ len( directory ) : ].strip( " " + os.sep )

            address = utilities.slashPath( address )

        # absolute path

        else :

            address = utilities.fileHeader + utilities.slashPath( address )

        description = utilities.string( description, default = "" )

        text = "<" + \
               self.imageCode + " " + \
               self.altCode + " = "  + '"' + description + '"' + \
               self.srcCode + " = "  + '"' + address + '"' + \
               ">"

        return text





    def link (

        self,
        address = None,
        description = None,
        directory = None,
        ) :

        """ returns a link. If it is a file below directory, uses a relative link """

        if utilities.isEmpty( address ) : return ""

        directory = utilities.normalizePath( directory, normalize = False )

        if utilities.isUrl( address ) :

            description = utilities.string( description, default = address )

        else :

            address = utilities.normalizePath( address, normalize = False )

            # relative path

            if ( ( not utilities.isEmpty( directory ) ) and ( address.startswith( directory ) ) ) :

                address = address[ len( directory ) : ].strip( " " + os.sep )

                address = utilities.slashPath( address )

            # absolute path

            else :

                address = utilities.fileHeader + utilities.slashPath( address )

            description = utilities.string( description, default = "" )

        text = "<" + \
               self.linkCode + " " + \
               self.hrefCode + " = " + '"' + address + '"' + \
               ">" + \
               description + \
               "</" + self.linkCode + ">"
        
        return text




    def listToAscii (

        self,
        textList = None,
        stateList = None,
        path = None,
        copy = True
        ) :

        """ converts a pair of lists text + state into a flat html text """
               
        
        if utilities.isEmpty( textList ) : return ""

        if utilities.isEmpty( stateList ) : return ""

        if utilities.isEmpty( path ) : local = None

        else : local = utilities.localDirectory ( path )

        size = min( len( textList ), len( stateList ) )

        body = ""

        for iField in range( size ) :

            state = stateList[ iField ]

            text = textList[ iField ]

            htmlText = self.asciiToHtml( text )

            if state is None :

                body = body + htmlText

            elif state == "line" :

                body = body + "<" + self.newLineCode + ">"

            elif state == "horizontal" :

                body = body + "<" + self.horizontalLineCode +  ">"

            elif state.startswith ( "heading" ) :

                level = utilities.integer( state[ len( "heading" ) : ], default = 1 )

                if utilities.isIndex( level - 1, self.headingCodeList ) :

                    tag = self.headingCodeList[ level - 1 ] # does not contain < > 

                    body = body + \
                           "<" + tag + ">" + \
                           htmlText + \
                           "</" + tag + ">" + \
                           "<" + self.newLineCode + ">"

            elif state == "underline" :

                body = body + \
                       "<" + self.underlineCode + ">" + \
                       htmlText + \
                       "</" + self.underlineCode + ">"

            elif state == "strikethrough" :

                body = body + \
                       "<" + self.strikethroughCode + ">" + \
                       htmlText + \
                       "</" + self.strikethroughCode + ">"

            elif state == "teletype" :

                body = body + \
                       "<" + self.teletypeCode + ">" + \
                       htmlText + \
                       "</" + self.teletypeCode + ">"

            elif state == "bold" :

                body = body + \
                       "<" + self.boldSimpleCode + ">" + \
                       htmlText + \
                       "</" + self.boldSimpleCode + ">"
                
            elif state == "italic" :

                body = body + \
                       "<" + self.italicSimpleCode + ">" + \
                       htmlText + \
                       "</" + self.italicSimpleCode + ">"
                
            elif state == "boldItalic" :

                body = body + \
                       "<" + self.boldSimpleCode + ">" + \
                       "<" + self.italicSimpleCode + ">" + \
                       htmlText + \
                       "</" + self.italicSimpleCode + ">" + \
                       "</" + self.boldSimpleCode + ">"

            elif state.startswith( "big" ) :

                level = utilities.integer( state[ len( "big" ) : ], default = 1 )

                openTag = "<" + self.bigCode + ">"

                closeTag = "</" + self.bigCode + ">"

                body = body + \
                       level * openTag + \
                       htmlText + \
                       level * closeTag


            elif state.startswith( "small" ) :

                level = utilities.integer( state[ len( "small" ) : ], default = 1 )

                openTag = "<" + self.smallCode + ">"

                closeTag = "</" + self.smallCode + ">"

                body = body + \
                       level * openTag + \
                       htmlText + \
                       level * closeTag

            elif state == "link" :

                if utilities.featureDelimiter in text :

                    address, description = text.split( utilities.featureDelimiter, 1 )

                    address = address.strip()

                    description = description.replace( '"', ' ' ).replace( "'", " " ).strip()

                else :

                    address = text.strip()

                    description = address

                if ( ( bool( copy ) ) and
                     ( not utilities.isUrl( address ) ) and
                     ( not utilities.isEmpty( local ) ) and
                     ( not address.startswith( local ) )
                     ):

                    target = local + utilities.pathLastNameWithExtension( address )

                    utilities.pathCopy( address, target )

                    address = target

                body = body + self.link( address, description )


            elif state == "image" :


                if utilities.featureDelimiter in text :

                    address, description = text.split( utilities.featureDelimiter, 1 )

                    address = address.strip()

                    description = description.replace( '"', ' ' ).replace( "'", " " ).strip()

                else :

                    address = text.strip()

                    description = address


                if ( ( bool( copy ) ) and
                     ( not utilities.isUrl( address ) ) and
                     ( not utilities.isEmpty( local ) ) and
                     ( not address.startswith( local ) )
                     ):

                    target = local + utilities.pathLastNameWithExtension( address )

                    utilities.pathCopy( address, target )

                    address = target

                body = body + self.image( address, description )

            elif state == "widget" :

                widget, text = text.split( utilities.featureDelimiter, 1 )

                widget = widget.strip()

                text = text.replace( '"', ' ' ).replace( "'", " " ).strip()

                body = body + self.widget( widget, text )

            # special tag: content added to text, in html-compatible format
            
            elif state == "special"  :

                body = body + htmlText


            # html native, e.g., preserved tags added to text, no modification
            
            elif state == "html"  :

                body = body + text

            # unknown tag, e.g., wiki: skips
            
            else :

                None
                
        
        return body




    def listToHtml (
        
        self,
        textList = None,
        stateList = None,
        path = None,
        copy = None
        
        ) :

        """ converts a pair of lists text-tag into a complete html text,

        path is the target path. linked files and images are copied in its local directory if it exists

            warning: links to files and images only work with absolute paths

            """

        body = self.listToAscii(
            textList = textList,
            stateList = stateList,
            path = path,
            copy = copy
            )

        return self.header() + self.body( body )





    def removeTags (

        self,
        text = None
        ) :

        """ remove all tags from the text """

        if utilities.isEmpty( text ) : return ""

        size = len( text )

        # there are tags inside

        iStart = text.find( "<" )

        if iStart < 0 : iStart = size

        filtered = text[ : iStart ]

        # removes tags. enters only if there are tags inside
        
        while iStart < size :

            iOpen = text.find( "<", iStart )

            if iOpen < 0 :

                filtered = filtered + text[ iStart : len( text ) ]

                break

            filtered = filtered + text[ iStart : iOpen ]

            iClose = text.find( ">", iOpen + 1 )

            if iClose < 0 : break

            # skips the tag

            iStart = iClose + 1

        return self.htmlToAscii( filtered )
    




                   
    def splitSpecial (

        self,
        text = None,
        state = None
        ) :

        """ splits a text into sequences of normal and special strings, returns lines and states """

        if utilities.isEmpty( text ) : return [ ], [ ]

        size = len( text )
        
        lt = self.asciiToHtml( "<" )

        gt = self.asciiToHtml( ">" )

        lineList = [ ]

        stateList = [ ]

        iStart = 0

        iClose = 0

        while iStart < size :

            iTag = text.find( lt, iClose )

            if iTag < 0 :

                lineList.append( text[ iStart : ] )

                stateList.append( state )

                break

            tag = None

            iClose = iTag + len( lt )

            for special in self.specialList :

                if not text.startswith( special, iTag ) : continue

                # found
                
                tag = special

                iEnd = text.find( gt, iClose )

                if iEnd >= 0 : iClose = iEnd + len( gt )

                else : iClose = size

                break

            if not tag is None :

                if iTag > iStart :

                    lineList.append( text[ iStart : iTag ] )

                    stateList.append( state )

                lineList.append( self.htmlToAscii( text[ iTag : iClose ] ) )

                stateList.append( "special" )

                iStart = iClose

            iTag = iClose

        return lineList, stateList                

        
        





        
    def stateHeading (

        self,
        state = None,
        tag = None
        ) :


        """ returns the state of heading corresponding to the new tag (heading, level 2..6 or None ) """


        if tag is None : return state


        # remove a heading level
        
        if tag.endswith( "Stop" ) :

            if state is None : None

            elif tag.startswith( state ) : state = None


        # adds a heading level
        
        if tag.endswith( "Start" ) :

            newState = tag[ : - len( "start" ) ]

            if state == newState : None

            else : state = newState

            
        return state


                





    def stateSize (

        self,
        state = None,
        tag = None
        ) :

        """ Returns the new size after a tag "big", "small" (start or stop ) """

        if tag is None : return state
        
        # increment after the tag

        if tag.endswith( "Start" ) : delta = 1

        elif tag.endswith( "Stop" ) : delta = -1

        else : return state

        # small : reverses the delta size
        
        if "small" in tag : delta = - delta
        

        # current size ( in levels, from 0 = normal size )
        
        if state is None : level = 0

        elif state.startswith( "big" ) : level = utilities.integer( state[ len( "big" ) : ], default = 1 )

        elif state.startswith( "small" ) : level = - utilities.integer( state[ len( "small" ) : ], default = 1 )

        else : level = 0

        # new size

        level = level + delta

        # generates the state name
        
        if level > 1 : state = "big" + utilities.string( level )

        elif level == 1 : state = "big"

        elif level == 0 : state = None

        elif level == -1 : state = "small"

        else : state = state = "small" + utilities.string( - level )


        return state





            

    def stateStyle (

        self,
        state = None,
        tag = None
        ) :

        """ style of font, bond and/or italic, after a tag 'bold' or 'italic', start or stop """

        if tag is None : return state

        tag = tag.lower()

        # action : add or remove
        
        if tag.endswith( "start" ) : add = True

        elif tag.endswith( "stop" ) : add = False

        else : return state
        
        # style : bold or italic
        
        if "bold" in tag : bold = add

        else : bold = None

        if "italic" in tag : italic = add

        else : italic = None

        # result

        if bold == True :

            if state == "boldItalic" : None

            elif state == "italic" : state = "boldItalic"

            else : state = "bold"

        elif bold == False :
            
            if state == "bold" : state = None

            elif state == "boldItalic" : state = "italic"

        if italic == True :

            if state == "boldItalic" : None

            elif state == "bold" : state = "boldItalic"

            else : state = "italic"

        elif italic == False :
            
            if state == "italic" : state = None

            elif state == "boldItalic" : state = "bold"

        return state







    def tagClose (

        self,
        tag = None,
        complete = False
        ) :

        """ returns a normalized closing tag for 'tag', removing spaces and final > """

        if utilities.isEmpty( tag ) : return ""


        # tag already normalized

        if ( ( tag.startswith ( "</" ) ) and ( tag.endswith( ">" ) ) ) :

            if not bool( complete ) : return tag.strip( "> " )

            else : return tag
           

        # there is a space inside
        
        iSpace = tag.find( " " )

        if iSpace >= 0 : tag = tag[ : iSpace ]

        iClose = tag.find( ">" )

        if iClose >= 0 : tag = tag[ : iClose ]

        if tag.startswith( "</" ) : None

        elif tag.startswith( "<" ) : tag = "</" + tag[ 1 : ]

        else : tag = "</" + tag

        if bool( complete ) : tag = tag + ">"

        else : tag = tag.strip( "> " )

        return tag







    def textBetweenTags (

        self,
        text = None,
        position = None,
        tag = None,
        skip = None
        ) :

        """ gets the text between 2 tags <xxx ... > and </xxx ... >

            the tag can be a list, in this case checks items in order

            returns position after closing tag, text, and tag or -1 None None

            """

        # argument is a list : recursive call
        
        if type( tag ) == list :

            for item in tag :

                index, field, item = self.textBetweenTags(
                    text = text,
                    position = position,
                    tag = item,
                    skip = skip
                    )

                if index >= 0 : return index, field, item

            return -1, None, None

                

        position, openTag = self.findTag(
            text = text,
            position = position,
            tag = tag,
            skip = skip
            )

        if position < 0 : return -1, None, None

        tagClose = "</" + tag

        iEnd = text.find( tagClose, position  )

        if iEnd < 0 : return -1, None, None

        return iEnd + len( tagClose ), text[ position : iEnd ], tag

        


    def widget (

        self,
        category = None,
        text = None,
        ) :

        """ returns a widget, button, input or select.

            WARNING: HTML information is lost, wiki information is not. the widget is just here for visual help
            
            """

        if utilities.isEmpty( category ) : return ""

        category = category.strip().lower()

        text = utilities.string( text, default = "" )

        if utilities.featureDelimiter in text : text, definition = text.split( utilities.featureDelimiter, 1 )

        else : definition = ""

        definition = definition.strip()

        text = text.strip()

        # recodes category within widget
        
        prefix = "button"

        if not utilities.isEmpty( definition ) : definition = " " + utilities.featureDelimiter + " " + definition
        
        line = "<" + self.labelCode + ">" + \
               category.upper() + " " + text + definition + \
               "<" + self.inputCode + \
               " " + self.valueCode + '=' + '"' + "widget" + '"' + \
               " " + self.typeCode + '=' + '"' + prefix + '"' + \
               ">" + \
               "</" + self.labelCode + ">"

        return line





# -----------------------------------
# creates the global singleton object if not already here
#

if not "html" in globals() : html = Html()
         
        

