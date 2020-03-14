
""" Miscellaneous methods for texts (strings) processing.

    """


import os

import re


class Texts :


    """ Miscellaneous methods for texts (strings) processing.

        """

    # characters normalization table

    characterTable = None


    # delimiters of comments

    commentDelimiterList = [
        "#",
        "\n"
        ]
    
    
    # list of codes ( don't move from here : must be defined after the code attributes )

    flatCodeList = [
##        "<comma>",
        "<line>",
##        "<sp>",
##        "<space>",
        "<tab>",
        "<square>",
##        "<semicolumn>",
##        "<quote>",
##        "<dquote>",
        "<void>",
        "(void)"
        ]
    
    # list of corresponding items in texts ( "lines" ) - must match codeFlatList

    flatOriginalList = [
##        ",",
        "\n",
##        " ",
##        " ",
        "\t",
        "#",
##        ";",
##        "'",
##        '"',
        "",
        ""
        ]
    
    # list of delimiters ( must match codeList )

    delimiterList = [
        ",",
        "\n",
        " ",
        " ",
        "\t"
        ]
    
    # code of end of line
    
    eolCode = "<line>"

    # list of characters used in path

    pathCharacterList = [
        " ",
        "!",
        "@",
        "#",
        "$",
        "%",
        "",
        "&",
        "*",
        "(",
        ")",
        "/",
        "\\",
        ":",
        ".",
        "_",
        "-",
        "~",
        os.sep
        ]

    
    # quotes

    quoteList = [ '"', "'" ]

    # reserved in regular expressions

    regularExpressionReservedList = [
        ".",
        "{",
        "}",
        "[",
        "]",
        "(",
        ")",
        "|",
        "\\",
        "^",
        "$",
        "<",
        ">",
        "=",
        ":",
        "?",
        "!"
        ]


    # for search sequences, words are consecutive

    searchStickList = [ ".",  "-" ]

    # code of end of line
    
    spaceCode = "<sp>"
    
    # special characters list

    specialCharacterList = [
        ',',
        '.',
        ':',
        ';',
        '?',
        '!',
        '(',
        ')',
        '[',
        ']',
        '{',
        '}',
        '+',
        '*',
        '-',
        '~',
        '/',
        '\\',
        '"',
        "'",
        '@',
        '#',
        '$',
        '%',
        '^',
        '&',
        '|'
        ]


    # list of string arguments

    stringFormatList = [
        "capitalize",       # capitalize ( 1st letter in upper case, remainder is the same )
        "class",            # alias for class identifier
        "classidentifier",  # class syntax, capitalized words without spaces
        "consonants",        # consonants only
        "identifier",       # words without spaces, first is not capitalized, the others are capitalized
        "initials",         # initials
        "join",             # words witout space, preserves case of first word, others are capitalized
        "lower",            # lower case
        "minus",            # minus-separated words
        "normalized",       # normalized : only accentless alphanumerical, spaces and -
        "path",             # correct path name
        "sentence",         # sentence, sequence of words separated by one space, 1st capitalized, the remainder is not.
        "sentences",        # multiple sentences.
        "split",            # split in words using upper case,  digits, puntuation marks and '_' '-' as separators
        "strict",           # strict file name, but spaces are allowed
        "strictclass",      # strict capitalized file name : sequence of capitalized words without space, 1st may be in upper/lower, remainder upper, "-".
        "strictidentifier", # strict identifier file name : sequence of capitalized words without space, 1st may be in upper/lower, remainder upper, "-".
        "strictsplit",      # strict name with spaces : sequence of capitalized words without space, 1st may be in upper/lower, remainder upper, "-".
        "strictunderscore", # strict undesrcored name : sequence of capitalized words without space, 1st may be in upper/lower, remainder upper, "-".
        "title",            # capitalized sentence
        "slashtitle",       # title / title - hierarchical, e.g., project / delivery
        "uncapitalize",     # uncapitalize ( 1st letter in lower case, remainder is the same )
        "underscore",       # underscored-separated words
        "unicode",          # unicode (returns a unicode object, not a string
        "upper",            # upper case
        ]

    
    # code of tab

    tabCode = "<tab>"
    
    # unicode format
    
    unicodeFormat = None

    # code of void strings

    voidCode = "<void>"

    # lists of delimiters

    wordDelimiterList = [
        " ",
        ",",
        "\t",
        "="
        ]




        


                 
    def asciiToFlat (

        self,
        text = None,
        default = None
        ) :

        """ Converts a string with lines and tabs into a flat string.

            each occurrence of delimiterList is replaced by the corresponding code

            replaces tag header '<' by '<!' so that codes found in text are not recognized afterwards
            e.g.,  '<sp>' becomes '<!sp>" 

            """

        text = self.string( text, default = default )

        # empty text : <void>

        if self.isEmpty( text ) : return self.voidCode


        # replaces tag header '<' by '<!'

        text = text.replace( "<", "<!" )

        for index in range( len( self.flatCodeList ) ) :

            # exception : empty delimiter ( void )

            if self.isEmpty( self.flatOriginalList[ index ] ) : continue

            # replaces delimiter by its code
        
            text = text.\
                   replace( self.flatCodeList[ index ], "<" + self.flatCodeList[ index ] + ">" ).\
                   replace( self.flatOriginalList[ index ], self.flatCodeList[ index ] )

        return text



    def asciiToLines (

        self,
        text = None
        ) :

        """ Converts a text containing \n into a list of lines (strings) """

        if text is None : return None

        # removes spurious characters that screw splitlines ( chr(13) )

        if "\r" in text : return text.replace( "\r", "" ).splitlines()

        else : return text.splitlines()




    def asciiToPersons (

        self,
        text = None,
        connector = "and"
        ) :


        """ Returns a list of persons in format last name, initials of first and middle name from an ascii text """

        if self.isEmpty( text ) : return [ ]

        connector = self.string( connector, default = " " )

        text = text.\
               replace( " " + connector.upper() + " ", " " + connector + " " ).\
               replace( "&&", " " + connector + " " ).\
               replace( "&", " " + connector + " " ).\
               replace( '"', "'" ).\
               replace( "{", "" ).\
               replace( "}", "" ).\
               replace( "(", "" ).\
               replace( ")", "" ).\
               replace( "[", "" ).\
               replace( "]", "" ).\
               replace( ":", "," ).\
               replace( ";", "," ).\
               replace( "_", "-" ).\
               replace( " -", "-" ).\
               replace( "~", " ").\
               replace( "- ", "-" ).\
               replace( ",,", "," ).\
               replace( "..", "." ).\
               replace( " .", "." ).\
               replace( ".", ". " ).\
               replace( "  ", " " )



        # splits persons with keyword " and ". gives a list of texts with all the person's name, e.g., "toto, a."

        persons = text.split( " " + connector + " " )

##        print "asciiToPersons initial persons ", persons

        # each person is supposedly a pair name1 , name 2. If there are more commas, creates new persons

        names = [ ]

        for person in persons :
           
            names.extend( self.splitPersonName( person ) ) 

        if self.isEmpty( names ) : return [ ]

        # if there is a odd number of names, tries to insert a "" after a name

        size = len( names )

        # normalizes each word and determines possible type of each word: bit 0 = can be initials, bit 1 = can be a family name
        
        types = size * [ 0 ]

##        print "asciiToPersons size ", size, names

        for index in range( size ) :

            # normalizes the word: strips weird characters

            word = names[ index ]

            if "." in word :

                types[ index ] = 1 # initials only

                word = word.replace( ".", " " )

            # splits 

            words = self.textToWords( word )

            # joins again (removed dots and double spaces )

            names[ index ] = self.wordsToText( words )

            # empty stuff: could be a missing first name
            
            if len( words ) <= 0 :

                minimum = 0

                maximum = 0


            # length of subwords

            else :

                lengths = map( len, words )

                maximum = max( lengths )

                minimum = min( lengths )

            # all > 3 : can only be a name

            if types[ index ] == 1 : pass

            elif minimum > 3 : types[ index ] = 2

            elif maximum == 0 : types[ index ] = 0

            elif maximum == 1 : types[ index ] = 1

            else : types[ index ] = 3

