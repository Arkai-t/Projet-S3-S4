#!

""" Key Logger for Windows """

import gc

import math

import os

import sys

import time

from api.External import *

from guiPygame.StateWindow import *

if sys.platform == "win32" :

    import pythoncom    

    import pyHook       

    import win32api     


class KeyLogger ( StateWindow ) :

    """ Key Logger for Windows. Captures keyboard and mouse events from all applications
        and produces logs in two different formats, Key logs and KPC logs ( see below )

        The logger is launched by the external script startKeyLogger.py* (it calls method startLogger)

        When the logger launched, a window is displayed, with the path to current key log.
        The application records all keyboard and mouse events from windows event thread. It is frozen, i.e., even the
        close button is deactivated.

        To suspend temporarily the recording and to resume it, use external scripts suspendKeyLogger.py* and
        resumeKeyLogger.py*. These scripts inject specific keys in the event thread of Windows.

        To stop the recording, click on the window or use the script stopKeyLogger.py*. It injects a specific
        key in the event thread of windows.

        To place specific marks in the log, e.g., start of a test session, of a block or a trial, use the scripts:
        startSession.py*. stopSession.py*, startBlock.py*, etc.
        These scripts inject special keys in the event thread that are captured by the Key Logger(s) currently running.


        Key logs contain user actions on keyboard and mouse:
            key press or release,
            mouse move
            mouse wheel
            mouse button press and release
            start* and stop* , injected events that indicate start and stop of test sessions, blocks trials.

            see documentation of function writeLog for file format

        Kpc logs contains operations, i.e.,
            P = point at a position x,y,
            C = click a mouse button
            K = enter key or press function key
            A = automatic key, e.g., auto repeat
            W = rolls mouse wheel
            Q = idle entry ( equivalent to pauses, or M operations in KLM models )

            see documentation of writeKpc for file format

        The operations of KPC logs are composed of multiple key events. For instance, a Point is composed of a sequence
        of mouse moves, a Wheel is composed of a sequence of mouse wheel elementary movements, etc.

        As a consequence, THE KPC LOGS ARE NOT FULLY SEQUENTIAL: the operations can overlap in time. For instance you
        move the mouse with one hand and you write with the other; you click while moving the mouse (you do not stop
        your movement while clicking, etc.).

        The KPC log contains the operations in order of increasing start time. For each operation, it indicates the start
        time, the total duration and the time of overlap.
        
        The overlaps occurs for Point and Wheel operations, and for the Quiet periods. Conversely, C, K and A operations
        are atomic.

        The quiet periods correspond to a pause in the actioning of mouse and keyboard. They are detected when there are
        no events for a duration equal or superior to 1 second ( this default value can be changed from the configuration
        file ).

            Former models like KPC assumed that pauses were indicators of mental activity. This is certainly true in
            some cases, but there may be other reasons. So we prefer to assume nothing about the nature of the pauses.
            
        
        The conversion from Keylogs to KPC logs is as follows
        
        Q ( quiet period )
        
        detection: difference between the time T of current event En and time Tn-1 of event En-1 >= pauseThreshold (1s).
        
        start time: Tn-1  + sampling period (10ms)
        
        stop time: the time Tn+1 of next event, En+1

            Note that a Q events may end before the next operation ( K P C W A  ) starts (because some key events do not
            start operations)

        K ( key of keyboard )

        detection: a key press event that corresponds to a key that was not already pressed.

            Note that a combination shift+a corresponds to 2 K operations.

        The corresponding key is the character corresponding to the key if it is displayable (in this case the key log
        contains an ASCII code for the key), the descriptor provided by the key log(e.g.,  Lshift ) otherwise.

            the prefix "Alt+" is added if some ALT key is currently pressed

            the prefix "Ctrl+" is added if some CONTROL key is currently pressed

            the prefix "Shift+" is added if some SHIFT key is currently pressed and the key is not an alphabetical, e.g.
            you may have "Shift+1", but "A", not "Shift+a".
            

        The start time of a K event is the time Tn of event En of the key press.

        The end time it the start time of the next operation in the KPC log.
        
        
        A ( automatic key )

        detection: a key press event that corresponds to a key that 1) is already pressed, 2) is not a special key
        CONTROL, SHIFT or ALT.

        The corresponding key, the start time and the endtime are determined like for K events.

        C:

        detection: a mouse press event.

        Attributes of the event: the corresponding button is "left", "center" or "right". Coordinates X, Y.
        
        The start time is the time Tn of event En of the button press.

        The end time it the start time of the next operation in the KPC log.

        P ( pointing )

        detection: a mouse move event that is occurring when there is no Point operation in execution (see below)

        Attributes of the event initial and final coordinates X, Y. distance between initial and final point ( straight
        line ), length of the path followed between initial and final points.

        start time : the time Tn of the mouse move event

        Detection of the end : when the delay between two mouse move events is larger than a continuity threshold (100 ms)
        and when a different event occurs meanwhile, e.g.,

            "mouse move                       mouse move" is OK ( a Q period occurs, but the P operation follows)
                        <  10 seconcs  ...    >

            "mouse move  click    mouse move" is OK ( a C operation occurs, but the P operation follows)
                        <  50 ms >

                        
            "mouse move      Click        mouse move" is not OK: the P operation ends.
                         <    200 ms   >

        end time: the start time of the next operation in the KPC log.


        W ( mouse wheeling )

        detection: a mouse wheel event that is occurring when there is no Wheel operation in execution (see below)

        Attributes of the event initial coordinates X, Y.
        distance in steps ( sum of the wheel movements upwards +1 or downwards -1)
        number of wheel movements ( may be higher than distance, if user went back and forth).

        start time : the time Tn of the mouse wheel event

        Detection of the end : when the delay between two mouse wheel events is larger than a continuity threshold (100 ms)
        and when a different event occurs meanwhile, e.g.,

            "mouse wheel                       mouse wheel" is OK ( a Q period occurs, but the W operation follows)
                        <  10 seconcs  ...    >
                        
            "mouse wheel  mouse move   mouse wheel" is OK ( a P operation starts, but the W operation follows)
                        <  50 ms      >

            "mouse wheel      Click     mouse wheel" is not OK: the W operation ends.
                         <    200 ms   >

        end time: the start time of the next operation in the KPC log.

        Finally, the duration of an operation is the difference end time - start time ( in fact, the duration is stored
        but not the end time. We only used the end time for simplifity in the foregoing explanations)

        The duration of overlap of operation X is the sum of the time intervals in which some other operation occurs.
       
        """

    # flag arguments are ok

    argumentFlag = None
    
    # current block

    block = None

    # index of current event in eventList

    eventIndex = None

    # list of events
    
    eventList = None

    # window where last event occurred

    eventWindow = None

    # handler of log file

    fileHandler = None

    # logger is frozen ( suspended ) or not

    frozen = None

    # hook manager to capture window's events

    hookManager = None

    # index of active mouse move in kpc list

    kpcPointIndex = None

    # index of active Quiet operation in kpc list

    kpcQuietIndex = None

    # key currently in repetition ( in kpc list )

    kpcRepeatKey = None

    # index of active mouse wheel in kpc list

    kpcWheelIndex = None

    # offset to compute absolute time from event's time stamp

    offsetTimeS = None

    # buffer of KPC events

    operationList = None

    # buttons currently pressed ( in producing KPC log )

    pressedButtonList = None

    # time of press of button in S
    
    pressedButtonTimeList = None

    # keys currently pressed ( in producing kpc log )

    pressedKeyList = None

    # time of press of key in S
    
    pressedKeyTimeList = None

    # number of events that were removed from log ( for duplicate time stamps or crossed time stamps )

    removed = None

    # special keys, shift, alt, etc. ( in producing kpc log )

    reservedKeyList = None

    # current session

    session = None
    
    # start time in seconds ( time stamp of first event received )

    startTimeS = None

    # path to temporary file

    temporaryPath = None

    # current trial

    trial = None

    # configuration of key logger
    
    from keylogger_configuration import *

    try :

        from configuration.keylogger_configuration import *

    except Exception, exception :

        from keylogger_configuration import *

    # configuration of window
    
    from window_configuration import *

    try :

        from configuration.window_configuration import *

    except Exception, exception :

        from window_configuration import *




    def __init__ ( self ) :


        """ Constructor """

        self.argumentFlag = self.setArguments()

        self.setDefault()

        StateWindow.__init__( self )

        self.setPaths()

        self.checkIO()



    def appendEvent (

        self,
        event
        ) :

        """ Adds an event at the end of self.eventList.

            Completes it with date (may change during the logging).

            """


        # log is frozen.

        if bool( self.frozen ) : return False

        # reference time set at first event
        
        if self.startTimeS is None : self.startTimeS = float( event.Time ) / 1000.

        if self.offsetTimeS is None : self.offsetTimeS = time.time() - float( event.Time ) / 1000.

        # increments size of eventList
        
        if not self.isIndex( self.eventIndex, self.eventList ) :

            if self.eventIndex is None : self.eventIndex = 0

            if self.eventList is None : self.eventList = [ ]

            if self.eventIndex >= len( self.eventList ) : self.eventList = self.eventList + self.bufferSize * [ None ]

        # appends the event
        
        self.eventList[ self.eventIndex ] = event

        self.eventIndex = self.eventIndex + 1

        # date and hour of the event

        event.date = time.strftime( "%Y %m %d - %H:%M:%S", time.localtime() )

        return True



                
    def buildKpc ( self ) :

        """ builds the log of KPC operations in memory, self.operationList, from the FILE key_log.tsv

            Note. Reading the log file again is somehow slower than using the memory buffer self.eventList
            but it allows building the KPC log at any time after the end of loggingm and building different
            versions of the KPC log with different time constants.
            
            """

        # opens log file (returns None if void, does not exist, etc.)

        fileHandler = self.fileOpen( self.logPath, mode = "r" )

        if fileHandler is None : return False
        
        self.operationList = [ ]

        self.pressedKeyList = [ ]

        self.pressedKeyTimeList = [ ]

        self.pressedButtonList = [ ]

        self.pressedButtonTimeList = [ ]

        # time stamp of 1st event ( in key log )

        if not bool( self.absoluteFlag ) : previousTimeStampS = 0.

        elif ( not self.startTimeS is None ) and ( not self.offsetTimeS is None ) : previousTimeStampS = self.startTimeS + self.offsetTimeS

        else : previousTimeStampS = 0.
        
        # index of last operation ( in KPC log )

        previousOperation = -1
        
        # indexes of current point operaton, quiet operation and wheel operation ( may bo != last operation )

        self.kpcPointIndex = None

        self.kpcQuietIndex = None
        
        self.kpcWheelIndex = None
        
        self.kpcRepeatKey = None

        index = 0

        while True :

            index = index + 1

            line = fileHandler.readline()

            # end of file

            if len( line ) <= 0 : break
           
            # removes starting and trailing spaces, skips line is empty

            line = line.strip().rstrip()

            if len( line ) == 0 : continue

            # skips comments

            if line[ 0 ] == "#" : continue

            # splits line using commas as delimiters

            fields = line.split( self.fieldDelimiter )

            if len( fields ) <= 1 : continue

            # error in length ( windows name is too weird )

            if len( fields ) < 9 :

                operation = "error length " + str( len( fields ) ) + " " + line
                
                self.kpcAppend( operation = operation )

                continue

            # fields of event in key log

            identifier = fields[ 0 ]

            window = fields[ 2 ]

                
            # checks whether the window name spilled on next fields ( occurred when contained commas, in previous version)

            iField = 3

            while ( ( iField < len( fields ) ) and ( not fields[ iField ] == "widget" ) ) :

                window = window + self.fieldDelimiter + fields[ iField ]

                iField = iField + 1
                

            if iField >= len( fields ) :

                operation = "error window name " +  line
                
                self.kpcAppend( operation = operation )

                continue

                

            widget = fields[ iField + 1 ]

            date = fields[ iField + 3 ]
                
            timeStampS = float( fields[ iField + 5 ] )

            # elapsed between events = estimated duration 

            elapsedS = timeStampS - previousTimeStampS

            # fields of KPC event

            operation = None

            argumentList = None
           
            # injected events start* and stop* : remains identical

            if identifier.startswith( "st" ) :

                operation, argumentList = self.kpcStartStop(
                    identifier = identifier,
                    time = timeStampS,
                    session = int( fields[ iField + 9 ] ),
                    block =  int( fields[ iField + 11 ] ),
                    trial = int( fields[ iField + 13 ] )
                    )
                
                
            # injected events synchronization : remains identical

            if identifier.startswith( "synchronization" ) :

                operation, argumentList = self.kpcSynchronization(
                    identifier = identifier,
                    time = timeStampS,
                    )
                
                

            # C ( click )


            elif ( ( identifier.startswith( "mouse" ) ) and ( identifier.endswith( "Down" ) ) ) :

                operation, argumentList = self.kpcMouseDown(
                    identifier = identifier,
                    time = timeStampS,
                    x = int( fields[ iField + 9 ] ),
                    y = int( fields[ iField + 11 ] )
                    )


            # buttons up : removes from pressed buttons

            elif ( ( identifier.startswith( "mouse" ) ) and ( identifier.endswith( "Up" ) ) ) :

                operation, argumentList = self.kpcMouseUp(
                    identifier = identifier,
                    time = timeStampS,
                    x = int( fields[ iField + 9 ] ),
                    y = int( fields[ iField + 11 ] )
                    )
            


            # P : mouse move

            elif identifier == "mouseMove" :

                operation, argumentList = self.kpcMouseMove(
                    identifier = identifier,
                    time = timeStampS,
                    x = int( fields[ iField + 9 ] ),
                    y = int( fields[ iField + 11 ] )
                    )

                


            # W : mouse wheel

            elif identifier == "mouseWheel" :

                operation, argumentList = self.kpcMouseWheel(
                    identifier = identifier,
                    time = timeStampS,
                    x = int( fields[ iField + 9 ] ),
                    y = int( fields[ iField + 11 ] ),
                    direction = int( fields[ iField + 13 ] )
                    )



            # K key pressed
            
            elif ( ( identifier.startswith ( "key" ) ) and ( identifier.endswith( "Down" ) ) ) :

                operation, argumentList = self.kpcKeyDown(
                    identifier = identifier,
                    time = timeStampS,
                    key = fields[ iField + 9 ],
                    ascii = int( fields[ iField + 11 ] ) )


            # key up : removes from pressed keys
            
            elif ( ( identifier.startswith( "key" ) ) and ( identifier.endswith( "Up" ) ) ) :

                operation, argumentList = self.kpcKeyUp(
                    identifier = identifier,
                    time = timeStampS,
                    key = fields[ iField + 9 ],
                    ascii = int ( fields[ iField + 11 ] ) )

                # terminates current auto repeat if there is one
                
                self.kpcRepeatKey = None
                    

            # manages pauses
            
            # any event causes end of previous pause

            if not self.kpcQuietIndex is None :

                self.kpcSetDuration( self.kpcQuietIndex, timeStampS )

                self.kpcQuietIndex = None

            # pause

            elif elapsedS >= self.pauseThresholdS :


                # appends event itself

                self.kpcQuietIndex = self.kpcAppend(
                    operation = "Q",
                    window = window,
                    widget = widget,
                    date = date,
                    time = previousTimeStampS + self.samplingPeriodS )
        
            previousTimeStampS = timeStampS


          
            # checks whether current Pointing is ending ( only if the last event is not a mouse move )

            if ( ( not self.kpcPointIndex is None ) and ( not identifier == "mouseMove"  ) ) :

                # delay since last mouse move is above the continuity threshold ( 2 sample periods )

                if self.kpcEndTimeS( self.kpcPointIndex ) + self.continuityThresholdS < timeStampS :

                    self.kpcPointIndex = None


            # checks whether current Wheeling is ending ( only if the last event is not a mouse wheel )
           
            if ( ( not self.kpcWheelIndex is None ) and ( not identifier == "mouseWheel" ) ) :

                # delay since last mouse wheel is above the continuity threshold ( 2 sample periods )
            
                if self.kpcEndTimeS( self.kpcWheelIndex ) + self.continuityThresholdS < timeStampS :

                    self.kpcWheelIndex = None
                

            # manages operations

            if not operation is None :


                currentIndex = self.kpcAppend(
                    operation = operation,
                    window = window,
                    widget = widget,
                    date = date,
                    time = timeStampS,
                    argumentList = argumentList
                    )

                # sets duration of previous operation, if there is one, except for "Q" events that have no side effects 

                self.kpcSetDuration(
                    index = previousOperation,
                    time = timeStampS
                    )

                # sets persistent operations wheel, point

                if operation == "P" :

                    self.kpcPointIndex = currentIndex

                elif operation == "W" : self.kpcWheelIndex = currentIndex

                previousOperation = currentIndex


        # updates the overlaps

        self.kpcUpdateOverlap()

        # closes log file
        
        self.fileClose( fileHandler )

        return True
        

        



    def checkIO ( self ) :

        """ checks the file accesses """

        if self.isEmpty( self.logPath ) : return False

        # creates directory of log

        directory, dummy = os.path.split( self.logPath )

        ok1 = self.directoryCreate( directory )
        

        if self.isEmpty( self.kpcPath ) : return False

        # creates directory of log

        directory, dummy = os.path.split( self.kpcPath )

        ok2 = self.directoryCreate( directory )

        # opens log file in append mode or write mode (avoids destroying it)

        if os.path.isfile( self.logPath ) : ok3 = self.fileOpen( self.logPath, mode = "a" )

        else : ok3 = self.fileOpen( self.logPath, mode = "w" )

        ok4 = self.fileClose( self.logPath )

        return ( ok1 and ok2 and ok3 and ok4 )








    def identifier (

        self,        
        text = None,
        ) :
        
        """ Returns the argument in "identifier" format: lowercasewordCapitalizedWords

            Returns None for empty or undefined argument.

            """

        if text is None : return None
        
        # splits the text in words using tab and space as separators
        
        words = text.split(" ")

        # no words
        
        if len( words ) <= 0 : return None


        # adds words beginning in uppercase with no separators
        
        text = ""

        first = True
        
        for word in words :

            if first : text = word

            else : text = text + word.capitalize()

            first = False               

        return text



    




    def key (

        self,
        value
        ) :

        """ Sends a key with the given value in the event thread of Windows """

        # displays error window

        if not sys.platform == "win32" :

            self.displayWindow( "error" )

            self.waitDelay( close = True )
        
        win32api.keybd_event( value, 0 ) 

        


    def keyboardListener (

        self,
        event
        ) :

        """ Receives keyboard events and handles special keys ( stop, suspend, resume..) "

            Stores event in self.eventList, if the logger is not frozen ( self.frozen is False )

            if receives a key event with Id = self.keyStopLogger, stops logging, writes key log and KPC log.

            if receives a key event with Id = self.keySuspendLogger, sets flag self.frozen to True, no events are
            stored in buffer self.eventList ( the suspend event itself is stored ).

            if receives a key event with Id = self.keyResumeLogger, sets flag self.frozen to False, the events are
            stored again in buffer self.eventList ( the resume event itself is stored ).
            
            """

        # stores in buffer self.eventList only if not frozen
        
        if not self.frozen : self.appendEvent( event )

        # the remainder of this method checks only injected keys

        if not event.Injected : return True

        # stops logging and exits with no error
        
        if event.KeyID == self.keyStopLogger : self.stopLogger()


        # suspends logging
        
        elif event.KeyID == self.keySuspendLogger :

            self.frozen = True

            # changes icon and color of panel and iconifies

            self.setWindow( "halt" )


        # resumes logging

        elif event.KeyID == self.keyResumeLogger :

            self.frozen = False

            # changes icon and color of panel to cyan

            self.setWindow( "record" )

            # event in log.                              

            self.appendEvent( event )

            


        return True            




    def keyName (

        self,
        key = None,
        ascii = None
        ) :

        """ Determines the name of a key (for KPC log ) from the key identifier and the ascii code """
        

        # normalizes arguments

        if key is None : key = ""

        if ascii is None : ascii = ""
        

        # key is reserved, ctrl, alt, etc.

        if key in self.reservedKeyList : return key


        # alphabetical : takes its ascii code, because key is always in upper case
        
        if ( ( ascii < 256 ) and ( chr( ascii ).isalpha() ) ) : name = chr( ascii )

        # non alphabetical, shift pressed, "shift+key"
        
        elif ( ( "Lshift" in self.pressedKeyList ) or ( "Rshift" in self.pressedKeyList ) ) : name = "Shift+" + key

        # normal non alphabetical : takes key

        else : name = key

        # adds prefixes Alt or Ctrl
        
        if ( ( "Lmenu" in self.pressedKeyList ) or ( "Rmenu" in self.pressedKeyList ) ) : name = "Alt+" + name

        if ( ( "Lcontrol" in self.pressedKeyList ) or ( "Rcontrol" in self.pressedKeyList ) ) : name = "Ctrl+" + name

        return name


    def kpcAppend (

        self,
        operation = None,
        window = None,
        widget = None,
        date = None,
        time = 0,
        duration = 0,
        overlap = 0,
        argumentList = None
        ) :

        """ Adds an operation to the buffer self.operationList

            Operation is a list of values [ operation (name), window, widget, date, time stamp, duration, overlap (0)
            
            The remainder is composed of pairs attribute values, depending on the type of operations, e.g.,
            [ xPix, *, yPix, * ]

            returns the index of operation in self.operationList
            
            """

        empty = self.isEmpty( self.operationList )

        if empty : self.operationList = [ ]

        if self.isEmpty( argumentList ) : argumentList = [ ]

        currentIndex = len( self.operationList )

        self.operationList.append( [ operation, window, widget, date, time, duration, overlap ] + argumentList )

        return currentIndex
        




    
    def kpcDurationS (

        self,
        index = None
        ) :

        """ Returns the duration in seconds of operation # index, or None

            Warning: the duration may be provisional for P and W operations.

            Returns None if index is incorrect or buffer operationList is empty.

            """

        if not self.isIndex( index, self.operationList ) : return False

        return self.operationList[ index ][ 5 ]



    def kpcEndTimeS (

        self,
        index = None
        ) :

        """ Returns the final time in seconds of operation # index, or None.

            Warning: the duration may be provisional for P and W operations.

            Returns None if index is incorrect or buffer operationList is empty.

            """

        if not self.isIndex( index, self.operationList ) : return False

        return self.operationList[ index ][ 4 ] + self.operationList[ index ][ 5 ]
    

    
    def kpcKeyDown (

        self,
        identifier = None,
        time = None,
        key = None,
        ascii = None,
        ) :

        """ Receives a key down during construction of KPC log, returns operation and argument

            Updates the list of pressed keys self.pressedKeyList and of times self.pressedKeyTimeList

            Returns a pair operation, argument list.
            
            Operation K for keys that are really pressed  or A when the key is generated by auto repeat

            The argument list contains the key, i.e., a string with prefixs Alt+ Shift+ and Ctrl+.
            Note that argument list is an attribute value list ( see below )

            Returns None None if the event do not correspond to a new operation.

            
            """

        if self.isEmpty( identifier ) : return None, None


        # this is auto repeat

        if key in self.pressedKeyList :

            # ... but it is not registered with special keys ( reserved )

            if key in self.reservedKeyList : return None, None
           
            operation = "A"

        # this is a new key

        else :

            operation = "K"


            # updates list of pressed keys and of times

            self.pressedKeyList.append( key )

            self.pressedKeyTimeList.append( time )


        # determines the text of the key.

        name = self.keyName( key, ascii )
        
        argumentList = [ "key", name ]

        return operation, argumentList

        

    def kpcKeyUp (

        self,
        identifier = None,
        time = None,
        key = None,
        ascii = None,
        ) :

        """ Receives a key up during construction of KPC log

            Generates an operation only if the flag keyReleaseFlag is true.

            Updates the list of pressed keys self.pressedKeyList and of times self.pressedKeyTimeList

            Returns True if identifier is correct, False otherwise ( should not occur )
            
            """

        if self.isEmpty( identifier ) : return None, None


        # error : was not pressed

        if not key in self.pressedKeyList : return None, None


        # determines the text of the key (before touching to the list of key pressed, that determines prefix Ctrl+...

        name = self.keyName( key, ascii )

        # updates list of pressed keys ( keeps press time before deleting )

        index = self.pressedKeyList.index( key )

        pressTime = self.pressedKeyTimeList[ index ]

        self.pressedKeyList.pop( index )

        self.pressedKeyTimeList.pop( index )

      
        # if self.keyReleaseFlag is True, generates a K

        if not bool( self.keyReleaseFlag ) : return None, None

        # returns a K operation
        
        operation = "K"

        argumentList = [ "key", name, "releaseAfterS", time - pressTime ]

        return operation, argumentList


        
    def kpcMouseDown (

        self,
        identifier = None,
        time = None,
        x = None,
        y = None
        ) :

        """ Receives a mouse button dowm during construction of KPC log

            Updates the list of pressed mouse buttons self.pressedButtonList and of times self.pressedButtonTimeList

            Returns a pair operation, argument list.
            
            Operation is aleays C, argument list contains the position X Y and the button
            Note that argument list is an attribute value list ( see below )

            Returns None None if the event do not correspond to a new operation.


            """

        if self.isEmpty( identifier ) : return None, None

        if identifier.startswith( "mouseLeft" ) : button = "left"

        elif identifier.startswith( "mouseCenter" ) : button = "center"

        elif identifier.startswith( "mouseRight" ) : button = "right"

        else : return None, None

        # updates list of pressed buttons

        if not button in self.pressedButtonList :

            self.pressedButtonList.append( button )

            self.pressedButtonTimeList.append( time )

        operation = "C"

        argumentList = [ "xPix", x, "yPix", y, "button", button ]

        return operation, argumentList



    def kpcMouseMove (

        self,
        identifier = None,
        time = None,
        x = None,
        y = None,
        ) :

        """ Receives a mouse move during construction of KPC log


            If there is no P operation in course, returns operation, argument list ( caller will create a new one ).

            Operation is aleays P, argument list contains the position X Y
            Note that argument list is an attribute value list ( see below )

            If there is a P operation in course, updates its attributes: new final point, distance, and length of traject,
            new provisional duration.
                        
            In this case, returns None None

            """

        if self.isEmpty( identifier ) : return None, None

        # there is no current Pointing operation: new Pointing

        if self.kpcPointIndex is None :

            operation = "P"

            argumentList = [ "xPix", x, "yPix", y, "xFinalPix", x, "yFinalPix", y, "distancePix", 0., "lengthPix", 0. ]

            return operation, argumentList


        # updates current point operation

        else :

            # duration (1 additional period , eg. mouse move at 1000 -> end at 1010). Only for checking continuity

            duration = time - self.kpcStartTimeS( self.kpcPointIndex )
            
            self.operationList[ self.kpcPointIndex ][ 5 ] = duration  + self.samplingPeriodS

            # instant displacement

            dx = x - self.operationList[ self.kpcPointIndex ][ 12 ] 

            dy = y - self.operationList[ self.kpcPointIndex ][ 14 ]
            
            displacement = round( math.sqrt( dx * dx + dy * dy ), 2 )

            # distance from origin
            
            deltaX = x - self.operationList[ self.kpcPointIndex ][ 8 ] 

            deltaY = y - self.operationList[ self.kpcPointIndex ][ 10 ]
            
            distance = round( math.sqrt( deltaX * deltaX + deltaY * deltaY ), 2 )

            self.operationList[ self.kpcPointIndex ][ 12 ] = x

            self.operationList[ self.kpcPointIndex ][ 14 ] = y

            self.operationList[ self.kpcPointIndex ][ 16 ] = distance

            self.operationList[ self.kpcPointIndex ][ 18 ] = self.operationList[ self.kpcPointIndex ][ 18 ] + displacement

            return None, None




        
    def kpcMouseUp (

        self,
        identifier = None,
        time = None,
        x = None,
        y = None
        ) :


        """ Receives a mouse button up during construction of KPC log

            Updates the list of pressed buttons self.pressedButtonList and of times self.pressefButtonTimeList
            
            Generates a C event only if the flag mouseReleaseFlag is True, and previous mouse down was more than 100 ms ago
            ( continuityThreshold )
            
            Operation is aleays C, argument list contains the position X Y and the button
            Note that argument list is an attribute value list ( see below )

            Returns None None if the event do not correspond to a new operation.


            """

        if self.isEmpty( identifier ) : return None, None

        if identifier.startswith( "mouseLeft" ) : button = "left"

        elif identifier.startswith( "mouseCenter" ) : button = "center"

        elif identifier.startswith( "mouseRight" ) : button = "right"

        else : return None, None

        # was not pressed, error
        
        if not button in self.pressedButtonList : return None, None

        # updates list of pressed buttons ( keeps press time before deleting )

        index = self.pressedButtonList.index( button )

        pressTime = self.pressedButtonTimeList[ index ]

        self.pressedButtonList.pop( index )

        self.pressedButtonTimeList.pop( index )

      
        # only if self.buttonReleaseFlag is True, generates a C operation

        if not bool( self.buttonReleaseFlag ) : return None, None

        # returns a C operation
        
        operation = "C"

        argumentList = [ "xPix", x, "yPix", y, "button", button, "releaseAfterS", time - pressTime ]

        return operation, argumentList
    


    def kpcMouseWheel (

        self,
        identifier = None,
        time = None,
        x = None,
        y = None,
        direction = None,
        ) :

        """ Receives a mouse wheel during construction of KPC log


            If there is no W operation in course, returns operation, argument list ( caller will create a new one ).

            Operation is aleays W, argument list contains the position X Y
            Note that argument list is an attribute value list ( see below )

            If there is a W operation in course, updates its attributes: new wheel movement, i.e., sum of
            the wheel elementary movements +1 -1, new number of elementary wheel movements.
                        
            In this case, returns None None


            """

        if self.isEmpty( identifier ) : return None, None

        # there is no current Wheeling operation: new Wheeling

        if self.kpcWheelIndex is None :

            operation = "W"

            argumentList = [ "xPix", x, "yPix", y, "moved", direction, "number", 1 ]

            return operation, argumentList


        # updates current Wheeling operation

        else :

            # duration (1 additional period , eg. mouse move at 1000 -> end at 1010). Only for checking continuity

            duration = time - self.kpcStartTimeS( self.kpcWheelIndex )
            
            self.operationList[ self.kpcWheelIndex ][ 5 ] = duration  + self.samplingPeriodS

            # final displacement

            self.operationList[ self.kpcWheelIndex ][ 12 ] = self.operationList[ self.kpcWheelIndex ] [ 12 ] + direction

            # number of wheel operations

            self.operationList[ self.kpcWheelIndex ][ 14 ] = self.operationList[ self.kpcWheelIndex ] [ 14 ] + 1

            return None, None






    def kpcSetDuration (

        self,
        index = None,
        time = None
        ) :

        """ Sets the duration of an operationof the buffer self.operationList.

            Returns True if OK ( normal case ) , False if index is incorrect or buffer operationList is empty.
            
            """

        if not self.isIndex( index, self.operationList ) : return False

        if time is None : return False

        self.operationList[ index ][ 5 ] = time - self.operationList[ index ][ 4 ]

        return True




    def kpcStartStop (

        self,
        identifier = None,
        time = None,
        session = None,
        block = None,
        trial = None
        ) :

        """ Receives a start or stop event

            Returns a pair operation, argument list.
            
            Operation is the identifier itself, argument list is session, block, trial ( with identifiers )

            Returns None None if the event do not correspond to a new operation.


            """

        if self.isEmpty( identifier ) : return None, None

        operation = identifier

        argumentList = [ "session", session, "block", block, "trial", trial ]

        return operation, argumentList


            

    def kpcStartTimeS (

        self,
        index = None
        ) :

        """ Returns the start time in seconds of operation # index, or None

            Returns None if index is incorrect or buffer operationList is empty.

            """

        if not self.isIndex( index, self.operationList ) : return False

        return self.operationList[ index ][ 4 ]




    def kpcSynchronization (

        self,
        identifier = None,
        time = None,
        ) :

        """ Receives a synchronization event

            Returns a pair operation, argument list.
            
            Operation is the identifier itself, argument list is session, block, trial ( with identifiers )

            Returns None None if the event do not correspond to a new operation.


            """

        if self.isEmpty( identifier ) : return None, None

        operation = identifier

        argumentList = [ ]

        return operation, argumentList



    def kpcUpdateOverlap ( self ) :

        """ Updates the overlap between operations.

            overlao is the field self.operationList[ * ] [ 6 ].

            For each operation X of self.operationList, checks the following operations that start before the end time
            of X, and determines the area of the overlapping zone.

            To avoid that embedded operations are counted several times, uses an interval [ initialTime, finalTime ]
            that is initialized to start time(X) end time(X).
            When an operation Y intersects [ initialTime, finalTime ], the intersecting part is added to the duration and
            initialTime becomes the end time of Y.           
            
            """

        if self.isEmpty( self.operationList ) : return

        for index in range( len( self.operationList ) ) :

            finalTime = self.kpcEndTimeS( index )

            initialTime = self.kpcStartTimeS( index )

            self.operationList[ index ][ 6 ] = 0

            for inner in range( index + 1, len( self.operationList ) ) :

                startTime = self.kpcStartTimeS( inner )

                endTime = self.kpcEndTimeS( inner )

                duration = self.kpcDurationS( inner )

                # passed the end of the current operation

                if startTime >= finalTime : break

                if endTime <= initialTime : continue

                overlap = min( finalTime, endTime ) - max( initialTime, startTime )
                
                self.operationList[ index ][ 6 ] = self.operationList[ index ][ 6 ] + overlap

                initialTime = max( initialTime, startTime ) + overlap


        return True




    def mouseListener (

        self,
        event
        ) :

        """ Receives mouse events and writes them in log buffer

            Stores event in self.eventList, if the logger is not frozen ( self.frozen is False )
            
            if receives a click in the label of the window, stops logging, writes key log and KPC log.

                        
            """

        # stores event in buffer only if logger is not suspended
        
        if not self.frozen : self.appendEvent( event )

        # checks whether must stop the application

        ok = self.mouseHandler(
            name = event.MessageName,
            origin = event.Window
            )

        if ok : self.stopLogger()

        return True

        


    def openTemporaryFile (

        self,
        previousPath = None,
        mode = None,
        
        ) :

        """ Opens the temporary file in which log will be written.

            PreviousPath is the path to previous log ( key log or kpc log ). This file may be appended if self.writeMode
            is "append"

            Mode  is "append" or "write", default is self.writeMode

            If mode is "append", the handler is opened in "a" mode otherwise it is opened in "w" ( overwrite ) mode
            
            Returns a file handler or None if problems

            """

        # previous log file is by default the key log

        if self.isEmpty( previousPath ) : previousPath = self.logPath

        # mode is by default self.writeMode

        if self.isEmpty( mode ) : mode = self.writeMode
        
        # default = "keyLogger.tmp same directory than log
        
        # there is a tmp path ( abnormal end ) : appends or overwrites, according to self.writeMode ("write", "append")
        
        if self.filePresent( self.temporaryPath ) :

            if mode.startswith( "a" ) : mode = "a"

            else : mode = "w"

            fileHandler = self.fileOpen( self.temporaryPath, mode = mode )

        # there is a log file : renames it .tmp and appends or overwrite
        
        elif self.filePresent( previousPath ) :

            # this will append to previous log file

            if mode.startswith( "a" ) :

                try :

                    os.rename( previousPath, self.temporaryPath )

                    mode = "a"

                except Exception, exception :

                    return None

            # this will overwrte previous log file

            else :

                try :

                    os.remove( previousPath )

                    mode = "w"

                except Exception, exception :

                    return None

            fileHandler = self.fileOpen( self.temporaryPath, mode = mode )

        # otherwise, creates
        
        else :

            fileHandler = self.fileOpen( self.temporaryPath, mode = "w" )

        return fileHandler




    
    def sameEvent (

        self,
        event1 = None,
        event2 = None
        ) :

        """ returns True iff same event ( except time information ) """

        if event1 == event2 : return True

        if event1 is None : return False

        if event2 is None : return False

        if not event1.MessageName == event2.MessageName : return False

        # keys : checks the key itself, the event name is the same even if keys are different

        if event1.MessageName.startswith( "key" ) :

            return ( event1.KeyID == event2.KeyID ) and ( event1.Key == event2.Key )

        # mouse : no problem, the events click move ets have different names
        

        return True




    def setArguments ( self ) :

        """ sets parameters from the command line

            Arguments of the command line are of the form *.exe, x1=v1, x2=v2... (OR x1 = v1 OR x1 v1).

            x1 must be an existing parameter (string integer boolean or float)

            WARNING: case sensitive

            controls:
            
            When the list of arguments is splitted its length must be even.

            The value of an argument must be convertible into the corresponding type


            returns True iff OK.

            
            """

