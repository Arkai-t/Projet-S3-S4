
""" Types of files and directories managed by the system """


import sys

from api.Utilities import *

from api.TypeNode import *




class Types :


    """ Types of files and directories managed by the system """


    # loads standard file, then tries the redefined file and if fails, reloads original

    from type_configuration import *

    try :

        from configuration.type_configuration import *

    except Exception, exception :

        from type_configuration import *

    
    # templates 

    templateList = None   

    # list of type objects

    typeList = None



    def getTemplate (

        self,
        text = None
        ) :

        """ Returns the template corresponding to the text ( description ), i.e., a path

            Searches a template with this description in self.template*List
            Returns None in case of problems

            """

        if utilities.isEmpty( text ) : return None

        # not loaded yet
        
        if not type( self.templateList ) == list : return None


        for item in self.templateList :

            if utilities.pathDescription( item, format = "split" ) == utilities.pathDescription( text, format = "split" ) :

                return item


        return None


        
    def getType (

        self,
        identifier = None,
        strict = True,
        backwards = False
        ) :

        """ Gets a type (new types) from its identifier 

            identifier can be an index, a TypeNode object ( returns this object ), or a string

            if strict is True, looks for a type with this name, else looks for a type that corresponds to the prefix

            backwards = True iff ... well.
            
            Returns a TypeNode object or None

            """

        if utilities.isEmpty( self.typeList ) : return None

        if isinstance( identifier, TypeNode ) : return identifier

        if utilities.isIndex( identifier, self.typeList ) : return self.typeList[ identifier ]

        identifierFlag = not utilities.isEmpty( identifier )

        if not identifierFlag  : return None

        # goes forward or backwards
        
        if bool( backwards ) : itemList = reversed( self.typeList )

##            *EF 2009 04 18
##            
##            itemList = self.typeList
##
##            itemList.reverse()

        else : itemList = self.typeList

        for item in itemList :

            if item is None : continue

            elif bool( strict ) :

                if not item.identifier == identifier : continue

            else :

                if not identifier.startswith( item.identifier ) : continue

            return item

        return None





    def isType (

        self,
        identifier = None
        ) :

        """ returns true iff the identifier is a type """

        if utilities.isEmpty( self.typeList ) : return False

        if isinstance( identifier, TypeNode ) : return True

        if utilities.isEmpty( identifier ) : return False

        for item in self.typeList :

            if item is None : continue

            if item.identifier == identifier : return True

        return False
        
    

    def loadTypes ( self ) :

        """ Loads new types """

        self.typeList = [ ]

        index = 0

        for item in dir( self ) :

            if item.startswith( "_" ) : continue

            if not item.endswith( "Type" ) : continue

            value = getattr( self, item )

            if not type( value ) == list : continue

            if len( value ) < 2 : continue
            
            identifier = utilities.string( value[ 0 ], format = "lower" )

            description = utilities.string( value[ 1 ] )

            self.typeList.append(
                TypeNode(
                    index = index,
                    identifier = identifier,
                    description = description
                    )
                )

            index = index + 1


        # writes list of types for popups

        self.writeTypeChoiceList( path = utilities.entryListPath( "type" ) )
        
        # reads the templates for the files, directories and procedures

        self.templateList = self.readTemplates()

        # writes list of templates for popups

        self.writeTemplateList(
            path = utilities.entryListPath( "template" ),
            templates = self.templateList
            )
        
        

        
    def readTemplates ( self ) :

        """ Reads the templates of a given category, file, directory, procedure """

        items = utilities.directoryPaths(
            self.typesPath,
            recursive = False,
            reserved = 1    # removes items with reserved name, but works in reserved directories
            )


        return items

        

        








    def writeTemplateList (

        self,
        path = None,
        templates = None
        ) :

        """ Writes the list of the available templates for a given category, file, directory, procedure... """

        if utilities.isEmpty( path ) : return

        if utilities.isEmpty( templates ) : return

        text = ""
        
        for template in templates :

            if template is None : continue
           
            text = text + utilities.pathDescription( template ) + "\n"
            
        if not utilities.fileRead( path ) == text : utilities.fileWrite( path, text )
        
            



    def writeTypeChoiceList (

        self,
        path = None,
        ) :

        """ Writes the list of types (simplified format) for popup choices """

        if utilities.isEmpty( path ) : return

        if utilities.isEmpty( self.typeList ) : self.typeList = []

        text = ""
        
        for item in self.typeList :

            if item is None : continue

            text = text + \
                   utilities.string( item.identifier, default = "" ) + \
                   " (" + \
                   utilities.string( item.description, default = "" ) + \
                   ")" + "\n"

        # writes only if it is different of current list ( avoids changing time of modification at each run )

        if not utilities.fileRead( path ) == text : utilities.fileWrite( path, text )
        
            

        
        