##            print "   ", index, word, names[ index ], types[ index ], words, minimum, maximum




##        if size % 2 :
##
##            for index in range( size - 1 ) :
##
##                if ( ( names[ index ].find( "." ) < 0 ) and
##                     ( names[ index + 1 ].find( "." ) < 0 ) ) :
##
##                    names.insert( index, "" )
##
##                    break
##
##            if len( names ) % 2 : names.append( "" )



        # places the names, finding first and last names. processes by packs of 2 words

        persons = [ ]

##        print "___build list"

        index = 1

        size = len( names )

        while True :

            # at the end, odd number of words. adds a "" i.e. empty initials

            if index >= size :

                if size % 2 :

                    names.append( "" )

                    types.append( 0 )

                    size = size + 1

                    continue

                break

            # 1st and 2nd words and their types

            word0 = names[ index - 1 ]

            type0 = types[ index - 1 ]
            
            word1 = names[ index ]

            type1 = types[ index ]

##            print "  ", index, word0, type0, word1, type1,
            

            # 2 of them are initials or void: nothing to do, skips

            if ( type0 <= 1 ) and ( type1 <= 1 ) :

                index = index + 2

                continue

            # 2 of them are family names: inserts a void initials after first

            if ( type0 == 2 ) and ( type1 == 2 ) :

                names.insert( index, "" )

                types.insert( index, 0 )

                size = size + 1

                word1 = ""

                type1 = 0
                
            # one is empty: this is the first name (initials )

            if type0 <= 1 :

                firstNames = word0

                lastNames = word1
            
            elif type1 <= 1 :

                firstNames = word1

                lastNames = word0

            elif type0 == 2 :

                firstNames = word1

                lastNames = word0

            elif type1 == 2 :

                firstNames = word0

                lastNames = word1

            else :

                firstNames = word0

                lastNames = word1

            # capitalizes last names
            
            lastNames = self.string( lastNames, format = "title" )

            # capitalizes first names, adds dots to initials

            words = self.textToWords( firstNames )

            firstNames = ""

            for word in words :

                if len( word ) == 1 : word = word.upper() + "."

                elif ( ( len( word ) == 2 ) and ( word[ -1 ] == "." ) ) : word = word.upper()

                elif ( ( len( word ) == 3 ) and ( word[ 1 ] == "-" ) ) : word = word.upper() + "."

                elif ( ( len( word ) == 4 ) and ( word[ 1 ] == "-" ) and ( word[ -1 ] == "." ) ) : word = word.upper()

                # several initials stuck together
                
                elif word.isupper() :

                    expanded = ""

                    for char in word : expanded = expanded + char + "." + "~"

                    word = expanded[ : -1 ]

                # multi letters initial

                else : word = word.capitalize()

                firstNames = firstNames + word + "~"

            firstNames = firstNames.strip( " ~" )

##            print "first name", firstNames, "last", lastNames

            # removes coding of commas, spaces etc., then splits first name and remainder with comma
          
            persons.append( [ lastNames, firstNames ] )

            index = index + 2


        return persons

    

    def boolean (

        self,
        value = None,
        default = None
        ) :

        """ Converts a value into a boolean, returns default if impossible """

        value = self.integer( value, default = None )

        if value is None : return default

        return bool( value )




        
    def capitalize (

        self,
        text = None
        ) :

        """ Capitalizes (looses intermediary upper cases)

            Minimal control on arguments

            """

        if self.isEmpty( text ) : return text

        return text.capitalize()




    def commonPrefix (

        self,
        text1 = None,
        text2 = None
        ) :

        """ Returns the common prefix between text1 and text2 """

        if self.isEmpty( text1 ) : return ""
        
        if self.isEmpty( text2 ) : return ""

        size = min( len( text1 ), len( text2 ) )

        for index in range( size ) :

            if not text1[ index ] == text2[ index ] : return text1[ : index ]

        return text1[ : size ]

                        
        
    def commonSuffix (

        self,
        text1 = None,
        text2 = None
        ) :

        """ Returns the common suffix between text1 and text2 """

        if self.isEmpty( text1 ) : return ""
        
        if self.isEmpty( text2 ) : return ""

        size = min( len( text1 ), len( text2 ) )

        for index in range( 1, size ) :

