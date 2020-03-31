
""" Reference files management. Read/write and access formatted files (BibTeX format)

    See on wikipedia for information on  BibTeX format
   
 
    """


from api.Utilities import *

from api.Clock import *


class BibFile :
    
    """ Reference files management. Read/write and access formatted files (BibTeX format)

    See on wikipedia for information on  BibTeX format
   
        
        The basic internal representation of a table file is a list of lines, each line being a list of words
        (i.e., a list of lists)


        """

    # attributes read from file or to write to file

    attributeList = None

    # specific fields

    author = None

    # bibfile

    bibPath = None

    # bib type

    bibtex = None

    # binding with context variables

    bind = None

    # file description

    description = None

    # link to file

    filePath = None
    
    # list of fields of bibtex records

    fieldList = None
    
    # matrix of fields for each type

    fieldMatrix = None
    
    # key for alphabetical indexing

    key = None

    # missing fields

    missingList = None
        
    # owner

    owner = None
    
    # file name
    
    path = ""

    # dictionary of publications

    publicationDictionary = None

    # dictionary of publishers

    publisherDictionary = None
    
    # list of publishers (reduced keywords)

    publisherList = None

    # list of mandatory fields for each type

    requiredMatrix = None

    # title

    title = None

    # this year and century

    thisCentury = None
    
    thisYear = None

        
    # list of bibtex types

    typeList = None

    # values read from file or to write to file

    valueList = None

    # year of document

    year = None

##    # path to zip file
##
##    zipPath = None


    
    from bibtex_configuration import *

    try :

        from configuration.bibtex_configuration import *

    except Exception, exception :

        from bibtex_configuration import *
    


    def __init__ ( self ) :

        """ Constructor. Does absolutely nothing
           
            """

        self.resetData()

        self.setDefault()




    def asciiToLatex (

        self,
        text = None
        ) :

        """ converts an ASCII string with special characters into a latex text with escape \ sequences """

        if utilities.isEmpty( text ) : return ""

        result = ""

        for char in text :

            if char.isalnum() :

                result = result + char

            elif char in self.escapeTable :

                index = self.escapeTable.index( char, 1 )

                result = result + self.escapeTable[ index - 1 ]

            else :

                result = result + char

        return result.strip()



    def asciiToList (

        self,
        text = None,
        path = None

        ) :

        """ reads a BiBTex file and/or text and generates a pair of lists line + tag (for converter only)

            cleans the fields from { }.
            
            """

        self.read(
            text = text,
            path = path
            )

        textList = [ ]

        stateList = [ ]

        size = min( len( self.attributeList ), len( self.valueList ) )

        for index in range( size ) :

            attribute = self.attributeList[ index ]

            value = self.valueList[ index ]
            
            value = utilities.asciiToFlat( value, default = utilities.voidCode )

            value = value.replace( "{", "" ).replace( "}", "" )

            textList.append( attribute +  + value )

            stateList.append( None )

            textList.append( " " )

            stateList.append( "line" )
        
        return textList, stateList


    

    def attributeValueListToTable (

        self,
        attributeList = None,
        valueList = None,
        bind = True
        ) :

        """ Converts a pair attribute value list into a table

            bind means that context variables will be updated

            """

        self.bind = bool( bind )

        if utilities.isEmpty( attributeList ) : attributeList = self.attributeList

        if utilities.isEmpty( valueList ) : valueList = self.valueList

        if ( ( utilities.isEmpty( attributeList ) ) or ( utilities.isEmpty( valueList ) ) ) : return [ ]

        if ( not len( attributeList ) == len( valueList ) ) : return [ ]
        

        # specific fields

        self.author = ""

        self.bibtex = ""

        self.description = ""

        self.key = ""

        self.title = ""

        self.year = ""

        # attribute - value lists

        table = [ ]
        
        for index in range( len( attributeList ) )  :

            attribute = utilities.string( attributeList[ index ], format = "identifier", default = "" )

            value = utilities.string( valueList[ index ], default = utilities.voidCode )

            attribute, value = self.normalizeAttributeValue( attribute, value )

            if utilities.isEmpty( attribute ) : continue

            # lines of the table are identifier, type of widget (empty), value

            table.append( [ attribute, utilities.voidCode, value ] )


        # fills context variables from specific fields

        self.setVariables()

        return table

        
        



    def attributeValueListToText (

        self,
        attributes = None,
        values = None,
        bind = True,
        normalize = True
        ) :

        """ Converts a list of lines attribute-value into a text, in BibTex format


            bind means that context variables will be updated

            normalize means that attributes are normalized again

            """

        self.bind = bool( bind )

        if attributes is None : attributes = self.attributeList

        if values is None : values = self.valueList
        
        if not type( attributes ) == list : return ""

        if not type( values ) == list : return ""

        if not len( attributes ) == len( values ) : return ""

        # by default, uses the context variable reference (reference type) to determine the type

        self.referenceType = utilities.getVariable( "type" )

        if not self.referenceType in self.typeList : self.referenceType = self.bibtex

        if not self.referenceType in self.typeList : self.referenceType = "misc"

        # prefix will be added at the end
        
        text = ""

##        print "bibfile.avlistToText"
        
        # lines

        for index in range( len( attributes ) ) :

            attribute = attributes[ index ]

            value = utilities.flatToAscii( values[ index ] )

            
            # not written in output

            if attribute is None : continue

            if attribute == "bibtex"  : continue

            if value is None : continue

            if bool( normalize ) :

                attribute, value = self.normalizeAttributeValue( attribute, value  )
            
                if attribute is None : continue

            # gets the type of reference


            # recodes value in bibtex/latex format, with \ escape sequences (for author, don t convert the tilde - used in initials
            
            value = self.asciiToLatex( value )

            # writes line with attribute = {value}
            
            line = " " + attribute + " = " + '{' + value + '}' + "," + "\n"

            text = text + line

        # prefix

        self.key = self.normalizeKey()

        if utilities.isEmpty( self.key ) : self.key = "REF"
        
        text = "\n @" + \
               self.referenceType + \
               "{" + \
               self.key + \
               "," + \
               "\n" + \
               text

            
        # footer line : close }

        text = text + " }" + "\n\n"

        return text






        
    def bibToAttributeValueList (

        self,
        text = None,
        bind = True
        ) :

        """ Parses a text containing bib information and returns a pair attribute-value

            bind means that context variables will be updated

            """

        self.bind = bool( bind )


        # finds the header

        iPrefix = self.findBibPrefix( text )

        # not found

        if iPrefix < 0 : return [ ], [ ]

        # gets the type

        iKey = text.find( "{", iPrefix )

        if iKey <= iPrefix + 1 : return [ ], [ ]

        bibType = utilities.string( text[ iPrefix + 1 : iKey ], default = "", format = "lower" )

        attributeList = [ "reference" ]

        valueList = [ bibType ]

        # skips BibTeX reference

        iEnd = text.find( ",", iKey )

        if iEnd < 0 : return [ ], [ ]
            
        iLine = text.find( "\n", iEnd )

        if iLine < 0 : return [ ], [ ]
            
        iField = iLine + 1

        quoted = 0

        while True :


            # finds = or close

            iEqual = text.find( "=", iField )

            if iEqual < 0 : break

            # looks for closing key preceding =

            iClose = text.find( "}", iField )

            if ( ( iClose < iEqual ) and ( iClose >= 0 ) ) : break

            attribute = utilities.string( text[ iField : iEqual ], format = "identifier" )

            if utilities.isEmpty( attribute ) : return [ ], [ ]

            # delimitates value

            level = 0

            quotes = 0

            iStart = -1

            iEnd = iEqual + 1

            while True :

                if iEnd >= len( text ) :

                    break

                # initial quote

                elif ( ( text[ iEnd ] == '"' ) and ( iStart < 0 ) ) :

                    iStart = iEnd + 1

                    quoted = 1

                
                # initial opening key :
                
                elif ( ( text[ iEnd ] == "{" ) and ( iStart < 0 ) ) :

                    iStart = iEnd + 1

                    level = level + 1

                # final quote (not counted in intermediary keys )

                elif ( ( text[ iEnd ] == '"' ) and ( level <= 0 ) and ( quoted > 0 ) ) :

                    break
                
                # intermediary keys { }
                
                elif text[ iEnd ] == "{" :

                    level = level + 1

                elif text[ iEnd ] == "}" :

                    level = level - 1

                elif ( ( text[ iEnd ] == "," ) and ( level <= 0 ) and ( quoted <= 0 ) ) :

                    break

                elif ( ( text[ iEnd ] == "\n" ) and ( level <= 0 ) ) :

                    break

                iEnd = iEnd + 1

            if iStart < 0 : iStart = iEqual + 1

            # removes quotes and spaces
            
            value = text[ iStart : iEnd ].lstrip( '" ' ).rstrip( '" ' )

            # normalizes special attributes

            if attribute == "author" : value = self.normalizeAuthor( value )

            elif attribute == "bib" : value = self.normalizePath( value )

            elif attribute == "booktitle" : value = self.normalizeBookTitle( value )

            elif attribute == "editor" : value = self.normalizeEditor( value )

            elif attribute == "file" : value = self.normalizePath( value )

            elif attribute == "journal" : value = self.normalizeJournal( value )

            elif attribute == "month" : value = self.normalizeMonth( value )

            elif attribute == "pages" : value = self.normalizePages( value ).replace( "--", "-" )

