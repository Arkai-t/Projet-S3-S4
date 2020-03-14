

""" Book manager. Registers the notes and the events in notes file and log file.

    """

from api.Utilities import *

from api.Logger import *



class Book :

    """ Book manager. Registers the notes and the events in notes file and log file. """


    # count of events
    
    count = None

    # error description
    
    error = None

    # command received in an event
    
    eventCommand = None
   
    # event origin
    
    eventOrigin = None

    # text of event (string to instantiate)

    eventText = None
    
    # log path

    logPath = None

    # last sampling time in milliseconds
    
    lastTimeMs = None
    
    # directory of lab book
    
    notesDirectory = None

    # pending notes
    
    pendingDirectory = None

    # displays popup messages

    popup = None

    # first line of a note

    separationLine = 80 * "-" + utilities.lineDelimiter

    # text of last note

    text = None



    def __init__ ( self ) :

        """ Constructor

            name is the name used to identify the current script (and the communication directory)
            Recommended: DONT TOUCH, leave default = BOOK.

            """


        # prepares the variables using during book management

        self.resetVariables()

        # log  and notes file

        self.notesDirectory = sys.notesPath

        self.logPath = self.notesDirectory + "log.tsv"

        self.pendingDirectory = sys.pendingPath

        # Redirects the log manager to book's log file

        logger.set( self.logPath )





    def checkTable (

        self,
        table = None
        ) :

        """ Checks that a table contains a Note, i.e., a subject field and a text field
            
            Does NOT check correctness of content
            
            """

        if utilities.isEmpty( table ) : return False

        subjectFlag = False

        textFlag = False


        for line in table :

            if len( line ) < 3 : continue

            identifier = line[ 0 ].lower()

            if identifier == "subject" : subjectFlag = True

            elif identifier == "text" : textFlag = True

            if ( ( subjectFlag ) and ( textFlag ) ) : return True

        return False


        


    def message (
        
        self,
        sender = None,
        event = None,
        pattern = None,
        to = None,
        popup = None
        ) :


        """ Processes a message received from other processes.

            sender, event, subject + text are the fields of the event

            Note. If subject and text are undefined

            To is a path to one or several notes files ( a list, in this case )

            popup = callback to displays popup messages or not


            """
        
        # destination
        
        to = self.parseTarget( to )

        if utilities.isEmpty( to ) : return False
        
        
        # argument is a list of paths to notes files

        if type( to ) == list :

            for index in range( len( to ) ) :

                if not to[ index ] == "clipboard" : to[ index ] = utilities.normalizePath( to[ index ], normalize = False )

        # argument is a single notes file
        
        elif not utilities.isEmpty( to ) :

            to = utilities.normalizePath( to, normalize = False )

        # default = notes directory

        else :

            to = self.notesDirectory


        # popup windows

        previousPopup = self.popup
        
        if callable( popup ) : self.popup = popup

        # increments message counter

        if not type( self.count ) == int : self.count = 0
        
        self.count = self.count + 1

        # updates the context time variables
        
        utilities.setVariable( "date", clock.today() )

        utilities.setVariable( "time", clock.hour() )

        # direct call: assigns attributes

        if type( sender ) == str : self.eventOrigin = sender

        else : self.eventOrigin = utilities.getVariable( "program", default = "" )

        if type( event ) == str : self.eventCommand = event

        else : self.eventCommand = ""


        # pattern (or default)

        if not pattern is None : self.eventText = utilities.instantiate( pattern )

        else : self.eventText = utilities.instantiate( utilities.getMessage( "notePattern" ) )


        # writes to text file (the text will be placed in self.text at first call to writeText

        self.text = None

        # destination is a list of files

        if type( to ) == list :

            for item in to :

                self.writeText( path = item )

        # destination is a single file 

        else :

            self.writeText( path = to )


        # saves previous log path, registers and restores

        previousLogPath = logger.logPath

        logger.logPath = self.logPath

        self.writeLog( path = to )

        logger.logPath = previousLogPath

        # resets event variables (so that LabBook messages have no origin )

        self.eventOrigin = None

        self.eventCommand = None

        self.popup = previousPopup

        return True





    def noteToText ( self ) :

        """ fills attribute self.text with the note """

        # appends to the text

        if utilities.isEmpty( self.eventText ) : return

        # first line: separation ( ----- )

        text = self.separationLine + utilities.lineDelimiter

        # second line : date
                
        text = text + clock.date() + utilities.lineDelimiter

        # then, the pattern

        text = text + utilities.flatToAscii( self.eventText ) + utilities.lineDelimiter


        # stores the text of the note locally
        
        self.text = text

        

            
        
    def parseTarget (

        self,
        target = None
        ) :

        """ parses a text containing the name of destinations and returns a list of paths """

        if utilities.isEmpty( target ) : return None

        path = [ ]

        if "book" in target :

            path.append( self.notesDirectory  )
        
        if "pending" in target :
        
            path.append( self.pendingDirectory )

        if "object" in target :

            path.append( utilities.instantiate( "(_selected)", default = "" ) + os.sep + "notes" + os.sep )
        
        if "procedure" in target :
        
            path.append( utilities.instantiate( "(_procedure)", default = "" ) + os.sep + "notes" + os.sep )

        if "clipboard" in target :

            path.append( "clipboard" )
        
        # to data : tags file name with the cpu so that different logs can be merged

        if "data" in target :
        
            cpu = utilities.string( utilities.getVariable( "cpu", default = "" ), format = "underscore" )

            if not utilities.isEmpty( cpu ) : cpu = "_" + cpu

            path.append( utilities.instantiate( "(data)", default = "" )  + os.sep + "notes" + cpu + os.sep )
        
        # must have at least one destination

        if utilities.isEmpty( path ) : return None


        return path

        

            



    def resetVariables ( self ) :

        """ Activates the process """
        
        # count of events

        self.count = 0

        # starts now, in case
        
        self.lastTimeMs = 0

        utilities.error = ""



       
    
    def writeLog (

        self,
        path = None
        ) :
        

        """ Writes a standard event to log

            text is a string, a list of string or none (default is the current description)

            """


        # no notes path : takes that of log

        if path is None : path = self.notesDirectory

        # transforms the template into fields
        
        if utilities.isEmpty( self.eventText ) : return

        append = ""

        items = self.eventText.splitlines()

        index = 0

        size = len( items )

        while index < size :

            item = items[ index ].strip( " :-;,=" )

            index = index + 1

            words = utilities.textToWords(
                item,
                delimiters = [ " ", ":", ";", "=", ",", "-", "\t" ],
                number = 2
                )

            if len( words ) <= 0 : continue

            identifier = words[ 0 ]

            if len( words ) < 2 : value = ""

            else : value = words[ 1 ]

            # value is "..." : the remainder of the text is the value

            if value == "..." : 

                value = utilities.linesToAscii( items[ index : ] )

                index = size
            
            append = append + \
                     utilities.string( identifier, format = "identifier" ) + \
                     utilities.fieldDelimiter + \
                     utilities.asciiToFlat( value ) + \
                     utilities.fieldDelimiter

        # writes in log ( Logger detects whether logPath and copyPath are defined or not )
        
        logger.writeEvent(
            identifier = utilities.getMessage( "note" ),
            software = utilities.string( self.eventOrigin, format = "title" ),
            result = "ok",
            append = append
            )

        return True



    def writeText (

        self,
        path = None
        ) :

        """ Writes a text in notes file
        
            path is a text file into which the event is written ( appended )

            """


        # default path = current notes path

        if utilities.isEmpty( path ) : path = self.notesDirectory

        # the path is a directory : appends date and time to the name

        if path.endswith( os.sep ) :

            # pattern  of name

            name = utilities.getMessage( "noteFile" )
   
            name = utilities.instantiate( name )

            name = utilities.string( name, format = "strictunderscore" )
            
            if utilities.isEmpty( name ) : name = "note" + "_" + clock.date( format = "%Y_%m_%d_%H_%M_%S" )

            path = path + name + ".txt"

        # the text of the note has not already been built

        if utilities.isEmpty( self.text ) : self.noteToText()

        # this is not a text file, does nothing

        if path == "clipboard" :

            text = "clipboard"

            result = True

        
        # writes in file

        else :

            text = utilities.pathName( utilities.pathDirectory( path ) ) + os.sep + \
                   utilities.pathLastNameWithExtension( path )

            result = utilities.fileAppend( path, utilities.lineDelimiter + self.text )

            if not result : utilities.error = "Book - writeNotes"


        if not callable( self.popup ) : return
        

        if result :

            text = text + \
                   " " + \
                   utilities.getMessage( "written" )

            self.popup(
                text = text,
                mode = "line"
                )

        else :

            text = text + \
                   " " + \
                   utilities.getMessage( "notWritten" ) + \
                   "\n" + \
                   utilities.string( utilities.error, default = "" )

            self.popup(
                text = text,
                mode = "line",
                button = utilities.getMessage( "Continue" )
                )
                    


        
# creates the singleton if not already here


if not "book" in globals() : book = Book()
 