##            print " ", index, " / ", size, text1[ - index ], text2 [ - index ]

            if not text1[ - index ] == text2[ - index ] :

                if index == 1 : return ""

                else : return text1[ - index + 1 : ]

        return text1[ - size : ]




    def consonants (

        self,
        text = None
        ) :

        """ returns the consonants of the text """

        result = ""

        for character in self.normalized( text ).lower() :

            if not character.isalpha() : continue

            if character in "aeiouy" : continue

            result = result + character
            
        return result


    def content (

        self,
        text = None,
        index = None,
        default = None
        ) :

        """ Returns the indexth element of a text and/or a list.

            accepts negative indexes (counted from the end)

            returns None if out of range and/or there is a type mismatch

            """

        if self.isIndex( index, text ) : return text[ index ]

        # permutes arguments if required

        elif self.isIndex( text, index ) : return index[ text ]

        else : return default


            
    def endswith (

        self,
        text1 = None,
        text2 = None,
        strip = None
        ) :

        """ returns True iff text1 endswith text2. Works with None or empty texts

            if strip is a string, removes heading and training spaces and characters contained in "strip"
            
            """


        if self.isEmpty( text2 ) : return True

        if self.isEmpty( text1 ) : return False

        if strip is None : return text1.endswith( text2 )
        
        elif type( strip ) == str : return text1.strip( strip ).endswith( text2.strip( strip ) )

        else : return text1.strip().endswith( text2.strip() )




    def expandKeywords (

        self,
        word = None,
        keywords = None,
        itemList = None,
        ) :

        """ separates a word, i.e., splits the list of keywords that prefix it,

            if the itemlist is defined, places the delimiters in this list 

            returns the word trimmed

            
            """

        if self.isEmpty( keywords ) : return word

        iAppend = 0
        
        index = 0

        while True :

            if index >= len( word ) : break

            for keyword in keywords :

                # does not process alphanumerical or parentheses

                if ( ( keyword.isalnum() ) or ( keyword == "(" ) or ( keyword == ")" ) ) : continue

                if word.startswith( keyword, index ) :

                    append = self.expandParenthesis( word[ iAppend : index ], itemList )
                        
                    if not itemList is None   :

                        if len( append ) > 0 : itemList.append( append )

                        itemList.append( keyword )

                    iAppend = index + len( keyword )

                    index = iAppend - 1 # will be incremented now

                    break

            index = index + 1

        return word[ iAppend : ]





    def expandParenthesis (

        self,
        word = None,
        itemList = None,
        ) :

        """ separates a word, i.e., splits ((, )) etc and places in a list of items


            if the itemlist is defined, places the delimiters in this list 

            returns the word trimmed
            
            """


        if word.startswith( "((" ) :

            if not itemList is None : itemList.append( "(" )

            word = word[ 1 : ]

        if ( ( word.startswith( "(" ) ) and ( word.count(  "(" ) > word.count( ")" ) ) ) :

            if not itemList is None : itemList.append( "(" )

            word = word[ 1 : ]
            
        if word.endswith( "))" )  :

            append = word[ : -1 ]
            
            if ( ( not itemList is None ) and ( not self.isEmpty( append ) ) ) : itemList.append( word[ : -1 ] )

            word = ")"


        if ( ( word.endswith( ")" ) ) and ( word.count( ")" ) > word.count( "(" ) ) ) :

            append = word[ : -1 ]

            if ( ( not itemList is None ) and ( not self.isEmpty( append ) ) ) : itemList.append( word[ : -1 ] )

            word = ")"

        return word

    
        

    def findDelimiter (

        self,
        text = None,
        first = None,
        last = None,
        delimiters = None
        ) :

        """ Submethod of textToWords. Finds the first delimiter of a list in a text, in a given range of positions

            Returns a pair: position, delimiter found, or -1, None

            """
        

        if self.isEmpty( text ) : return -1, None

        if self.isEmpty( delimiters ) : return -1, None

        # conversion of delimiters : strings -> list of string

        if not type( delimiters ) == list : delimiters = [ self.string( delimiters ) ]

        # normalizes the range of search
        
        if not type( first ) == int : first = 0

        if first < 0 : first = len( text ) + 1 - first

        if not self.isIndex( first, text ) : first = 0

        if not type( last ) == int : last = len( text )

        if last < 0 : last = len( text ) + 1 - last

        if not self.isIndex( last, text ) : last = len( text )

        # searches
        
        firstDelimiter = None

        firstPosition = last

        # finds closest occurrence of some of the field delimiters

        for delimiter in delimiters :

            if self.isEmpty( delimiter ) : continue

            position = text.find( delimiter, first, last )

            if position < 0 : continue

                
            # leftmost delimited changed ( changes only during first step )
            
            if position < firstPosition :

                firstDelimiter = delimiter

                firstPosition = position

        # nothing found

        if firstDelimiter is None : firstPosition = -1
        
        return firstPosition, firstDelimiter
    


    def flatToAscii (

        self,
        text = None
        ) :

        """ Converts a flat string without tabs or end of lines into a string with ...

            <code> becores code, e.g., <<tab>> becomes <tab>
            and <code> becomes the delimiter , e.g., <tab> -> "\t"

            """

        if text is None : return None

        text = self.string( text )

        # replaces successively all delimiters ( inefficient ! )

        for index in range( len( self.flatCodeList ) ) :
           
            text = text.replace( self.flatCodeList[ index ], self.flatOriginalList[ index ] )
            

        # replaces tag starter, i.e., '<' that were changed into '<!' 

        text = text.replace( "<!", "<" )
        
        return text





    def flatToLines (

        self,
        text = None
        ) :

        """ Converts a text containing \n into a list of lines (strings) """


        return self.asciiToLines( self.flatToAscii( text ) )



    def flatToPersons (

        self,
        text = None,
        connector = "and",
        ) :


        """ Returns a list of persons in format last name, initials of first and middle name """

        if self.isEmpty( text ) : return [ ]

        return self.asciiToPersons(
            text = self.flatToAscii( text ),
            connector = connector,
            )
    

    def flatToText (

        self,
        text = None
        ) :

        """ converts a flat text into a string composed of space-delimited words """

        if self.isEmpty( text ) : return text

        for delimiter in self.flatCodeList : text = text.replace( delimiter, " " )

        text = text.replace( "  ", " " )

        return text.strip()
    
        
      
    def findArgument(

        self,
        text = None,
        texts = None,
        format = None
        ) :   

        """ Finds a word in a list of arguments and returns a pair text, position

            Normalizes the strings in lower case

            Returns None, -1 if not found

            """

        if text is None : return None, -1    

        # if list is empyt or undefined
        
        if ( ( texts is None ) or ( len( texts ) <= 0 ) ) : return None, -1


        # lower case then removes spaces and tabs
        
        normalizedText = text.lower().replace( " ", "" ).replace( "\t", "" )
        
        # loop on texts
        
        for index in range( len( texts ) ) :
                
            item = texts[ index ]

            # lower case then removes spaces and tabs
            
            normalizedItem = item.lower().replace( " ", "" ).replace( "\t", "" )
        
            # equals: identified is derined
            
            if normalizedText == normalizedItem :

                return item, index

        # not found
        
        return None, -1


    def firstLetterUpper (

        self,        
        text = None
        ) :

        """ Version of capitalize with the first letter in upper case, but does not touch the rest

            For instance, on x = "controlCenter" , firstLetterUpper( x ) = "ControlCenter", but
            x.capitalize() = "Controlcenter"

            """
        
        if text is None : return None

        if len(text) <= 0 : return ""
        
        return text[ 0 ].upper() + text[ 1 : ]



    def float (

        self,
        value = None,
        default = None
        ) :

        """ Converts a value into an integer, returns default if impossible """

        if value is None : return default

        if type( value ) == int : return float( value )

        if type( value ) == bool : return float( value )

        if type( value ) == float : return value

        if not type( value ) == str : return default

        try :

            value = float( value )

            return value

        except Exception, exception :

            None

        if len( value ) == 0 : return default
        
        if value.lower() == "true" : return 1.

        if value.lower() == "false" : return 0.

        return default


    def getMessage (

        self,
        name = None,
        ) :

        """ Returns  some message defined by its name, e.g., "user" """


        if self.context is None : return name


        try :
            
            message = self.context.getMessage( name )

            if message is None : return name

            else : return message

        except Exception, exception :

            return name



    def getVariable (

        self,
        name = None,
        default = ""
        ) :

        """ Returns the value of some context variable defined by its name, e.g., "user" """


        if self.context is None : return None

        try :
            
            return self.context.getVariable( name, default = default )

        except Exception, exception :

            return None

    

    def getPattern (

        self,
        name = None,
        default = ""
        ) :

        """ Returns the pattern of some context variable defined by its name, e.g., "user" """

        if self.context is None : return None

        try :

            return self.context.getPattern( name, default = default )

        except Exception, exception :

            return None

    

    def identifier (

        self,        
        text = None,
        first = "lower",
        separator = " "
        ) :
        
        """ Identifier format: lowercasewordCapitalizedWords

            First tells what to do with 1st letter "same", "upper", "lower" (default)

            Separator is the character inserted between words

            Minimal control on arguments

            """

        if text is None : return None
        
        # splits the text in words using tab, space, underscores and minus as separators
        
        words = text.replace("\t", " ").replace( "_", " " ).replace( "-", " ").replace( "\n", " ").split(" ")

        # no words
        
        if len( words ) <= 0 : return None

        # first symbol

        firstWord = True

        # adds words beginning in uppercase with no separators
        
        text = ""
        
        for word in words :
            
            if len( word ) <= 0 : continue # occurs with double delimiters, e.g. \t\t

            if not firstWord : text = text + word[ 0 ].upper() + word[ 1 : ] 

            elif first == "lower" : text = word[ 0 ].lower() + word[ 1 : ]
                
            elif first == "upper" : text = word[ 0 ].upper() + word[ 1 : ]

            else : text = word

            firstWord = False
                

        return text


    def include (

        self,
        items = None,
        item = None
        ) :

        """ Includes an item in a list """

        if not type( items ) == list : return False

        if not item in items : items.append( item )

        return True




    def index (

        self,
        items = None,
        item = None
        ) :

        """ returns the index of the item in the list (or the string) or -1 if absent """

        if type( items ) == str :

            try :

                return items.find( item )

            except Exception, exception :

                return -1

        elif type( items ) == list :

            try :

                return items.index( item )

            except Exception, exception :

                return -1

        else :

            return -1


    def initials (

        self,
        text = None
        ) :

        """ returns the initials of the words of the text """

        if self.isEmpty( text ) : return ""

        text = self.normalized( text )

        text = self.split( text, first = "lower" )

        words = self.textToWords( text )

        text = ""

        for word in words :
            
            if ( len( word ) > 0 ) and ( word[ 0 ].isalnum() ) : text = text + word[ 0 ]

        return text

    

    def instantiate (
        
        self,
        text = None,
        forced = None,
        format = None,
        default = "",
        openCode = "(",
        closeCode = ")",
        quoteCode = "!",
        slashCode = os.sep
        ) :

        """ Instantiates the variables (name), (date), etc. in a text

            After instantiation, path is normalized in order to remove duplicates "\\" etc.

            Format gives the format of normalization ( see self.string( format = **). Default is None
            
            Forced replaces the current value of all variables, defined or not, in the text ( variables are unchanged )

            Default is the value of undefined variables

            """


        if self.isEmpty( text ) : return ""

        if self.context is None : return text

        iClose = - len( closeCode )

        while True :

            iOpen = text.find( openCode, iClose + len( closeCode ) )

            if iOpen < 0 : return text

            iClose = text.find( closeCode, iOpen )

            if iClose < 0 : return text

            # quoted variable after ( : removes one quote

            if text.startswith( quoteCode, iOpen + len( openCode ) ) :

                text = text[ : iOpen + len( openCode ) ] + text[ iOpen + len( openCode ) + len( quoteCode ) : ]

                iClose = iOpen

                continue

            # looks for the pattern (..) in the list of variables patterns. Remplaces openCode and closeCode by ( )

            try :

                index = self.context.patternList.index( "(" + text[ iOpen + len( openCode ) : iClose ] + ")" )

            except Exception, exception :

                continue

            try :

                item = self.context.variableList[ index ]

            except Exception, exception :

                continue


            # gets the value (starts in lower case)

            value = self.getVariable( item )

            if not self.isEmpty( forced ) : value = forced

            value = self.string( value, default = default, format = format )

            # recodes slashes is required

            if not slashCode == os.sep : value = value.replace( os.sep, slashCode )

            
            # prepares pattern, the string to replace in text

            pattern = text[ iOpen : iClose + len( closeCode ) ]

            text = text[ : iOpen ] + text[ iOpen : ].replace( pattern , value )

            # sets iClose backward, in case the values were shorter than the patterns
            
            iClose = iOpen + 1 # ** max( len( value ) -1, 0 )
                
        return text





    def integer (

        self,
        value = None,
        default = None
        ) :

        """ Converts a value into an integer, returns default if impossible """

        if value is None : return default

        if type( value ) == int : return value

        if type( value ) == bool : return int( value )

        if type( value ) == float : return int( value )

        if not type( value ) == str : return default

        value = value.strip()

        if len( value ) == 0 : return default
        
        if value.isdigit() : return int( value )

        value = value.lower()

        if value == "true" : return 1

        if value == "false" : return 0

        if value.startswith( "0x" ) :

            result = 0

            for digit in value[ 2 : ] :

                if ( ( digit >= '0' ) and ( digit <= '9' ) ) : result = 16 * result + ord( digit ) - ord( '0' )

                elif ( ( digit >= 'a' ) and ( digit <= 'f' ) ) : result = 16 * result + 10 + ord( digit ) - ord( 'a' )

                else : return default

            return result
            
            

        # numerical value with sign

        sign = 1

        for index in range( len( value ) ) :

            if value[ index ] == "+" :

                continue

            elif value[ index ] == "-" :

                sign = sign * -1

            else :

                if not value[ index : ].isdigit() : return default

                return sign * int( value[ index : ] )


        return default

    
    


    def isEmpty (

        self,
        text = None
        ) :

        """ Returns True iff the argument is a non empty string or sequence """

        if text is None : return True

        try :

            return len( text ) <= 0

        except Exception, exception :

            return True

    
    def isIndex (

        self,
        index = None,
        text = None,
        ) :

        """ Returns True iff the first argument is a correct index of the second, list/string, or sequence

            accepts negative indexes ( from the end )
            
            """

        if not type( index ) == int : return False

        if self.isEmpty( text ) : return False

        if index < 0 : return self.isIndex( len( text ) - index, text )

        if index >= len( text ) : return False

        return True



    def isPattern (

        self,
        name = None,
        ) :

        """ Returns True iff the string is the pattern of some variable
            
            """


        if self.context is None : return False

        try :
            
            return self.context.isPattern( name )

        except Exception, exception :

            return False




    def isVariable (

        self,
        name = None,
        ) :

        """ Returns True iff the string name corresponds to some context variable
        
            suffixes Variable and Value are accepted, e.g., xxx, xxxVariable,  xxxValue

            format prefixes u_, x_ etc. are accepted

            Warning: may bug if variable is in uppercase
            
            """


        if self.context is None : return False

        try :
            
            return self.context.isVariable( name )

        except Exception, exception :

            return False

        


        
    def listToFlat (

        self,
        list = None
        ) :

        """ Converts a list to a text comma-delimited """


        return self.asciiToFlat( self.linesToAscii( list ) )



    def linesToAscii (

        self,
        lines = None
        ) :

        """ Converts a list into a text with \n """
        
        if lines is None : lines = [ ]

        elif not type( lines ) == list : lines = [ lines ]

        text = ""
        
        for value in lines :
            