##            elif attribute == "zip" : value = self.normalizePath( value )

            elif attribute == "title" : value = self.normalizeTitle( value )
##
            elif attribute == "year" : value = self.normalizeYear( value )

            value = value.strip().replace( "{", "" ).replace( "}", "" )

            attributeList.append( attribute )

            valueList.append( value )

            # goes to the end of line after the comma
            
            iLine = text.find( "\n", iEnd )

            iField = max( iEnd + 1, iLine + 1 )


        return attributeList, valueList

            

        
    def bibToTable (

        self,
        text = None
        ) :

        """ Parses a text containing bib information and returns a pair attribute-value """

        self.attributeList, self.valueList = self.bibToAttributeValueList( text )

        return self.attributeValueListToTable()



    def checkAuthorList (

        self,
        names = None
        ) :

        """ Checks that the author list is composed of pair last-name, initials of first names or vice versa """

        if utilities.isEmpty( names ) : return False

        if len( names ) % 2 : return False

        for index in range( 0, len( names ), 2 ) :

            i0 = names[ index ].find( "." )

            if ( ( i0 >= 0 ) and ( i0 + 1 < len( names[ index ] ) ) ) : return False

            i1 = names[ index + 1 ].find( "." )

            if ( ( i1 >= 0 ) and ( i1 + 1 < len( names[ index + 1 ] ) ) ) : return False
            
            # 2 dotted names = incorrect

            if ( ( i0 >= 0 ) and ( i1 >= 0 ) ) : return False
            

        return True




    
    def checkBib (

        self,
        text = None
        ) :

        """ Checks that a text contains at least one BibTeX record

            Detects headers @type{
            
            Does NOT check correctness of syntax
            
            """

        index = self.findBibPrefix( text )

        return index >= 0






    def checkComplete (

        self,
        fieldList = None
        ) :

        """ checks completion of current attribute value list """

        self.missingList = [ ]

        index = utilities.index( self.typeList, self.bibtex )

        if index < 0 : return False

        if utilities.isEmpty( fieldList ) : fieldList = self.requiredMatrix[ index ]

        # no attributes list

        if utilities.isEmpty( self.attributeList ) :

            self.missingList = fieldList

            return False

        # checks the required attributes
        
        for item in fieldList :

##            name = "reference" + item.capitalize() #**RF
##
##            if not name in self.attributeList : self.missingList.append( item )

            if not item in self.attributeList : self.missingList.append( item )

        return utilities.isEmpty( self.missingList )



    
    def checkTable (

        self,
        table = None
        ) :

        """ Checks that a table contains a BibTeX record

            Detects attribute bibtex
            
            Does NOT check correctness of content
            
            """

        if utilities.isEmpty( table ) : return False


        for line in table :

            if len( line ) < 3 : continue

            identifier = line[ 0 ].lower()

            if identifier == "bibtex" : return True

        return False






        
    def deleteAttribute (

        self,
        attribute = None,
        attributes = None,
        values = None
        ) :

        """ deletes an attribute in self.attributeList, self.valueList

            attributes, values override self.attribute/valueList

            returns True False

            """


        if utilities.isEmpty( attribute ) : return None

        if utilities.isEmpty( value ) : return None

        if attributes is None : attributes = self.attributeList

        if values is None : values = self.valueList


        attribute = utilities.string( attribute , format = "identifier" )

        index = utilities.index( attributes, attribute )

        if index < 0 : return False

        attributes.pop( index )

        values.pop( index )

        return True
            
        

        
        
    def deleteValue (

        self,
        attribute = None,
        attributes = None,
        values = None
        ) :

        """ deletes an attribute in self.attributeList, self.valueList. Aloas of deleteAttribute

            attributes, values override self.attribute/valueList

            returns True False

            """

        return self.deleteAttribute( attribute, attributes, values )





    def findBibPrefix (

        self,
        text = None
        ) :

        """ Returns the position of the header of a bib tex in a text

            Detects headers @type{
            
            Returns -1 if not found position otherwise
            
            """

        if utilities.isEmpty( text ) : return -1

        # looks for a sequence "@bibtype{"

        for prefix in self.typeList :

            index = text.find( "@" + prefix + "{" )

            if index >= 0 : return index

            index = text.find( "@" + prefix.upper() + "{" )

            if index >= 0 : return index

        return -1




    def firstAuthor (

        self,
        text = None
        ) :

        """ returns the 1st author's family name """

        if text is None : text = self.author

        if text is None : return ""

        author = utilities.asciiToPersons( text )

        if len( author ) <= 0 : return ""

        if len( author[ 0 ] ) <= 0 : return ""
        
        author = author[ 0 ][ 0 ].lower()

        author = utilities.string( author, format = "strict" )

        if author.isalpha() : return author
    
        filtered = ""

        for character in author :

            if character.isalpha() : filtered = filtered + character

        return filtered



        
    def getValue (

        self,
        attribute = None,
        attributes = None,
        values = None,
        format = None
        ) :

        """ Returns the value of the "attribute" in the double list attributes-values,

            attributes-values override self.attributeList, self.valueList if they are defined

            the attribute is sought as it or if not found, as referenceAttribute

            if format is
                None,  returns value as it,
                anything else returns a ascii text with esoteric symbols removed ({ } and keyword, ~ etc.

            returns the value or None if problem or not found

            """

        if utilities.isEmpty( attribute ) : return None

        if attributes is None : attributes = self.attributeList

        if values is None : values = self.valueList

        if not type( attributes ) == list : return None

        if not type( values ) == list : return None

        if not len( attributes ) == len( values ) : return None

        index = utilities.index( attributes, attribute )

        # tries with referenceAttribute

        if index < 0 :

