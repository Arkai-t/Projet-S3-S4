""" Executable block, i.e., object that contains a call() method, in python or in C """


import sys

import os

import array

import struct

from api.Utilities import *

from api.Clock import *

from api.External import *


class Block :

    """ processing block of Signal Memory Box """

    # processing function

    call = None

    # data buffer used for C modules (char * )

    dataArray = None
    
    # pointer to data buffer used for C modules (char * )

    dataBuffer = None

    # list containing initial data

    dataList = None

    # size of ...

    dataSize = None

    # dll with execute method

    dll = None

    # processing method. will be assigned to executeExternal () or executeInternal ()

    execute = None

    # flag to indicate that we use an external execute(), thus arrays of values instead of lists

    externalFlag = None
    
    # identifier

    identifier = None

    # level of line in the block diagram : max( level( input lines ) ) + 1

    level = None

    # module from where the execute() method is loaded

    module = None
    
    
    



    def __init__ (

        self,
        identifier = None,
        module = None,
        dll = None,
        dataList = None
        
        ) :

        """ constructor """

        # format of buffer

        if type( dataList ) == list : self.dataList = dataList

        elif not type( dataList ) is None : self.dataList = [ dataList ]


        # sets default values

        self.setDefault()

        # sets attributes from parameters

        self.identifier = utilities.string( identifier, default = self.identifier )

        # if there is a module

        if not module is None : self.setModule( module )

        # if there is a dll

        if not dll is None : self.setDll( dll )

        # assigns the execution method to internal or external

        if bool( self.externalFlag ) : self.execute = self.executeExternal

        else : self.execute = self.executeInternal

        # prepares execution

        self.reset()





    def executeInternal ( self ) :

        """ executes the processing block on the input lines , writes the output lines """

        return self.call( self )

        




    def executeExternal ( self ) :

        """ executes the processing block on the input lines , writes the output lines """

        return self.call(
            self.dataBuffer,
            self.dataSize
            )
        




    def getData ( self ) :

        """ gets the data buffer and places it in dataList. use the format of dataList items to unpack **EF WEIRD """

        iList = 0

        iArray = 0

        for iList in range( len( self.dataList ) ) :

            item = self.dataList[ iList ]

            if type( item ) == str :

                length = len( item )

                format = length * "c"

            elif type( item ) == int :

                length = struct.calcsize( "i" )

                format = "i"


            elif type( item ) == float :
            
                length = struct.calcsize( "d" )

                format = "d"

            else : continue

            try :

                self.dataList[ iList ] = struct.unpack( format, self.dataArray[ iArray : iArray + length ] )[ 0 ]

            except Exception, exception :

                None
                
            iArray = iArray + length

                

        




    def reset ( self ) :

        """ resets/sets the data buffers. prepares dataSize, dataArray, and for external functions, dataBuffer

            note that dataSize can be larger than the list of formats (data buffer may be used as work buffer)
            
            """

        dataBuffer = ""

        for item in self.dataList :

            if type( item ) == str : None

            elif type( item ) == int : item = struct.pack( "i", item )

            elif type( item ) == float : item = struct.pack( "d", item )

            else : continue

            dataBuffer = dataBuffer + item
            
        self.dataSize = max( self.dataSize, len( dataBuffer ) )

        self.dataArray = array.array( "c", self.dataSize * [ chr( 0 ) ] )

        for index in range( len( dataBuffer ) ) :

            self.dataArray[ index ] = dataBuffer[ index ]

        if bool( self.externalFlag ) :

            self.dataBuffer, dummy = self.dataArray.buffer_info()




        
        
    def setDefault ( self ) :

        """ sets default values """

        self.dataSize = 0
        
        self.identifier = "block"
        

    

    def setDll (

        self,
        dll = None
        ) :

        """ sets the attributes of the object from a .py module """

        self.externalFlag = False
        
        self.dll = dll

        try :

            if callable( dll.call ) :

                self.call = dll.call

                self.externalFlag = True

        except Exception, exception :

            None




    def setModule (

        self,
        module = None
        ) :

        """ sets the attributes of the object from a .py module """

        self.module = module


        try :

            if callable( module.call ) : self.call = module.call

        except Exception, exception :

            None

        try :

            if type( module.dataList ) == list : self.dataList = module.dataList

        except Exception, exception :

            None








def loadBlock ( path = None ) :

    """ returns a block, loaded from path """

    # path name

    name = utilities.pathName( path )

    # reads the module

    module = external.loadModule( path )

    if module is None : return None

    # checks whether there is a dll

    dll = external.loadLibrary( path )

    block = Block(
                identifier = name,
                module = module,
                dll = dll,
                )

    return block