##            text = text + self.string( value, default = self.voidCode ) + "\n"

            text = text + self.flatToAscii( value ).replace( "\n", " " ) + "\n"

        return text


        
    def listToText (

        self,
        list = None
        ) :

        """ Converts a list into a text with \n """

        text = self.linesToAscii( list )

        if self.isEmpty( text ) : return text

        lineDelimiter = None

        if not self.context is None :

            try :

                lineDelimiter = self.lineDelimiter

            except Exception, exception :

                None

        if lineDelimiter is None : lineDelimiter = "\n"
            
        return text.replace( lineDelimiter, " " ).replace( self.voidCode, "" ).replace( "  ", " " ).strip()
        

        
    def listToWords (

        self,
        list = None
        ) :

        """ Converts a list into a text with \n """

        return self.textToWords( self.linesToAscii( list ) )
        
        


    def lower (

        self,
        text = None
        ) :

        """ Lower case

            Minimal control on arguments

            """

        if text is None : return None

        return text.lower()




    def findPattern (

        self,
        pattern = None,
        text = None,
        ) :

        """ Matches a (compiled) regular expression, returns start, end positions or -1 -1  """


        if self.isEmpty( text ) : return -1, -1

        try :

            found = re.search( pattern, text )

            if found is None : return -1, -1

            else : return found.start(), found.end()

        except Exception, exception :

            return -1, -1



    def findWords (

        self,
        pattern = None,
        text = None
        ) :

        """ Finds a set of words (pattern) in a text, returns the start and end position or -1 -1

            search is done in any order and case-insensitive

            pattern is a text composed of space-separated words or a list

            """


        if self.isEmpty( text ) : return -1, -1

        if not type( pattern ) == list : pattern = self.textToWords( pattern )

        if self.isEmpty( pattern ) : return -1, -1

        iMin = len( text )

        iMax = 0

        text = text.lower()

        for word in pattern :

            i = text.find( word.lower() )

            if i < 0 : return -1, -1

            iMin = min( iMin, i )

            iMax = max( iMax, i )

        return iMin, iMax

        

        
        

        

    def maximum (

        self,
        items = None,
        default = None
        ) :

        """ returns the maximal number found in a list of items """

        if self.isEmpty( items ) : return default

        mValue = None

        for item in items :

            item = self.float( item )

            if item is None : None

            elif mValue is None : mValue = item

            elif item > mValue : mValue = item

        if mValue is None : mValue = default

        return mValue
    
        
    

    def match (

        self,
        text1 = None,
        text2 = None
        ) :

        """ Returns True iff the two texts match. One of the text ( but not both ) may contain * or ? """

        # one at least is empty
        
        empty1 = self.isEmpty( text1 )

        empty2 = self.isEmpty( text2 )

        if ( ( empty1 ) or ( empty2 ) ) : return ( empty1 and empty2 )

        # one at least contains wild cards

        wild1 = ( ( text1.find( "*" ) ) or ( text1.find( "?" ) ) )

        wild2 = ( ( text2.find( "*" ) ) or ( text2.find( "?" ) ) )

        if wild1 :

            pattern = self.searchPattern( text1 )

            position, length = self.findPattern( pattern, text2 )

            return ( position == 0 ) and ( length == len( text2 ) )

        elif wild2 :

            pattern = self.searchPattern( text2 )

            position, length = self.findPattern( pattern, text1 )

            return ( position == 0 ) and ( length == len( text1 ) )      

        else :

            return text1 == text2

              



    def minimum (

        self,
        items = None,
        default = None
        ) :

        """ returns the minimal number found in a list of items """

        if self.isEmpty( items ) : return default

        mValue = None

        for item in items :

            item = self.float( item )

            if item is None : None

            elif mValue is None : mValue = item

            elif item < mValue : mValue = item

        if mValue is None : mValue = default

        return mValue
    
        
            
    def minusWords (

        self,
        text = None
        ) :
        
        """ Title format: words (all capitalized) separated by spaces
        
            Splits words using uppercase letters, digits and separators
            
            Minimal control on arguments

            """

        return self.split( text, capitalize = False, first = "lower", separator = "-" )




    def normalized (

        self,
        text = None,
        ) :

        """ Normalized string, no accents

            Minimal control on arguments

            """

        if text is None : return None

