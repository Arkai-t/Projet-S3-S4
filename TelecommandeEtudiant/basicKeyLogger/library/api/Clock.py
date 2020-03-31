
""" Class that handles dates, time and timers. Can send single events or periodical events at a given period.

    Wraps some methods of time, e.g., sleep, localtime, gmttime and formatted time

   
    """


from threading import *

import sys

import time

    
class Clock :


    """ Class that handles dates, time and timers. Can send single events or periodical events at a given period.

        Uses a Timer object. This object is marked with an attribute owner = "Clock" so that it can be identified anywhere
   
        """

    # flag to avoid multiple levels of interruption
    
    busy = None
    
    # call back
    
    command = None
    
    # number of events sent since last start
    
    count = None

    # format for short dates
    
    dayFormat = None

    # format for dates (day + time)
    
    dateFormat = None

    # default period

    defaultPeriodMs = 1
    
    # delay until next event
    
    delayMs = None
    
    # end time in Ms
    
    endTimeMs = None

    # compact format for day

    fileDayFormat = None

    # compact format for date of files

    fileDateFormat = None
    
    # time of next event
    
    nextTimeMs = None

    # number of events to send
    
    number = None

    # owner of the timer - used to identify the threads from outside
    
    owner = None
    
    # period in Ms
    
    periodMs = None
    
    # reference time : first creation of the clock instance

    referenceTimeS = None

    # creation time of the clock object

    startS = None
    
    # start time in Ms
    
    startTimeMs = None

    # tick method: time.clock or time.time, according to OS

    tick = None

    # format for hours
    
    timeFormat = None

    # offset for clocks

    timeOffset = None

    # its one-shot timer object
    
    timer = None




    def __init__ (
        
        self,
        startTimeMs = None,
        endTimeMs = None,
        periodMs = None,
        number = None,
        owner = None,
        dayFormat = None,
        timeFormat = None,
        dateFormat = None,
        command = None
        ) :

        """ Constructs the object, does not do anything else

            """

        # resets work variables
        
        self.reset()

        # creation time

        self.startS = self.timeS()

        # initializes attributes

        if dayFormat is None : self.dayFormat = "%Y %m %d"

        else : self.dayFormat = str( dayFormat )

        if timeFormat is None : self.timeFormat = "%H:%M:%S"

        else : self.timeFormat = str( timeFormat )
        
        if dateFormat is None : self.dateFormat = "%Y %m %d - %H:%M:%S"

        else : self.dateFormat = str( dateFormat )

        self.set(
            startTimeMs = startTimeMs,
            endTimeMs = endTimeMs,
            periodMs = periodMs,
            number = number,
            owner = owner,
            command = command
            )
        


        
    def clockMs ( self ) :

        """ Returns the current clock in milliseconds (integer)

            Integer number
            
            """

        # in case the reference time has not been initialized

        return int( ( self.tick() - self.timeOffset ) * 1000 )
##       
##        if sys.platform == "win32" : return int( time.clock() * 1000 )
##
##        else : return int( ( time.time() - self.referenceTimeS ) * 1000 )
    


    def clockS ( self ) :

        """ Returns the current clock in seconds (float). precision under windows about 3 mus

                        
            """

        return self.tick() - self.timeOffset