##            if attribute.startswith( "reference" ) : return None
##
##            attribute = "reference" + attribute.capitalize() #**RF

            index = utilities.index( attributes, attribute )

            if index < 0 : return None

        value = values[ index ]


        # no formatting

        if format is None : return value

        # formatting

        value = value.replace( "{", "" ).replace( "}", "" ).strip()

        if attribute == "pages" : value = "pp. " + value.replace( "--", "-" )

        elif attribute == "author" : value = value.replace( ".~", "." ).replace( " and ", ", " )

        elif attribute == "editor" : value = value.replace( ".~", "." ).replace( " and ", ", " )

        return value



    def inField (

        self,
        text = None,
        words = None,
        mode = "order"
        ) :

        """ returns True iff all key words (string or list) are in text.

            mode :
            "order" means that they are all present in the same order
            "all" means that they are all present
            other: means that one at least is present


            """

        text = str( text )

##        print "infield", text, words

        if words is None : return True

        if type( words ) == str : words = utilities.textToWords( words )
        
        if len( words ) <= 0 : return True

        index = 0

        for word in words :

            # absent

            if not word in text :

                if ( mode == "all" ) or ( mode == "order" ) : return False

                continue

            # here, the word is in text, but not at the desired position

            iWord = text.find( word, index )

            if iWord < 0 : return False

            # here, it is in text, at the desired position. In whatever order, does nothing

            if mode == "all" : pass

            # in order, increases the desired position

            elif mode == "order" : index = iWord + len( word )

            # finds one, this is it
            
            else : return True

        return True


    def isAbbreviation (

        self,
        text1 = None,
        text2 = None,
        words1 = None,
        words2 = None,
        size1 = None,
        size2 = None,
##        trace = False 
        ) :

        """ checks whether text1 is an abbreviation of text2 

            words1 and words2 are presliced words of each arguments, size1 size2 are the total size of their words.

            if undefined, recomputed here
            
            returns
            0 if not compatible
            1 if compatible, but not a real abbreviation(e.g. , there are trailing words, there are no abbreviations)
            2 if text1 is an abbreviation of text2 (no trailing words, at least 1 abbreviated word)

            """


        if text1 is None : return 0

        if text2 is None : return 0

        # needs normalization (no lists of words as arguments )

        if words1 is None :

            text1 = self.normalizePublication( text1 )

            words1 = self.publicationToWords( text1 )

            size1 = sum( len( word ) for word in words1 )
            

        elif size1 is None : size1 = sum( len( word ) for word in words1 )
            
        if words2 is None :

            text2 = self.normalizePublication( text2 )

            words2 = self.publicationToWords( text2 )

            size2 = sum( len( word ) for word in words2 )

        elif size2 is None : size2 = sum( len( word ) for word in words2 )



        # fast verifications

        if size2 < size1 : return 0
        
        if text2.startswith( text1 ) : return 1

        # searches the abbreviated words in increasing positions (greedy strategy)

        iWord = 0

        result = 1  # for now, compatible but not a true abbreviation

        size = len( words2 )

##        if trace : print "ISABSENTENCE"
        
        for abbreviation in words1 :

            while True :

                # some abbreviation(s) not found
                
                if iWord >= size : return 0

                word = words2[ iWord ]
##
##                if trace: print "  compare", word1, word2 


                iWord = iWord + 1

                # same word: works, but not considered an abbreviation
                
                if abbreviation == word : break

                # true abbreviation

                if self.isAbbreviationWord( abbreviation, word ) : break
                
                # this word cannot be skipped

                if not word in self.omissionList : return 0

            # this abbreviation  is a true abbreviation

            if len( abbreviation ) < len( word ) : result = 2

##            if trace : print abbreviation, word, dot, shorter, trueAbbreviation


        # remaining words: must be short or can be omitted in order to be a true abbreviation

        remainder = False

        for word in words2[ iWord : ] :
            
            # this word cannot be skipped
            
            if not word in self.omissionList :

                remainder = True

                break
                

        # is a true abbreviation, or there are no trailing words: this is it

        if ( result == 2 ) or ( not remainder ) : return result

        # here, compatible nothing more, and there is a remainder: tries to cut it

        iEnd = text2.find( ":" )

        if iEnd < 0 : iEnd = text2.find( "/" )

        if iEnd < 0 : iEnd = text2.find( "(" )

        if iEnd < 0 : iEnd = text2.find( "-" )

        if iEnd < 0 : return result

        else : return max( result, self.isAbbreviation( text1, text2[ : iEnd ], words1, None, size1, None ) )

        



    def isAbbreviationWord (

        self,
        abbreviation = None,
        word = None,
        normalize = None
        ) :

        """ checks whether 1st argument is abbreviation of 2nd

            Arguments are words. No validations of arguments

            returns True/False

            """

        if abbreviation is None : return False

        if word is None : return False

        if bool( normalize ) :

            abbreviation = abbreviation.strip( " .[]{}();:,'" + '"' ).lower()

            word = word.strip( " .[]{}();:,'" + '"' ).lower()

        # particular case: &

        if abbreviation == "&" : abbreviation = "and"

        if word == "&" : word = "and"

        sizeAbbreviation = len( abbreviation )

        sizeWord = len( word )

        # fast verifications

        if sizeAbbreviation == 0 : return False

        if sizeWord < sizeAbbreviation : return False

        if not abbreviation[ 0 ] == word[ 0 ] : return False

        if word.startswith( abbreviation ) : return True

        # determines common part of the word & abbreviation

        for index in range( 1, sizeAbbreviation  ) :

            if not abbreviation[ index ] == word[ index ] : break
        
        
        abbreviation = abbreviation[ index : ]

        word = word[ index : ]

        index = -1

        for character in abbreviation :

            if character in "aeiouy" : return False

            index = word.find( character, index + 1 )

            if index < 0 : return False

        return True


        


    def latexToAscii (

        self,
        text = None
        ) :

        """ converts a latex string with \ sequences into an ascii text """

        if utilities.isEmpty( text ) : return ""

        # converts the escape sequences of accents

        if "{\\" in text :

            size = len( self.escapeTable )

            for index in range( 1, size, 2 ) :

                escape = self.escapeTable[ index - 1 ]

                character = self.escapeTable[ index ]

                text = text.replace( escape, character )


        # removes the remaining protection characters and the delimiters

        text = text.\
               replace( "\\", "").\
               replace( "{", "" ).\
               replace( "}", "" ).\
               replace( "\t", " " ).\
               replace( "\n", " " ).\
               strip( " " )
               