##        if self.context is None : return text

        if self.isEmpty( self.characterTable ) : return ""

        delimiterList = self.wordDelimiterList + self.commentDelimiterList 

        if delimiterList is None : delimiterList = [ ]
            
                
        normalizedText = ""

        previous = ""

        for character in text :

            # checks spaces and delimiters

            if character in delimiterList :

                # previous was already a space

                if not previous == " " : 

                    normalizedText = normalizedText + " "

                    previous = " "

                continue

            isUpper = character.isupper()

            for item in self.characterTable :

                if not character in item : continue

                if isUpper : previous = item[ 0 ].upper()

                else : previous = item[ 0 ]

                normalizedText = normalizedText + previous

                break

        return normalizedText




    def patternIndex (

        self,
        name = None,
        ) :

        """ Returns the index of some pattern
            
            """


        if self.context is None : return None

        try :
            
            return self.context.patternIndex( name )

        except Exception, exception :

            return None



    def patternVariable (

        self,
        name = None,
        ) :

        """ Returns the variable associated to some pattern
            
            """


        if self.context is None : return None

        try :
            
            return self.context.patternVariable( name )

        except Exception, exception :

            return None





    def personsToAscii (

        self,
        persons = None,
        connector = "and",
        openKey = "{",
        closeKey = "}"
        ) :

        """ Returns one line composed of persons' names (last, first ) separated by "and" """


        if self.isEmpty( persons ) : return ""

        connector = self.string( connector, default = " " )

        openKey = self.string( openKey, default = "" )

        closeKey = self.string( closeKey, default = "" )

        if type( persons ) == list : None

        else :  persons = self.flatToPersons( persons )

        text = ""

        for person in persons :

            if self.isEmpty( person ) : continue

            firstNames = person[ 1 ]

            lastNames = person[ 0 ]
            
            if ( ( "-" in lastNames ) or ( " " in lastNames ) or ( not lastNames.islower() ) ) :

                lastNames = openKey + lastNames + closeKey

            # adds to text
            
            text = text + \
                   lastNames + \
                   ", " + \
                   firstNames + \
                   " " + connector + " "

        # removes last "and" and comma

        if len( text ) >= 5 : text = text[ : -5 ]

        text = text.strip().strip( "," )

        return text

        
    def personsToFlat (

        self,
        persons = None,
        connector = "and"
        ) :

        """ Returns one line composed of persons' names (last, first ) separated by "and" """

        return self.asciiToFlat( self.personsToAscii( persons, connector ) )


    def personsToLines (

        self,
        persons = None,
        connector = "and"
        ) :

        """ Returns a text of several lines composed of persons' names (last, first ) tabulated """

        if self.isEmpty( persons ) : return ""

        if type( persons ) == list : None

        else :  persons = self.flatToPersons( persons )
        
        # determines length of last and first names

        firstNamesLength = 0

        lastNamesLength = 0
        
        for person in persons :

            if self.isEmpty( person ) : continue

            firstNamesLength = max( firstNamesLength, len( person[ 1 ] ) )
            
            lastNamesLength = max( lastNamesLength, len( person[ 0 ] ) )
            
                                    
        # creates lines

        text = ""
    
        
        for person in persons :

            if self.isEmpty( person ) : continue

            text = text + \
                   self.string( person[ 1 ], format = "capitalize" ).ljust( firstNamesLength ) + \
                   " " + \
                   self.string( person[ 0 ] ).ljust( lastNamesLength ) + \
                   "\n"

        return text

        

    def prefix (

        self,
        text = None,
        prefix = None
        ) :

        """ Returns the prefix of the text that matches a predefined (list of) prefixes.
        
            returns "" if there is no match

            """

        if self.isEmpty( text ) : return ""

        if self.isEmpty( prefix ) : return ""

        if type( prefix ) == list :

            for item in prefix :

                if text.startswith( item ) : return item

            return ""

        else :

            if text.startswith( prefix ) : return prefix

            return ""





        
    def safePath (

        self,
        text = None
        ) :

        """ Returns a safe version of the text that contain only alphanumerical and path characters
        
            removes final "." and " " that may screw windows ( unremovable files )
            
            """

        if text is None : return None

        pathCharacterList = self.pathCharacterList

        filtered = ""

        driveFlag = False   # control of ":"

        specialFlag = False

        for char in text :

            if char.isalnum() :

                filtered = filtered + char

            elif char in pathCharacterList :

                # accepts only one ":", before first /, and not as first character
                
                if ( ( char == ":" ) and ( ( specialFlag ) or ( filtered == "" ) ) ) : continue

                specialFlag = True  # there are special characters

                filtered = filtered + char

        
        # removes initial and final dots and spaces that screw windows

        return filtered.strip( ". " )

    


    def searchPattern (

        self,
        text = None
        ) :

        """ Returns a search pattern (see module re) from the text """


        if self.isEmpty( text ) : return None

        delimiters = self.wordDelimiterList + self.commentDelimiterList

        if delimiters is None : delimiters = [ ]

        # generates an expression that represent a non-null sequence of delimiters
        
        delimiterPattern = "\n"  # line delimiter

        for delimiter in delimiters :

            if delimiter in self.regularExpressionReservedList : delimiterPattern = delimiterPattern + "|\\" + delimiter

            else : delimiterPattern = delimiterPattern + "|" + delimiter

        delimitersPattern = "[" + delimiterPattern + "]+"

        nonDelimiterPattern = "[^(" + delimiterPattern + ")]"

        nonDelimitersPattern = nonDelimiterPattern + "*"

        anythingPattern = ".*"

        precededByDelimiterPattern = "(?<=" + delimiterPattern + ")"
        
        followedByDelimiterPattern = "(?=" + delimiterPattern + ")"

        finalDelimiterPattern = "(" + delimiterPattern + "|$)"

        
        # generates the regular expression
        
        pattern = ""

        index = 0

        character = ""

        while index < len( text ) :

            previousCharacter = character

            character = text[ index ]

            index = index + 1

            # skips double spaces and double *

            if ( ( character == previousCharacter ) and ( character == "*" ) ) : continue
            
            if ( ( character == previousCharacter ) and ( character == " " ) ) : continue

            # next character            

            if index < len( text ) : nextCharacter = text[ index ]

            else : nextCharacter = ""

            # delimiter (only if not preceded by another delimiter, or *

            if character == " " :

##                if previousCharacter == "*" : continue

                pattern = pattern + delimitersPattern

                continue

            # * : wildcard

            if character == "*" :

                # "  *  "

                if ( ( previousCharacter == " " ) and  ( nextCharacter == " " ) ) :

                    pattern = pattern + precededByDelimiterPattern + anythingPattern + followedByDelimiterPattern

                # *XXX
                
                elif previousCharacter == " " :

                    pattern = pattern + precededByDelimiterPattern + nonDelimitersPattern


                # XXX*
                
                elif nextCharacter == " " :

                    pattern = pattern + nonDelimitersPattern + followedByDelimiterPattern

                # XXX*YYY

                else :

                    pattern = pattern + nonDelimitersPattern

                continue
            

            # starts a regular expression ( ' or " ): looks for closing quote, not preceded by \

            if ( ( character == "'" ) or ( character == '"' ) ) :

                end = index

                while True :

                    end = text.find( character, end )

                    if end < 0 :

                        end = len( text )

                        break

                    if not text[ end - 1 ] == "\\" : break

                    end = end + 1

                pattern = pattern + "(" + text[ index : end ] + ")" 

                index = end + 1

                continue


                
            # normal character
            

            # if starts a word, checks that it is preceded by a delimiter
                
            if previousCharacter == " " : pattern = pattern + precededByDelimiterPattern

            # builds a set of equivalent characters by looking at characterTable

            characters = []

            # first, looks for a set that starts with the caracter

            for item in self.characterTable :

                if not self.isEmpty( characters ) : break

                if self.isEmpty( item ) : continue

                if item[ 0 ] == character :  characters = item

            # not found : looks for a set that contains "character"

            for item in self.characterTable :

                if not self.isEmpty( characters ) : break
                
                if self.isEmpty( item ) : continue

                if character in item : characters = item

            # character itself

            if self.isEmpty( characters ) :
            
                pattern = pattern + character

            # found a set : alternative

            else :

                pattern = pattern + "["

                for other in characters :

                    if other in self.regularExpressionReservedList : pattern = pattern + "\\" + other

                    else : pattern = pattern + other

                pattern = pattern + "]"

        # if ends a word, checks that it is preceded by a delimiter
                
        if not character == " " : pattern = pattern + finalDelimiterPattern

        return re.compile( pattern, re.DOTALL )     # DOTALL means that "." matches end of line, allows working on several lines
        




    def sentences (

        self,
        text = None
        ) :
        
        """ Sequence of sentences. Capitalizes 1st and after puntuation marks
        
            Splits words using uppercase letters, digits and separators
            
            Minimal control on arguments

            """

        if self.isEmpty( text ) : return ""

        text = text.\
               replace( "(", " ( " ). \
               replace( ")", " ) " ). \
               replace( ".", " . " ). \
               replace( ":", " : " ). \
               replace( ";", " ; " ). \
               replace( ",", " , " )

