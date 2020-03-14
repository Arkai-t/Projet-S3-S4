""" basic network object, uses UDP (python DataGrams), sends and receives packets, messages and data """

import sys

import os

import socket

from api.Utilities import *

from api.Clock import *


class BasicNetwork :

    """ basic network object, uses UDP (python DataGrams), sends and receives packets, messages and data """

    # default values

    defaultPort = 50000

    defaultSize = 2048

    defaultTimeoutMs = 2000


    # address of this device

    address = None

    # broadcast address

    broadcastAddress = "255.255.255.255"

    # counts of packets, received packets, sent packets

    countListened = None

    countReceived = None

    countSent = None

    
    
    # error message

    error = None

    # field delimiter

    fieldDelimiter = None
    
    # message buffer

    inBuffer = None

    # content of message

    inContent = None

    # data buffer

    inData = None

    # prefix of last message

    inPrefix = None

    # socket
    
    inSocket = None

    # time of last message

    inTimeS = None

    # instant of last minute (for traffic counters )

    lastMinuteS = None
    
    # origin of a message

    origin = None
    
    # message buffer

    outBuffer = None

    # content of message

    outContent = None

    # data buffer

    outData = None

    # prefix of last message

    outPrefix = None

    # socket
    
    outSocket = None

    # time of last message

    outTimeS = None

    # prefixes of messages (this list is completed in extensions of this class )

    prefixList = [
        "ack",      # the reply message of ad-hoc networks and/or general acknowledge
        "nack",     # general negative reponse, not acknowledge
        "receive",  # requests a buffer (e.g. a file)
        "send",     # sends a buffer
        "data",     # sends one data packet
        ]
        
    # socket
    
    receiveSocket = None

    # socket
    
    sendSocket = None

    # size of message buffer

    size = None
    
    # start time of current session  (clock ticks, and seconds )

    startMs = None
        
    startS = None
        
    # time out for reception

    timeoutMs = None

   
    

    def __init__ (

        self,
        address = None,
        port = None,
        size = None,
        timeoutMs = None
        ) :

        """ constructor, creates sockets for broadcast and peer to peer messages """

        self.setDefault(
            address = address,
            port = port,
            size = size,
            timeoutMs = timeoutMs
            )

             
        # reception in broadcast mode:
        
        self.inSocket = self.socket( mode = "in" )
        
        self.outSocket = self.socket( mode = "out" )

        self.startS = clock.timeS()

        # resets packet counters

        self.resetCounters()

        # sends initial packet to get its own address

        self.checkAddress()


        

    def checkAddress ( self ) :

        """ sends and receives a packet to set its own address """

        address = self.address

        content = utilities.string( self.identifier, default = "" ) + self.fieldDelimiter + \
                  utilities.string( self.address, default = "" )

        
        result = self.sendMessage(
            prefix = "in",
            content = content
            )

##        print "checkAddress sends message ", "in - ", content, "->", result


        if result is None : return False

        # receives a message (modifies the address so that the message is read )

        self.address = "0.0.0.0"
        
        result = self.receiveMessage( prefix = "in" )

        self.address = address

        if result is None : return False

        if not self.inContent == content : return False

        self.address = self.origin

##        print "BasicNewtork setAddress found ", self.address

        return True

        


    def checkTraffic ( self ) :

        """ checks the changes of status and broadcasts new status if there is one """

        timeS = clock.timeS()

        minuteS = int( timeS / 60 ) * 60

        if self.lastMinuteS is None : self.lastMinuteS = minuteS

        if  minuteS > self.lastMinuteS : self.resetCounters()

            




    def message (

        self,
        prefix = None,
        content = None
        ) :

        """ builds a message with the given prefix, the time and the content (comma-separated),

            writes it in self.outBuffer

            returns True iff
            
            """

        if not type( prefix ) == str : return False

        if not type( content ) == str : content = utilities.string( content, default = "" )

        self.outBuffer = str( prefix ) + self.fieldDelimiter + \
                      "%.6f" % clock.timeS() + self.fieldDelimiter + \
                      str( content )

        return True



        
    def receiveData (

        self,
        path = None,
        origin = None
        ) :

        """ receives data from the origin and eventually writes it to a file. Reads a sequence of data packets of self.size

            returns True iff OK

            """

        if utilities.isEmpty( origin ) : origin = self.origin

        if utilities.isEmpty( origin ) : return False

        self.inData = ""

        index = 0

        count = None
        
        # reads packets, i.e., messages of the form data, data, number, count, xxxxx
        
        while True :

            if ( ( not count is None ) and ( index >= count ) ) : break

            # reads a packet
            
            thisData = self.receiveMessage(
                prefix = "data",
                origin = origin,
                timeout = self.timeoutMs / 1000,
                )

            if thisData is None : return False

            # checks the packet number : splits with 4 commas (prefix, time, number, count,,,)

            items = thisData.split( self.fieldDelimiter, 4 )

            if len( items ) < 5 : return False

            # not the expected packet

            thisIndex = utilities.integer( items[ 2 ] )

            thisCount = utilities.integer( items[ 3 ] )
            
            if not index == thisIndex : return False

            # the count of packets changed
            
            if count is None : count = thisCount

            elif not count == thisCount : return False
            
            # appends the data

            self.inData = self.inData + items[ 4 ]

