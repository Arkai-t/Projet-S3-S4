""" ad-hoc network, builds dynamically lists of neighbors and exchanges status information """

import random

from api.BasicNetwork import *

from api.NetworkNode import *


class AdHocNetwork ( BasicNetwork ) :

    """ ad-hoc network, builds dynamically lists of neighbors and exchanges status information """

    # default values

    defaultDescription = "unknown"

    defaultIdentifier = "unknown"

    defaultPeriodPollMs = 100

    defaultPeriodChangeMs = 1000

    defaultPeriodListenMs = 1000

    defaultPeriodBroadcastMs = 5000

    defaultPeriodNeighborMs = 5000

    defaultStatus = "None"

    
    # list of addresses of neighbors (dynamic table)

    addressList = None

    # flag busy or not (avoids overlaps of timer calls )

    busy = None

    # description : hardware, software, version...

    description = None

    # elapsed time during current session

    elapsedMs = None

    # my identifier

    identifier = None

    # identifiers of neighbors (dynamic table)

    identifierList = None

    # last time the status was broadcasted
    
    lastBroadcastMs = None
    
    # last time change was checked

    lastChangeMs = None

    # last time the network was listened

    lastListenMs = None

    # last time the neighbors were cjhecked

    lastNeighborMs = None
    
    # list of neighbors (dynamic table)

    neighborList = None

    # flag online or not

    online = None

    # period for broadcasting status on the network

    periodBroadcastMs = None

    # period of polling changes

    periodChangeMs = None

    # period to listen the network

    periodListenMs = None

    # period to update active neighbors

    periodNeighborMs = None

    # period of polling

    periodPollMs = None

    
    # prefixes of messages (this list is completed in extensions of this class )

    prefixList = [
        "ack",      # the reply message of ad-hoc networks and/or general acknowledge
        "nack",     # general negative reponse, not acknowledge
        "status",   # sends status, ptp or broadcast
        "status?",  # requests status, ptp or broadcast
        "status!",  # sets destinatary status (answer = status)
        "status??", # asks to anybody for the status of some node
        "time",     # synchronization message (determines offset between real time clocks
        "stop",     # the "leave" notification message of ad-hoc networks
        "send",     # sends a buffer
        "data",     # sends one data packet (used by basic network, intermediate packets)
        "file",     # requests a buffer (e.g. a file)
        "line",     # sends values of time variables (packed into a packet)
        "stop!",    # command - exits the application on destinatary
        "restart!", # command - restarts the application on destinatary
        ]


    # previous status

    previousStatus = None

    # current status

    status = None

    # timer for periodic activity

    timer = None

    
    

    def __init__ (

        self,
        identifier = None,
        description = None,
        status = None,
        address = None,
        port = None,
        size = None,
        timeoutMs = None,
        periodMs = None,
        periodChangeMs = None,
        periodBroadcastMs = None,
        periodNeighborMs = None,
        periodListenMs = None,
        ) :

        """ constructor, creates sockets for broadcast and peer to peer messages """

        # who I am, and my status
        
        self.identifier = utilities.string( identifier, default = self.defaultIdentifier )

        self.status = utilities.string( status, default = self.defaultStatus )

        self.description = utilities.string( description, default = self.defaultDescription )

        # polling periods

        self.periodPollMs = utilities.integer( periodMs, default = self.defaultPeriodPollMs )

        self.periodBroadcastMs = utilities.integer( periodBroadcastMs, default = self.defaultPeriodBroadcastMs )

        self.periodListenMs = utilities.integer( periodListenMs, default = self.defaultPeriodListenMs )

        self.periodNeighborMs = utilities.integer( periodNeighborMs, default = self.defaultPeriodNeighborMs )

        self.periodChangeMs = utilities.integer( periodChangeMs, default = self.defaultPeriodChangeMs )


                                            
        BasicNetwork.__init__(
            self,
            address = address,
            port = port,
            size = size,
            timeoutMs = timeoutMs
            )

        self.neighborList = [ ]

        self.addressList = [ ]

        self.identifierList = [ ]

        self.timer = Clock()




    def broadcastStatus ( self ) :

        """ broadcast the status on the network """

        clockMs = clock.clockMs()

        if self.lastBroadcastMs is None : self.lastBroadcastMs = clockMs

        periodS = self.periodBroadcastMs / 2 + random.random() * self.periodBroadcastMs

        if clockMs < self.lastBroadcastMs + self.periodBroadcastMs : return False
                
        self.lastBroadcastMs = clockMs

        self.sendStatus()

        return True




    def checkNeighbors ( self ) :

        """ marks as off line the neighbors that did not communicate within 4 broadcast periods """

        if utilities.isEmpty( self.neighborList ) : return False

        clockMs = clock.clockMs()

        if self.lastNeighborMs is None : self.lastNeighborMs = clockMs

        if clockMs < self.lastNeighborMs + self.periodNeighborMs : return False
        
        self.lastNeighborMs = clockMs

        result = False

        for neighbor in self.neighborList :

            # already off line

            if not bool( neighbor.online ) : continue

            # needs the delay between clocks to proceed
            
            if ( ( neighbor.shiftS is None ) or ( neighbor.timeS is None ) ) : continue

            timeout = max( self.periodBroadcastMs / 1000., neighbor.averagePeriodS ) * 4.

            if neighbor.shiftS + neighbor.timeS >= clock.timeS() - timeout : continue

            neighbor.online = False

            result = True

        return result


                

    def checkStatus ( self ) :

        """ checks the changes of status and broadcasts new status if there is one """

        clockMs = clock.clockMs()

        if self.lastChangeMs is None : self.lastChangeMs = clockMs

        if clockMs < self.lastChangeMs + self.periodChangeMs : return False
        
        self.lastChangeMs = clockMs

        if self.status == self.previousStatus : return False

        self.previousStatus = self.status