##        print "setarguments", sys.argv

        if len( sys.argv ) <= 1 : return True

        # parameters that can be modified: non private int, bool, float and strings

        parameterList = list( item
                              for item in dir( self )
                              if ( type( getattr( self, item ) ) in [ int, float, bool, str ] ) and
                                 ( not item.startswith( "_" ) )
                              )

        # list of arguments, splitted when + is encountered
        
        argumentList = [ ]

        for argument in sys.argv[ 1 : ] :

            for item in argument.strip( "/$%=" ).split( "=" ) :

                if len( item ) > 0 : argumentList.append( item )

        # length of the list

##        print "parsed arguments", argumentList
##        print "       parameters", parameterList
        
        size = len( argumentList )

        if size <= 0 : return True

        if size % 2 : return False
        

        # sets arguments, respects current type

        result = True

        for index in range( 1, size, 2 ) :

            attribute = argumentList[ index - 1 ]

            value = argumentList[ index ]

            if not attribute in parameterList :

                result = False

                continue

            try :

                currentType = type( getattr( self, attribute ) )

                if currentType == bool : setattr( self, attribute, bool( value ) )

                elif currentType == int : setattr( self, attribute, int( value ) )

                elif currentType == float : setattr( self, attribute, float( value ) )

                elif currentType == str : setattr( self, attribute, str( value ) )

            except Exception, exception :

                result = False

        return result

        
        
    def setDefault ( self ) :

        """ sets default values """

        self.reservedKeyList = [ "Lshift", "Rshift", "Lcontrol", "Rcontrol", "Lmenu", "Rmenu", "Capital" ]


        
        


    def setPaths ( self ) :

        """ normalizes the paths """

        self.logPath = self.normalizePath( self.logPath )

        self.kpcPath = self.normalizePath( self.kpcPath )
            
        # temporary file
        
        directory, dummy = os.path.split( self.logPath )
        
        self.temporaryPath = directory + os.sep + "temporary.tmp"




        

    def startLogger ( self ) :


        """ Starts logging and freezes the application """

        # displays error window

        if not sys.platform == "win32" :

            self.displayWindow( "error" )

            self.waitDelay( close = True )

        # error in argument list

        if not bool( self.argumentFlag ) :

            self.displayWindow( "command" )

            self.waitDelay( close = True )

        # already active

        if external.isActive( "keylogger" ) :

            self.displayWindow( "present" )

            self.waitDelay( close = True )

        external.activate( "keylogger" )
        

        # displays then minimizes main window

        self.displayWindow( "record" )


        # unfreezes

        self.frozen = False

        # create a hook manager

        self.hookManager = pyHook.HookManager()

        # watch for all keyboard events

        self.hookManager.KeyDown = self.keyboardListener

        self.hookManager.KeyUp = self.keyboardListener

        # set the hook

        self.hookManager.HookKeyboard()

        # watch for all mouse events

        self.hookManager.MouseAll = self.mouseListener

        # set the hook

        self.hookManager.HookMouse()


        # forever loop: writes logs periodically and pump windows events

        timeS = time.time()

        midnightS = timeS - timeS % ( 3600 * 24 )

        if self.dayStartS >= 0. : startS = self.dayStartS + midnightS

        else : startS = -1.
        
        if self.dayStopS >= 0. : stopS = self.dayStopS + midnightS

        else : stopS = -1.

        if self.writePeriodS <= 0. : nextS =  -1.

        elif startS >= 0. : nextS = startS + self.writePeriodS

        else : nextS = time.time() + self.writePeriodS

        while True :

            timeS = time.time()

            # not started yet

            if ( startS >= 0. ) and ( timeS < startS ) :

                time.sleep( 1. )

                continue


            # ended

            if ( stopS >= 0. ) and ( timeS >= stopS ) :

                self.key( self.keyStopLogger )

                continue

            # time to write intermediate logs
            
            if ( nextS > 0. ) and ( timeS >= nextS ) :

                nextS = nextS + self.writePeriodS

                # a key in log
                
                self.key( self.keyStartWrite )

                self.writeLog()

                self.writeKpc()

                self.writeMode = "a"    # from now, appends

                self.eventList = [ ]

                self.eventIndex = 0

                # a key in log
                
                self.key( self.keyStopWrite )

                gc.collect()

                continue

            # gets and processes windows messages                

            pythoncom.PumpWaitingMessages()