##        print text

        words = self.textToWords(
            text,
            delimiters = [ " ", "\t", "\n" ],
            leaveQuotes = True
            )

##        print words

        text = ""

        capitalize = True

        for word in words :

            if ( word == "." ) or ( word == ":" ) :

                capitalize = True

            elif capitalize :

                word = word.capitalize()

                capitalize = False

            else :

                capitalize = False

            text = text + word + " "

##            print text
            

        # normalizes again

        text = text.\
               replace( "( ", "(" ). \
               replace( " )", ")" ). \
               replace( " .", "." ). \
               replace( " :", ":" ). \
               replace( " ;", ";" ). \
               replace( " ,", "," ). \
               strip()
               

        return text 

        

        





    def setVariable (

        self,
        name = None,
        value = None
        ) :

        """ Sets the valus of some context variable defined by its name, e.g., "user"

            returns True/False
            
            """

        if self.context is None : return False
        
        if value is None : return False

        try :

            return self.context.setVariable( name, value )

        except Exception, exception :

            return False
        




    def slashPath (

        self,
        path = None
        ) :
        
        """ Normalizes a path with / instead of os.sep

            Returns the normalized path or None if problem

            """

        if path is None : return None

        path = self.safePath( path )

        # replaces / and \ by / (one of the two may be useless)
        
        path = path.replace( "\\", "/" ).replace( os.sep, "/" ).replace( "//", "/" )

        return path




    def slashTitle (

        self,
        text = None
        ) :

        """ title / title. Hierarchized, e.g., project / delivery """

        if text is None : return None

        text = self.osPath( text )

        if text.endswith( os.sep ) : text = text[ : -1 ]

        directory, name = os.path.split( text )

        dummy, name1 = os.path.split( directory )

        name2, dummy = os.path.splitext( name )

        return self.title( name1 + " / " + name2 )
    

        

        
    def sortedSet (

        self,
        data = None,
        reverse = False
        ) :

        """ Transforms the data into an ordered list with no repetitions

            Reverse true means decreasing order
            
            """

        if data is None : return [ ]

        if not type( data ) == list : return [ data ]

        #*EF 2009 04 18

        return sorted( set( data ), reverse = bool( reverse ) )

##        sortedList = list( set( data ) )
##
##        sortedList.sort()
##
##        if bool( reverse ) : sortedList.reverse()
##
##        return sortedList
##       


    def skipDelimiters (

        self,
        text = None,
        first = None,
        last = None,
        delimiters = None
        ) :

        """ Skips all the delimiters of a list in a text, in a given range of positions

            Returns a position, after last delimiter found, or -1

            """
        

        if self.isEmpty( text ) : return -1

        if self.isEmpty( delimiters ) : return -1

        # conversion of delimiters : strings -> list of string

        if not type( delimiters ) == list : delimiters = [ self.string( delimiters ) ]

        # normalizes the range of search
        
        if not type( first ) == int : first = 0

        if first < 0 : first = max( 0, len( text ) + 1 - first )

        if not type( last ) == int : last = len( text )

        if last < 0 : last = max( 0, len( text ) + 1 - last )

        last = min( last, len( text ) )


        while first < last :

            # length of delimiter of maximal length that matches
            
            maxLength = 0

            for delimiter in delimiters :

##                if self.isEmpty( delimiter ) : continue # done in the 2 following lines

                length = len( delimiter )

                if length <= maxLength : continue

                # fast way of checking whether the text == the delimiter ( no copies )

                if text.find( delimiter, first, min( first + length, last ) ) < 0 : continue

                maxLength = length

            # not found

            if maxLength <= 0 : break

            first = first + maxLength


        return first

            

    def split (

        self,
        text = None,
        capitalize = False,
        first = "upper",
        separator = " ",
        separators = None,
        
        ) :
        
        """ Sentence format: words (1st capitalized) separated by spaces
        
            Splits words using uppercase letters, digits and separators

            Capitalize indicates whether all words are capitalized or only the 1st one

            If capitalize is False, "first" tells what to do with first letter: "same", "upper" (default), "lower".

            Separator is the symbol inserted between words

            Separators is the list of separators used to split words
            
            Minimal control on arguments

            """

        if text is None : return None

        if len( text ) <= 0 : return ""

        if not type( separators ) == list : separators = [ ",", ";", "\t", " ", "_", "-", "\n" ]

        sentence = ""
            
        char = " "      # to remove initial separators

        firstWord = True

        upper = False

        lower = False

        alpha = False

        digit = False

##        print "Texts.split( ", text, ")", capitalize, first, separator, separators 
        
        for index in range( len( text ) ) :

            last = char

            lastAlpha = alpha

            lastDigit = digit

            lastLower = lower

            lastUpper = upper

            char = text[ index ]

            # upper case , digit, etc.

            alpha = False

            digit = False

            upper = False

            lower = False

            # digits
            
            if char.isdigit() :

                digit = True


            # normal letters
            
            elif char.isalpha() :

                alpha = True

                if char.isupper() : upper = True

                else : lower = True

            # extended alpha (includes accented letters )
            
            elif char  in self.alphaList :

                alpha = True

                if char in self.upperList : upper = True

                elif char in self.lowerList : lower = True
                

            # separators: writes only the 1st one
            
            elif char in separators  :
                
                if not last in separators : sentence = sentence + separator

                continue

            # upper case = new word if previous was no upper case or digit
            
            if ( ( upper ) and ( not lastUpper ) and ( not lastDigit ) ) :
                    
                if not last in separators : sentence = sentence + separator

                if bool( capitalize ) : None
                    
                elif not firstWord : char = char.lower()

                elif first == "lower" : char = char.lower()
                    
                elif first == "upper" : None
                    
                else : None


            # digit, previous was not digit nor upper case: new word 
            
            elif ( ( digit ) and ( not lastDigit ) and ( not lastUpper ) ) :

                if not last in separators : sentence = sentence + separator

            # minus, previous was not minus, starts a word

            elif ( ( char == "-" ) and  ( not last == char ) ) :

                if not last in separators : sentence = sentence + separator
                
            # underscore, previous was not underscore, starts a word

            elif ( ( char == "_" ) and  ( not last == char ) ) :

                if not last in separators : sentence = sentence + separator

            # os.sep, previous was not underscore, starts a word

            elif ( ( char == os.sep ) and  ( not last == char ) ) :

                if not last in separators : sentence = sentence + separator
                
            # word starting in lower case
            
            elif ( ( lower ) and ( not lastAlpha ) ) :

                if not last in separators : sentence = sentence + separator

                if capitalize : char = char.upper()
                    
                elif not firstWord : None

                elif first == "lower" : None
                    
                elif first == "upper" : char = char.upper()
                    
                else : None
                
            # appends character (as it for capitalized sentences, in lower otherwise )