##        print "checkStatus detected change", clockMs, self.identifier, self.status

        self.sendStatus()

        return True


        
        


    def executeMessage (

        self,
        prefix = None,
        timeS = None,
        identifier = None,
        origin = None,
        content = None
        ) :

        """ dummy function, should be replaced by external handler. Executes non-status messages """

##        print "execute unknown message", prefix, " from ", identifier, clock.clockMs()

        None


        
        
    def getAddress (

        self,
        identifier = None
        ) :

        """ returns the IP address of some equipment, from the dynamic table """

        index = utilities.index( self.identifierList, identifier )

        if index < 0 : return None

        if not utilities.isIndex( self.neighborList, index ) : return None

        neighbor = self.neighborList[ index ]

        if neighbor is None : return None

        return self.neighborList[ index ].address




        
    def getStatus (

        self,
        identifier = None,
        destination = None
        
        ) :

        """ gets the status of some equipment, defined by its identifier and/or its IP address
            if identifier and address are undefined, this is a broadcast
            
            """

        if utilities.isEmpty( destination ) : destination = self.getAddress( identifier )

        self.sendMessage(
            prefix = "status?",
            destination = destination
            )

        count = 0

        while True :

            result = self.receiveStatus( origin = destination )

            if not bool( result ) : break

            count = count + 1

            if not utilities.isEmpty( destination ) : break
            
        return count
    



    def listenMessages ( self ) :

        """ reads a sequence of contiguous messages """

        clockMs = clock.clockMs()

        if self.lastListenMs is None : self.lastListenMs = clockMs

        if clockMs < self.lastListenMs + self.periodListenMs : return False
        
        self.lastListenMs = clockMs

        result = False

        while True :

            ok = self.receiveMessage( timeout = 0 )

            if not ok : break

            result = True

            self.processMessage()
            
        return result



        
    def poll ( self ) :

        """ handles the clock events (polling, send status etc ) """

        if bool( self.busy ) : return

        self.busy = True

        self.checkStatus()

        self.checkTraffic()

        self.broadcastStatus()

        self.listenMessages()

        self.checkNeighbors()

        self.busy = False






    def processMessage ( self ) :

        """ polls messages from neighbors and  updates list of neighbors """


        if utilities.isEmpty( self.inContent ) : return False

