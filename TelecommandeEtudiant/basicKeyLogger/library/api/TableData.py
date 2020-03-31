
""" Data structure containing a set of lines organized as a table
    
 
    """


from api.Utilities import *


class TableData :
    
    """ Data structure containing a set of lines organized as a table

        In addition, there are several attributes that define the separators, etc.
        
        


        """


   
    # delimiters used in file formats

    commentDelimiterList = None

    # comment numbers (line in source file)
    
    commentNumberList = [ ]

    # comments
    
    commentTextList = [ ]

    # count of lines
    
    count = 0L

    # delimiter list, for special file formats ( each element is a list or a single delimiter )

    delimiterList = None

    # error status
    
    error = None

    # format used for floats: decimal fixed

    floatFormat = None
    
    # line numbers (line in source file)
    
    lineNumberList = [ ] 

    # number of words on the line

    lineSize = None

    # string to strip from comments and lines

    stripString = None




    def __init__ ( self ) :
        
        """ Constructor. Does absolutely nothing
           
            """


        # initializes variables from utilities

        utilities.commentDelimiterList = utilities.commentDelimiterList

        self.delimiterList = utilities.wordDelimiterList

        # characters to strip from texts and comments
        
        self.stripString = utilities.commentDelimiter + utilities.lineDelimiter + " \r\t,"

        for character in utilities.commentDelimiterList :

            if not character in self.stripString : self.stripString = self.stripString + character

        self.floatFormat = "%25.6f"
        
        # initializes data

        self.resetData()
        


    



        
        
    def addLine (

        self,
        text = None,
        size = None,
        strict = None,
        variable = None
        
        ) :

        """ Processes and checks the line according to Table format

            Condition : all lines have the same number of words

            Checks the number of words. 

            Returns True if line is compatible with the format, False otherwise

            """

        # tries to split with its normal delimiter (tab)

        words = self.splitLine(
            text,
            size = size,
            variable = variable,
            delimiter = "\t"
            )

        if words is None : words = self.splitLine(
            text,
            size = size,
            variable = variable,
            delimiter = ","
            )

        if words is None : words = self.splitLine(
            text,
            size = size,
            variable = variable,
            delimiter = " "
            )

        if words is None : return False

        utilities.error = ""

        # checks the forbidden characters ( error message already set )

        if ( ( bool( strict ) ) and ( not self.checkForbiddenCharacters( words ) ) ) : return False
        
                   
        # OK: appends the line

        self.lineWordsList.append( words )

        # flattens

        index = 0

        for word in self.lineWordsList[ -1 ] :

            if ( ( "<" in word ) or ( "(" in word ) ) :

                self.lineWordsList[ -1 ][ index ] = utilities.flatToAscii( word )

            index = index + 1

        

        return True



    

    def checkForbiddenCharacters (

        self,
        words = None
        ) :

        """ Checks whether the words contain forbidden characters, i.e.m characters that are protected <comma>, etc. """

        if utilities.isEmpty( words ) : return True

        if type( words ) == str : words = [ words ]

        for word in words :

            if utilities.isEmpty( word ) : continue

            for index in range( len( utilities.flatOriginalList ) ) :

                character = utilities.flatOriginalList[ index ]

                protected = utilities.flatCodeList[ index ]

                if utilities.isEmpty( character ) : continue

                if character in word :

                    self.setError( "forbidden character in " + word + ": [" + character + "] replace by " + protected )

                    return False

        return True

                                   

        
   




    def extractComment (
        
        self,
        line = None
        ) :

        """ Extracts the comment from a line

            Returns a pair line, comment.
            The line is truncated before the first comment delimiter
            The comment begins immediately after the first comment delimiter
            
            The comment and/or the line may be empty.
            
            Note that the endOfLine character is considered a comment delimiter


        """

        if line is None : return None
    
        size = len( line )

        endLine = size

        startComment = size

        # loop on comment delimiters (note that EOL is considered a comment delimiter)
        
        for comment in utilities.commentDelimiterList : 

            position = line.find( comment, 0, endLine )
                    
            if position >= 0 :

                endLine = position

                startComment = position + len( comment )
                

        # removes leading and trailing spaces and tabs
        
        comment = line[ startComment : ].strip( self.stripString )

        line = line[ : endLine ].strip( self.stripString )

        # Returns truncated line

        return line, comment








        


    def getLine (
        
        self,
        lines = None,
        number = None
        ) :

        """ Returns a line defined by its position (number) in a list (lines)

            If lines is None, the default list is self.lineWordsList

            If number is None, the first element of the list is returned

            """

        if lines is None : lines = self.lineWordsList
        
        if number is None : number = 0

        try :
            
            line = lines [ number ]

        except Exception, exception :
            
            line = None
            
            self.setError( "getLine( line " + utilities.string( number ) + " ) - out of boundaries" )

        return line





    def resetData ( self ) :
    
        """ Initializes the data before reading a file

            lines, decorations, linesIdentifiers  are empty lists.
        """

        self.lineWordsList = []
        
        self.lineNumberList = []
        
        self.commentTextList = []
        
        self.commentNumberList = []


   
 
            

    def setError (

        self,
        text = None
        ) :


        """ Sets the error attributes. Prefixes with line number """

        if ( ( self.count is None ) or
             ( utilities.isEmpty( self.lineNumberList ) ) or
             ( self.count < 0 ) or
             ( self.count >= len( self.lineNumberList ) ) ) :

             utilities.error = utilities.string( text )

        else :

            utilities.error = utilities.string( self.lineNumberList[ self.count ] ) + " " + utilities.string( text )



    def splitLine (

        self,
        text = None,
        size = None,
        variable = None,
        delimiter = None
        ) :

        """ splits a line with some delimiter """
        

        # control: if no size defined, variable is true

        if not type( size ) == int : variable = True
        
        # sequences of tabs and spaces are merged, except for puntuation marks

        if ( ( delimiter == "\t" ) or ( delimiter == " " ) ) :

            delimiter2 = delimiter + delimiter

            while delimiter2 in text :

                text = text.replace( delimiter2, delimiter )

        if bool( variable ) : words = text.split( delimiter )

        elif ( type( self.lineSize ) == int ) and ( self.lineSize > 1 ) : words = text.split( delimiter, self.lineSize - 1 )

        else : words = text.split( delimiter )

                
        # empty list

        if utilities.isEmpty( words ) : return None

        # checks size


        if not type( size ) == int : return words

        elif len( words ) == size : return words

        elif len( words ) < size :
            
            self.setError( "addLine() - length of line incorrect (too short)" )

            return None

        elif not bool( variable )  :

            self.setError( "addLine() - length of line incorrect (too long)" )

            return None

        else : return words
             