##               strip( '"' ).\
##               strip( " '\t.;:,{}" )

        return text


    
    def lineToAttributeValue (

        self,
        text = None
        ) :

        """ Parses a line and returns a pair attribute - value """

        if utilities.isEmpty( text ) : return None, None

        text = text.strip()

        # this is a first line

        if text.startswith( "@" ) :

            index = text.find( "{" )

            if index < 0 : return None, None

            attribute = "reference"

            value = text[ 1 : index ].strip()

            return attribute, value

        # this is a last line

        if text == "}" :

            return None, None

        # normal line : should contain attribute = 

        iSeparator = text.find( "=" )

        # ... otherwise looks for first space, tab or comma

        if iSeparator >= 0 : index = iSeparator

        elif " " in text : index = text.find( " " )

        elif "\t" in text : index = text.find( "\t" )

        elif "," in text : index = text.find( "," )

        elif ":" in text : index = text.find( ":" )

        elif ";" in text : index = text.find( ";" )

        elif "." in text : index = text.find( "." )

        else : return None, None

        # gets the word -> 1st delimiter

        attribute = text[ : index ]

        # no formal separator ( = ) dot or delimiter inside, splits there, e.g. vol.12, pp.22 33

        if iSeparator < 0 :

            underscored = utilities.string( attribute, format = "strictunderscore" )

            iSeparator = underscored.find( "_" )

            if iSeparator > 0 :
                
                index = iSeparator

                attribute = text[ : index ]

        # normalizes attribute
        
        attribute = utilities.string( attribute , format = "strict" )

        attribute = attribute.strip()

        if len( attribute ) <= 0 : return None, None

        # value = remainder of the line
        
        value = text[ index + 1 : ]

        # removes the protection symbols '{' and '}' from the value

        value = self.latexToAscii( value )

        # strips trailing commas and spaces and quotes

        return attribute, value






    def listToAscii (

        self,
        textList = None,
        stateList = None,
        bind = True
        ) :

        """ converts a pair of lists text + state into a flat BiBTex text

            bind means that context variables will be updated

            """

        self.bind = bool( bind )
               
        if ( ( utilities.isEmpty( textList ) ) or ( utilities.isEmpty( stateList ) ) ) : return ""

        attributeList = [ ]

        valueList = [ ]

        for index in range( len( textList ) ) :

            state = stateList[ index ]

            line = textList[ index ]

            # only plain text
            
            if not utilities.isEmpty( state ) : continue

            words = line.split( utilities.fieldDelimiter ) ##***EF

            if len( words ) <= 1 : continue

            attribute = words[ 0 ]

            if utilities.isEmpty( attribute ) : continue

            if len( words ) >= 3 : value = words[ 2 ]
              
            else : value = words[ 1 ]

            if utilities.isEmpty( value ) : continue

            attributeList.append( attribute )

            valueList.append( value )

        text = self.attributeValueListToText( attributeList, valueList )

        return text




    def normalizeAttributeValue (

        self,
        attribute = None,
        value = None
        ) :

        """ normalizes a pair attribute value """
      
        if ( ( utilities.isEmpty( attribute ) ) or ( utilities.isEmpty( value ) ) ) : return None, None

        attribute = utilities.string( attribute, format = "identifier" )

        if attribute == "reference" : pass

        elif attribute == "bibtex" : pass

        elif attribute in self.aliasDictionary : attribute = self.aliasDictionary[ attribute ]

        elif attribute in self.fieldList : pass

        else : return None, None

        # first normalization of value: removes external {}, quotes, and strips spaces

        value = value.strip( ";,: /\\" )

        size = len( value )

        while True : 

            if value.startswith( "{" ) and value.endswith( "}" ) : value = value[ 1 : -1 ]
            
            if value.startswith( "(" ) and value.endswith( ")" ) : value = value[ 1 : -1 ]
            
            if value.startswith( "[" ) and value.endswith( "]" ) : value = value[ 1 : -1 ]
            
            if value.startswith( '"' ) and value.endswith( '"' ) : value = value[ 1 : -1 ]

            if value.startswith( "'" ) and value.endswith( "'" ) : value = value[ 1 : -1 ]

            value = value.strip( ";,: /\\" )

            if len( value ) == size : break

            size = len( value )

        # normalizes fields
        
        if attribute == "author" :

            value = self.normalizeAuthor( value )

            self.author = value

        elif ( ( attribute == "reference" ) or ( attribute == "bibtex" ) ) :

            attribute = "bibtex"

            value = utilities.string( value, format = "identifier" )
       
            self.bibtex = value

        elif attribute == "booktitle" : value = self.normalizeBookTitle( value )

        elif attribute == "description" :

            value = self.normalizeDescription( value )

            self.description = value

        elif attribute == "editor" : value = self.normalizeEditor( value )

        elif attribute == "journal" : value = self.normalizeJournal( value )

        elif attribute == "month" : value = self.normalizeMonth( value )

        elif attribute == "pages" : value = self.normalizePages( value )

        elif attribute == "title" :

            value = self.normalizeTitle( value )

            self.title = value

        elif attribute == "year" :

            value = self.normalizeYear( value )

            self.year = value

##        elif attribute == "bib" :
##
##            value = self.normalizePath( value )
##
##            self.bibPath = value

        elif attribute == "file" :

            value = self.normalizePath( value )

            self.filePath = value
            
        elif attribute == "owner" :

            value = utilities.string( value, format = "title" )

            self.owner = value

        # other values: strips delimiters
        
        else : value = str( value ).strip( " ()[].;:,/\\{}-_" )



        # cleans value

##        print "normalize", str( attribute), str( value )

        value = value.strip().replace( "{", "" ).replace( "}", "" )

##        # recodes attribute: reference becomes bibtex and the remainder has a prefix reference **RF
##
##        if ( ( not attribute == "bibtex" ) and ( not attribute.startswith( "reference" ) ) ) :
##
##            attribute = "reference" + utilities.string( attribute, format = "class" )

        return attribute, value





        
    def normalizeAuthor (

        self,
        text = None
        ) :

        """ Normalizes a list of authors """

##        print "normalizeAuthor", text

        # removes digits and parentheses ( probably come from the year , e.g., zozo, l. (1983) )

        if text is None : return ""

        text = text.strip( " {}()[]0123456789-"  )
        
        return utilities.personsToAscii( text )




    def normalizeBookTitle (

        self,
        text = None
        ) :

        """ Normalizes the title of a book. Removes initial in: from> etc """

        text = self.normalizeTitle( text )

        text = self.normalizeSeparators( text )

        for bit in [ "in", "from", "In", "From" ] :

            if text.startswith( bit ) :

                text = text[ len( bit ) : ]

                break

        return self.normalizeTitle( text )
        

        


    def normalizeDescription (

        self,
        value = None
        ) :

        """ normalizes the description field """

        if utilities.isEmpty( value ) : return ""

        return utilities.string( value.replace( "{", "" ).replace( "}", "" ), format = "sentence" )





    def normalizeEditor (

        self,
        text = None
        ) :

        """ Normalizes a list of editors. removes keywords ed, eds ed. eds. """