##        print "processMessage", self.inPrefix, clock.clockMs()

        # discards messages IN (first connection of a device) and DATA (send 1 data packet)

        # restarts

        if self.inPrefix == "restart!" :

            os._exit( 3 )

        # aborts

        elif self.inPrefix == "stop!" :

            os._exit( 0 )


        elif self.inPrefix == "in" :

            None

        elif self.inPrefix == "data" :

            return False

        # this is somebody's status

        elif self.inPrefix == "status" :

            self.updateNeighbors()

        # this is somebody leaving

        elif self.inPrefix == "stop" :

            self.updateNeighbors()

        # request for status

        elif self.inPrefix == "status?" :

            self.sendStatus( destination = self.origin )

        # change status

        elif self.inPrefix == "status!" :

            try :

                identifier, elapsed, description, status = self.inContent.split( self.fieldDelimiter, 3 )

            except Exception, exception :

                return False

            if utilities.isEmpty( status ) : return False

            # external handler
            
            if callable( self.setStatus ) : self.setStatus( status )
            
        # this is somebody's status

        elif self.inPrefix == "time" :

            self.receiveTime()

        # this is a data transmission

        elif self.inPrefix == "file" :

            self.receiveFile()


        # packet of values from time variables
        
        elif self.inPrefix == "line" :

            self.receiveLine()

        # aborts the receiver, special exit to restart

        elif self.inPrefix == "restart!" :

            os._exit( 3 )

        # aborts the receiver, normal exit

        elif self.inPrefix == "stop!" :

            os._exit( 0 )

        # external handler

        elif callable( self.executeMessage ) :

            self.executeMessage(
                prefix = self.inPrefix,
                origin = self.origin,
                timeS = self.inTimeS,
                content = self.inContent
                )

        return True

        


    def receiveFile (

        self,
        prefix = "file"
        ) :

        """ receives a data file """

        # checks whether there is an identifier: status messages, the identifier is just after the date

        if not self.inPrefix == prefix : return False

        if utilities.isEmpty( self.inContent ) : return False

        path = utilities.normalizePath( self.inContent, normalize = False )

        result = self.sendMessage(
            prefix = "ack",
            destination = self.origin
            )

        if not result : return False

##        print "receiveFile", clock.clockMs(), self.origin, path


        result = self.receiveData(
            origin = self.origin,
            path = path
            )

        if not result : return False

        return True
            



    def receiveLine ( self ) :


        """ receives a packet of data of time variable """

        # checks whether there is an identifier: status messages, the identifier is just after the date

        if utilities.isEmpty( self.inContent ) : return False

        if self.inData is None : self.inData = self.inContent

        else : self.inData = self.inData + self.inContent

        print "receiveLine", self.origin, len( self.inData),
        
        result = self.sendMessage(
            prefix = "ack",
            destination = self.origin
            )

        print result
        
        return result
        


        
    def receiveTime ( self ) :

        """ updates list of neighbors """

        # loop on a sequence of time messages

##        print "receiveTime", self.origin

        count = None

        senderTimeS = None

        receiverTimeS = None

        senderOffsetS = None

        senderTransmissionS = None

        neighbor = None

        while True :
            
            # splits the message

            try :
                       
                identifier, \
                count, \
                senderTimeS, \
                receiverTimeS, \
                senderOffsetS, \
                senderTransmissionS = self.inContent.split( self.fieldDelimiter, 5 )

            except Exception, exception :

                return False

            # normalizes arguments
            
            count = utilities.integer( count )

            if count is None : return False
           
            senderTimeS = utilities.float( senderTimeS )

            if senderTimeS is None : return False
            
            receiverTimeS = utilities.float( receiverTimeS )
            
            if receiverTimeS is None : return False