##            print "Texts.split ", text, " text[", index, "]=", text[ index ], " -> ", char, " cap ", capitalize
            
                
            if bool( capitalize ) : sentence = sentence + char

            else : sentence = sentence + char.lower()

            firstWord = False

        return sentence.rstrip( separator )



        
    def splitPersonName (

        self,
        text = None
        ) :

        """ Splits a text into a pair initials of first names - last names or vice versa """


        if self.isEmpty( text ) : return [ ]
        
        # the text contains a comma: splits and splits separately each segment
        
        if text.find( "," ) >= 0 :

            words = [ ]

            for word in text.split( "," ) :

                # starts with a dot: transfers it to previous word

                if word.startswith( "." ) :

                    if len( words ) > 0 : words[ -1 ] = words[ -1 ] + "."

                    word = word.lstrip( " ." )

                names = self.splitPersonName( word )

                words.extend( names )

            return words


        # normal case : no commas

        items = text.replace( "\n", " ").replace( "\t", " " ).replace( "  ", " " ).split()



        # builds a list of booleans "contains a dot or is an initial vs. not", and removes the empty words by the way
        
        words = [ ]

        dots = [ ]

        for item in items :

            item = item.strip().replace( "..", "." )

            if self.isEmpty( item ) : continue

            # particular case : a single dot, previous list is not empty

            if item .startswith( "." ) :

                if len( words ) > 0 :

                    words[ -1 ] = words[ -1 ] + "."

                    dots[ -1 ] = True

                item = item.lstrip( " ." )

            if len( item ) <= 0 : continue

            # ok, appends it

            words.append( item )

            if len( item ) == 1 : initial = True

            elif ( ( len( item ) == 3 ) and ( item[ 1 ] == "-" ) ) : initial = True

            elif ( ( len( item ) <= 4 ) and ( item[ -1 ] == "." ) ) : initial = True

            else : initial = False

            dots.append ( initial )

        # puts together the sequences of words that contain / do not contain dots

        names = [ ]

        index1 = 0

        while index1 < len( words ) :

            index2 = index1 + 1

            while ( ( index2 < len( words ) ) and ( dots[ index1 ] == dots[ index2 ] ) ) :

                index2 = index2 + 1

            if dots[ index1 ] :

                names.append( self.wordsToText( words[ index1 : index2 ] ) )

            else :

                names.append( self.wordsToText( words[ index1 : index2 ] ).replace( ".", "" ) )


            index1 = index2


        return names



            
    def startswith (

        self,
        text1 = None,
        text2 = None,
        position = 0,
        strip = None
        ) :

        """ returns True iff text1[ position : ] starts with text2. Works with None or empty texts 

            if strip is a string, removes heading and training spaces and characters contained in "strip"
            
            """


        if self.isEmpty( text2 ) : return True

        if self.isEmpty( text1 ) : return False

        if not type( position ) == int : return False

        if strip is None : return text1[ position : position + len( text2 ) ] == text2
        
        elif type( strip ) == str : return text1[ position : ].strip( strip ).startswith( text2.strip( strip ) )

        else : return text1[ position : ].strip().startswith( text2.strip() )

        
    

    def string (

        self,
        text = None,
        texts = None,
        format = None,
        default = None,
        size = None
        ) :

        """ Normalizes a text argument (text) with a reference list (texts).
            Both the text and the reference list may contain spaces and/or tabs
        
            First, try to identify the text in the reference list "texts" by comparing normalized strings,
            i.e. in lower case with no spaces. If texts is None or empty, takes the original text itself.

            Default is the default value

            Size if the length of the string

            Returns the reference text or the text itself in the given "format" :
                None (default) : returns the text of the reference list.
                Upper : returns a text in uppercase
                Lower : returns a text in lower case
                Normalized : returns a string in lower case with no accents
                Capitalize : returns a capitalized text (1 upper case letter, then lower case)
                Identifier : returns a copy in which spaces have been removed, all words but the first one begin in upper case
                ClassIdentifier : returns a copy in which spaces have been removed, all words begin in upper case
                Sentence : words are separated by one space, first word in upper case.
                Split : words separated by one space, uses upper case, digits, puntuation marks '_' as separators
                Safe : replaces all non-alphanumerical characters by _ or "" (note: spaces -> _ )

                Note that returning the reference text would not be sufficient,
                e.g., display a word in uppercase whereas the reference text is in lowercase.
            
            Returns None if text is None or not found in texts

            """

       
        # preprocessing


        # strings : nothing

        if type( text ) == str :

            None
            
        # contains special characters : encodes them
       
        elif type( text ).__name__ == "unicode" :

            text = self.unicodeToString( text )


        # explodes lists
            
        elif ( ( type( text ) == list ) and ( len( text ) > 0 ) ) :

            resultText = "[ "

            for item in text :

                resultText = resultText + self.string( item ) + ", "

            text = resultText + " ]"

        # undefined : returns default value
        
        elif text is None :

            return default
            
        # non lists, non strings : serializes
        
        else :

            text = str( text )
            

        # no list or format: just converts and returns

        if ( ( texts is None ) and ( format is None ) ) :

            # size of result

            if ( ( type( size ) == int ) and ( size >= 0 ) ) : text = text.ljust(size)[ : size ]

            return text


        # lower case then removes spaces and tabs
        
        normalizedText = text.lower().replace( " ", "" ).replace( "\t", "" )
        

        # if list is defined, searches in list
        
        if not self.isEmpty( texts ) :

            # returns a pair argument- position or None, -1
            
            identified, dummy = self.findArgument(
                text = text,
                texts = texts )

            # not found ?
            
            if identified is None : return default

            # otherwise, substitutes
            
            text = identified

        # no text
        
        if self.isEmpty( text ) : return text
        
        # normalizes format

        if format is None : format = "none"
        
        format = format.lower()

        # nothing

        if format == "none" :

            None

        # lower case
        
        elif format == "lower" :
            
            text = self.lower( text )


        # uncapitalize ( 1st letter in lower case, remainder is the same )
        
        elif format == "uncapitalize" :
            
            text = self.uncapitalize( text )

            
        # upper case
        
        elif format == "upper" :
            
            text = self.upper( text )

        # capitalize ( 1st letter in upper case, remainder is the same )
        
        elif format == "capitalize" :
            
            text = self.capitalize( text )

        # consonants only

        elif format == "consonants" :

            text = self.consonants( text )

        # words without spaces, first is not capitalized, the others are capitalized
        
        elif format == "identifier" :
            
            text = self.identifier( text )

        # initials

        elif format == "initials" :

            text = self.initials( text )

        # words witout space, preserves case of first word, others are capitalized
        
        elif format == "join" :
            
            text = self.identifier( text, first = "same" )

        # class syntax, capitalized words without spaces
        
        elif format == "classidentifier" :
            
            text = self.identifier( text, first = "upper" )

        elif format == "class" :        # alias for class identifier
            
            text = self.identifier( text, first = "upper" )


        # minus-separated words

        elif format == "minus" :

            text = self.minusWords( text )

        # normalized : only accentless alphanumerical, spaces and -
        
        elif format == "normalized" :
            
            text = self.normalized( text )
            
        # correct path name
        
        elif format == "path" :

            text = self.safePath( text )

        # sentence, sequence of words separated by one space, 1st capitalized, the remainder is not.
        
        elif format == "sentence" :

            text = self.split( text, first = "upper" )

        
        elif format == "sentences" :

            text = self.sentences( text )

        # split in words using upper case,  digits, puntuation marks and '_' '-' as separators
        
        elif format == "split" :
            
            text = self.split( text, first = "same" )

        # strict file name, but spaces are allowed
        
        elif format == "strict" :

            text = self.normalized( text )

        # strict capitalized file name : sequence of capitalized words without space, 1st may be in upper/lower, remainder upper, "-".
        
        elif format == "strictclass" :

            text = self.identifier( self.normalized( text ), first = "upper" )

        # strict identifier file name : sequence of capitalized words without space, 1st may be in upper/lower, remainder upper, "-".
        
        elif format == "strictidentifier" :

            text = self.identifier( self.normalized( text ) )

        # strict name with spaces : sequence of capitalized words without space, 1st may be in upper/lower, remainder upper, "-".
        
        elif format == "strictsplit" :

            text = self.normalized( self.underscoreWords( text ) ).replace( "-", " " ).replace( "  ", " " )


        # strict undesrcored name : sequence of capitalized words without space, 1st may be in upper/lower, remainder upper, "-".
        
        elif format == "strictunderscore" :

            text = self.normalized( self.underscoreWords( text ) ).replace( "-", "_" ).replace( "__", "_" )

        # capitalized sentence
        
        elif format == "title" :
            
            text = self.title( text )

        # underscored-separated words

        elif format == "underscore" :

            text = self.underscoreWords( text )

        # title / title - hierarchical, e.g., project / delivery

        elif format == "slashtitle" :

            text = self.slashTitle( text )
            
        # unicode (returns a unicode object, not a string

        elif format == "unicode" :

            text = self.stringToUnicode( text )
            

        # size of result

        if ( ( type( size ) == int ) and ( size >= 0 ) ) : text = text.ljust(size)[ : size ]

        return text



    def stringToUnicode (

        self,
        text = None,
        encoder = None
        ) :

        """ Converts a string into a unicode object using standard encoder """

        if self.isEmpty( text ) : return text

        if encoder is None : encoder = self.unicodeFormat

        try :

            encoded = unicode( text, encoder ) 

            return encoded

        # could not encode the whole string : goes by bits
            
        except Exception, exception :

            None

        encoded = ""

        for index in range( len( text ) ) :

            try :

                character = unicode( text[ index ], encoder )

            except Exception, exception :

                character = " "

            encoded = encoded + character

        return encoded




    def suffix (

        self,
        text = None,
        suffix = None
        ) :

        """ Returns the suffix of the text that matches a predefined (list of) suffixes.
        
            returns "" if there is no match

            """

        if self.isEmpty( text ) : return ""

        if self.isEmpty( suffix ) : return ""

        if type( suffix ) == list :

            for item in suffix :

                if text.endswith( item ) : return item

            return ""

        else :

            if text.endswith( suffix ) : return suffix

            return ""


    def sum (

        self,
        value = None
        ) :

        """ returns the sum of the value (list, integer, float) """

        if type( value ) == int : return value

        elif type( value ) == float : return value

        elif type( value ) == str : value = self.textToWords( value )

            

        elif type( value ) == list : None

        else : return 0

        # sums the elements of a list

        result = 0

        for item in value :

            if type( item ) == int :  result = result + item

            elif type( item ) == float : result = result + item

            elif not self.integer( item ) is None : result = result + self.integer( item )

            elif not self.float( item ) is None : result = result + self.float( item )

            elif type( item ) == list : result = result + self.sum( item )

        return result
    

                

    def textToWords (

        self,
        text = None,
        delimiters = None,
        number = None,
        variable = None,
        leaveQuotes = None,
        leaveEmpty = True,
        separate = False,
        keywords = None
        ) :


        """ Splits a text and returns a list of words.

            Uses the list of delimiters, or, by default, tab, space end of line

            Number indicates how many words we have to split

            LeaveQuotes indicates whether quotes are left in the words or not. In any case, a quoted expression
            is considered a word, whatever its content.

            leaveEmpty indicates whether empty words are removed. This consists in subsuming
            all delimiters into a single one, so that there is nothing like a,,b -> 'a','','b'

            separate checks the words that contain parenthesis, and if there is a '((', '))' or a mismatch
            separates

            keywords = list of keywords to separate ( if this list is not empty, separate becomes true 
            
            """

        if self.isEmpty( text ) : return [ ]

        if type( text ) == list : return text

        if not self.isEmpty( keywords ) : separate = True

       
        # no special delimiters : uses tab
        
        if type( delimiters ) == list : fieldDelimiterList = delimiters

        elif type( delimiters ) == str : fieldDelimiterList = [ delimiters ]

        else : fieldDelimiterList = self.wordDelimiterList

        # splits according to delimiter list. Warning: this is a list of strings OR of lists

        itemList = [ ]

        start = 0

        count = 1   # counts delimiters, compared to # of words .. 1 more

        while True :

            # end of text reached

            if start >= len( text ) : break

            # number of words reached


            if ( ( type( number ) == int ) and
                 ( number > 0 ) and
                 ( count >= number ) and
                 ( not bool( variable ) )
                 ) : break

            count = count + 1

            # detects quotes ' or "

            # quoted string : starts searching delimiter after the closing quote


            if text[ start ] in self.quoteList : quote = text[ start ]

            else : quote = ""

            if len( quote ) > 0 :

                quote = text[ start ]

                startDelimiter = text.find( quote, start + 1 )

                if startDelimiter < 0 : startDelimiter = start + 1


            # otherwise, starts here
            
            else :

                startDelimiter = start


            # loops for searching repeated field delimiters

            firstPosition, firstDelimiter = self.findDelimiter(
                text = text,
                first = startDelimiter,
                last = len( text ),
                delimiters = fieldDelimiterList
                )


            # not found any delimiter : stops splitting and return empty list

            if firstDelimiter is None : break

            # loop to find sequences of the same occurrences ( greedy match )

            lastPosition = self.skipDelimiters(
                text = text,
                first = firstPosition + len( firstDelimiter ),
                last = len( text ),
                delimiters = fieldDelimiterList
                )

            if lastPosition < 0 : lastPosition = firstPosition + len( firstDelimiter )


            # appends the item, with leading and trailing spaces and tabs removed and quote, if any

            if bool( leaveQuotes ) : remove = " \t"

            else : remove = " \t" + quote

            word = text[ start : firstPosition ].strip( remove )


            # not quoted, and double parenthesis : separates

            if ( ( bool( separate ) ) and ( len( quote ) <= 0 ) ) :

                word = self.expandKeywords( word, keywords, itemList )

                word = self.expandParenthesis( word, itemList )

            
            if ( ( bool( leaveEmpty ) ) or ( not self.isEmpty( word ) ) ) : itemList.append( word )

            start = lastPosition 


        # appends remainder, with leading and trailing spaces and tabs removed

        if bool( leaveQuotes ) : remove = " \t" 

        else : remove = " \t" + '"' + "'"

        word = text[ start :  ].strip( remove )

        # not quoted, and double parenthesis : separates

        if ( ( bool( separate ) ) and ( len( quote ) <= 0 ) ) :

            word = self.expandKeywords( word, keywords, itemList )

            word = self.expandParenthesis( word, itemList )
        
                
        if ( ( bool( leaveEmpty ) ) or ( not self.isEmpty( word ) ) ) : itemList.append( word )
            

        return itemList            

       

    

        

    def title (

        self,
        text = None
        ) :
        
        """ Title format: words (all capitalized) separated by spaces
        
            Splits words using uppercase letters, digits and separators
            
            Minimal control on arguments

            """

        return self.split(
            text,
            capitalize = True,
            separators = [ ",", ";", "\t", " ", "_", "-", "\n", "." ]
            )



    def uncapitalize (

        self,
        text = None
        ) :

        """ Uncapitalizes (looses intermediary upper cases)

            Minimal control on arguments

            """

        if self.isEmpty( text ) : return text

        return text[ 0 ].lower() + text[ 1 : ]



    def underscoreWords (

        self,
        text = None
        ) :
        
        """ Title format: words (all capitalized) separated by spaces
        
            Splits words using uppercase letters, digits and separators
            
            Minimal control on arguments

            """

        return self.split( text, separator = "_" ).lower()



    def unicodeToString (

        self,
        text = None,
        encoder = None
        ) :

        """ Converts a unicode string into a flat string using standard encoder """

        if self.isEmpty( text ) : return text

        if encoder is None : encoder = self.unicodeFormat

        try :

            encoded = str( text.encode( encoder ) ) # use global encoder

            return encoded

        # could not encode the whole string : goes by bits
            
        except Exception, exception :

            None

        encoded = ""

        for index in range( len( text ) ) :

            try :

                character = str( text[ index ].encode( encoder ) )

            except Exception, exception :

                character = " "

            encoded = encoded + character

        return encoded
        




    def upper (

        self,
        text = None
        ) :

        """ Upper case

            Minimal control on arguments

            """

        if text is None : return None

        return text.upper()




    def variableIndex (

        self,
        name = None,
        ) :

        """ Returns the index of some variable
            
            """


        if self.context is None : return None

        try :
            
            return self.context.variableIndex( name )

        except Exception, exception :

            return None





    def wordsToText (

        self,
        list = None,
        separator = " "
        ) :

        """ Converts a list of words into a text with \n (default) or separator """

        if not separator == "\n" : return self.flatToText( self.linesToAscii( list ) ).replace( "\n", separator )

        else : return self.flatToText( self.linesToAscii( list ) )
    
        
