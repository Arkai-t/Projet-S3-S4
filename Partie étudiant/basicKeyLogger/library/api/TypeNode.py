""" Object representing a type of files or directories
 
    """


from api.Utilities import *

            
class TypeNode :

    """ Object representing a type of files or directories """

    # can be backuped

    backupFlag = None

    # components, i.e., types that can be created inside this one

    componentList = None

    # can be deleted or not

    deleteFlag = None

    # description

    description = None

    # places of items
    
    directoryList = None

    # expandable or not

    expandFlag = None

    # extensions of items
    
    extensionList = None

    # can go to directory or not

    gotoFlag = None
    
    # index of this type in the array

    index = None

    # path to installer file
    
    installer = None

    # identifier
    
    identifier = None

    # can create components

    newFlag = None
    
    # can be opened or not

    openFlag = None

    # prefixes of items
    
    prefixList = None

    # can be renamed

    renameFlag = None


    
    def __init__(
        
        self,
        index = None,
        identifier = None,
        installer = "",

        description = None,

        componentList = [],
        directoryList = [],
        extensionList = [],
        prefixList = [],

        backup = None,
        delete = None,
        expand = None,
        goto = None,
        new = None,
        open = None,
        rename = None,
        ) :

        

        """ Constructor.

            """

        self.set(
            index = index,
            identifier = identifier,
            installer = installer,

            description = description,

            componentList = componentList,
            directoryList = directoryList,
            extensionList = extensionList,
            prefixList = prefixList,

            backup = backup,
            delete = delete,
            expand = expand,
            goto = goto,
            new = new,
            open = open,
            rename = rename,
            ) 
            

        
        # initializes data with default values


    def get ( self ) :

        """  Returns a n-uple with all values """


        return self.index, \
               self.identifier, \
               self.installer, \
               self.componentList, \
               self.directoryList, \
               self.extensionList, \
               self.prefixList, \
               self.backupFlag, \
               self.gotoFlag, \
               self.deleteFlag, \
               self.expandFlag, \
               self.newFlag, \
               self.openFlag, \
               self.renameFlag, \

    


    def set (

        self,
        index = None,
        identifier = None,
        installer = None,

        componentList = None,
        directoryList = None,
        extensionList = None,
        prefixList = None,

        description = None,

        backup = None,
        delete = None,
        expand = None,
        goto = None,
        new = None,
        open = None,
        rename = None,
        ) :

        """ Replaces the data of the node with new values

            Index may be a text, searched in self.textList

            """


        if type( index ) == int : self.index = int( index )

        if not identifier is None : self.identifier = utilities.string( identifier )
        
        if not installer is None : self.installer = installer # DO NOT NORMALIZE, may be ""
             
        if type( componentList ) == list : self.componentList = componentList

        if type( directoryList ) == list : self.directoryList = directoryList

        if type( extensionList ) == list : self.extensionList = extensionList

        if type( prefixList ) == list : self.prefixList = prefixList

        backup = utilities.integer( backup )

        if not backup is None : self.backupFlag = bool( backup )
        
        delete = utilities.integer( delete )

        if not delete is None : self.deleteFlag = bool( delete )
        
        goto = utilities.integer( goto )

        if not goto is None : self.gotoFlag = bool( goto )
        
        expand = utilities.integer( expand )

        if not expand is None : self.expandFlag = bool( expand )
        
        new = utilities.integer( new )

        if not new is None : self.newFlag = bool( new )
        
        open = utilities.integer( open )

        if not open is None : self.openFlag = bool( open )
       
        rename = utilities.integer( rename )

        if not rename is None : self.renameFlag = bool( rename )
       
        # description of the type

        if not description is None : self.description = utilities.string( description )
        

        

        