##        # in case the reference time has not been initialized
##        
##        if sys.platform == "win32" : return time.clock()
##
##        else : return time.time() - self.referenceTimeS
    



    def date (
        
        self,
        format = None,
        time = None,
        place = "local"
        ) :

        """ Returns a string with the current date and time in a given format

            Accepts two types for argument "time"
            a 9-uple obtained as result of some time method, e.g. time.localtime()
            an integer, i.e., absolute elapsed time in seconds.

            Place is "local" ( local time, default ) or "gmt" ( gmt time )

            By default time is current time and format is  YYYY MM DD HH:MM:SS
            
            """

        if format is None : format = self.dateFormat

        if self.isTimeList( time ) : return self.timeListToString( time, format )

        elif place == "local" : return self.timeListToString( self.localTimeList( time ), format )
    
        else : return self.timeListToString( self.localTimeList( time ), format )
    

    def day (

        self,
        format = None,
        time = None,
        place = "local"
        ) :

        """ Returns the day corresponding to the time

            Accepts two types for argument "time"
            a 9-uple obtained as result of some time method, e.g. time.localtime()
            an integer, i.e., absolute elapsed time in seconds.

            Place is "local" ( local time, default ) or "gmt" ( gmt time )

            By default time is current time and format is  YYYY MM DD HH:MM:SS
            
            By default time is current time and format is  YYYY MM DD HH:MM:SS

        """

        if format is None : format = self.dayFormat

        if self.isTimeList( time ) : return self.timeListToString( time, format )

        elif place == "local" : return self.timeListToString( self.localTimeList( time ), format )
    
        else : return self.timeListToString( self.localTimeList( time ), format )
    
        
    def gmtTimeList (
        
        self,
        timeList = None
        ) :

        """ Returns the gtm time as a n-uple yy, mm, etc. (see python doc of module time )

            argument is None or a 9-uple representing a time, like the result of methods like time.localtime()

            """

        if type( timeList ) == int : None

        elif type( timeList ) == float : timeList = int( timeList )

        else : timeList = None
        
        return time.gmtime( timeList )



    def handler ( self ) :

        """ Called when the one shot timer sends its event """


        # counter
        
        self.count = self.count + 1

        # updates number of events to send
        
        if self.number > 0 : self.number = self.number - 1
        
        # stops and deletes timer
        
        self.stop()
        
##        if not self.timer is None : del( self.timer )

        # next event
        
        if self.nextTimeMs is None : self.nextTimeMs = self.clockMs()
        
        self.nextTimeMs = self.nextTimeMs + self.periodMs
        
        # triggers one shot timer for next event
        
        self.trigger()
            
        # external call back
        
        if not self.command is None  :
  
            # already busy executing command
            
            if self.busy : return
            
            self.busy = True
            
            self.command()
            
            self.busy = False




    def hour (
        
        self,
        format = None,
        time = None,
        place = "local"
        ) :

        """ Returns a string with the hour corresponding to "time".

            Accepts two types for argument "time"
            a 9-uple obtained as result of some time method, e.g. time.localtime()
            an integer, i.e., absolute elapsed time in seconds.

            Place is "local" ( local time, default ) or "gmt" ( gmt time )

            By default time is current time and format is  YYYY MM DD HH:MM:SS

            """

        if format is None : format = self.timeFormat

        if self.isTimeList( time ) : return self.timeListToString( time, format )

        elif place == "local" : return self.timeListToString( self.localTimeList( time ), format )
    
        else : return self.timeListToString( self.localTimeList( time ), format )

         
    
    def isTimeList (

        self,
        timeList = None
        ) :

        """ Determines whether the argument is a 9-uple representing a time,
            like the value returned by sime time methods like time.localtime()

            """

        return isinstance( timeList, time.struct_time )

    

    def localTimeList (
        
        self,
        timeList = None
        ) :

        """ Returns the local time as a n-uple yy, mm, etc. (see python doc of module time )

            argument is None or a 9-uple representing a time, like the result of methods like time.localtime()

            if seconds is defined, it is taken instead of current time

            """


        if type( timeList ) == int : None

        elif type( timeList ) == float : timeList = int( timeList )

        else : timeList = None

        return time.localtime( timeList )

    
    def now (
        
        self,
        format = None,
        time = None
        ) :

        """ Alias for date. Returns a string with the date and time corresponding to "time"

            Accepts two types for argument "time"
            a 9-uple obtained as result of some time method, e.g. time.localtime()
            an integer, i.e., absolute elapsed time in seconds.

            By default time is current time and format is  YYYY MM DD HH:MM:SS
            
            """

        return self.date(
            format = format,
            time = time
            )

    

    def pause ( self ) :

        """ Alias for stop. Pauses the clock, but does not loose parameters """
        
        self.stop()


        
    def reset ( self ) :

        """ Resets the variables, except command, period and count """

        self.busy = False
        
        self.startTimeMs = None

        self.endTimeMs = None

        self.lastMs = None

        self.number = None

        self.command = None
        
        self.periodMs = self.defaultPeriodMs

        self.count = 0

        self.delayMs = None

        self.nextTimeMs = None

        self.owner = "clock"

        if self.referenceTimeS is None : self.referenceTimeS = time.time()

        # defines tick method and time offset (in linux, time.clock is the consumed cpu time,
        # whereas in windows, time.time does not work well

        if sys.platform == "linux2" :

            self.timeOffset = self.referenceTimeS

            self.tick = time.time

        else :

            self.timeOffset = 0

            self.tick = time.clock
            



    def resume ( self ) :

        """ Resumes the clock, with same parameters """

        self.trigger()


    def seconds ( self ) :

        """ Alias of timeS """

        return self.timeS()
    
        
    def secondsToString (

        self,
        seconds = None,
        format = None
        ) :

        """ Converts a time expressed in seconds into a formated string . Default is current time """

        if seconds is None : seconds = time.time()

        if not type ( format ) == str : format = self.timeFormat

        if not type ( format ) == str : return ""
        
        # values of seconds minutes and hours

        hours = int( seconds / 3600 )

        minutes = int( seconds % 3600 ) / 60

        seconds = int( seconds % 60 )

        return format.\
               replace( "%H", str( hours ) ).\
               replace( "%M", str( minutes ).rjust( 2, '0' ) ).\
               replace( "%S", str( seconds ).rjust( 2, '0' ) )

        


    def set (
        
        self,
        startTimeMs = None,
        endTimeMs = None,
        periodMs = None,
        number = None,
        command = None,
        owner = None
        ) :

        """ Sets the parameters

            number == -1 means infinite number of events

            Returns True is an event will be sent, False otherwise
            
            """

        # start time (default is now, first event will occur after one period)
        
        self.startTimeMs = startTimeMs
        
        if self.startTimeMs is None : self.startTimeMs = self.clockMs()

        # endtime (or none )
        
        self.endTimeMs = endTimeMs

        # period : at least 1 ms
        
        if not periodMs is None : self.periodMs = periodMs
        
        elif self.periodMs is None : self.periodMs = self.defaultPeriodMs
        
        self.periodMs = max( 1, self.periodMs )

        # number of events. if undefined : one event if no end time, infinite if there is an endtime
        
        if type( number ) == int : self.number = number

        elif type( number ) == float : self.number = int( number )

        elif number is None : self.number = -1

        # changed default behavior: repeats infinitely if number of repetitions undefined