##        print "normalizeAuthor", text

        if utilities.isEmpty( text ) : return ""

        text = text.strip( "{}()[].;,: " )

        # removes prefixes ed, eds, etc.

        for bit in [ "editors", "editor", "eds", "eds.", "ed", "ed." ] :

            if text.startswith( bit + " " ) :

                text = text[ len( bit ) + 1 : ]

                break

        # removes suffixes ed, eds, etc.

        for bit in [ "editors", "editor", "eds", "eds.", "ed", "ed." ] :
            
            if text.endswith( "  " + bit ) :

                text = text[ : - len( bit ) - 1 ]

                break

        return utilities.personsToAscii( text )


        
    def normalizeJournal (

        self,
        text = None
        ) :

        """ Normalizes a journal's name. """

        return self.normalizeTitle( text )
                



    def normalizeKey ( self ) :

        """ normalizes the key from the fields ( the key is the unique name of the shared item, in bookcase ) """


        # normalizes first author
        
        author = self.firstAuthor( self.author )        

        key = utilities.pathShared(
            category = self.bibtex,
            author = author,
            year = self.year,
            title = self.title
            )

        # takes  name and removes double underscores
        
        key = utilities.pathName( key ).replace( "__", "_" ).strip( " _" )

        return key




        
    def normalizeMonth (

        self,
        text = None
        ) :

        """ Normalizes the month """


        if text is None : return ""

        elif not type( text ) == str : text = str( text )

        elif len( text ) <= 0 : return "" 

        # strips and replace intermediate separators (if there are some ) by spaces, then removes any weird character
        
        text = utilities.split( text.strip( " ;,.:-_/{}()[]" ) )

        text = utilities.string( text, format = "strict" )

        # several words, leaves as it (there will be a normalization of month year later)
        
        if " " in text : return text

        # otherwise, month

        value = utilities.integer( text )

        # it is probably a string
        
        if value is None : return text

        # invalid integer

        elif ( value <= 0 ) or ( value > 12 ) : return ""

        # returns month's identifier (alpha)
        
        else : return str( self.monthList[ value - 1 ] ).capitalize()

               


    def normalizeMonthYear (

        self,
        month = None,
        year = None
        ) :


        """ Verifies the attributes month/year (often given together )
            
            returns True iff did something
            
        """

        if utilities.isEmpty( month ) : month = ""

        if utilities.isEmpty( year ) : year = ""

        if utilities.isEmpty( month ) : text = year

        elif utilities.isEmpty( year ) : text = month

        else : text = month + " " + year

        # places spaces and separates


        # strips and replace intermediate separators (if there are some ) by spaces, removes any weird character

        text = text.strip( " ;,.:-_/{}()[]" )

        text = utilities.string( text, format = "strict" )

        text = utilities.split( text )

        words = utilities.textToWords( text )

        month = None

        year = None

        possible = None

        for word in words :

            word = word.strip( "/-_\\+,.;:|" ).lower()

##            print "       checks ", word,

            if word in self.monthList :

                month = word

##                print " found month", month, year

                continue

            value = utilities.integer( word )

            if value is None : possible = value

            elif value <= 0 : pass

            elif not month is None : year = value

            elif value > 12 : year = value

            else : month = self.monthList[ value - 1 ]

##            print "  other", month, year

        if ( month is None ) and ( not possible is None ) : month = possible

        if year is None : pass

        elif year < 100 : year = self.normalizeYear( year )

        else : year = str( year )

        if not month is None : month = month.capitalize()

        return month, year
    


        
    def normalizePages (

        self,
        text = None
        ) :

        """ Normalizes the page numbers """

        if utilities.isEmpty( text ) : return ""

        # removes keywords p. pp. to etc.

        for bit in [ "pp.", "p.", "&", "-", " to ", " and " ] :

            text = text.replace( bit, " " )
##
##        text = text.\
##                replace( "pp.", " " ).\
##                replace( "p.", " " ).\
##                replace( " to ", " " ).\
##                replace( "&", " " ).\
##                replace( " and ", " " ).\
##                replace( "-", " " )

        text = utilities.string( text, format = "strict" )

        # splits into words
        
        words = utilities.textToWords( text )

        if utilities.isEmpty( words ) : return ""

        # joins consecutive integers or non-integers with --

        text = words[ 0 ]

        previous = words[ 0 ].isdigit()

        minus = False

        for word in words[ 1 : ] :

            isdigit = word.isdigit() 

            minus = ( not minus ) and ( previous == isdigit )

            previous = isdigit

            if minus : text = text + "--"

            else : text = text + " "

            text = text + word

        return text.strip()



        
    def normalizePath (

        self,
        text = None
        ) :

        """ Normalizes a file: uses / instead of os.sep, removes the bookcase if file is already shared """

        if utilities.isEmpty( text ) : return ""

        text = utilities.slashPath( text )

        if sys.platform == "win32" : text = text.lower()

        bookcase = utilities.getVariable( "bookcase", default = "" )

        if utilities.isEmpty( bookcase ) : return text

        # normalizes prefix, removes bookcase if path starts with it
        
        bookcase = utilities.slashPath( bookcase ).strip( "/" )

        if sys.platform == "win32" : bookcase = bookcase.lower()

        if text.startswith( bookcase ) : text = text[ len( bookcase ) : ].lstrip( "/" )

        return text






    def normalizePublication (

        self,
        text = None
        ) :

        """ normalizes the title of a journal or a 'inbook' (e.g., proceedings) """

        if text is None : return ""

        text = text.\
               replace( "'", " " ).\
               replace( '"', " " ).\
               replace( "\t", " " ).\
               replace( ".", ". " ).\
               replace( ",", ", " ).\
               replace( ":", ": " ).\
               replace( ";", "; " ).\
               replace( "-", " - " ).\
               replace( "(", " ( " ).\
               replace( ")", " ) " ).\
               replace( "[", " ( " ).\
               replace( "]", " ) " ).\
               replace( "{", " ( " ).\
               replace( "}", " ) " ).\
               replace( "/", "/ " ).\
               replace( "\\", "\\ " ).\
               strip()


        size = len( text )

        while True :

            text = text.\
                   replace( "  ", " " ).\
                   replace( " .", "." ).\
                   replace( " ,", "," ).\
                   replace( " ;", ";" ).\
                   replace( " :", ":" ).\
                   replace( ",,", "," ).\
                   replace( ",;", "," ).\
                   replace( ",:", "," ).\
                   replace( ",.", "," ).\
                   replace( ";,", ";" ).\
                   replace( ";;", ";" ).\
                   replace( ";:", ";" ).\
                   replace( ";.", ";" ).\
                   replace( ":,", ":" ).\
                   replace( ":;", ":" ).\
                   replace( "::", ":" ).\
                   replace( ":.", ":" )

            if len( text ) == size : break

            size = len( text )

        text = text.strip( " .;,:-_" )

        return text





    def normalizePublisher (

        self,
        text = None
        ) :

        """ normalizes the name of a publisher """

        return self.normalizePublication( text )

    

    def normalizeSeparators (

        self,
        text = None
        ) :

        """ normalizes the separators (double spaces, ;. etc. """

        if text is None : return ""

        text = text.\
               replace( "\t", " " ).\
               replace( ",", ", " ).\
               replace( ":", ": " ).\
               replace( ";", "; " ).\
               replace( "[", "(" ).\
               replace( "]", ")" ).\
               strip()


        size = len( text )

        while True :

            text = text.\
                   replace( "  ", " " ).\
                   replace( " .", "." ).\
                   replace( " ,", "," ).\
                   replace( " ;", ";" ).\
                   replace( " :", ":" ).\
                   replace( ",,", "," ).\
                   replace( ",;", "," ).\
                   replace( ",:", "," ).\
                   replace( ",.", "," ).\
                   replace( ";,", ";" ).\
                   replace( ";;", ";" ).\
                   replace( ";:", ";" ).\
                   replace( ";.", ";" ).\
                   replace( ":,", ":" ).\
                   replace( ":;", ":" ).\
                   replace( "::", ":" ).\
                   replace( ":.", ":" )

            if len( text ) == size : break

            size = len( text )

        text = text.strip( " .;,:-_" )

        # missing parentheses

        closing = text.count( "(" ) - text.count( ")" )

        if closing > 0 : text = text + ( closing * ")" )

        elif closing < 0 : text = ( ( - closing ) * "(" ) + text
        
        return text

    
        

    def normalizeTitle (

        self,
        text = None
        ) :

        """ Normalizes the title """

        text = self.normalizeSeparators( text )

        if len( text ) == 0 : return ""

        return "{" + text[ 0 ].upper() + text[ 1 : ] + "}"