##            print " ... parsed ", count, senderTimeS, receiverTimeS

            # end of the sequence of time messages
            
            if count <= 0 : break

            # already known or new neighbor
            
            if neighbor is None :

                index = utilities.index( self.identifierList, identifier )

                if index < 0 :

                    self.neighborList.append( NetworkNode(
                        address = self.origin,
                        identifier = identifier,
                        fieldDelimiter = self.fieldDelimiter
                        ) )

                    self.identifierList.append( identifier )

                    index = -1
                    
                neighbor = self.neighborList[ index ]

                neighbor.repetitions = None

                neighbor.transmissionS = None

                neighbor.offsetTimeS = None

            # sets or updates time count and time

            if neighbor.repetitions is None : repetitions = 0

            else : repetitions = neighbor.repetitions

            # transmission time (of 2 transactions )

            transmissionS = neighbor.transmissionS

            timeS = clock.timeS()
                
            if receiverTimeS == 0. : transmissionS = 0.

            elif repetitions == 0 : transmissionS = timeS - receiverTimeS

            elif transmissionS == 0. : transmissionS = timeS - receiverTimeS

            else : transmissionS = ( repetitions * transmissionS + timeS - receiverTimeS ) / ( repetitions + 1 )

            neighbor.transmissionS = transmissionS

            # offset

            offsetS = neighbor.offsetTimeS

            if senderTimeS == 0. : offsetS = 0.

            elif repetitions == 0 : offsetS = senderTimeS - transmissionS / 2. - timeS

            elif offsetS == 0. : offsetS = senderTimeS - transmissionS / 2. - timeS

            else : offsetS = ( repetitions * offsetS + senderTimeS - transmissionS / 2. - timeS ) / ( repetitions + 1 )
                
            neighbor.offsetTimeS = offsetS

            neighbor.repetitions = repetitions + 1

            # this was the last message, no need to answer, averages with the data computed by sender

            if count <= 1 : break

            content = self.identifier + self.fieldDelimiter + \
                      str( count - 1 ) + self.fieldDelimiter + \
                      str( timeS ) + self.fieldDelimiter + \
                      str( senderTimeS ) + self.fieldDelimiter + \
                      str( offsetS ) + self.fieldDelimiter + \
                      str( transmissionS )

##            print "    repetitions ", neighbor.repetitions, " send", content
                      
            ok = self.sendMessage(
                prefix = "time",
                destination = self.origin,
                content = content
                )

            if not ok : return False

            # here, has sent one message with count 1, does not have answer
            
            if count <= 2 : break

            ok = self.receiveMessage(
                prefix = "time",
                origin = self.origin,
                timeout = self.timeoutMs / 1000,
                )

            if not ok : return False


        # averages sender's and this device's estimates

        if neighbor is None : return False

        print "   --> repetitions    ", neighbor.repetitions
        print "   --> offset time    ", neighbor.offsetTimeS, "sender's", senderOffsetS
        print "   --> my transmission", neighbor.transmissionS, "sender's", senderTransmissionS

        senderOffsetS = utilities.float( senderOffsetS, default = - neighbor.offsetTimeS )

        neighbor.offsetTimeS = ( neighbor.offsetTimeS - senderOffsetS ) / 2.

        senderTransmissionS = utilities.float( senderTransmissionS, default = neighbor.transmissionS )

        neighbor.transmissionS = ( neighbor.transmissionS + senderTransmissionS ) / 2.
        
        return True

        

    def requestFile (
        
        self,
        path = None,
        destination = None,
        target = None,
        prefix = "file",
        ) :

        """ asks for a data file """

        # default target is the file name of the original path

        path = utilities.normalizePath( path, normalize = False )

        if utilities.isEmpty( target ) : target = utilities.pathLastNameWithExtension( path )

        # prefix plus ?, to ask for ...

        prefix = utilities.string( prefix, default = "file" )
        
        # checks whether there is an identifier: status messages, the identifier is just after the date
        
        result = self.sendMessage(
            prefix = prefix + "?" ,
            destination = destination,
            content = target,
            )

        if not result : return False

        result = self.receiveMessage(
            origin = destination,
            prefix = prefix
            )

