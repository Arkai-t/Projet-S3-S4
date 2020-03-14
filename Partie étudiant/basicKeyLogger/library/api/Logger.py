""" Provides functions for writing events and/or messages into files.

    """


from api.Utilities import *

from api.TableFile import *

from api.Clock import *

class Logger :

    """ Provides functions for writing events and/or messages into files.

        """


    # error
    
    error = None

    # keyword

    computerKeyword = None
   
    # duplicate file
    
    copyPath = None

    # current computer

    cpu = None
    
    # keyword

    dateKeyword = None

    # keyword

    errorKeyword = None

    # keyword

    eventKeyword = None

    # initial path of log (forced )
    
    initialPath = None

    # path of current log
    
    logPath = None

    # name of current log
    
    name = None
    
    # keyword

    noneKeyword = None
    
    # keyword

    resultKeyword = None

    # keyword

    softwareKeyword = None

    # keyword

    timestampKeyword = None

    # text to write to log in buffer mode

    text = None

    # keyword

    warningKeyword = None

    
    
    def __init__ (

        self,
        path = None,
        ) :

        """ Initializes the log object, opens the log file

            path is the path to the log file. Default path is ../log/_labBook/log.tsv. UNUSED

          
            Also, initializes a clock counter for time stamps. The time reference will be that of the most recent call to
            constructor

            Does not throw exceptions.

            """

       
        # no log path for now (important for reset, it tries to save previous files )

        self.logPath = None

        # default values

        self.setDefault()
        
        # default log path
            
        self.set( path = os.sep + "log.tsv" )

            
        
        

    def date (

        self,
        format = None,
        value = None
        ) :

        """ Returns a string with the current date and time in format YYYY MM DD HH:MM:SS

            format and value overrides the default values
            
            """

        if format is None : format = "%Y %m %d - %H:%M:%S"

        if value is None : value = time.localtime()
        
        return time.strftime(format , value )

    
        

        

    

    def extractComment (

        self,
        line = None
        ) :

        """ Returns a line truncated before the first comment delimiter

            Copy of TablFile.extractComment

        """

        if line is None : return None
    
        size = len( line )

        # loop on comment delimiters (note that EOL is considered a comment delimiter)
        
        for comment in commentDelimiters :
            
           
            position = line.find( comment, 0, size )
                    
            if ( ( position >= 0 ) and
                 ( position < size ) ) :
                size = position

        # Returns truncated line
        
        return line[ : size ]

    





    def path (

        self,
        name = None,
        extension = None
        ) :

        """ Returns a path to the file .logPath\\name.tsv ( or the given extension ) for the given script

            Default script = current script
            
            Default name is "log", i.e. a path to logfile
       
            Returns None if self.logPath is undefined

            """

        if utilities.isEmpty( name ) : name = "log"

        if extension is None : extension = "tsv"
        
        directory = utilities.pathDirectory( self.logPath )

        return utilities.normalizePath( directory + os.sep + name + "." + extension, normalize = False )



        
    def set (
        
        self,
        path = None
        ) :

        """ Sets or resets the log path """

        

        # sets new log path

        if path is None : return

        self.logPath = utilities.normalizePath( path, normalize = False )
        
        

    def setDefault ( self ) :

        """ default values """

        if self.computerKeyword is None : self.computerKeyword = "computer"

        if self.cpu is None : self.cpu = "none"
        
        if self.dateKeyword is None : self.dateKeyword = "date"

        if self.errorKeyword is None : self.errorKeyword = "error"

        if self.eventKeyword is None : self.eventKeyword = "event"

        if self.noneKeyword is None : self.noneKeyword = "none"
        
        if self.resultKeyword is None : self.resultKeyword = "result"

        if self.softwareKeyword is None : self.softwareKeyword = "software"

        if self.timestampKeyword is None : self.timestampKeyword = "timestampS"

        if self.warningKeyword is None : self.warningKeyword = "warning"
    
        

    def write (

        self,
        line = None,
        console = None,
        direct = None,
        ) :

        """ Writes a line in the log. Closes and reopens immediately 

            Returns True/False

            """

        direct = utilities.boolean( direct, default = True )

        console = utilities.integer( console, default = 0 )

        if line is None : return False

        if utilities.isEmpty( self.logPath ) : return True

        # console echo ( does not add end of line, it is already here )

        if bool( console ) :  print line,   # comma prevents end of line


        # bufferized
        
        if not bool( direct ) :

            if utilities.isEmpty( self.text ) : self.text = ""

            self.text = self.text + line

            return True

        # otherwise, sticks the previous text buffer before the line and writes

        if not utilities.isEmpty( self.text ) :

            line = self.text + line

            self.text = None
            

        result = utilities.fileAppend( self.logPath, line )

        if not result :

            utilities.error = "Logger - write : could not append to log files"

            return False


        # copy path is a list
        
        if type( self.copyPath ) == list :

            for copyPath in self.copyPath :
        
                result = utilities.fileAppend( copyPath, line )

                if not result :

                    utilities.error = "Logger - writeCopy : "  + copyPath

                    return False

        # copy path is a string
        
        elif not utilities.isEmpty( self.copyPath ) :

            result = utilities.fileAppend( self.copyPath, line )

            if not result :

                utilities.error = "Logger - writeCopy : "  + self.copyPath

                return False
            
    
        return True


        
    def writeCommentLine (

        self,
        logName = None,
        comment = None,
        console = None,
        direct = None
        ) :
        

        """ Writes a comment in log file and eventually prints it on console.

            comment is a sentence (spaces allowed). It will be preceded by # and considered a comment. By default ""

            console is a flag indicating whether the message is written on console(True) or not (False)

            logName is the name of the script in execution (default = no change).
            May be changed to write in a new log. In this case, closes current log and opens in append mode

            
            Returns True / False
            
            Does not throw exceptions.

            """


        # sets default values: None is an empty line
        
        if comment is None : comment = ""

        # builds line ( with EOL )
        
        line = utilities.commentDelimiter + " " + utilities.string( comment, default = "" ) + utilities.lineDelimiter

        # writes in log
        
        result = self.write(
            line,
            console = console,
            direct = direct,
            
            )

        if not result : utilities.error = "Logger - writeCommentLine : could not write comment"
        
        return result



    def writeEmptyLine (

        self,
        logName = None,
        console = None,
        direct = None,
        ) :
        

        """ Writes an empty line in log file and eventually prints it on console.

            console is a flag indicating whether the message is written on console(True) or not (False)
            
            logName is the name of the script in execution (default = no change).
            May be changed to write in a new log. In this case, closes current log and opens in append mode

            Returns True / False
            
            Does not throw exceptions.

            """

        # writes in log
        
        result = self.write(
            utilities.lineDelimiter,
            console = console,
            direct = direct
            )

        if not result : utilities.error = "writeEmptyLine"

        return result

    

    def writeError (

        self,
        logName = None,
        software = None,
        computer = None,
        date = None,
        timestampS = None,
        result = None,
        append = None,
        comment = None,
        console = None,
        direct = None,
        ) :
        
        """ Writes an event in log file and eventually prints it on console.

            logName is the name of the script in execution (default = no change).
            May be changed to write in a new log. In this case, closes current log and opens in append mode

            software is the origin of the event. 
            Normally, it is the caller's __name__ . By default, it is None

            computer is current computer
            Default is self.cpu

            date is the date + time of the event log, normally in format YYYY MM DD HH:MM:SS.
            By default, takes current date.

            timestampS is the time stamp of the event log in seconds, normally an integer.
            By default, takes current time stamp (absolute time in seconds)
            
            result is the result of the test. By default, None

            append is a string that is appended before the comment.
            WARNING: if append is defined it MUST be formatted according to the format of the log (tabs etc.)
            
            comment is a sentence (spaces allowed). It will be preceded by # and considered a comment. By default ""

            console is a flag indicating whether the message is written on console(True) or not (False)
            
            Returns True / False
            
            Does not throw exceptions.

            """
        
        return self.writeEvent(
                    logName = logName,
                    identifier = self.errorKeyword,
                    software = software,
                    computer = computer,
                    date = date,
                    timestampS = timestampS,
                    result = result,
                    append = append,
                    comment = comment,
                    console = console,
                    direct = direct
                    )
        





    def writeEvent (

        self,
        logName = None,
        identifier = None,
        software = None,
        computer = None,
        date = None,
        timestampS = None,
        result = None,
        append = None,
        comment = None,
        console = None,
        direct = None
        ) :
        
        """ Writes an event or and error in log file and eventually prints it on console.

            logName is the name of the log (default = no change).
            May be changed to write in a new log. In this case, closes current log and opens in append mode

            identifier is either "error" or "event" (default)

            software is the origin of the event. 
            Normally, it is the caller's __name__ . By default, it is None

            computer is current computer
            Default is self.cpu
            
            date is the date + time of the event log, normally in format YYYY MM DD HH:MM:SS.
            By default, takes current date.

            timestampS is the time stamp of the event log in seconds, normally an integer.
            By default, takes current time stamp (absolute time in seconds)
            
            result is the result of the test. By default, None

            append is a string that is appended before the comment.
            WARNING: if append is defined it MUST be formatted according to the format of the log (tabs etc.)
            
            comment is a sentence (spaces allowed). It will be preceded by # and considered a comment. By default ""

            console is a flag indicating whether the message is written on console(True) or not (False)
            
            Returns True / False
            
            Does not throw exceptions.

            """
        
        # sets default values

        console = utilities.integer( console, default = 0 )

        # identifier
        
        if utilities.isEmpty( identifier ) : identifier = self.eventKeyword
        
        # today in format YYYY MM DD HH:MM:SS
        
        if utilities.isEmpty( date ) : date = clock.date()

        # elapsed time since first call of clock in this session in musec.
        
        if timestampS is None : timestampS = clock.timeS()

        else : timestampS = float( timestampS )

        delimiter = utilities.fieldDelimiter

        # builds line

        line = ""

        # identifier
        
        if not identifier is None : line = line + identifier + delimiter

        # date (always)
        
        line = line + self.dateKeyword + delimiter + utilities.string( date, default = "" ) + delimiter
        
        # time stamp (always)

        line = line + self.timestampKeyword + delimiter + utilities.string( timestampS, default = "" )  + delimiter

        # computer and software
        
        if not computer is None : line = line + self.computerKeyword + delimiter + utilities.string( computer ) + delimiter 
        
        if not software is None : line = line + self.softwareKeyword + delimiter + utilities.string( software ) + delimiter

        # result
        
        if not result is None : line = line + self.resultKeyword + delimiter + utilities.string( result )

        # prints only the beginning ( console is 1, partial print ) 

        if console == 1 : print line

        # appended fields
        
        if not append is None : line = line + utilities.string( append )

        # final comment ( # separated )
        
        if not comment is None : line = line + \
                                        utilities.commentDelimiter + " " + \
                                        utilities.asciiToFlat( comment, default = "" )

        # EOL
        
        line = line + utilities.lineDelimiter

        # writes in log
        
        result = self.write(
            line,
            direct = direct,
            console = ( console > 1 )
            )

        if not result : utilities.error = "writeEventOrError"

        return result


    def writeWarning (
        
        self,
        logName = None,
        software = None,
        computer = None,
        date = None,
        timestampS = None,
        result = None,
        append = None,
        comment = None,
        console = None,
        direct = None,
        
        ) :
        
        """ Writes a warning in log file and eventually prints it on console.

            logName is the name of the script in execution (default = no change).
            May be changed to write in a new log. In this case, closes current log and opens in append mode

            software is the origin of the event. 
            Normally, it is the caller's __name__ . By default, it is None

            computer is current computer
            Default is self.cpu

            date is the date + time of the event log, normally in format YYYY MM DD HH:MM:SS.
            By default, takes current date.

            timestampS is the time stamp of the event log in seconds, normally an integer.
            By default, takes current time stamp (absolute time in seconds)
            
            result is the result of the test. By default, None

            append is a string that is appended before the comment.
            WARNING: if append is defined it MUST be formatted according to the format of the log (tabs etc.)
            
            comment is a sentence (spaces allowed). It will be preceded by # and considered a comment. By default ""

            console is a flag indicating whether the message is written on console(True) or not (False)
            
            Returns True / False
            
            Does not throw exceptions.

            """
        
        return self.writeEvent (
                    logName = logName,
                    identifier = self.warningKeyword,
                    software = software,
                    computer = computer,
                    date = date,
                    timestampS = timestampS,
                    result = result,
                    append = append,
                    comment = comment,
                    console = console,
                    direct = direct
                    )
        




    def writeFooter (
        
        self,
        text = None,
        logName = None,
        console = None,
        direct = None
        ) :

        """ Writes a footer with a given text

            The text may have several lines

            logName is the name of the script in execution (default = no change).
            May be changed to write in a new log. In this case, closes current log and opens in append mode

            Returns True / False

            """
        
        if text is None : text = ""

        # splits the text in lines
        
        lines = utilities.asciiToLines( text )
        
        self.writeEmptyLine(
            logName = logName, # for eventually changing log file name
            console = console,
            direct = direct
            )
        
        self.writeCommentLine(
            comment = None,
            console = console,
            direct = direct
            )
        
        for line in lines :
            
            self.writeCommentLine(
                comment = 12 * " " + line,
                console = console,
                direct = direct
                )
        
        self.writeCommentLine(
            comment = 48 * "-",
            console = console,
            direct = direct
            )
        
        self.writeCommentLine(
            comment = None,
            console = console,
            direct = direct
            )
        
        self.writeEmptyLine(
            console = console,
            direct = direct
            )


  


    def writeHeader (
        
        self,
        text = None,
        logName = None,
        console = None,
        direct = None
        ) :

        """ Writes a header with a given text

            The text may have several lines

            logName is the name of the script in execution (default = no change).
            May be changed to write in a new log. In this case, closes current log and opens in append mode


            Returns True / False

            """
        
        if text is None : text = ""

        # splits the text in lines
        
        lines = utilities.asciiToLines( text )
        
        self.writeEmptyLine(
            logName = logName, # for eventually changing log file name
            console = console,
            direct = direct
            ) 
        
        self.writeCommentLine(
            comment = None,
            console = console,
            direct = direct
            )
        
        self.writeCommentLine(
            comment = 48 * "-",
            console = console,
            direct = direct
            )
        
        for line in lines :
            
            self.writeCommentLine(
                comment = 12 * " " + line,
                console = console,
                direct = direct
                )
            
        self.writeCommentLine(
            comment = None,
            console = console,
            direct = direct
            )
        
        self.writeEmptyLine(
            console = console,
            direct = direct
            )








        
# creates the global singleton object if not already here

if not "logger" in globals() : logger = Logger()
         
    
       
            
        
        
        
        
            
   

        