##            print "receiveData index", index, "this ", thisIndex, thisCount,
                        
            # acknowledges waits for confirmation, with ACK and a time posterior to send time

            content = utilities.string( index ) + self.fieldDelimiter + \
                      utilities.string( count ) + self.fieldDelimiter + \
                      items[ 4 ]
            
            ok = self.sendMessage(
                prefix = "ack",
                destination = origin,
                content = content
                )

            if ok is None : return False

##            print "send ack", (not ok == None)
            
            index = index + 1

        # if there is a path, writes the result

        if utilities.isEmpty( path ) : return True

        ok = utilities.fileWrite( path, self.inData, mode = "wb" )

        if ok : return True

        # error writing file

        self.error = "Network.receiveData " + utilities.string( utilities.error, default = "" )

        return False




    def receiveMessage (

        self,
        prefix = None,
        timeS = None,
        origin = None,
        timeout = None,
        ) :

        """ gets a message in broadcast mode, fills the message buffer

            if receives an invalid messages (sender, time or prefix are incorrect), throws it away (message is lost ).

            returns True iff OK
            
            """

        previousTimeout = self.inSocket.gettimeout()

        if timeout is None : timeout = previousTimeout

        else : self.inSocket.settimeout( timeout )        

        while True :
            
            ok = self.receivePacket( )

            # received nothing
            
            if not ok : break

            items = self.inBuffer.split( self.fieldDelimiter, 2 )

            if len( items ) <= 2 : continue

            # controls the message

            if ( ( not prefix is None ) and ( not prefix == items[ 0 ] ) ) : continue

            if ( ( not timeS is None ) and ( not timeS <= items[ 1 ] ) ) : continue

            if ( ( not origin is None ) and ( not origin == self.origin ) ) : continue

            # prefix of message
            
            self.inPrefix = items[ 0 ]

            # time of message

            self.inTimeS = items[ 1 ]

            # content of message

            self.inContent = items[ 2 ]

            break

##        if ok : print "BNWK receive message", self.inPrefix, self.inContent

        if not timeout == previousTimeout : self.inSocket.settimeout( previousTimeout )

        return ok



    def receivePacket (

        self,
        origin = None
        ) :

        """ gets a message (a packet) in broadcast mode or peer to peer, fills the message buffer

            discards the messages until the correct one (with the desired origin) is received

            returns True iff OK
            
            """

        if self.inSocket is None : self.inSocket = self.socket( mode = "in" )

        self.error = ""

        while True :

            try :        

                text, address = self.inSocket.recvfrom( self.size )

            except Exception, exception :

                self.error = "Network.readMessage : " + str( exception )

                return False
            
            if text is None : break

            self.countListened = self.countListened + 1

            # keeps on reading until the sender is correct
            
            if address[ 0 ] == self.address : continue

            if ( ( not origin is None ) and not ( address[ 0 ] == origin ) ) : continue

            # everything works
            
            self.inBuffer = text

            self.origin = address[ 0 ]

            self.countReceived = self.countReceived + 1

            break

        return True



        

    def resetCounters ( self ) :

        """ resets the counters for traffic statistics """
        
        self.countListened = 0

        self.countSent = 0

        self.countReceived = 0

        timeS = clock.timeS()

        self.lastMinuteS = int( timeS / 60 ) * 60
    



    def sendData (

        self,
        path = None,
        data = None,
        destination = None
        ) :

        """ sends data to the destination, file or buffer. Cuts the content in blocks of self.size

            returns True iff OK

            """

        if utilities.isEmpty( destination ) : destination = self.origin

        if utilities.isEmpty( destination ) : return False

        # places the data in attribute self.outData

        if not data is None : self.outData = data
        
        elif utilities.filePresent( path ) : self.outData = utilities.fileRead( path, mode = "rb" )

        if utilities.isEmpty( self.outData ) : return False

        size = len( self.outData )

        # size of the packets
        
        packetSize = self.size - 32

        if packetSize <= 0 : return None

        # number of packets
        
        packets = size / packetSize

        if size % packetSize > 0 : packets = packets + 1

        for packet in range( packets ) :

            first = packet * packetSize

            last = min( size, first + packetSize )

            count = str( packet) + self.fieldDelimiter + str( packets ) + self.fieldDelimiter
            
            ok = self.sendMessage(
                prefix = "data",
                content = count + self.outData[ first : last ],
                destination = destination
                )

            if not ok : return None

##            print "sendData packet ",packet, " / ", packets,

            # waits for confirmation, with ACK and a time posterior to send time
            
            ok = self.receiveMessage(
                prefix = "ack",
                origin = destination,
                timeout = self.timeoutMs / 1000,
                )