##        print "receive message ", destination, prefix, result

        if not result : return False

        result = self.receiveFile( prefix = prefix )

        return result     



    def sendFile (
        
        self,
        path = None,
        destination = None,
        target = None,
        prefix = "file",
        ) :

        """ sends a data file """

        # default target is the file name of the original path

        path = utilities.normalizePath( path, normalize = False )

        if utilities.isEmpty( target ) : target = utilities.pathLastNameWithExtension( path )
        
        # checks whether there is an identifier: status messages, the identifier is just after the date
        
        result = self.sendMessage(
            prefix = prefix,
            destination = destination,
            content = target,
            )

        if not result : return False

        result = self.receiveMessage(
            prefix = "ack",
            origin = destination,
            timeout = self.timeoutMs / 1000,
            )


        if not result : return False

##        print "sendFile", clock.clockMs(), destination, self.outContent

        result = self.sendData(
            destination = destination,
            path = path
            )

        if not result : return False

        return True


            

    def sendLine (

        self,
        data = None,

        ) :

        """ sends a buffer containing the values of time variables (line) . This version is a broadcast!! """

        if not data is None : self.outData = data

        self.outData = data

        # checks whether there is an identifier: status messages, the identifier is just after the date
        
        # this device is a supervisor: does nothing


        for neighbor in self.neighborList :

            result = self.sendMessage(
                prefix = "line",
                destination = neighbor.address,
                content = self.outData,
                )

            if not result : return False

            result = self.receiveMessage(
                prefix = "ack",
                origin = neighbor.address,
                timeout = self.timeoutMs / 1000,
                )

            if not result : return False

        return True



        
    def sendStatus (

        self,
        prefix = None,
        identifier = None,
        description = None,
        status = None,
        elapsed = None,
        destination = None
        
        ) :

        """ broadcasts and/or sends the status of this equipment to some destinatary

            elapsed is the duration in seconds of the current on-line epoch
            
            """

        if utilities.isEmpty( identifier ) : identifier = self.identifier
        
        if utilities.isEmpty( identifier ) : return False

        if utilities.isEmpty( status ) : status = self.status

        else : status = utilities.string( status )

        if status is None : return False

        if not status.endswith( self.fieldDelimiter ) : status = status + self.fieldDelimiter

        if utilities.isEmpty( description ) : description = self.description

        else : description = utilities.string( description )

        if description is None : return False
        
        # default prefix = status

        if utilities.isEmpty( prefix ) : prefix = "status"

        if elapsed is None : elapsed = clock.timeS() - self.startS

        else : elapsed = utilities.float( elapsed, default = 0. )

        elapsed = "%.6f" % elapsed

        # estimates the size of a message : prefix, timeS, identifier, elapsed in ms, description, reset/append,
        
        sizeHeader = len( prefix ) + 1 + \
                     20 + 1 + \
                     len( identifier ) + 1 + \
                     len( elapsed ) + 1 + \
                     len( description ) + 1 + \
                     8 + 1 

        sizeStatus = len( status )

        if sizeHeader + sizeStatus < self.size :

            action = "reset"

            content = identifier + self.fieldDelimiter + \
                      elapsed + self.fieldDelimiter + \
                      description + self.fieldDelimiter + \
                      action + self.fieldDelimiter + \
                      status
            

            ok = self.sendMessage(
                prefix = prefix,
                content = content,
                destination = destination
                )

            return ( not ok is None )


