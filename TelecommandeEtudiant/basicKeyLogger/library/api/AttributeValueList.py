
""" Attribute value list, generalizes to PropertyList (java) or Dictionary (Python)

    *EF 2009 04 18 to optimize

    
    """


from api.Utilities import *

from api.TableFile import *


class AttributeValueList :

    """ Attribute value list, generalizes to PropertyList (java) or Dictionary (Python)

    """



    # list of attributes
    
    attributeList = None

    # list of values
    
    valueList = None

    # uses an error status string
    
    error = None

    def __init__ (
        
        self,
        attributes = None,
        values = None
        ) :

        """ Constructor. Initial attributes and values are optional """

        self.clear()

        self.insert( attributes, values )



    def attributes (
        
        self,
        value = None
        ) :

        """ Returns the list of attributes that correspond currently to some value

            Thows no exception

            """

        if value is None : return self._attributeList
        
        
        # loop on pairs

        attributes = [ ]
        
        for index in range( len( self._valueList ) ) :
            
            if ( ( value == self._valueList[ index ] ) and ( index < len( self._attributeList ) ) ) :
                
                attributes.append( self._attributeList[ index ] )
            
        return attributes


    def clear ( self ) :


        """ Empties the list """

        self._attributeList = [ ]

        self._valueList = [ ]
        
        utilities.error = ""
        
        
    def delete (
        
        self,
        attribute
        ) :

        """ Deletes a pair or a list of pairs

            Returns True if the pair(s) aree absent after the operation


            If argument is None : returns True
            
            """

        # if both are none, returns True
        
        if attribute is None :
            
            utilities.error = ""
            
            return True
        

        # a good pair
        
        elif self.isAttribute( attribute ) :

            # already absent
            
            index = utilities.index( self._attributeList, attribute )
            
            if index < 0 : return True
            
            self._attributeList = self._attributeList[ : index ] + self._attributeList [ index + 1 : ]
            
            self._valueList = self._valueList[ : index ] + self._valueList [ index + 1 : ]

            return True
            

        # 2 lists of the same size, composed of valid pairs
        
        elif self.isAttributes( attribute ) :

            for word in attribute :

                # dont use recursively self.delete, it would flatten the lists
                
                index = utilities.index( self._attributeList, word )

                # already absent

                if index < 0 : continue
                
                self._attributeList = self._attributeList[ : index ] + self._attributeList [ index + 1 : ]
                
                self._valueList = self._valueList[ : index ] + self._valueList [ index + 1 : ]

            utilities.error = ""
            
            return True              

        # otherwise...
        
        else :
            
            utilities.error = "AttributeValueList.delete : invalid arguments"
            
            return False


    def extend (
        
        self,
        attributeValueList = None
        ) :

        """ Merges 2 LAVs. alias for self.merge """
        
        result = self.merge( attributeValueList )
        
        return result
    

    def get (
        
        self,
        attribute = None
        ) :

        """ Returns value of attribute (s). Alias for self.value """

        return self.value( attribute )
            


    def getLists ( self ) :

        """ returns the pair of list attributes values """

        return self._attributeList, self._valueList

        
        
    def index (
        
        self,
        attribute
        ) :

        """ Returns the index of an attribute or a list of attributes

            Thows no exception

            """

        # a good, simple attribute
        
        if self.isAttribute( attribute ) :
 
            index = utilities.index( self._attributeList, attribute )

            if index < 0 : return None

            else : return index

        # a list of attributes
        
        elif self.isAttributes( attribute ) :

            indexes = []
            
            for word in attribute :
                
                if not word in self._attributeList : continue

                indexes.append( utilities.index( self._attributeList, word ) )

            return indexes

        # invalid attribute
        
        else :
            
            utilities.error = "AttributeValueList.index : Invalid attribute"

            return None



        
    def insert (
        
        self,
        attribute = None,
        value = None
        ) :

        """ Adds a pair or a list of pairs attribute-value 

            returns True if the pair(s) are in the structure after this operation

            If both arguments are None : returns True
            
            """

        # if both are none, returns True
        
        if ( ( attribute is None ) and ( value is None ) ) :
            
            utilities.error = ""
            
            return True
        
        
        # ia good pair
        
        elif self.isPair( attribute, value ) :

            # already here
            
            oldValue = self.value( attribute )

            if oldValue is None :
                

                self._attributeList.append( attribute )
                
                self._valueList.append( value )

                utilities.error = ""
                
                return True
            
            else : return oldValue == value
            

        # 2 lists of the same size, composed of valid pairs
        
        elif self.isPairs( attribute, value ) :

            result = True
            
            utilities.error = ""

            for index in range( len( attribute ) ) :

                if value[ index ] is None :
                    
                    utilities.error = "AttributeValueList.insert : undefined value"
                    
                    result = False
                    
                    continue

                oldValue = self.value( attribute[ index ] )

                # inserts if absent (WARNING: DONT use recursively self.insert, it would flatten the lists)
                
                if oldValue is None :
                    
                    self._attributeList.append( attribute[ index ] )
                    
                    self._valueList.append( value[ index ] )
                    
                # already here
                
                elif not oldValue == value[ index ] :
                    
                    utilities.error = "AttributeValueList.insert : attribute of list already here"
                    
                    result = False


            return result

        # otherwise...
        
        else :
            
            utilities.error = "AttributeValueList.insert : invalid arguments"
            
            return False


    def isAttributeValueList (
        
        self,
        attributeValueList = None
        ) :

        """ Checks whether the argument is a valid attribute-value list

            this is an object, with a list of attributes that are valid,
            a list of values that are valid
            and both lists have the same size

            """

        if attributeValueList is None : return False

        if not type( attributeValueList ).__name__ == "instance" : return False

        try :
           
            return self.isPairs( attributeValueList.attributes, attributeValueList.values ) 


        except Exception, exception :
            
            utilities.error = "AttributeValueList : not a Attribute-Value Object"
            
            return False

        

    def isAttribute (
        
        self,
        attribute = None
        ) :

        """ Checks that we have a good attribute, i.e., a non-null string """

        if not type( attribute ) == str :
            
            utilities.error = "AttributeValueList.isAttribute : non-string attribute"
            
            return False
        
        if len( attribute ) <= 0 :
            
            utilities.error = "AttributeValueList.isAttribute : empty attribute"
            
            return False

        utilities.error = ""
        
        return True

    
    
    def isAttributes (
        
        self,
        attributes = None
        ) :

        """ Checks that we have a list of good attributes, i.e., non-null strings

            Warning: repetitions of same attribute if the list are licit
            
            """

        if not type( attributes ) == list :
            
            utilities.error = "AttributeValueList.isAttributes : not a list"
            
            return False

        for attribute in attributes :

            if not self.isAttribute( attribute ) : return False

        return True
    

    def isPair (
        
        self,
        attribute = None,
        value = None
        ) :

        """ Checks that we have a good attribute-value pair.

            Attribute is a string, non-empty

            Value is not None

            """

        utilities.error = ""
        
        if not self.isAttribute( attribute ) : return False
        
        if value is None :
            
            utilities.error = "AttributeValueList.isPair : None value"
            
            return False

        utilities.error = ""
        
        return True
    


    def isPairs (
        
        self,
        attributes = None,
        values = None
        ) :

        """ Checks that we have a good list of pairs attribute-value

            These must be two lists of the same size

            Note that accepts None values (no harm done)

            No duplicate attributes

            """            

        if ( ( not type( attributes ) == list ) or ( not type( values ) == list ) ) :

            utilities.error = "AttributeValueList.isPairs : non-lists"
            
            return False

        if not len( attributes ) == len( values ) :

            utilities.error = "AttributeValueList.isPairs : lists of different sizes"
            
            return False

        # Checks that we have good pairs and
        # that if we have duplicate attributes, they have the same value
        
        for index in range( len( attributes ) ) :
            
            attribute = attributes[ index ]

            # not a good pair
            
            if not self.isAttribute( attribute ) : return False

            # duplicate with different value
            
            index1 = attributes.index( attribute )
            
            if ( ( index1 < index ) and ( not values[ index1 ] == value ) ) :
                
                utilities.error = "AttributeValueList.isPairs : duplicate attribute with different values"
                
                return False

        utilities.error = ""

        return True



    def merge (
        
        self,
        attributeValueList = None
        ) :

        """ Merges 2 LAVs """

        if not self.isAttributeValueList( attributeValueList ) : return False

        result = self.insert( attributeValueList.attributes, attributeValueList.values )

        return result


    def read (
        
        self,
        path = None,
        strict = None
        ) :

        """ Reads a file containing a list of lines, with one attribute per line (attribute) and a unique value
        
            The file is tab delimited
            
            If the value is comma separated, it is itself a list

            """

        self._attributeList, self._valueList = tableFile.readAttributeValueList(
            path = path,
            strict = strict
            )

        
        
            


    def replace (
        
        self,
        attribute = None,
        value = None
        ) :

        """ Inserts or replace pair(s). Alias for self.set  """

        result = self.set( attribute, value )
        
        return result

            

    def size ( self ) :

        """ Number of pairs """

        if not type( self._attributeList ) == list : return 0

        if not type( self._valueList ) == list : return 0

        return min( len( self._attributeList ), len( self._valueList ) )

    
    def set (
        
        self,
        attribute = None,
        value = None
        ) :

        """ Replaces a pair or a list of pairs attribute-value 
            
            Returns True if all the new pair(s) are the list after the operation

            If both arguments are None : returns True
            
            """

        # if both are none, returns True
        
        if ( ( attribute is None ) and ( value is None ) ) :
            
            utilities.error = ""
            
            return True
        
        # a good pair
        
        elif self.isPair( attribute, value ) :

            # not here

            index = utilities.index( self._attributeList, attribute )
            
            if index < 0 :
                
                self.insert( attribute, value )
                
                utilities.error = ""
                
                return True

            # already here:
            
            else :
                
                if index < len( self._valueList ) : self._valueList[ index ] = value
                
                utilities.error = ""
                
                return True
   

        # 2 lists of the same size, composed of valid pairs
        
        elif self.isPairs( attribute, value ) :

            for index in range( len( attribute ) ) :

                word = attribute[ index ]
                
                newValue = value[ index ]

                if newValue is None : continue

                # not here
                
                if not word in self._attributeList :
                    
                    self.insert( word, newValue )                
 
                # already here:
                
                else :
                    
                    index = self._attributeList.index[ word ]
                    
                    if index < len( self._valueList ) : self._valueList[ index ] = newValue

            utilities.error = ""
            
            return True               

        # otherwise...
        
        else :
            
            utilities.error = "AttributeValueList.replace : invalid arguments"
            
            return False


    def sort (
        
        self,
        criterion = None,
        order = None,
        attributes = None,
        values = None
        ) :

        """ Sorts the lists attributes, values according to the criterion and the order

            The 2 last arguments overrides the method: sorts the 2 lists instead of self._attributeList, self._valueList
            
            criterion = "attribute" (default), "value", "none"

            order = "<" increasing, ">" decreasing, or "none"

            Sort indicates whether it is sorted : by attribute (default), value or none
           
            Returns a pair of sorted lists self._attributeList, self._valueList

            """

        # sort criterion: attribute, value or none
        
        criterion = criterion.lower()

        if not criterion in [ "none", "value", "attribute" ] :

            criterion = "attribute"

        # order: increasing (>0, default) none (0) or decreasing
        
        order = order.lower()

        if not order in [ "none", ">", "<" ] :

            order = "<"

        if order == "none" : criterion = "none"
        

        # list to sort
        
        local = ( ( type( attributes ) == list ) and
                 ( type( values ) == list ) and
                 ( len( attributes ) == len( values ) ) ) 

        # takes the lists of the object
        
        if not local :
            
            attributes = self._attributeList
            
            values = self._valueList
                
        # no sort
        
        if criterion == "none" : return attributes, values

        # sort: use insertion algorithm, coz most of the time the AVL is almost sorted
        
        for rank2 in range( len( attributes ) ) :

            attribute2 = attributes[ rank2 ]
            
            value2 = values[ rank2 ]
            
            rank1 = rank2 - 1

            if criterion == "attribute" : v2 = attribute2
            
            else : v2 = value2

            while True :
                
                if rank1 < 0 : break
              
                if criterion == "attribute" : v1 = attributes[ rank1 ]
                
                else : v1 = values[ rank1 ]

                if ( ( order == "<" ) and ( v1 <= v2 ) ) : break
                
                if ( ( order == ">" ) and ( v1 >= v2 ) ) : break

                # shifts right
                
                attributes[ rank1 + 1 ] = attributes[ rank1 ]
                
                values[ rank1 + 1 ] = values[ rank1 ]
                    
                rank1 = rank1 - 1

            # inserts last element (rank2) in the place that have been freed
            
            if rank1 + 1 < rank2 :
                
                attributes[ rank1 + 1 ] = attribute2
                
                values[ rank1 + 1 ] = value2


        # not local : saves results in the lists of the object
        
        if not local :
            
            self._attributeList = attributes
            
            self._valueList = values
            
        return attributes, values


        

        
    def value (
        
        self,
        attribute
        ) :

        """ Returns the value of an attribute or a list of attributes

            Thows no exception

            """

        # a good, simple attribute
        
        if self.isAttribute( attribute ) :
 
            index = utilities.index( self._attributeList, attribute )

            if index < 0 : return None
            
            if index >= len( self._valueList ) : return None     # should not occur

            return self._valueList[ index ]

        # a list of attributes
        
        elif self.isAttributes( attribute ) :

            values = []
            
            for word in attribute :

                index = utilities.index( self._attributeList, word )
                
                if index < 0 : continue

                # warning: DONT use recursively self.value, it would flatten the list

                if index < len( self._valueList ) : values.append( self._valueList[ index ] )

            return values

        # invalid attribute
        
        else :
            
            utilities.error = "AttributeValueList.value : invalid attribute"

            return None


    def write (
        
        self,
        path = None,
        fieldDelimiter = None,
        commentDelimiter = None
        ) :

        """ Writes attributes and values to a file
        
            The file is tab delimited
            
            If the value is comma separated, it is itself a list

            """

        tableFile.writeAttributeValueList(
            path = path,
            identifiers = self._attributeList,
            values = self._valueList,
            fieldDelimiter = fieldDelimiter,
            commentDelimiter = commentDelimiter
            )

        
    
# creates the global singleton object if not already here

if not "attributeValueList" in globals() : attributeValueList = AttributeValueList()
         
        