##        else : self.number = -1
##        
##        # undefined number
##        
##        if self.number is None :
##
##            if not self.endTimeMs is None : self.number = -1    # infinite
##
##            else : self.number = 1                              # one shot

        # command: only if defined
        
        if callable( command ) : self.command = command

        # owner
        
        if not owner is None : self.owner = str( owner )

        


    def sleepMs (
        
        self,
        durationMs
        ) :

        """ Waits for the specified duration.

            Blocks current thread, but does not block processor (sleeps )

            Does not stop the generation of events
            
            Returns the duration waited

            DOES NOT WORK - CPU REMAINS ACTIVE ??? 
            
            """

        if durationMs is None : durationMs = 1

        elif type( durationMs ) == int : durationMs = float( durationMs )

        elif not type( durationMs ) == float : return 0

        if durationMs <= 0.  : return 0
        
        time.sleep( float( durationMs ) / 1000. )

        return int( durationMs )
        

 

    def sleepS (
        
        self,
        durationS = None
        ) :

        """ Waits for the specified duration.

            Blocks current thread, but does not block processor (sleeps )

            Does not stop the generation of events
            
            Returns the duration waited

           """

        if durationS is None : durationS = 0.001 # 1 ms, minimal sleep time
        
        elif type( durationS ) == int : durationS = float( durationS )

        elif not type( durationS ) == float : return 0

        if durationS <= 0. : return 0
                
        time.sleep( durationS )

        return durationS
        



        
    def start (
        
        self,
        startTimeMs = None,
        endTimeMs = None,
        periodMs = None,
        number = None,
        command = None
        ) :

        """ Sets the timer with the desired parameters

            number == -1 means infinite number of events

            Returns True is an event will be sent, False otherwise
            
            """

        # first, deletes the previous timer if it was active
        
        self.stop()
        
        # resets event counter
        
        self.count = 0

        self.set(
            startTimeMs = startTimeMs,
            endTimeMs = endTimeMs,
            periodMs = periodMs,
            number = number,
            command = command
            )

        # next event is the start time
        
        self.nextTimeMs = self.startTimeMs

        # prepares the next event
        
        result = self.trigger() 

        return result


    def stop ( self ) :

        """ Stops clock """


        if not self.timer is None : self.timer.cancel()
            
        if not self.timer is None : del( self.timer )

        self.timer = None   # this is redunredunredundant!
        

        
    def stopAll (
        
        self,
        owner = None
        ) :

        """ Stops all the timers with a given owner. Default owner is Clock

            if owner is "", cancels all timers created with a "owner" attribute

            Note: cannot use standard keywords this module is a layer below standards.
            
            """

        if owner is None : owner = self.owner

        owner = owner.lower()
       
        # for all active thread
        
        for thread in enumerate() :

            # this is a widget's timer
            
            try :
                
                threadOwner = thread.owner.lower()
                
                if ( ( len( owner ) <= 0 ) or ( threadOwner == owner ) ) : thread.cancel()

            except Exception, exception :

                None




    def stringToTimeList (

        self,
        text = None,
        format = None
        ) :

        """ Converts a string containing a date/time in a given format into a time list  """

        if ( ( format is None ) or ( len( format ) <= 0 ) ) : format = self.dateFormat # does not use utilities...

        if not type( text ) == str : return None

        return time.strptime( text, format )


    def stringToTimeS (

        self,
        text = None,
        format = None
        ) :

        """ converts a string containing a date/time in a given format into a time in seconds """

        timeList = self.stringToTimeList(
            text = text,
            format = format
            )

        if timeList is None : return 0.

        return time.mktime( timeList )
        


    def timeListToString (

        self,
        timeList = None,
        format = None
        ) :

        """ Converts a time list into a string, with a given format """

        if ( ( format is None ) or ( len( format ) <= 0 ) ) : format = self.dateFormat # does not use utilities... 
        
        if not self.isTimeList( timeList ) : return ""

        return time.strftime( format, timeList )

    
    
    def timeS ( self ) :

        """ Returns the current time and date in seconds since the epoch (see python doc of module time )

            Floating point number.
            
            """

        return time.time()

    

        

    def today (
        
        self,
        format = None
        ) :

        """ Returns the local date of today in format YYYY MM DD 

            format overrides the default values
            
            """

        if format is None : format = self.dayFormat
        
        return self.timeListToString( time.localtime(), format )

    

    def trigger (  self ) :

        """ Prepares a timer for the next event, if there is one

            Waits for at least one periodMs, and/or until startTimeMs, the first of the two that occurs

            Does nothing if endTimeMs will be passed or if the number of events to send is <= 0

            Returns True if there is a next event, false otherwise
            
            """

        # current time, and next tick time
        
        clockMs = self.clockMs()
        
        if self.nextTimeMs is None : self.nextTimeMs = clockMs

        
        # time of last event is passed
        
        if ( ( not self.endTimeMs is None ) and ( self.nextTimeMs >= self.endTimeMs ) ) : return False

        # number of events is done
        
        if ( ( not self.number is None ) and ( self.number == 0 ) ) : return False

        # creates a new timer and starts it
        
        self.delayMs = max( 0, self.nextTimeMs - clockMs )
        
        self.timer = Timer( float( self.delayMs ) / 1000, self.handler )

        # marks the origin of the timer
        
        if not self.owner is None : self.timer.owner = self.owner

##        print "clock.start timer ", self.number, clockMs, self.endTimeMs

        self.timer.start()
        
        return True


    def waitMs (
        
        self,
        durationMs = None
        ) :

        """ Alias of sleepMs. Waits for the specified duration.

            Blocks current thread, but does not block processor (sleeps )

            Does not stop the generation of events
            
            Returns the duration waited
            
            """

        return self.sleepMs( durationMs )
        

    def yesterday (
        
        self,
        format = None
        ) :

        """ Returns the local date of yesterday in format YYYY MM DD 

            format overrides the default values
            
            """

        if format is None : format = self.dayFormat

        return self.date(
            format = format,
            time = time.localtime( time.time() - 24* 3600 ) )

# -----------------------------------
# creates a global singleton if not already here
#

if not "clock" in globals() : clock = Clock()
         
        
