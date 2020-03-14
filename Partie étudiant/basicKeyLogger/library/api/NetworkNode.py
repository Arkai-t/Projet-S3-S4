""" information on a node of a ad-hoc network kept by neighbor nodes """

from api.Clock import *

from api.Utilities import *


class NetworkNode  :

    """ information on a node of a ad-hoc network kept by neighbor nodes """


    # address (ip)

    address = None


    # statistics on delays of transmission (if available )
    
    averageDelayMs = None

    averageSquaredDelayMs = None

    # statistics on inter-message periods

    averagePeriodS = None

    averageSquaredPeriodS = None

    # date of last status change

    changeS = None

    # number of messages, OK messages, KO messages, timed out messages, changes of addresses and of status

    countAck = None

    countAddressChange = None

    countStatusChange = None

    countMessage = None

    countNack = None

    countTimeout = None


    # last transmission delay with this node

    delayMs = None

    # hardware of this device

    description = None

    # field delimiter

    fieldDelimiter = None

    
    # identifier

    identifier = None

    # instant of starting online

    offlineTimeS = None

    # offset of timers between host and this device

    offsetTimeS = None

    # current state of communication (on line off line

    online = None

    # elapsed time (duration of current online epoch)

    onlineDurationS = None

    # instant of starting online

    onlineTimeS = None
    
    # last shift of dates of this node

    periodS = None

    # prefix of last message

    prefix = None

    # time of last message (as stated by receptor)

    receptionS = None

    # number of repetitions of last message (used for time synchronization )

    repetitions = None

    # shift, i.e. difference between reception time (according to receiver's clock) and emission time (emitter's clock)

    shiftS = None

    # time of last reset

    startS = None
    
    # last status of this node

    status = None

    # last date received from the node
    
    timeS = None

    # transmission latency for an exchange, e.g., during time exchange sequences

    transmissionS = None

    


    def __init__ ( 

        self,
        address = None,
        identifier = None,
        description = None,
        fieldDelimiter = None
        
        ) :

        """ constructor """


        self.address = utilities.string( address )

        self.identifier = utilities.string( identifier )

        self.description = utilities.string( description )

        self.fieldDelimiter = utilities.string( fieldDelimiter, default = "," )
        
        # resets the data
        
        self.reset()
        

    def normalizeStatus(

        self,
        status = None

        ) :

        """ normalizes a status string, to make it the text of an attribute value list """

        words = utilities.textToWords( status, delimiters = self.fieldDelimiter )


        if len( words ) % 2 > 0 : words = words[ : -1 ]

        size = len( words ) / 2

        identifiers = words[ :: 2 ]

        values = words[ 1 :: 2 ]

        # assigns values in case of duplicates (rightmost is prioritary) and kills the duplicates

        for index in range( size ) :

            identifier = identifiers[ index ]

            value = values[ index ]

            first = identifiers.index( identifier )

            if first < index :

                values[ first ] = value

                identifiers[ index ] = None

        # regenerates the text

        text = ""

        for index in range( size ) :

            identifier = identifiers[ index ]

            value = values[ index ]

            if identifier is None : continue

            text = text + identifier + self.fieldDelimiter + value + self.fieldDelimiter

        return text
            
                
        

        

    def statistics ( self ) :

        """ returns a string with statistics on this network node """

        text = utilities.string( self.identifier, default = "unknown" ) + self.fieldDelimiter

        text = text + "description" + self.fieldDelimiter + \
               utilities.string( self.description, default = "" ) + self.fieldDelimiter

        text = text + "startTimeS" + self.fieldDelimiter + \
               utilities.string( self.startS, default = "" ) + self.fieldDelimiter

        text = text + "lastReceptionTimeS" + self.fieldDelimiter + \
               utilities.string( self.receptionS, default = "" ) + self.fieldDelimiter

        text = text + "address" + self.fieldDelimiter + \
               utilities.string( self.address, default = "" ) + self.fieldDelimiter

        text = text + "averageDelayMs" + self.fieldDelimiter + \
               utilities.string( self.averageDelayMs, default = "" ) + self.fieldDelimiter

        text = text + "averageSquaredDelayMs" + self.fieldDelimiter + \
               utilities.string( self.averageSquaredDelayMs, default = "" ) + self.fieldDelimiter

        text = text + "averagePeriodS" + self.fieldDelimiter + \
               utilities.string( self.averagePeriodS, default = "" ) + self.fieldDelimiter

        text = text + "averageSquaredPeriodS" + self.fieldDelimiter + \
               utilities.string( self.averageSquaredPeriodS, default = "" ) + self.fieldDelimiter

        text = text + "countMessage" + self.fieldDelimiter + \
               utilities.string( self.countMessage, default = "" ) + self.fieldDelimiter

        text = text + "countAck" + self.fieldDelimiter + \
               utilities.string( self.countAck, default = "" ) + self.fieldDelimiter

        text = text + "countNack" + self.fieldDelimiter + \
               utilities.string( self.countNack, default = "" ) + self.fieldDelimiter

        text = text + "countTimeout" + self.fieldDelimiter + \
               utilities.string( self.countTimeout, default = "" ) + self.fieldDelimiter

        text = text + "countAddressChange" + self.fieldDelimiter + \
               utilities.string( self.countAddressChange, default = "" ) + self.fieldDelimiter

        text = text + "countStatusChange" + self.fieldDelimiter + \
               utilities.string( self.countStatusChange, default = "" ) + self.fieldDelimiter

        return text


        


    def string ( self ) :

        """ prints this network node """

        text = "node " + utilities.string( self.identifier, default = "unknown" ) + "\n"

        for attribute in dir( self ) :

            if attribute.startswith( "_" ) : continue

            value = getattr( self, attribute )

            if callable( value ) : continue

            text = text + " " + attribute + self.fieldDelimiter + utilities.string( value, default = "" ) + "\n"

        return text


    
            

    def reset ( self ) :

        """ resets the data """
        
        # counters and statistics

        self.countAddressChange = 0

        self.countStatusChange = 0
        
        self.countMessage = 0

        self.countAck = 0

        self.countNack = 0

        self.countTimeout = 0

        self.averageDelayMs = 0.

        self.averageSquaredDelayMs = 0.

        self.averagePeriodS = 0.

        self.averageSquaredPeriodS = 0.

        # last message

        self.receptionS = None

        self.shiftS = None

        self.timeS = None

        self.delayMs = None

        self.status = None

        self.prefix = None

        # off line

        self.online = None

        self.onlineDurationS = None

        self.onlineTimeS = None

        self.offlineTimeS = None

        # start time for statistics

        self.startS = clock.timeS()
        



    def update (

        self,
        prefix = None,
        description = None,
        status = None,
        receptionS = None,
        address = None,
        timeS = None,
        delayMs = None,
        onlineS = None,
        online = None,
        result = None,
        ) :

        """ updates the statistics with the results of a query "status?" to this node

            result is

            "time out"

            "nack"

            "ack" status is initialized

            "set" : status is initialized then merged (attributes are unique)

            "add" status is merged with former

            
            """

       
        # time of message

        currentTime = clock.timeS()

        if receptionS is None : self.receptionS = currentTime

        else : self.receptionS = utilities.float( receptionS, default = 0. )

        # time (internal clock) of emissor of message

        if timeS is None : timeS = currentTime

        else : timeS = utilities.float( timeS, default = 0. )

        # delay in transmission

        delayMs = utilities.integer( delayMs, default = 0 )

        # count of messages
        
        self.countMessage = self.countMessage + 1

        # description of the device: hardware, software, version...

        self.description = utilities.string( description )

        # last address

        address = utilities.string( address )

        if self.address is None :

            self.address = address

        elif not self.address == address :

            self.countAddressChange = self.countAddressChange + 1
        
            self.address = address

        # last message prefix

        self.prefix = utilities.string( prefix, default = "" )
        
        # time out

        if result == "timeout" :

            self.countTimeout = self.countTimeout + 1

            # offline (was online or undefined )

            if not self.online == False :
                
                self.onlineTimeS = 0.

                self.offlineTimeS = currentTime

                self.online = False

            return


        # nack

        elif result == "nack" :

            self.countNack = self.countNack + 1

            # offline (was online or undefined )

            if not self.online == False :
                
                self.onlineTimeS = 0.

                self.offlineTimeS = currentTime

                self.online = False

            return



        # ack (message can be status or stop)

        elif result == "ack" :

            if not type( status ) == str : status = ""

