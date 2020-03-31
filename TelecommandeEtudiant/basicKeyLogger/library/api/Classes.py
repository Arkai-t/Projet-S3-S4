
""" Miscellaneous methods for accessing classes and instances

    """


import os



class Classes :


    """ Miscellaneous methods for accessing classes and instances

        """

    
    def attribute (

        self,
        parent,
        component
        ) :

        """ Returns the identifier of the component in parent, None if absent """

        if parent is None : return None
        
        try :
            
            names = dir( parent )

        except Exception, exception :

            names = []

        for name in names :

            if getattr( parent, name ) == component : return name

        return None


            
      


    def identifiers (

        self,
        parent = None,
        category = None,
        prefix = None,
        suffix = None,
        ) :

        """ Returns the list of identifiers of the subobjects of parent that are instances of category (may be a type, a class or a list of )

            If the class is undefined, returns the directory of the object (names of all its components)
            
            """

        if parent is None : return []
        
        if prefix is None : prefix = ""

        if suffix is None : suffix = ""

        if category is None : None

        elif not type( category ) == list : category = [ category ]

        elif len( category ) <= 0 : category = None
        
        try :
            
            names = dir( parent )

        except Exception, exception :

            names = []
            

        selected = []
        
        for name in names :

            # protected name
            
            if name.startswith( "_" ) : continue

            # checks prefix and suffix
            
            if not name.startswith( prefix ) : continue

            if not name.endswith( suffix ) : continue

            # tries to verify whether the object is an instance of someClass (exception for None objects )

            if not category is None :

                value = getattr( parent, name )
            
                try :

                    ok = max( isinstance( value, item ) for item in category )

                    if not ok : continue

                except Exception, exception :

                    continue


            # verifies all criteria
            
            selected.append( name )

        return selected



    def call (

        self,
        parent = None,
        name = None,
        arguments = None
        ) :

        """ Executes the method parent.name if it is present and callable

            returns True/False
            
            """

        method = self.value( parent, name )

        try :            

            if callable( method ) : method( arguments )

            return True

        except Exception, exception :

            return False
        

        
    def contains (

        self,
        parent = None,
        name = None
        ) :

        """ Returns the value of the attribute in parent, None if absent """

        if parent is None : return False
        

        try :            

            value = getattr( parent, name )

            return True

        except Exception, exception :

            return False


 
    def value (

        self,
        parent = None,
        name = None,
        default = None
        ) :

        """ Returns the value of the attribute in parent, None if absent """

        if parent is None : return default

        try :            

            return getattr( parent, name )

        except Exception, exception :

            return default

            

    def values (

        self,
        parent = None,
        category = None,
        prefix = None,
        suffix = None
        ) :

        """ Returns the list of identifiers of the subobjects of parent that are instances of category ( may be a type, aclass or a list of )

            If the class is undefined, returns the directory of the object (names of all its components)
            
            """

        if parent is None : return []
        
        if prefix is None : prefix = ""

        if suffix is None : suffix = ""

        if category is None : None

        elif not type( category ) == list : category = [ category ]

        elif len( category ) <= 0 : category = None
        
        try :
            
            names = dir( parent )

        except Exception, exception :

            names = []
            

        selected = []
        
        for name in names :

            # protected name
            
            if name.startswith( "_" ) : continue

            # checks prefix and suffix
            
            if not name.startswith( prefix ) : continue

            if not name.endswith( suffix ) : continue

            value = getattr( parent, name )
            

            # tries to verify whether the object is an instance of someClass (exception for None objects )

            if not category is None :
            
                try :

                    ok = max( isinstance( value, item ) for item in category )

                    if not ok : continue

                except Exception, exception :

                    continue


            # verifies all criteria
            

            selected.append( getattr( parent, name ) )

        return selected







                
                

            
        