##        print "AdHocNetwork.sendStatus", identifier, status[ : 40 ], "(", sizeStatus, "/", self.size, ")"

        # here, we have to split

        sizePacket = self.size - sizeHeader - 1

        result = True

        iStart = 0

        iLast = 0

        while iStart < sizeStatus :

            iMiddle = status.find( self.fieldDelimiter, iLast + 1, iStart + sizePacket )

            if iMiddle < 0 : iMiddle = sizeStatus

            iEnd = status.find( self.fieldDelimiter, iMiddle, iStart + sizePacket )

            # still fits into a packet
            
            if iEnd >= 0 : 

                iLast = iEnd

                continue

            # does not fit : sends until iLast

            if iStart == 0 : action = "ack"

            else : action = "append"
            
            content = identifier + self.fieldDelimiter + \
                      elapsed + self.fieldDelimiter + \
                      description + self.fieldDelimiter + \
                      action + self.fieldDelimiter + \
                      status[ iStart : iLast ]

            ok = self.sendMessage(
                prefix = prefix,
                content = content,
                destination = destination
                )

            if ok is None : return False

            iStart = iLast + 1  # skips the delimiter

            iLast = iLast + 1

        
        return True



    def sendStop (

        self,
        identifier = None,
        description = None,
        status = None,
        elapsed = None,
        destination = None
        
        ) :


        """ sends a stop message (leaving the network ) . Like status, but other prefix """

        result = self.sendStatus(
            prefix = "stop",
            identifier = identifier,
            description = description,
            status = status,
            elapsed = elapsed,
            destination = destination
            )
            
        
        return result




    def sendTime (

        self,
        count = None,
        senderTime = None,
        receiverTime = None,
        destination = None
        
        ) :

        """ sends a time message """

        if utilities.isEmpty( destination ) : return False

        count = utilities.integer( count, default = 2 )

        if count <= 0 : return False

        if senderTime is None : senderTime = clock.timeS()

        if receiverTime is None : receiverTime = 0.

        content = self.identifier + self.fieldDelimiter + \
                  str( count ) + self.fieldDelimiter + \
                  str( senderTime ) + self.fieldDelimiter + \
                  str( receiverTime ) + self.fieldDelimiter + \
                  str( 0. ) + self.fieldDelimiter + \
                  str( 0. )

        if destination is None : destination = self.origin

        print "sendTime", destination, content
                  
        ok = self.sendMessage(
            prefix = "time",
            destination = destination,
            content = content
            )

        if not ok : return False

        ok = self.receiveMessage(
            prefix = "time",
            origin = destination,
            timeout = self.timeoutMs / 1000,
            )

        if not ok : return False

        ok = self.receiveTime()

        return ok



    def setStatus (
        
        self,
        status = None
        ) :

        """ dummy function that sets the status """

        if utilities.isEmpty( status ) : return False
        
        self.status = status

        return True

        

            
    def start ( self ) :

        """ starts a session """

        self.online = True

        self.startS = clock.timeS()

        self.resetCounters()

        self.checkAddress()

        self.sendStatus()

        if self.periodPollMs > 0 :

            self.timer.start(
                periodMs = self.periodPollMs,
                command = self.poll,
                )
        

        
        

        



    def stop ( self ) :

        """ stops the current session """


        self.sendStop()

        self.online = False

        self.timer.stop()


        

    def updateNeighbors ( self ) :

        """ updates list of neighbors """

        # checks whether there is an identifier: status messages, the identifier is just after the date

        if ( ( not self.inPrefix == "status" ) and ( not self.inPrefix == "stop" ) ) : return False

        if utilities.isEmpty( self.inContent ) : return False

        try :
                   
            identifier, elapsed, description, status = self.inContent.split( self.fieldDelimiter, 3 )

        except Exception, exception :

            return False

        # already known
        
        index = utilities.index( self.identifierList, identifier )

        if index < 0 :

##            print "new neighbor", clock.clockMs(), identifier, self.origin

            self.neighborList.append( NetworkNode(
                address = self.origin,
                identifier = identifier,
                fieldDelimiter = self.fieldDelimiter
                ) )

            self.identifierList.append( identifier )

            index = -1

        # gets the action of the status

        if status.startswith( "set" + self.fieldDelimiter ) :

            action = "set"  

            status = status[ 4 : ]

        elif status.startswith( "add" + self.fieldDelimiter ) :

            action = "add"

            status = status[ 4 : ]

        else :

            action = "ack"

        self.neighborList[ index ].update(
            result = action,
            address = self.origin,
            onlineS = elapsed,
            description = description,
            status = status,
            timeS = self.inTimeS,
            online = ( self.inPrefix == "status" ),
            )


        return True