##        pythoncom.PumpMessages()
        
        


    def stopLogger ( self ) :

        """ stops key logging and writes logs """

        self.frozen = True

        # a key in log

        self.key( self.keyStartWrite )
        
        # window becomes dark blue

        self.setWindow( "stop" )

        # pumps last events

        pythoncom.PumpWaitingMessages()

        # writes logs

        self.writeLog()

        self.writeKpc()


        # ends the display

        self.endDisplay()

        # ... and leaves

        sys.exit( -1 )
        


        
    def writeEvent (

        self,
        event
        ) :

        """ Writes an event to key log. Uses the file handler self.fileHandler that is already opened

            Returns True is could write, False in case of problem 
            
            """

        if self.fileHandler is None : return False

        identifier = self.identifier( event.MessageName )

        # changes identifier for injected keys corresponding to events startSession stopSession etc.

        if ( ( identifier.startswith( "key" ) ) and ( bool( event.Injected ) ) ) :
            
            if event.KeyID == self.keyStopLogger : identifier = "stopLogger"
       
            elif event.KeyID == self.keySynchronization : identifier = "synchronization"
      
            elif event.KeyID == self.keySynchronization1 : identifier = "synchronization1"

            elif event.KeyID == self.keySynchronization2 : identifier = "synchronization2"

            elif event.KeyID == self.keySuspendLogger : identifier = "suspendLogger"

            elif event.KeyID == self.keyResumeLogger : identifier = "resumeLogger"

            elif event.KeyID == self.keyStartSession : identifier = "startSession"

            elif event.KeyID == self.keyStopSession : identifier = "stopSession"

            elif event.KeyID == self.keyStartBlock : identifier = "startBlock"

            elif event.KeyID == self.keyStopBlock : identifier = "stopBlock"

            elif event.KeyID == self.keyStartTrial : identifier = "startTrial"

            elif event.KeyID == self.keyStopTrial : identifier = "stopTrial"
       
            elif event.KeyID == self.keyStartWrite : identifier = "startWrite"

            elif event.KeyID == self.keyStopWrite : identifier = "stopWrite"

        # trails window name from previous events ( removes commas and tabs in case )
        
        if not self.isEmpty( event.WindowName ) :

            self.eventWindow = event.WindowName.\
                               replace( ",", " " ).\
                               replace( "\t", " " ).\
                               replace( "#", " " ).\
                               replace( "\n", " " )

        if self.isEmpty( self.eventWindow ) : self.eventWindow = ""

        # start time/offset were undefined (should not occur)
        
        if self.startTimeS is None : self.startTimeS = float( event.Time ) / 1000.

        if self.offsetTimeS is None : self.offsetTimeS = time.time() - float( event.Time ) / 1000.

        # time stamp, absolute or relative 

        if bool( self.absoluteFlag ) : timeStampS = float( event.Time ) / 1000. + self.offsetTimeS

        else : timeStampS = float( event.Time ) / 1000. - self.startTimeS

        # injected becomes a sync signal

        if identifier == "startTrial" : injected = 2

        elif bool( event.Injected ) : injected = 1

        else : injected = 0

        # builds line
        
        text = identifier + self.fieldDelimiter + \
               "window" + self.fieldDelimiter + self.eventWindow + self.fieldDelimiter + \
               "widget" + self.fieldDelimiter + str( event.Window ) + self.fieldDelimiter + \
               "date" + self.fieldDelimiter + event.date + self.fieldDelimiter + \
               "timeStampS" + self.fieldDelimiter + ( "%25.3f" % timeStampS ).strip() + self.fieldDelimiter + \
               "injected" + self.fieldDelimiter + str( injected ) + self.fieldDelimiter

        # mouse : adds x, y, wheel

        if identifier.startswith( "mouse" ) :

            text = text + \
                   "xPix" + self.fieldDelimiter + str( event.Position[ 0 ] ) + self.fieldDelimiter + \
                   "yPix" + self.fieldDelimiter + str( event.Position[ 1 ] ) + self.fieldDelimiter + \
                   "wheel" + self.fieldDelimiter + str( event.Wheel ) + self.fieldDelimiter

        # keyboard : adds key, ascii, scan code, extended keyboard and alt
        
        elif identifier.startswith( "key" ) :

            if self.isEmpty( event.Key ) : key = "<void>"

            else : key = event.Key

            if event.KeyID is None : keyId = "<void>"

            else : keyId = str( event.KeyID )
            
            text = text + \
                   "key" + self.fieldDelimiter + key + self.fieldDelimiter + \
                   "ascii" + self.fieldDelimiter + str( event.Ascii ) + self.fieldDelimiter + \
                   "scanCode" + self.fieldDelimiter + str( event.ScanCode ) + self.fieldDelimiter + \
                   "keyId" + self.fieldDelimiter + keyId + self.fieldDelimiter + \
                   "extended" + self.fieldDelimiter + str( event.Extended ) + self.fieldDelimiter + \
                   "alt" + self.fieldDelimiter + str( event.Alt ) + self.fieldDelimiter 


        # start and stop events : adds argument
        
        elif identifier.startswith( "st" ) :

            if self.session is None : self.session = 0

            if self.block is None : self.block = 0

            if self.trial is None : self.trial = 0

            # start trial

            if identifier == "startTrial" :

                self.trial = self.trial + 1

            elif identifier == "startBlock" :

                self.trial = 0

                self.block = self.block + 1

            elif identifier == "startSession" :

                self.trial = 0

                self.block = 0

                self.session = self.session + 1


            text = text + \
                   "session" + self.fieldDelimiter + str( self.session ) + self.fieldDelimiter + \
                   "block" + self.fieldDelimiter + str( self.block ) + self.fieldDelimiter + \
                   "trial" + self.fieldDelimiter + str( self.trial ) + self.fieldDelimiter
                   


        try :
            
            self.fileHandler.write( text + "\n" )
            
            result = True
            
        except Exception, exception :

            result = False

        return result




    def writeKpc ( self ) :

        """ Writes the KPC log file from the buffer of operations self.operationList

            According to self.writeMode, will append to existing log file or overwrite it.

            Returns True if anything was OK, false in case of problem in writing, undefined kpc path or empty
            operations buffer.

            File format

            KPC logs are tsv (comma separated values) files that can be read with text editors as well as spreadsheets.

            Each line contains an operation and/or a comment.
            
            Comment lines start with #.

            Operation lines contain the type of operation, followed by pairs attribute, value separated by commas.

            The beginning of the line is common to all the types of operations:

            types of operations:
                K ( press a key of keyboard )
                A ( key that is automatically generated, e.g., autorepeat )
                P ( point )
                C ( click a mouse button )
                W ( rolls the mouse wheel )
                Q ( quiet period )
                start(Activity) (Activity = Session, Block. Trial), stop(Activity),
                stopLogger, suspendLogger, resumeLogger

            window : the name of the window in which the event generates

            widget : the numerical Id of the widget in which the event generate ( coded by Windows )

            date : the data and time of event in format yyyy mm dd - hh:MM:SS

            timeStampS : the time at which the event occurred counted in seconds since the beginning of the execution
            of the logger.

                Note. Use the timeStampS to find out the corresponding event(s) in the key log.

            durationS : duration in seconds

            overlapS : total duration of overlapping events in seconds.

                Note. sum ( durationS ) - sum( overlapS ) = total duration.

            The remainder of the line is specific of each type of operation

            K :

                Key : the description of the key ( letter, digit, text, identifier, e.g., Lshift ) with prefixes Alt+...

            C :


                xPix : horizontal position of pointer in pixels ( 0 = left )

                yPix : vertical position of pointer in pixels ( 0 = top ; has to be inverted for plots, e.g., 768-yPix)

                button : "left", "center" or "right"

            P :
            
                xPix : initial horizontal position of pointer in pixels 

                yPix : initial ertical position of pointer in pixels

                xFinalPix : final horizontal position of pointer in pixels

                yFinalPix : final vertical position of pointer in pixels

                distancePix : distance ( in straight line ) between initial and final positions

                lengthPix : length of the path followed by mouse in pixels.

            W :
            
                xPix : initial horizontal position of pointer in pixels 

                yPix : initial ertical position of pointer in pixels

                movement : resulting movement of the wheel. Integer = sum of elementary wheel movements, +1 or -1

                number : number of wheel events ( greater than movement if user rolled up and down )

            Q :

                void.

            start(Activity), stop(Activity) :

                session : session number ( 0 if no session started )
                
                block : block number ( 0 if no block started )

                trial : trial number ( 0 if no trial started )

            """

        # no kpc file
        
        if self.isEmpty( self.kpcPath ) : return False

        # builds the log of KPC operations in memory

        ok = self.buildKpc()

        # nothing to write

        if not ok : return False

        # opens temporary file
        
        self.fileHandler = self.openTemporaryFile( self.kpcPath )

        if self.fileHandler is None : return False
        
        # writes elements of KPC buffer one per line, fields separated by commas

        result = True

        for fields in self.operationList :

            identifier = str( fields[ 0 ] )

            # error

            if identifier.startswith( "error" ) :

                try :

                    self.fileHandler.write( "# " + identifier + "\n" )


                except Exception, exception :

                    result = False

                    break
                
                continue
            
            # predefined fields, common to all types of operations
           
            text = identifier + self.fieldDelimiter

            text = text + \
                   "window" + \
                   self.fieldDelimiter + \
                   str( fields[ 1 ] ).replace( ",", " ").replace( "\t", " ").replace( "#", " " ).replace( "\n", " " ) + \
                   self.fieldDelimiter

            text = text + "widget" + self.fieldDelimiter + str( fields[ 2 ] ) + self.fieldDelimiter

            text = text + "date" + self.fieldDelimiter + str( fields[ 3 ] ) + self.fieldDelimiter

            text = text + "timeStampS" + self.fieldDelimiter + ( "%25.3f" % float( fields[ 4 ] ) ).strip() + self.fieldDelimiter

            text = text + "durationS" + self.fieldDelimiter + ( "%25.3f" % float( fields[ 5 ] ) ).strip() + self.fieldDelimiter

            text = text + "overlapS" + self.fieldDelimiter + ( "%25.3f" % float( fields[ 6 ] ) ).strip() + self.fieldDelimiter

            # specific fields ( arguments of operations ), come with their identifier

            for item in fields[ 7 : ] :

                text = text + str( item ) + self.fieldDelimiter


            # writes the line. "start" are preceded by # and "stop" are followed by # ( comments )

            try :

                if identifier.startswith( "start" ) : self.fileHandler.write( "#\n" )

                self.fileHandler.write( text + "\n" )

                if identifier.startswith( "stop" ) : self.fileHandler.write( "#\n" )

            except Exception, exception :

                result = False

                break

        # saves the file ( it is in the tmp path, for now )
        
        ok = self.fileClose( )

        # if ok, renames it as log
        
        if ok :

            if self.filePresent ( self.kpcPath ) : os.remove( self.kpcPath )

            os.rename( self.temporaryPath, self.kpcPath )

            ok = self.filePresent( self.kpcPath )

        # problem : deletes the temporary file

        else :

            os.remove( self.temporaryPath )

            
        if not ok : result = False

        return result and ok

        
        
    
        
    def writeLog ( self ) :

        """ Writes the log buffer to file.

            According to self.writeMode, will append to existing log file or overwrite it.

            Returns True if anything was OK, false in case of problem in writing, undefined kpc path or empty
            event buffer.

            File format

            Key logs are tsv (comma separated values) files that can be read with text editors as well as spreadsheets.

            Each line contains an event and/or a comment.
            
            Comment lines start with #.

            Event lines contain the type of event, followed by pairs attribute, value separated by commas.

            The beginning of the line is common to all the types of events:

            event type: keyDown, keyUp,
                        mouse(Button)Down (Button = Left Center or Right), mouse(Button)Up, mouseMove, mouseWheel,
                        start(Activity) (Activity = Session, Block. Trial), stop(Activity),
                        stopLogger, suspendLogger, resumeLogger

            window : the name of the window in which the event generates

            widget : the numerical Id of the widget in which the event generate ( coded by Windows )

            date : the data and time of event in format yyyy mm dd - hh:MM:SS

            timeStampS : the time at which the event occurred counted in seconds since the beginning of the execution
            of the logger.

            injected:
            2 for synchronization events, i.e., the 'startTrial' events.
            1 for other events created by software ( e.g., for the events start* and stop*. injected is 16.
            0 for events produced by the devices ( mouse or keyboard ),

            The remainder of the line is event specific

            keyDown, keyUp

                key : the name of the key. Uppercase letter or identifier, e.g., Lshift.

                ascii : ascii code, or 0 when the key produces no ascii code.
                
                scanCode : code of the physical key that have been touched (refers to the physical layout of keys)
                
                keyId : identifier of the key ( numerical )
                
                extended : 0 if the key comes from the main keyboard, positive integer otherwise (e.g., numerical pad)
                
                alt : 0 if alt key is not currently pressed, positive integer otherwise


            mouse(Button)Down, mouseButtonUp, mouseMove, mouseWheel

                xPix : horizontal position of pointer in pixels ( 0 = left )

                yPix : vertical position of pointer in pixels ( 0 = top ; has to be inverted for plots, e.g., 768-yPix)

                wheel : current movement of the wheel: 0 for all events, -1 +1 for mouseWheel events.

            
            start(Activity), stop(Activity) :

                session : session number ( 0 if no session started )
                
                block : block number ( 0 if no block started )

                trial : trial number ( 0 if no trial started )


            startLogger, suspendLogger, resumeLogger

                void.

            """

        if self.isEmpty( self.logPath ) : return False

        if not self.isIndex( self.eventIndex, self.eventList ) : return False

        # opens temporary file
        
        self.fileHandler = self.openTemporaryFile( self.logPath )

        if self.fileHandler is None : return False
        
        # write events. Filters events with crossed time stamps, and events of same type with same time stamps
        
        result = True

        # values for control of crossed time stamps or duplicates, e.g., 2 mouse move at same time stamp
        
        time = -1

        messageName = ""

        self.removed = 0

        for index in range( self.eventIndex ) :

            # time stamp and message of current event

            eventTime = self.eventList[ index ].Time

            eventMessageName = self.eventList[ index ].MessageName

            # increasing time stamps ok

            if eventTime > time :

                None

            # crossed time stamps : skips

            elif eventTime < time :

                self.removed = self.removed + 1

                continue

            # same event, same time stamp, not a command (start, stop ), same arguments : skips

            elif self.sameEvent( self.eventList[ index - 1 ], self.eventList[ index ] ) :

                self.removed = self.removed + 1

                continue

            # stores current values
            
            time = eventTime

            messageName = eventMessageName

            # writes the event

            result = self.writeEvent( self.eventList[ index ] )

            if not result : break ;


        # saves the file ( it is in the tmp path, for now )
        
        ok = self.fileClose( )

        # if ok, renames it as log
        
        if ok :

            if self.filePresent( self.logPath ) : os.remove( self.logPath )

            ok = os.rename( self.temporaryPath, self.logPath )

        # problem : deletes the temporary file

        else :

            os.remove( self.temporaryPath )

            
        if not ok : result = False

        return result



            
        
# creates the global singleton object if not already here

if not "keyLogger" in globals() : keyLogger = KeyLogger()

         
def go ( ) :


        """ Starts logger. allows calling key logger from the Launch object."""

        keyLogger.startLogger()


        

