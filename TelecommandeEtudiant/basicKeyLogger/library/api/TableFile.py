""" Table files management. Read/write and access formatted files (table files)

    Table files are organized in lines, composed of words
    Words are separated by TABs 
    Comments are managed separately, and can be reinserted when files are written
    
 
    """


from api.TableData import *


class TableFile ( TableData ) :
    
    """ Table files, e.g. script files and/or log files

        Tab files contain different types of lines, identified by a keyword,
        e.g., lines beginning with "trial x y z " are trials, "objects a b c " are objects, etc.

        Lines are composed of words (in a broad sense)

        By default, words are tab-separated, although this can be configurated.

        Words may contain spaces or any other character, but leading and trailing spaces are removed

        All the lines of a given type have the same number of words, eventually followed by comments

        Also, there are comment lines and/or empty lines. They are kept in a different structure and can be reinserted
        
        In the table format, there are no identifiers.
        The values are identified merely by the position of the words in the lines.
        All the lines must have the same number of words, once that comments are removed.
        
        The basic internal representation of a table file is a list of lines, each line being a list of words
        (i.e., a list of lists)


        """


    # file handler

    handler = None


    # line in file
    
    lineInFile = 0L


    # file name
    
    path = ""

    # size
    
    size = 0L

    # index of line in internal input buffer

    textIndex = None

    # entry text under the form of a list of strings ( lines )

    textList = None


    def __init__ ( self ) :
        
        
        """ Constructor. Does absolutely nothing
           
            """


        # initializes data and meta data
        
        TableData.__init__( self )




    def closeSource ( self ) :


        """ Closes the source, file or text """

        
        utilities.fileClose( self.handler )



    def closeTarget ( self ) :


        """ Closes the target, file or text """

        
        utilities.fileClose( self.handler )


        

    def openSource (

        self,
        path = None,
        text = None
        ) :

        """ Opens the source, either file or text """

        # this is a text

        if ( ( utilities.isEmpty( path ) ) and ( not utilities.isEmpty( text ) ) ) :

            self.textList = utilities.asciiToLines( text )

            self.textIndex = 0

            utilities.fileClose( self.handler )
            
            return True

        # this is a file

        else :
        
            # empties the entry buffer, may have remained after last reading

            self.textList = None

            self.textIndex = 0

            # path to file could not be set
           
            if not self.setPath( path ) :
                
                self.setError( "read-setPath() failed" )
                
                return False

            # file is not here
                
            if not utilities.filePresent( self.path ) :
                
                self.setError( "read-filePresent() failed" )
                
                return False

            
            # opens the handler, reads the lines and closes
            
            self.handler = utilities.fileOpen( self.path, "r" )
            
            if self.handler is None :
                
                self.setError( "read-fileOpen() failed" )
                
                return False

        return True



    def openTarget (

        self,
        path = None,
        text = None
        ) :

        """ Opens the target, either file or the global variable textList """

        # this is a text

        if ( ( utilities.isEmpty( path ) ) and ( not text is None ) ) :           

            self.textList = [ ]

            self.textIndex = 0

            utilities.fileClose( self.handler )
            
            return True

        # this is a file

        else :
        
            # empties the entry buffer, may have remained after last reading

            self.textList = None

            self.textIndex = 0
        
            # path to file could not be set
           
            if not self.setPath( path ) :
                
                self.setError( "read-setPath() failed" )
                
                return False
            
            # opens the handler, reads the lines and closes
            
            self.handler = utilities.fileOpen( self.path, "w" )
            
            if self.handler is None :
                
                self.setError( "write-fileOpen() failed" )
                
                return False

        return True

    

    def read (
        
        self,
        path = None,
        text = None,
        words = None,
        strict = None,
        variable = None,
        ) :

        """ Reads the file into lines

            Reads from a path and/or from a text.

            words is None or a fixed number of words

            void is a flag True if empty values are accepted, False otherwise

            if strict is True, refuses any character that is in the protection list ' ' must be <sp>, ',' <comma>, etc.

            Returns True if OK False otherwise

            Throws no exception

            
            """


        # initializes the lines

        self.resetData()
        
        # initializes the source, file or text

        result = self.openSource(
            path = path,
            text = text
            )

        if not result : return False

        # assigns to variable, whether defined or not
        
        self.lineSize = words

        # by default, everything ok
        
        result = True
        
        # reads lines one by one, stops when empty line
        
        self.count = 0              # effective line
    
        lineNumber = 0         # line number in file
            
        while True :

            line = self.readLine( lineNumber )

            if line is None :

                result = False

                break

            # line number in file
            
            lineNumber = lineNumber + 1
            
            # empty buffer (this is end of file, because the EOL is included in buffer)
            
            if len( line ) <= 0 : break

            # truncates the end of line and the comments: finds the leftmost comment or EOL delimiter
            
            line, comment = self.extractComment( line )

            # stores the comment line
            
            if len( comment ) > 0 :
                
                self.commentTextList.append( comment )
                
                self.commentNumberList.append( lineNumber )
            
            # empty line after removing comments -> stores in commentLines
            
            if len( line ) <= 0 : continue

                
            # appends the position of the line in the file
            
            self.lineNumberList.append( lineNumber )

            # processes and checks according to the type of file. words is a list of words, empty in case of problem
            
            result = self.addLine( line, words, strict, variable )
            
            # empty line (after removing comments and words) -> nothing
            
            if not result  : break

            # current line number
            
            self.count = self.count + 1 

        # that is all

        self.closeSource()

        return result



    

    def readAttributeValueList (
        
        self,
        path = None,
        text = None,
        strict = None,
        ) :

        """ Reads a file containing a list of lines, with one identifier per line (attribute) and a unique value
        
            The file is comma delimited
            
            Returns 2 arguments, a list of identifiers and a list of values (which may be themselves lists)

            In case of problem, returns 2 empyt lists

            """

        # reads, accepts space or tab, comma or = as first delimiter

        ok = self.read(
            path = path,
            text = text,
            words = 2,
            strict = strict
            )  # careful list with one element, this element is a list

        if not ok : return [], []

        identifiers = []
        
        values = []

        for line in self.lineWordsList :

            if len( line ) < 2 : continue    # anomaly: no pair on the line
            
            identifiers.append( line[ 0 ] )

            words = utilities.flatToAscii( line[ 1 ] )
            
            if len( words ) == 0 : values.append( "" )
            
            elif len( words ) == 1 : values.append( words[ 0 ] )
            
            else : values.append( words )

        return identifiers, values

    


    def readIdentifierValueList (
        
        self,
        path = None,
        text = None,
        strict = None
        ) :

        """ Alias for self.readAttributeValueList """
        
        return self.readAttributeValueList(
            path = path,
            text = text,
            strict = strict
            )





    def readLine (

        self,
        lineNumber = None
        ) :

        """ Reads a line. In case of problem, closes handler, sets error and returns None """


        # this is from a buffer
        
        if not utilities.isEmpty( self.textList ) :

            # end of source = empty string (NOT None, which is error )
            
            if not utilities.isIndex( self.textIndex, self.textList ) : return ""

            line = self.textList[ self.textIndex ]

            self.textIndex = self.textIndex + 1

            return line

        # this is from a file ( handler is open )
        
        try :
            
            line = self.handler.readline()

            return line
            
        except Exception, exception :
            
            utilities.fileClose( self.handler )
            
            self.setError( "read-readLine - exception reading" )
            
            return None
            


    def readList (

        self,
        path = None,
        text = None,
        strict = None
        ) :

        """ Alias for readValueList """

        return self.readValueList(
            path = path,
            text = text,
            strict = strict
            )




    def readTable (

        self,
        path = None,
        text = None,
        size = None,
        strict = None,
        variable = None
        ) :

        """ Alias for readValueTable """

        return self.readValueTable(
            path = path,
            text = text,
            size = size,
            strict = strict,
            variable = variable
            )


    

    def readValueList (
        
        self,
        path = None,
        text = None,
        strict = None,
        ) :

        """ Reads a file containing a list of lines, with one value per line
                   
            If the value is comma separated, it is itself a list

            Returns 2 arguments, a list of identifiers and a list of values (which may be themselves lists)

            In case of problem, returns 2 empty lists

            """

        ok = self.read(
            path = path,
            text = text,
            words = 1,
            strict = strict
            )

        if not ok : return []

        values = []

        for line in self.lineWordsList :

            # split with commas
            
            words = utilities.flatToLines( line[ 0 ] )

            if len( words ) == 0 : values.append( "" )
            
            elif len( words ) == 1 : values.append( words[ 0 ] )
            
            else : values.append( words )
         

        return values


    def readValueTable (

        self,
        path = None,
        text = None,
        size = None,
        strict = None,
        variable = None
        ) :

        """ Reads a table of values 

            Path is the file

            Size in the number of fields of each line

            if variable, splits last field
            
            """
        

        ok = self.read(
            path = path,
            text = text,
            words = size,
            strict = strict,
            variable = variable
            )

        if not ok : return []

        if utilities.isEmpty( self.lineWordsList ) : return [ ]

        return self.lineWordsList




    def setPath (
        
        self,
        path = None
        ) :

        """ Initializes the file name self.path and normalizes it.

            By default, keeps the old self.path, but normalizes it.

            Returns True if OK, False otherwise

            """

        if path is None : return True
        
        # normalizes the path
        
        path = utilities.normalizePath( path, normalize = False )
        
        self.path = path

        return True



    def tableToText (

        self,
        values = None,
        fieldDelimiter = None,
        commentDelimiter = None
        ) :

        """ Alias for writeTable """

        ok = self.writeTable(
            table = values,
            text = True,
            fieldDelimiter = fieldDelimiter,
            commentDelimiter = commentDelimiter
            )

        if utilities.isEmpty( self.textList ) : return ""

        return utilities.linesToAscii( self.textList )


    def write (

        self,
        path = None,
        table = None,
        identifiers = None,
        attributes = None,
        values = None,
        lists = None,
        text = False,
        fieldDelimiter = None,
        commentDelimiter = None
        ) :

        """ general write method: according to arguments, writes a table, attribute value lists or a list of values """

        # normalizes attributes ( alias identifiers = values )

        if ( ( identifiers is None ) and ( not attributes is None ) ) : identifiers = attributes

        # table
        
        if not utilities.isEmpty( table ) :

            ok = self.writeTable(
                table = table,
                path = path,
                text = text,
                fieldDelimiter = fieldDelimiter,
                commentDelimiter = commentDelimiter
                )

        # list of lists
        
        elif not utilities.isEmpty( lists ) :

            ok = self.writeLists(
                lists = lists,
                path = path,
                text = text,
                fieldDelimiter = fieldDelimiter,
                commentDelimiter = commentDelimiter
                )

        # identifiers-values or attributes-values            

        elif ( ( not utilities.isEmpty( identifiers ) ) and ( not utilities.isEmpty( values ) ) ) :

            ok = self.writeAttributeValueList (
                identifiers = identifiers,
                values = values,
                path = path,
                text = text,
                fieldDelimiter = fieldDelimiter,
                commentDelimiter = commentDelimiter
                )
            
        # values
        
        elif not utilities.isEmpty( values ) :

            ok = self.writeValueList (
                values = values,
                path = path,
                text = text,
                fieldDelimiter = fieldDelimiter,
                commentDelimiter = commentDelimiter
                )

        else :

            ok = False

        return ok
            

        
        

    def writeLinesAndComments (
        
        self,
        path = None,
        text = False,
        fieldDelimiter = None,
        commentDelimiter = None
        ) :

        """ Writes the lines and the comments to a file.

            The data written is :
            lines[] and lineNumberList[]
            comments[] and commentNumbers[]

            If the argument path is defined, self.path is initialized

            text is a flag, if it is true, the attribute self.text is initialized with the content of the file

            If commentNumbers and lineNumberList are defined, comments and lines are inserted like in the initial file,
            Empty lines are eventually added.
            
            Returns True if OK False otherwise

            Throws no exception
        """

        # default field & comment delimiters

        if fieldDelimiter is None : fieldDelimiter = utilities.fieldDelimiter

        if commentDelimiter is None : commentDelimiter = utilities.commentDelimiter

        # initializes the target, file or list of lines

        result = self.openTarget(
            path = path,
            text = text
            )

         
        # for simplicity, transforms undefined lists into empty lists
        
        if self.lineWordsList is None : self.lineWordsList = []
        
        if self.commentTextList is None : self.commentTextList = []
        
        if self.lineNumberList is None : self.lineNumberList = []
        
        if self.commentNumberList is None : self.commentNumberList = []

        currentLine = 1             # line number in file
        
        iLine = 0                   # index in self.lineWordsList
        
        iComment = 0                # index in self.commentTextList
        
        iLineMax = len( self.lineWordsList )
        
        iCommentMax = len( self.commentTextList )

        # by default, OK
        
        result = True
            
        while True :

            # finished with comments AND lines
            
            if ( ( iLine >= iLineMax ) and ( iComment >= iCommentMax ) ) : break

            # determines position (line number in file) of current line and current comment
            
            # line is undefined (all lines already written)
            
            if iLine >= iLineMax : lineNumber = -1

            # line number is undefined (e.g., comments entered manually, not from file)
            
            elif iLine >= len( self.lineNumberList ) : lineNumber = currentLine

            # comment is defined, its position (number) also.
            
            else : lineNumber = self.lineNumberList[ iLine ]
            
            # comment is undefined (all comments already written)
            
            if ( iComment >= iCommentMax ) : commentNumber = -1

            # comment line number is undefined (e.g., comments entered manually, not from file)
            
            elif iComment >= len( self.commentNumberList ) : commentNumber = currentLine

            # comment is defined, its position (number) also.
            
            else : commentNumber = self.commentNumberList[ iComment ]
                
            # determines what is written now, comment, line or both
            
            # comment undefined, we are sure that fileNumber >= 0, see first break in loop
            
            if commentNumber < 0 :
                
                next = "Line"
                
                emptyLines = lineNumber - currentLine

            # line undefined, we are sure that commentNumber >= 0, see first break in loop
            
            elif lineNumber < 0 :
                
                next = "Comment"
                
                emptyLines = commentNumber - currentLine

            # here lineNumber and commentNumber are >= 0: the lowest is the first written
            
            elif lineNumber < commentNumber :
                
                next = "Line"
                
                emptyLines = lineNumber - currentLine

            elif commentNumber < lineNumber :
                
                next = "Comment"
                
                emptyLines = commentNumber - currentLine

            else :
                
                next = "Both"
                
                emptyLines = commentNumber - currentLine

                            
            # empty lines up to the position of next comment and/or line
            
            emptyLines = self.writeEmptyLines( emptyLines )
            
            if emptyLines < 0 :
                
                result = False
                
                break  # IO error

            currentLine = currentLine + emptyLines
            
            # comment before line (or no line)
            
            if next == "Comment" :

                # writes comment
                
                writtenComments = self.writeComment(
                    index = iComment,
                    endOfLine = True,
                    commentDelimiter = commentDelimiter
                    )

                if writtenComments < 0 :
                    
                    result = False
                    
                    break  # IO error

                currentLine = currentLine + writtenComments

                iComment = iComment + 1

            # line before comment or no comment
            
            elif next == "Line" :

                # writes line
                
                writtenLines = self.writeLine(
                    index = iLine,
                    endOfLine = True,
                    fieldDelimiter = fieldDelimiter
                    )

                if writtenLines < 0 :
                    
                    result = False
                    
                    break  # IO error

                currentLine = currentLine + writtenLines

                iLine = iLine + 1


            # if line and comments are at the same position writes line-comment- eol
            
            else : # next == "Both" :
        
                writtenLines = self.writeLine(
                    index = iLine,
                    endOfLine = False,
                    fieldDelimiter = fieldDelimiter
                    )
                
                if writtenLines < 0 :
                    
                    result = False
                    
                    break  # IO error

                writtenComments = self.writeComment(
                    index = iComment,
                    endOfLine = True,
                    commentDelimiter = commentDelimiter
                    )

                if writtenComments < 0 :
                    
                    result = False
                    
                    break  # IO error

                # wrote something: increments current position in file
                
                if writtenLines + writtenComments > 0 :
                    
                    currentLine = currentLine + 1

                iLine = iLine + 1
                
                iComment = iComment + 1

        # error
        
        if not result : self.setError( "write ( line " + utilities.string(iLine) + " )" )
  
        # that is all

        self.closeTarget()

        return result




    def writeAttributeValueList (
        
        self,
        identifiers = None,
        attributes = None,
        values = None,
        path = None,
        text = None,
        fieldDelimiter = None,
        commentDelimiter = None
        ) :

        """ Writes an attribute value list into a file.

            The file is comma delimited

            The file contains 1 pair per line, one identifier (attribute) and one unique value

            In case of multiple values, a single value, comma delimited, is generated
        

            Returns True/False

            """

        # aliasing attributes = identifiers

        if ( ( identifiers is None ) and ( not attributes is None ) ) : identifiers = attributes

        return self.writeLists(
            lists = [ identifiers, values ],
            path = path,
            text = text,
            fieldDelimiter = fieldDelimiter,
            commentDelimiter = commentDelimiter
            )

    