##        return utilities.string( text.strip( " ;,.:-_" ), format = "sentences" )



    def normalizeVolumeNumber (

        self,
        volume = None,
        number = None
        ) :


        """ Verifies the attributes volume / number (often, the volume contains the number, e.g. 12(3)
            
            returns True iff did something
            
        """

        if utilities.isEmpty( volume ) : volume = ""

        if utilities.isEmpty( number ) : number = ""

        volume = volume.\
                 strip().\
                 replace( "[", "(" ).\
                 replace( "]", ")" )
    
        number = number.\
                 strip().\
                 replace( "[", "(" ).\
                 replace( "]", ")" )
                 

        if utilities.isEmpty( number ) : text = volume

        elif utilities.isEmpty( volume ) : text = number

        else : text = volume + " " + number

        text = self.normalizeSeparators( text )


        # no parentheses: looks for spaces, - and / ...number may be the second word

        if "(" in text : iFirst = text.rfind( "(" )

        elif "-" in text : iFirst = text.rfind( "-" )

        elif "/" in text : iFirst = text.rfind( "/" )

        elif " " in text : iFirst = text.rfind( " " )

        # no space, no -, no number

        else : return text.strip( " -_/" ), "" 


        # gets the numbers between parentheses

        if ")" in text : iLast = text.rfind( ")" )

        else : iLast = len( text )

        number = text[ iFirst + 1 : iLast ].strip()

##        print "normalizeVolumeNumber", text, "num", number
        

        # checks the number: digits, space or -. Anything else, returns volume and no number

        for character in number :

            if not character in "0123456789 -," : return text, ""
        
        # removes from volume

        volume = text[ : iFirst ] + text[ iLast + 1 : ]

        volume = volume.strip( " -_/" )
        
        return volume, number

        



        
    def normalizeYear (

        self,
        text = None
        ) :

        """ Normalizes the year """


        if text is None : return ""

        elif not type( text ) == str : text = str( text )

        elif len( text ) <= 0 : return "" 

        # strips and replace intermediate separators (if there are some ) by spaces, removes any weird character

        text = text.strip( " ;,.:-_/{}()[]" )

        text = utilities.string( text, format = "strict" )
        
        text = utilities.split( text )

        # several words, leaves as it (there will be a normalization of month year later)
        
        if " " in text : return text

        # otherwise, date

        year = utilities.integer( text )

        if year is None : return ""

        # normalizes the years expressed with 2 digits

        # 00..09..

        if year <= self.thisYear : return str( self.thisCentury + year )

        # 39, 45...

        elif year <= 100 : return str( self.thisCentury - 100 + year )

        # normal

        else : return str( year )
               

     
                               
    def publicationToWords (
        
        self,
        text = None,
        ) :

        """ normalizes a title to detect abbreviations """

        text = self.separatorsToSpaces( text )

        if len( text ) == 0 : return [ ]

        # this is an acronym

        if ( text.isupper() ) and ( text.isalpha() ) and ( not " " in text ) :

            return list( character.lower() for character in text )

        # normal

        words = [ ]

        for word in utilities.textToWords( text.lower() ) :

            if word == "" : continue

            # & : as it

            if word == "&" : words.append( word )

            # removes accents

            else : words.append( utilities.normalized( word ) )

        return words
        



    def read (

        self,
        path = None,
        text = None,
        bind = True
        ) :

        """ Reads a bib file "path" and initializes self.attributeList, self.valueList and self.text from file.

            bind True means that context variables will be updated
           
            
            """

       
        if not text is None : self.text = utilities.string( text )

        else : self.text = utilities.fileRead( path )

        self.attributeList, self.valueList = self.textToAttributeValueList( self.text, bind = bind )

        return not utilities.isEmpty( self.text )



    def readTable (

        self,
        path = None,
        bind = True
        
        ) :

        """ reads a bib file and returns a table composed of pairs attribute-value

            bind means that context variables will be updated


        """

        self.bind = bool( bind )
        
        self.read( path )

        if utilities.isEmpty( self.attributeList ) : return [ ]

        table = [ ]

        for index in range( len( self.attributeList ) ) :

            table.append( [ self.attributeList[ index ], self.valueList[ index ] ] )

        return table




    def reducedPublication (

        self,
        text = None
        ) :

        """ returns a publication in reduced mode, lower case, no accents, and omitted words (e.g. articles) removed """

        text = self.separatorsToSpaces( text )

        if len( text ) == 0 : return ""

        result = ""

        # this is an acronym

        if ( text.isupper() ) and ( text.isalpha() ) and ( not " " in text ) :

            for character in text :

                result = result + character.lower() + " "


        # normal

        else :

            for word in utilities.textToWords( text ) :

                if word == "" : continue

                if ( not word.isupper() ) and ( word in self.omissionList ) : continue

                # removes accents

                result = result + utilities.normalized( word ).lower() + " "

        return result.strip()



        
    def reducedPublisher (

        self,
        text = None
        ) :

        """ returns a publisher in reduced mode, lower case, no accents """

        text = self.separatorsToSpaces( text )

        if text is None : return ""

        result = ""

        for word in utilities.textToWords( text ) :

            if word == "" : continue

            if ( not word.isupper() ) and ( word in self.omissionList ) : continue

            # removes accents

            result = result + utilities.normalized( word ).lower() + " "

        return result.strip()



    
        


    def resetData ( self ) :

        """ Empties the data structure """
        
        self.attributeList = [ ]

        self.valueList = [ ]
        


    def separatorsToSpaces (

        self,
        text = None
        ) :

        """ transforms all separators into spaces """

        if text is None : return ""

        text = text.\
               replace( '.', " " ).\
               replace( '"', " " ).\
               replace( "'", " " ).\
               replace( "-", " " ).\
               replace( ";", " " ).\
               replace( ":", " " ).\
               replace( ",", " " ).\
               replace( "(", " " ).\
               replace( ")", " " ).\
               replace( "[", " " ).\
               replace( "]", " " ).\
               replace( "{", " " ).\
               replace( "}", " " ).\
               replace( "/", " " ).\
               replace( "\\", " " )

        return text
    

        
        
        
    def setAttribute (

        self,
        attribute = None,
        value = None,
        attributes = None,
        values = None
        ) :

        """ appends and/or replace a pair attribute-value to/in self.attributeList, self.valueList

            attributes, values override self.attribute/valueList

            returns the index in the lists or None
            
            """

        if utilities.isEmpty( attribute ) : return None

        if utilities.isEmpty( value ) : return None

        if attributes is None : attributes = self.attributeList

        if values is None : values = self.valueList


        attribute = utilities.string( attribute , format = "identifier" )

        index = utilities.index( attributes, attribute )