##            print "answer ", self.outPrefix, self.origin, (not ok is None )

            if not ok : return False

        return True
            


    
    def sendMessage (

        self,
        prefix = None,
        content = None,
        destination = None,
        ) :

        """ writes a message in broadcast mode or peer to peer ( message is in self.outBuffer)

            returns True iff ok
            
            """


        ok = self.message( prefix, content )

        if not ok : return False

        ok = self.sendPacket( destination = destination )

        if not ok : return False

        self.outPrefix = prefix

        self.outTimeS = clock.timeS()

        self.outContent = content

        return True

    


    def sendPacket (

        self,
        packet = None,
        destination = None,
        ) :

        """ writes a packet (message) in broadcast mode or peer to peer ( message is in self.outBuffer)

            returns True iff OK
            
            """

        if self.outSocket is None : self.outSocket = self.socket( mode = "out" )

        if self.outSocket is None : return False

        if not packet is None : self.outBuffer = packet

        if self.outBuffer is None : return False

        if not type( destination ) == str : destination = self.broadcastAddress

        try :        

            self.outSocket.sendto( self.outBuffer, ( destination, self.port ) )

        except Exception, exception :

            self.error = "Network.sendPacket : " + str( exception )

            return False

        self.countSent = self.countSent + 1

        self.countListened = self.countListened + 1

        return True



    def socket (
        
        self,
        mode = None,
        bind = None,
        connect = None,
        port = None,
        timeoutMs = None,
        ) :

        """ returns a socket according to mode (in, out, receive, send) or with the given binding or connection

            returns None in case of problem
            
            """

        self.error = ""

        try :
            
            sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )

        except Exception, exception :

            self.error = "Network.socket " + str( exception )

            return None
        

        if sock is None : return None

        # ports above 49... are for user application (linux convention)
        
        if not type( port ) == int : port = self.port

        # time out 

        if not type( timeoutMs ) == int : timeoutMs = self.timeoutMs

        sock.settimeout( timeoutMs / 1000 )
        

        # socket for listening in broadcast mode

        if mode == "in" :

            if not type( bind) == str : bind = ""

            try :

                sock.bind( ( bind, port ) )

            except Exception, exception :

                self.error = "Network.socket " + str( exception )

                return None


        # socket for emitting in broadcast mode or p.t.p.
        
        elif mode == "out" :


            # broadcast mode

            try :
            
                sock.setsockopt( socket.SOL_SOCKET, socket.SO_BROADCAST, 1 )

            except Exception, exception :

                self.error = "Network.socket " + str( exception )

                return None
                

            # this is done only in case of problems, e.g., nokias, require a first connection before broadcasting

            try :

                
                if type( connect ) == str : sock.connect( ( connect, port ) )

            except Exception, exception :

                self.error = "Network.socket " + str( exception )

                return None
            
        # no defined mode, but there is a binding required            
        
        elif type( bind ) == str :

            try :

                sock.bind( ( bind, port ) )

            except Exception, exception :

                self.error = "Network.socket " + str( exception )

                return None


        # no defined mode but there is a connection required

        elif type( connect ) == str :

            # this is done only in case of problems, e.g., nokias, require a first connection before broadcasting

            try :
                
                sock.connect( ( connect, port ) )

            except Exception, exception :

                self.error = "Network.socket " + str( exception )

                return None

        return sock




        
        
    def set (

        self,
        address = None,
        port = None,
        size = None,
        timeoutMs = None
        ) :

        """ sets the default attributes

            returns True iff OK
            
            """

        # no address: tries to get it from the socket module (may not work on some devices if network not accessed yet)
        
        if not address is None : self.address = address

        # port : user's application ports are above 49k in linux, default is 50000
        
        if not port is None : self.port = int( port )

        # size of messages in bytes

        if not size is None : self.size = int( size )
               
        # time out in seconds
        
        if not timeoutMs is None :

            self.timeoutMs = int( timeoutMs )

            try :

                self.inSocket.settimeout( self.timeoutMs / 1000 )

            except Exception, exception :

                self.error = "Network.set : " + str( exception )

                return False

        return True


        






        
        
    def setDefault (

        self,
        address = None,
        port = None,
        size = None,
        timeoutMs = None
        ) :

        """ sets the default attributes """

        # no address: tries to get it from the socket module (may not work on some devices if network not accessed yet)

        
        if address is None :

            try :
                
                self.address = socket.gethostbyname( socket.gethostname() )

            except Exception, exception :

                self.error = "Network.setDefault : " + str( exception )

                self.address = ""

        else :

            self.address = address

        # port : user's application ports are above 49k in linux, default is 50000
        
        if port is None : self.port = self.defaultPort

        else : self.port = int( port )

        # size of messages in bytes

        if size is None : self.size = self.defaultSize

        else : self.size = int( size )
               

        # time out in seconds
        
        if timeoutMs is None : self.timeoutMs = self.defaultTimeoutMs

        else : self.timeoutMs = int( timeoutMs )

        # delimiter

        self.fieldDelimiter = ","


        