##
##        # checks arguments
##        
##        if identifiers is None : identifiers = [ ]
##        
##        if values is None : values = [ ]
##        
##        if len( values ) <> len( identifiers ) :
##            
##            self.setError( "writeAttributeList() - size error" )
##            
##            return False
##
##        # empties comments & position of lines & commentsin the source file
##        
##        self.commentTextList = [ ]
##        
##        self.commentNumberList = [ ]
##        
##        self.lineNumberList = [ ]
##        
##        # generates the lines to write in file
##        
##        self.lineWordsList = [ ]
##        
##        for index in range( len( identifiers ) ) :
##
##            self.lineWordsList.append( [ ] )
##            
##            self.lineWordsList[ -1 ].append( identifiers[ index ] )
##
##            # list: a string comma-delimited
##           
##            if type( values[ index ] ) == list :  text = utilities.listToFlat( values[ index ] )
##
##            # string : flattens ( recodes spaces tab etc )
##           
##            elif type( values[ index ] ) == str :  text = utilities.asciiToFlat( values[ index ] )
##            
##            # a non-string , non-list value
##            
##            else : text = utilities.string( values[ index ] )
##
##            # void
##            
##            if utilities.isEmpty( text ) : text = utilities.voidCode
##
##            self.lineWordsList[ -1 ].append( text )
##        
##        ok = self.writeLinesAndComments(
##            path = path,
##            text = text,
##            fieldDelimiter = fieldDelimiter,
##            commentDelimiter = commentDelimiter
##            )
##
##        return ok
        


    def writeLists (
        
        self,
        lists = None,
        path = None,
        text = None,
        fieldDelimiter = None,
        commentDelimiter = None
        ) :

        """ Writes a list of lists as a table.

            The file is comma-delimited

            The file contains 1 pair per line, one identifier (attribute) and one unique value

            In case of multiple values, a single value, comma delimited, is generated
        

            Returns True/False

            """

        # checks arguments

        if not type( lists ) == list :
            
            self.setError( "writeLists() - invalid lists" )
            
            return False

        if utilities.isEmpty( lists ) : return False

        size = None
        
        for item in lists :

            if not type( item ) == list :

                self.setError( "writeLists() - invalid lists" )
                
                return False

            if size is None : size = len( item )

            elif not len( item ) == size :

                self.setError( "writeLists() - lists of different size" )
                
                return False
                

        # empties comments & position of lines & commentsin the source file
        
        self.commentTextList = [ ]
        
        self.commentNumberList = [ ]
        
        self.lineNumberList = [ ]
        
        # generates the lines to write in file
        
        self.lineWordsList = [ ]
        
        for index in range( size ) :

            self.lineWordsList.append( [ ] )

            for item in lists :

                value = item[ index ]
                
                # list: a string comma-delimited
               
                if type( value ) == list :  value = utilities.listToFlat( value )

                # string : flattens ( recodes spaces tab etc )
               
                elif type( value ) == str :  value = utilities.asciiToFlat( value, default = utilities.voidCode )
                
                # a non-string , non-list value
                
                else : value = utilities.string( value )

                # void
                
                if utilities.isEmpty( value ) : value = utilities.voidCode

                self.lineWordsList[ -1 ].append( value )

        # writes the words
        
        ok = self.writeLinesAndComments(
            path = path,
            text = text,
            fieldDelimiter = fieldDelimiter,
            commentDelimiter = commentDelimiter
            )

        return ok
        



    def writeComment (
        
        self,
        index = None,
        endOfLine = True,
        commentDelimiter = None
        ) :

        """ Writes self.commentTextList [ index ] in self.handler (already open), with or without end of line.

            according to endOfLine (default value True) writes an EOL character or not, but only if comment does not
            terminates with end of line.

            Returns the number of written lines (0 if out of bounds, 1 if OK) or -1 if IO error

            """

        # default comment delimiter

        if commentDelimiter is None : commentDelimiter = utilities.commentDelimiter

        # not a correct index, or no comment
        
        if not utilities.isIndex( index, self.lineWordsList ) :

            writtenComments = 0
        
        # writes to lines

        elif not self.textList is None :

            # adds an empty line
            
            if not utilities.isIndex( self.textIndex, self.textList ) : self.textList.append( "" )

            selt.textList[ -1 ] = self.textList[ -1 ] + \
                                  commentDelimiter + \
                                  utilities.string( self.commentTextList[ index ], default = "" ) 
            
            if ( ( endOfLine ) and ( not self.commentTextList[ index ].endswith( utilities.lineDelimiter ) ) ):

                self.textIndex = self.textIndex + 1

            writtenComments = 1

        # no handler
        
        elif self.handler is None :

            writtenComments = -1

        # handler
        
        else :
       
            try :
                
                self.handler.write( commentDelimiter + utilities.string( self.commentTextList[ index ], default = "" ) )
                
                if ( ( endOfLine ) and ( not self.commentTextList[ index ].endswith( utilities.lineDelimiter ) ) ):
                    
                    self.handler.write( utilities.lineDelimiter )
                    
                writtenComments = 1
                    
            except Exception, exception :
                
                utilities.fileClose( self.handler )
                
                self.setError( "writeComment-write() - exception" )
                
                writtenComments = -1

        return writtenComments
    






    def writeEmptyLines (
        
        self,
        emptyLines
        ) :

        """ Writes empty lines in self.handler (already open)

            Returns the number of written lines (0 if the argument is <= 0) if OK, -1 if IO error

            """
       
        if emptyLines is None : return 0

        if emptyLines <= 0 : return 0

        if not self.textList is None :

            self.textList.extend( emptyLines * "" )

            self.textIndex = self.textIndex + emptyLines


        elif self.handler is None :

            emptyLines = -1

        # there is a handler

        else :

            try :
                
                self.handler.write( emptyLines * utilities.lineDelimiter )
                    
            except Exception, exception :
                
                utilities.fileClose( self.handler )
                
                self.setError( "writeEmptyLines-write() - exception" )
                
                emptyLines = -1

        return emptyLines




    def writeLine (
        
        self,
        index = None,
        endOfLine = True,
        fieldDelimiter = None
        ) :

        """ Writes self.lineWordsList [ index ] in self.handler (already open), with or without end of line.

            according to endOfLine (default value True) writes an EOL character or not.

            Returns the number of written lines (0 if out of bounds, 1 if OK) or -1 if IO error

            """

        # default field delimiter

        if fieldDelimiter is None : fieldDelimiter = utilities.fieldDelimiter

        # not a correct index
        
        if not utilities.isIndex( index, self.lineWordsList ) :

            writtenLines = 0
        
        # writes to lines

        elif not self.textList is None :

            # adds an empty line
            
            if not utilities.isIndex( self.textIndex, self.textList ) : self.textList.append( "" )

            for word in self.lineWordsList[ index ] :

                # floats: overrides str(), which looses decimals

                if type( word ) == float : word = ( self.floatFormat % word ).strip()

                # empty or undefined : replaced by <void>

                elif not type( word ) == str : word = utilities.string( word, default = utilities.voidCode )

                elif utilities.isEmpty( word ) : word = utilities.voidCode
                
                self.textList[ -1 ] = self.textList[ -1 ] + word + fieldDelimiter
                
            if endOfLine:
                
                self.textIndex = self.textIndex + 1

            writtenLines = 1

        # no handler
        
        elif self.handler is None :

            writtenLines = -1

        # handler
        
        else :
       
            try :

                for word in self.lineWordsList[ index ] :

                    # floats: overrides str(), which looses decimals

                    if type( word ) == float : word = ( self.floatFormat % word ).strip()

                    # empty or undefined : replaced by <void>

                    elif not type( word ) == str : word = utilities.string( word, default = utilities.voidCode )

                    elif utilities.isEmpty( word ) : word = utilities.voidCode
                    
                    self.handler.write( word + fieldDelimiter )
                    
                if endOfLine:
                    
                    self.handler.write( utilities.lineDelimiter )
                    
                writtenLines = 1
                    
            except Exception, exception :
                
                utilities.fileClose( self.handler )
                
                self.setError( "writeLine-write() - exception" )
                
                writtenLines = -1

        return writtenLines
    
    

    def writeList (
        
        self,
        values = None,
        path = None,
        text = None,
        fieldDelimiter = None,
        commentDelimiter = None
        ) :

        """ Writes a single list (alias for writeValueList) """

        ok = self.writeLists(
            lists = [ values ],
            path = path,
            text = text,
            fieldDelimiter = fieldDelimiter,
            commentDelimiter = commentDelimiter
            )

        return ok

        


    def writeTable (
        
        self,
        values = None,
        table = None,
        path = None,
        text = None,
        fieldDelimiter = None,
        commentDelimiter = None
        ) :

        """ Writes a matrix of values, i.e. a table file
      
            Returns True/False

            """


        # checks arguments (aliasing table - values )

        if ( ( table is None ) and ( not values is None ) ) : table = values
        
        if table is None : table = [ ]
        
        # empties comments & position of lines & commentsin the source file
        
        self.commentTextList = [ ]
        
        self.commentNumberList = [ ]
        
        self.lineNumberList = [ ]
        
        # generates the lines to write in file
        
        self.lineWordsList = [ ]
        
        for index in range( len( table ) ) :

            value = table [ index ]

            if value is None : continue

            elif not type( value ) == list : value = [ value ]

            elif utilities.isEmpty( value ) : continue

            self.lineWordsList.append( list( value ) )

        
        ok = self.writeLinesAndComments(
            path = path,
            text = text,
            fieldDelimiter = fieldDelimiter,
            commentDelimiter = commentDelimiter
            )

        return ok



    def writeValueList (
        
        self,
        values = None,
        path = None,
        text = None,
        fieldDelimiter = None,
        commentDelimiter = None
        ) :

        """ Writes a list into a file.

            The file is comma delimited

            The file contains 1 value per line

            In case of multiple values, a single value, comma delimited, is generated
      
            Returns True/False

            """


        ok = self.writeLists(
            lists = [ values ],
            path = path,
            text = text,
            fieldDelimiter = fieldDelimiter,
            commentDelimiter = commentDelimiter
            )

        return ok

##        # checks arguments
##        
##        if values is None : values = [ ]
##        
##        # empties comments & position of lines & commentsin the source file
##        
##        self.commentTextList = [ ]
##        
##        self.commentNumberList = [ ]
##        
##        self.lineNumberList = [ ]
##        
##        # generates the lines to write in file
##        
##        self.lineWordsList = [ ]
##        
##        for index in range( len( values ) ) :
##
##            self.lineWordsList.append( [ ] )
##
##            # list: a string comma-delimited
##            
##            if type( values[ index ] ) is list :  text = utilities.listToFlat( values[ index ] )
##
##            # else: void
##            
##            elif values[ index ] is None : text = ""
##
##            # else a simple word
##            
##            else : text = utilities.string( values[ index ] )
##
##            self.lineWordsList[ -1 ].append( text )
##
##        
##        ok = self.writeLinesAndComments(
##            path = path,
##            text = text,
##            fieldDelimiter = fieldDelimiter,
##            commentDelimiter = commentDelimiter
##            )
##
##        return ok


# -----------------------------------
# creates the global singleton object if not already here
#

if not "tableFile" in globals() : tableFile = TableFile()
         
        