##        if attribute == "bibtex" : referenceAttribute = attribute #**RF
##
##        elif attribute.startswith( "reference" ) : referenceAttribute = attribute
##
##        else : referenceAttribute = "reference" + attribute.capitalize()
##
##        index = utilities.index( attributes, referenceAttribute )
##
##        if index < 0 : index = utilities.index( attributes, attribute )

        if index < 0 :
            
##            attributes.append( referenceAttribute ) #**RF

            attributes.append( attribute )

            values.append( None )

            index = -1

        values[ index ] = value

        return index





    def setAttributes (

        self,
        owner = None,        
        filePath = None,
        bibtex = None,
        key = None
        ) :

        """ sets the paths to bib file & the item,  sets the variables and the attribute-value list """


        # in case
        
        if utilities.isEmpty( self.attributeList ) : self.attributeList = [ ]

        if utilities.isEmpty( self.valueList ) : self.valueList = [ ]

        if not utilities.isEmpty( filePath ) :

            self.filePath = self.normalizePath( filePath )

            self.setAttribute( "file", self.filePath )

        if not utilities.isEmpty( owner ) :

            self.owner = utilities.string( owner, format = "title", default = "" )

            self.setAttribute( "owner", self.owner )

        if not utilities.isEmpty( bibtex ) :

            self.bibtex = str( bibtex )

            self.setAttribute( "bibtex", self.bibtex )

        if not utilities.isEmpty( key ) :

            self.key = str( key )



        

    def setDefault ( self ) :

        """ sets default values """

        # this year and century

        year = int( clock.today( format = "%Y" ) )

        self.thisYear = year % 100

        self.thisCentury = year - self.thisYear


        
        # list of bibtex fields

        self.fieldList = [ ]

        for items in self.fieldMatrix :

            for item in items :

                if not item in self.fieldList : self.fieldList.append( item )

        self.fieldList.sort()

        # list of months

        if ( not type( self.monthList ) == list ) or ( not len( self.monthList ) == 12 ) :

            self.monthList = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec" ]

        # list of words that can be omitted from publication's name (journal, booktitle )

        if not type( self.omissionList ) == list :
            
            self.omissionList = [
                "part",
                "series",
                "volume"
                ]




    def setDictionaries (

        self,
        publications = None,
        publishers = None
        ) :

        """ sets the dictionaries of publications and publishers

            also sets the list of publishers (reduced form) to determine the key of publisherDictionary from a field

            """

        # publications
        
        if type( publications ) == dict :

            self.publicationDictionary = publications
            

        # publishers
        
        if type( publishers ) == dict :

            if not self.publisherDictionary == publishers : self.publisherList = publishers.keys()

            self.publisherDictionary = publishers


        

    def setValue (
        
        self,
        attribute = None,
        value = None,
        attributes = None,
        values = None
        ) :

        """ alias for setAttribute. appends and/or replace a pair attribute-value to/in self.attributeList, self.valueList

            returns the index in the lists or None
            
            """

        return self.setAttribute( attribute, value, attributes, values )


        
        
    def setVariables ( self ) :

        """ sets context variables from attributes, completes the fields """


        # combines the key, description and year into a reference key

        self.key = self.normalizeKey()

        # no binding
        
        if not bool( self.bind ) : return

        if not utilities.isEmpty( self.author ) : utilities.setVariable( "author", self.author.replace( "{", "" ).replace( "}", "" ) )

        if not utilities.isEmpty( self.bibtex ) : utilities.setVariable( "type", self.bibtex )

        if not utilities.isEmpty( self.description ) : utilities.setVariable( "description", self.description )
        
        if not utilities.isEmpty( self.title ) : utilities.setVariable( "title", self.title.replace( "{", "" ).replace( "}", "" ) )
        
        if not utilities.isEmpty( self.year ) : utilities.setVariable( "year", self.year )
        




    def standardize (

        self,
        publications = None,
        publishers = None
        ) :

        """ standardizes the fields using dictionaries

            returns True if modified some field
            
            """

        # sets dictionaries (if defined )

        self.setDictionaries( publications, publishers )

        # journal and booktitle
        
        ok1 = self.standardizePublication( "journal" )

        ok2 = self.standardizePublication( "booktitle" )

        # publisher

        ok3 = self.standardizePublisher( "publisher" )

        # tries to standardize the editor (may be confused with publisher )
        
        ok4 = self.standardizePublisher( "editor" )

        # if this is the case, permutes

        if ok4 and not ok3 :

            editor = self.getValue( "editor", format = "ascii" )

            publisher = self.getValue( "publisher", format = "ascii" )

            self.setValue( "publisher", self.normalizePublisher( editor ) )

            self.setValue( "editor", self.normalizeEditor( publisher ) )

        return ok1 or ok2 or ok3 or ok4




    def standardizePublication ( 

        self,
        attribute = None,
        ) :

        """ standardizes the publication, journal or booktitle

            returns True if the pub title is standard (or was already standard)
            
            """
        
        title = self.getValue( attribute )

        if utilities.isEmpty( title ) : return False
        
        if self.publicationDictionary is None : return False

        reduced = self.reducedPublication( title )

        if not reduced in self.publicationDictionary : return False

        standard = self.publicationDictionary[ reduced ]

        if not type( standard ) == str : return False

        if standard == title : return True

##        print "standardize", attribute, "->", standard
##
##        utilities.fileAppend( "standardizePublication.tsv", attribute + "\t" + standard + "\n" )

        self.setValue( attribute, standard )

        return True



    def standardizePublisher (

        self,
        attribute = None,
        ) :

        """ standardizes the publisher

            returns True if the publisher is standard (or was already standard)

        """

        title = self.getValue( attribute )

        if utilities.isEmpty( title ) : return False

        if self.publisherDictionary is None : return False

        reduced = self.reducedPublisher( title )

        if reduced in self.publisherDictionary :

            found = True

        else :

            found = False

            for item in self.publisherList :

                if self.inField( reduced, item ) :

                    reduced = item

                    found = True

                    break

        if not found : return False

        standard = self.publisherDictionary[ reduced ]

##        print "standardize", attribute, "->", reduced, standard

        self.setValue( attribute, standard )

        if not type( standard ) == str : return False


        return True

        

            


    def tableToAttributeValueList (

        self,
        table = None,
        bind = True
        ) :

        """ Normalizes the entry table

            bind means that context variables will be updated

        """

        if utilities.isEmpty( table ) : return [ ], [ ]

        self.bind = bool( bind )

        # specific fields
       
        self.author = ""

        self.bibtex = ""

        self.description = ""

        self.key = ""

        self.title = ""

        self.year = ""

        # attribute - value lists

        attributeList = [ ]

        valueList = [ ]

##        print "bibfile.tableToAV", table
        
        for line in table :

            if not type( line ) == list : line = utilities.asciiToLines( line )

            if utilities.isEmpty( line ) : continue

            size = len( line )
            
            if size < 2 : continue

            attribute = utilities.string( line[ 0 ], format = "lower", default = "" )

            if utilities.isEmpty( attribute ) : continue