##            print "networknode.update ack status", status

            if self.status is None :

                self.status = status

                self.changeS = currentTime

            elif not self.status == status :

                self.countStatusChange = self.countStatusChange + 1

                self.changeS = currentTime

                self.status = status


        # append status

        elif result == "add" :

            if not type( status ) == str : status = ""

            if self.status is None : status = self.normalizeStatus( status )

            elif self.status.endswith( self.fieldDelimiter ) : status = self.normalizeStatus( self.status + status )

            else : status = self.normalizeStatus( self.status + self.fieldDelimiter + status )

##            print "networknode.update append status", status

            if not self.status  == status :

                self.status = status

                self.changeS = currentTime

        # ack (message can be status or stop)

        elif result == "set" :

            if not type( status ) == str : status = ""

            status = self.normalizeStatus( status )

##            print "networknode.update ack status", status

            if self.status is None :

                self.status = status

                self.changeS = currentTime

            elif not self.status == status :

                self.countStatusChange = self.countStatusChange + 1

                self.changeS = currentTime

                self.status = status


       # unknown result

        else :

            return

        # online (was offline or undefined )

        if ( ( bool( online ) ) and ( not self.online == True ) ) :
            
            self.onlineDurationS = utilities.float( onlineS, default = 0. )

            self.onlineTimeS = currentTime

            self.offlineTimeS = 0.

            self.online = True

        # offline (was online or undefined )

        if ( ( not bool( online ) ) and ( not self.online == False ) ) :
            
            self.onlineTimeS = 0.

            self.offlineTimeS = currentTime

            self.online = False           

        # number of correct messages ( for statistics )

        newCount = self.countAck + 1

        # delays in transmission (last one + statistics )
        
        self.delayMs = delayMs

        sumDelay = self.averageDelayMs * self.countAck

        sumSquaredDelay = self.averageSquaredDelayMs * self.countAck

        self.averageDelayMs = ( sumDelay + self.delayMs ) / newCount       

        self.averageSquaredDelayMs = ( sumSquaredDelay + self.delayMs * self.delayMs ) / newCount       


        # period (elapsed time ) since last message ok (last period + statistics )

        if self.timeS is None : self.periodS = 0.

        else : self.periodS = timeS - self.timeS

        sumPeriod = self.averagePeriodS * self.countAck

        sumSquaredPeriod = self.averageSquaredPeriodS * self.countAck

        self.averagePeriodS = ( sumPeriod + self.periodS ) / newCount       

        self.averageSquaredPeriodS = ( sumSquaredPeriod + self.periodS * self.periodS ) / newCount       

        # counter of correct messages
        
        self.countAck = newCount

        # time of last message
        
        self.timeS = timeS

        # last shift between timers (reception time, clock of receiver - emission time, clock of emitter )

        self.shiftS = self.receptionS - self.timeS

            

            


            

        




