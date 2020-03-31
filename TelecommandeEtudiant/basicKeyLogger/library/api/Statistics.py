
""" Statistics manager

    """

import math

from api.Utilities import *

from api.AttributeValueList import *


class Statistics :

    """ Statistics manager. constructs simple statistics and histograms

        There is a list of even categories ( names ) defined by the caller, and arrays containing for each event
        - number of events
        - sum of values
        - min
        - max
        - sum of squared values
        - values of histogram bins have precision 1, i.e., integers, no limit on the number of bins.
        - counts of histogram

        The access methods are the basic statistics, N Mean Stdev Min Max.
        Histograms and bins are accessed directly.

        Limitations: the number of bins is the same for all events
        Bins are obtained by dividing min - max into 
        

        """

    # size of data ( # of categories )
    
    _size = None
    
    # list of event types ( names )
    
    categoryList = [ ]
    

    # number of event types
    
    sizeCategories = 0
    
    # event count
    
    countList = [ ]

    # sum of values
    
    sumList = [ ]

    # sum of squared values
    
    sum2List = [ ]

    # min value
    
    minList = [ ]

    # max value
    
    maxList = [ ]

    # values encountered (for histogram, rounded to integers )
    
    valueList = [ ]

    # frequencies of values
    
    frequencyList = [ ]

    # object for sorting histogram
    
    attributeValueList = None
    
    def __init__ (
        
        self,
        categories = None
        ) :

        """ Constructor

            """

        self.set( categories = categories )






    def addCategory (

        self,
        category = None
        ) :

        """ Adds a category to the list
        
            returns the index or -1if problem
            
            """

        index = utilities.index( self.categoryList, category )

        if index >= 0 : return index

        self.categoryList.append( utilities.string( category ) )

        self.countList.append( 0 )
        
        self.sumList.append( 0. )
        
        self.sum2List.append( 0. )
        
        self.minList.append( 0. )
        
        self.maxList.append( 0. )
        
        self.valueList.append( [ ] )
        
        self.frequencyList.append( [ ] )

        index = self._size

        self._size = self._size + 1

        return index

        


    
    def categoryIndex (
        
        self,
        category = None
        ) :

        """ Returns the index of a category in the list, -1 in case of problem """

                
        if ( ( self.size() is None ) or ( self.size() <= 0 ) ) : return -1

        # default is 1st category        

        if category is None : category = self.categoryList[ 0 ]
            
        # checks whether category is correct

        category = utilities.string( category, self.categoryList )

        if category is None : return -1

        # category number

        return utilities.index( self.categoryList, category )


    def createArrays ( self ) :


        """ Creates empty arrays from a given categoryList

            Note that it uses a loop and append, because  N * [ [] ] creates coreferences to the same list

            """

        self.countList = [ ]
        
        self.sumList = [ ]
        
        self.sum2List = [ ]
        
        self.minList = [ ]
        
        self.maxList = [ ]
        
        self.valueList = [ ]
        
        self.frequencyList = [ ]

        for index in range( self.size() ) :


            self.countList.append( 0 )
            
            self.sumList.append( 0. )
            
            self.sum2List.append( 0. )
            
            self.minList.append( 0. )
            
            self.maxList.append( 0. )
            
            self.valueList.append( [ ] )
            
            self.frequencyList.append( [ ] )



    def event (
        
        self,
        value = None,
        category = None,
        create = None
        ) :

        """ Adds an event
        
            Default category is first one

            create indicates whether new categories can be added or not

            Returns True/False
            
            """

        # creates empty lists in case
        
        if self.size() <= 0 : self.reset()

        # default value is 0

        if value is None : value = 0

        # index of category

        index = self.categoryIndex( category )

        if index < 0 :

            if bool( create ) : index = self.addCategory( category )

            else : return False

        # updates counts

        floatValue = utilities.float( value, default = 0. )
        
        self.countList[ index ] = self.countList[ index ] + 1

        self.sumList[ index ] = self.sumList[ index ] + floatValue

        self.sum2List[ index ] = self.sum2List[ index ] + floatValue * floatValue

        self.minList[ index ] = min( self.minList[ index ], floatValue )

        self.maxList[ index ] = max( self.maxList[ index ], floatValue )

        # list of values: looks for integer value, and eventually, adds it to the list

        changed = self.updateHistogram(
            value = value,
            values = self.valueList[ index ],
            frequencies = self.frequencyList[ index ]
            )

        return True

        

    def get (

        self,
        category = None
        ) :
        
        """ Returns the statistics (NOT the histogram) for the category

            default category is 1st one
            

            """

        # default statistics

        count = 0

        mean = 0.

        stdev = 0.

        lowest = 0.

        highest = 0.

        index = self.categoryIndex( category )

        
        if index < 0 : return count, mean, stdev, lowest, highest

        # no event:

        if self.countList[ index ] <= 0 : return count, mean, stdev, lowest, highest

        # determines mean and stdev

        count = self.countList[ index ]
        
        mean = float( self.sumList[ index ]) / float( count )
        
        variance = float( self.sum2List[ index ] )  / float( count ) - mean * mean
        
        if variance <= 0 : stdev = 0.

        else : stdev = math.sqrt( variance )

        lowest = float( self.minList[ index ] )
        
        highest = float( self.maxList[ index ] )

        return count, mean, stdev, lowest, highest



    def getCategories ( self ) :

        """ Returns the category list """

        return self.categoryList


        
    def getCounts ( self ) :
        
        """ Returns the list of counts """

        return self.countList


        
    def getMaxs ( self ) :
        
        """ Returns the list of maxima """

        return self.maxList

    

    def getMins ( self ) :
        
        """ Returns the list of minima """

        return self.minList
    

        
    def getSums ( self ) :
        
        """ Returns the list of sums """

        return self.sumList


        
    def getSum2s ( self ) :
        
        """ Returns the list of squared sums """

        return self.sum2List

    
        
            

    def histogram (

        self,
        category = None,
        sort = None
        ) :
        
        """ Returns the histogram for the category

            Sort indicates whether it is sorted : by value (default), frequency or none

            default category is 1st one

            Returns 2 empty lists in case of problem
            
            """

        sort = utilities.string(
            sort,
            [ "none", "value", "frequency" ] )
        
        if sort is None : sort = "value"
        

        index = self.categoryIndex( category )
        
        if ( ( index < 0 ) or ( self.countList[ index ] <= 0 ) ) : return [], []

        # converts the sort criterion into those of AttributeValueList:
        
        if sort == "value" :
            
            criterion = "attribute"
            
            order = "<"

        elif sort == "frequency" :
            
            criterion = "value"
            
            order = ">"

        else :
            
            criterion = "none"
            

        # sorts with the LAV object.
        
        self.valueList[ index ], self.frequencyList [ index ] = attributeValueList.sort(
            criterion = criterion,
            order = order,
            attributes = self.valueList[ index ],
            values = self.frequencyList[ index ]
            )
            

        return self.valueList[ index ], self.frequencyList[ index ]



    def reset ( self ) :

        """ Resets the statistics, including the histograms
        
            unlike createData (which sets the arrays to 0), reset empties all the arrays
            
            """

        if ( ( self.size() is None ) or ( self.size() <= 0 ) ) : return False

        for index in range( self.size() ) :

            self.countList[ index ] = 0

            self.sumList[ index ] = 0

            self.sum2List[ index ] = 0

            self.minList[ index ] = 0

            self.maxList[ index ] = 0

            self.valueList[ index ] = [ ]

            self.frequencyList[ index ] = [ ]

        return True



    def set (

        self,
        categories = None
        ) :

        """ Sets the categories """

        if type( categories ) == list : self.categoryList = categories

        elif categories is None : self.categoryList = [ "event" ]

        else : self.categoryList = [ utilities.string( categories ) ]
        
        self._size = len( self.categoryList )
        
        # creates the arrays of statistics

        self.createArrays()


    def sort ( self ) :

        """ Sorts the data by increasing category

            Because it is unfrequent, uses a bubble sort
            
            """

        for index2 in range( 1, self.size() ) :

            for index1 in range( index2 ) :

                category2 = self.categoryList[ index2 ]
            
                category1 = self.categoryList[ index1 ]

                if category1 > category2 :

                    self.categoryList[ index1 ] = category2

                    self.categoryList[ index2 ] = category1
                    

                    temp = self.countList[ index1 ]

                    self.countList[ index1 ] = self.countList[ index2 ]

                    self.countList[ index2 ] = temp


                    temp = self.maxList[ index1 ]

                    self.maxList[ index1 ] = self.maxList[ index2 ]

                    self.maxList[ index2 ] = temp
                    

                    temp = self.minList[ index1 ]

                    self.minList[ index1 ] = self.minList[ index2 ]

                    self.minList[ index2 ] = temp
                    
        
                    temp = self.sumList[ index1 ]

                    self.sumList[ index1 ] = self.sumList[ index2 ]

                    self.sumList[ index2 ] = temp
                    

                    temp = self.sum2List[ index1 ]

                    self.sum2List[ index1 ] = self.sum2List[ index2 ]

                    self.sum2List[ index2 ] = temp
                    

                    temp = self.valueList[ index1 ]

                    self.valueList[ index1 ] = self.valueList[ index2 ]

                    self.valueList[ index2 ] = temp
        


                    temp = self.frequencyList[ index1 ]

                    self.frequencyList[ index1 ] = self.frequencyList[ index2 ]

                    self.frequencyList[ index2 ] = temp
        



    def size ( self ) :

        """ Size of the data ( number of event categories) """

        if self._size is None :

            if type( self.categoryList ) is None : self.categoryList = [ ]

            self._size = len( self.categoryList )

        return self._size
    

            
    def updateHistogram (

        self,
        value = None,
        values = None,
        frequencies = None
        ) :

        """ Adds the value to an histogram (values, histogram). If absent, adds a bin at the end

            Works with any lists, not those of the object

            returns True if added a bin, False otherwise

            """

        if value is None : return -1

        if values is None : return -1

        if frequencies is None : return -1

        if not len( values ) == len( frequencies ) : return -1

        rank = utilities.index( values, value )

        # finds the value

        if rank >= 0 :

            frequencies[ rank ] = frequencies[ rank ] + 1

            return False


        # not found: appends value, sorts and finds rank in sorted list

        else :
           
            values.append( value )

            frequencies.append( 1 )

            return True

        
# -----------------------------------
# creates the global singleton object if not already here
#

if not "statistics" in globals() : statistics = Statistics()
         
        
            
        
        
        
        
            
   

        