##            # attributes has a prefix ( from electronic form identifiers ) : removes it **RF
##
##            if attribute.startswith( "reference" ) : attribute = attribute.replace( "reference", "" )

##            value = utilities.listToText( line[ 2 : 2 ] )

            # according to line size: simple LAV attribute-value, form data attribute-type-value-date

            if size <= 2 : value = utilities.flatToAscii( line[ 1 ] )

            else : value = utilities.flatToAscii( line[ 2 ] )
            
            if utilities.isEmpty( value ) : continue

            packedValue = value.replace( " ", "" )

##            print "  ", attribute, value, packedValue, attribute in self.fieldList

            if attribute == "pages" : value = self.normalizePages( value )

            elif attribute == "bib" : value = self.normalizePath( value )

            elif attribute == "file" : value = self.normalizePath( value )

            elif attribute == "author" : value = self.normalizeAuthor( value )

            elif attribute == "booktitle" : value = self.normalizeBookTitle( value )

            elif attribute == "editor" : value = self.normalizeEditor( value )

            elif attribute == "journal" : value = self.normalizeJournal( value )

            elif attribute == "month" : value = self.normalizeMonth( value )

            elif attribute == "title" : value = self.normalizeTitle( value )

            elif attribute == "year" : value = self.normalizeYear( value )

            
            
            
            # other fields : encloses in "{", in case

            elif ( ( not packedValue.isalnum() ) and ( not packedValue.islower() ) ) :

                value = "{" + \
                        value.strip( " ;,.:-_{}" ) + \
                        "}"


            # this is a field, e.g. NOT a reserved keyword bibtex, prefix, or a comment #.

            if attribute in self.fieldList :

                attributeList.append( attribute )

                valueList.append( value )

            # fills specific fields
           
            # author

            if attribute == "author" : self.author = value.replace( "{", "" ).replace( "}", "" )

            # year

            elif attribute == "year" : self.year = value.strip( "{}" )

            # description

            elif attribute == "description" : self.description = self.normalizeDescription( value )

            # title
            
            elif attribute == "title" : self.title = self.normalizeTitle( value )
                    
            # bib tex reference

            elif ( ( attribute == "reference" ) or ( attribute == "bibtex" ) ) : self.bibtex = utilities.string( value, format = "identifier" )

##            # path to bib
##
##            elif attribute == "bib" : self.bibPath = value

            # path to file

            elif attribute == "file" : self.filePath = value

##            # path to zip
##
##            elif attribute == "zip" : self.zipPath = value
##

        # normalizations using multiple fields. Only now, when the attribute value list is completed

        volume = self.getValue( "volume", attributeList, valueList )

        number = self.getValue( "number", attributeList, valueList )

        if ( not utilities.isEmpty( volume ) ) or ( not utilities.isEmpty( number ) ) :

            volume, number = self.normalizeVolumeNumber( volume, number )

            self.setValue( "volume", volume, attributeList, valueList )

            self.setValue( "number", number, attributeList, valueList )


        year = self.getValue( "year", attributeList, valueList )

        month = self.getValue ("month", attributeList, valueList )

        if ( not utilities.isEmpty( year ) ) or ( not utilities.isEmpty( month ) ) :

            month, year = self.normalizeMonthYear( month, year )

##            print "  ->", month, year

            self.setValue( "month", month, attributeList, valueList )

            self.setValue( "year", year, attributeList, valueList )


        author = self.getValue( "author", attributeList, valueList )

        editor = self.getValue ("month", attributeList, valueList )

        if ( not utilities.isEmpty( editor ) ) and ( editor == author ) : self.deleteValue( "editor" )

        # fills context variables from specific fields

        self.setVariables()

        return attributeList, valueList



    def tableToBib (

        self,
        table = None,
        bind = True
        ) :

        """ Converts a table into a BibTeX text

            bind means that context variables will be updated


            """

        self.bind = bool( bind )

        # normalize the entry table

        self.attributeList, self.valueList = self.tableToAttributeValueList( table )

        self.text = self.attributeValueListToText( self.attributeList, self.valueList )

        return self.text
        


    def textToAttributeValueList (

        self,
        text = None,
        bind = True
        ) :

        """ Parses a text and converts it into a pair of lists attributes -values

            bind means that context variables will be updated

            """

        # there is some record in bib firmat in this text, parses it

##        if self.findBibPrefix( text ) >= 0 : return self.bibToAttributeValueList( text )
##

        self.bind = bool( bind )

        # specific fields

        self.author = ""

        self.bibtex = ""

        self.description = ""

        self.key = ""

        self.title = ""

        self.year = ""
        
        # a text coming from a table file
        
        if utilities.isEmpty( text ) : return [], []
       
        lines = utilities.asciiToLines( text )

        if utilities.isEmpty( lines ) : return [], []

        attributes = []

        values = []

        for line in lines :

            attribute, value = self.lineToAttributeValue( line )

            attribute, value = self.normalizeAttributeValue( attribute, value )

            if utilities.isEmpty( attribute ) : continue

            if utilities.isEmpty( value ) : continue

            if attribute in attributes : continue

            attributes.append( attribute )

            values.append( value )

        # normalizations using multiple fields. Only now, when the attribute value list is completed


        volume = self.getValue( "volume", attributes, values )

        number = self.getValue( "number", attributes, values )

        if ( not utilities.isEmpty( volume ) ) or ( not utilities.isEmpty( number ) ) :

            volume, number = self.normalizeVolumeNumber( volume, number )

            self.setValue( "volume", volume, attributes, values )

            self.setValue( "number", number, attributes, values )


        year = self.getValue( "year", attributes, values )

        month = self.getValue ("month", attributes, values )

        if ( not utilities.isEmpty( year ) ) or ( not utilities.isEmpty( month ) ) :

            month, year = self.normalizeMonthYear( month, year )

##            print "  ->", month, year

            self.setValue( "month", month, attributes, values )

            self.setValue( "year", year, attributes, values )


        author = self.getValue( "author", attributes, values )

        editor = self.getValue ("month", attributes, values )

        if ( not utilities.isEmpty( editor ) ) and ( editor == author ) : self.deleteValue( "editor" )

        # sets external variables
        
        self.setVariables()

        return attributes, values
       


    def write (
        
        self,
        path = None,
        table = None,
        bind = True,
        normalize = False
        ) :

        """ Alias for write table Writes a matrix of values, i.e. a table file

            bind means that context variables will be updated

            normalize means that values are normalized before writing
      
            Returns True/False

            """

        ok = self.writeTable(
            path = path,
            table = table,
            bind = bind,
            normalize = normalize
            )


        return ok



    def writeTable (
        
        self,
        path = None,
        table = None,
        bind = True,
        normalize = None
        ) :

        """ Writes a matrix of values, i.e. a table file

            bind means that context variables will be updated

            normalize means that values are normalized before writing
      
            Returns True/False

            """


        # if there is an argument, reads the entry table otherwise take current attribute-value list

        if not utilities.isEmpty( table ) :

            self.attributeList, self.valueList = self.tableToAttributeValueList( table, bind = bind )

        self.text = self.attributeValueListToText(
            self.attributeList,
            self.valueList,
            bind = bind,
            normalize = normalize
            )

        ok = utilities.fileWrite( path, self.text )

        return ok







# -----------------------------------
# creates the global singleton object if not already here
#

if not "bibFile" in globals() : bibFile = BibFile()
         
        

