

""" Interface with Context, Typed files and directories management


    """


import os 

import glob

import time

from api.Files import *

from api.PathNames import *

from api.Texts import *



class Items ( Files, PathNames, Texts ) :


    """ Interface with Context, Typed files and directories management

        """



    def archivedDataDirectory (

        self,
        path = None
        ) :

        """ Returns the directory that contains the  archives execution data of some object ( normally a procedure) """

        directory = self.localDirectory( path )

        if self.isEmpty( directory ) : return None

        return directory + "__data"

    

    def backupsDirectory (

        self,
        path = None
        ) :

        """ Returns the directory that contains the local archives of the item """


        if path is None : return None

        path = self.normalizePath( path, normalize = False )

        directory = self.pathDirectory( path )

        # name with heading __ removed
        
        name = self.pathLastNameWithoutExtension( path ).strip( "_" )

        resultPath = directory + os.sep + "__" + name + os.sep 

        return self.normalizePath( resultPath )



    def dataDirectory (

        self,
        path = None
        ) :

        """ Returns the directory that contains the execution data of the item ( normally a procedure ) """


        directory = self.localDirectory( path )

        if self.isEmpty( directory ) : return None

        return directory + "data" + os.sep



    def executionDataDirectory (

        self,
        script = None,
        procedure = None,
        selected = None
        ) :

        """ determines the execution data directory of 'procedure' on 'selected' item.

            normally it is _selected/procedures/_procedure's name/data/

            if the script is 'execute.pyw' or 'tutorial.pyw', does not alter the name of the procedure

            otherwise ( pop.pyw,  wizard.pyw...) takes 'main' as the procedure's name

            if there is no selected item, the data directory is _procedure/data/

            if nothing is defined, the data directory is ""

            """

        # local directory (means that there is a selected item)
        

        # there is a selected item: data is in _selected/procedures/_xxxx/data/

        if not self.isEmpty( selected ) :
            
               
            # normalizes name for FTK doc procedures 

            if ( ( script == "pop" ) or ( script == "wizard" ) ) : name = "main"

            elif utilities.isEmpty( procedure ) : name = "main"

            else : name = self.pathLastNameWithoutExtension( procedure )

            directory = self.localDirectory( selected ) + "procedures" + os.sep 
            
            dataDirectory = self.dataDirectory( directory + name )

        
        # no selected item : data directory is _procedure/data/

        elif not self.isEmpty( procedure ) :

            directory = self.pathDirectory( procedure )

            # normalizes name for all the standard procedures

            if ( ( script == "pop" ) or ( script == "wizard" ) ) :

                procedure = self.pathDirectory( procedure ) + "main"

            dataDirectory = self.dataDirectory( procedure )

        else :

            dataDirectory = ""

##        # determines local directory
##        
##        if ( ( self.isEmpty( local ) ) and ( not self.isEmpty( selected ) ) ) :
##
##            local = self.localDirectory( selected )
##        
##
##        if ( ( not self.isEmpty( procedure ) ) and ( not self.isEmpty( local ) ) ) :
##
##            # normal procedure called with execute.pyw, data in in _selected/procedures/_thisProcedure/
##            
##            if ( ( script == "execute" ) or ( script == "tutorial" ) ) : procedureName = self.pathLastName( procedure )
##
##            # main procedures called with wizard.pyw or pop.pyw, data is always in _selected/procedures/_main/
##
##            else : procedureName = "main"
##            
##            # data directory is .../procedures/_name/data/
##            
##            dataDirectory = self.dataDirectory( local + os.sep + "procedures" + os.sep + procedureName )
##
##        # no selected item, takes _procedure/data/
##        
##        elif not self.isEmpty( procedure ) :
##
##            dataDirectory = self.dataDirectory( procedure )
##
##        # nothing is defined, procedure nor selected item
##        
##        else :
##
##            dataDirectory = ""

        return dataDirectory
        
        


    def localDirectory (

        self,
        path = None
        ) :

        """ Returns the directory that contains the local archives of the item """

        if path is None : return None

        path = self.normalizePath( path, normalize = False )

        directory = self.pathDirectory( path )

        name = self.pathLastNameWithoutExtension( path )

        name = name.lstrip( "_" )

        resultPath = directory + os.sep + "_" + name + os.sep 

        return self.normalizePath( resultPath )


    
    def checkFileExtension (
        
        self,
        path = None,
        extensions = None
        ) :

        """ Checks whether the path has a given extension (defined from a list, or directly, as a string )

            If extension is a string, it is converted into [ extension ]

            Case insensitive.

            Default extension is "" """

        # no file
        
        if path is None : return False

        # list of allowed extension: default is empty list
        
        if extensions is None : extensions = [ "" ]

        elif type( extensions ) == str : extensions = [ extensions ]

        elif len( extensions ) <= 0 : extensions = [ "" ]
        
        # gets the extension of the file
        
        text = self.pathExtension( path )

        # loop on allowed extensions
        
        for extension in extensions :

            # removes (eventual) initial point
            
            if extension.startswith( "." ) : extension = extension[ 1 : ]

            if text.lower() == extension.lower() : return True

        return False


        
    def checkFilePrefix (
        
        self,
        path = None,
        prefixes = None,
        header = None
        ) :

        """ Checks whether the path' last name has a given prefix (defined from a list, or directly, as a string )

            header is a string that may eventually precede the prefix, e.g., procedureUsers...

            NOTE: header is optional in the file names

            Case insensitive.

            Default prefix is ""

            """

        # no file:
        
        if path is None : return False

        
        # list of allowed prefixes : default is empty list
        
        if self.isEmpty( prefixes ) : return True

        elif not type( prefixes ) == list : return False

        index = self.getFilePrefixIndex( path, prefixes, header )

        return ( index >= 0 )
        



##    def deliveryList (
##
##        self,
##        format = "path"
##        ) :
##
##        """ List of deliveries for all projects
##
##            Complete if a flag that means that projects are included
##
##            Format is the type of result "path" = full path, "project" = project + delivery
##            otherwise it is the format of the path's name
##
##            """
##
##
##
##        deliveryList = []
##
##        # list of projects
##        
##        projectList = self.projectList()
##
####        typeProjectIndex = self.findTypeIndex( name = "project", category = "directory" )
##
##        for project in projectList :
##
##            items = self.directoryPaths( project, recursive = False, reserved = 2 )
##            
##            for item in items :
##
##                # not a directory
##
##                if not item.endswith( os.sep ) : continue
##
####                if not self.pathCategory( item, parent = typeProjectIndex ).startswith( "delivery" ) : continue
##
##                # full paths
##                
##                if format == "path" :
##
##                    text = item
##
##                # project + delivery
##
##                elif format == "slashtitle" :
##
##                    text = self.string( item, format = "slashtitle" )
##
##                # names, only deliveries.
##                
##                else :
##
##                    text = self.string( self.pathLastName( item ), format = format )
##
##                deliveryList.append( text )
##
##            
##
##        return deliveryList
##

        

    def directoryFilesOfType (

        self,
        directory = None,
        pattern = None,
        parent = None
        ) :

        """ Returns the list of files of a directory that match the type "pattern"

            Parent is the parent's directory type, if known
            
            """

        if directory is None : directory = os.curdir

        items = self.directoryFiles( directory )

        files = [ ]

        for item in items :

            if self.matchType(
                item,
                pattern = pattern,
                parent = parent ) >= 0 :

                files.append( item )

        return files



        
    
    def entryListPath (

        self,
        name = None,
        ) :

        """ Returns a path to a file containing options for a popup menu,../electronicForms/common/entry-Name.txt

            """


        if self.context is None : return None

        try :


            name = self.string( name, format = "strictunderscore", default = "None" )

            if not name.startswith( "entry_" ) : name = "entry_" + name

            if name.endswith( "_txt" ) : name = name[ : - len( "_txt" ) ]

            name = name.strip ( " _" )

            name = name + ".txt"

            return self.normalizePath( sys.configurationPath + os.sep + name, normalize = False )

        except Exception, exception :

            return None
        

    
    def entryList (

        self,
        name = None,
        instantiate = False
        ) :

        """ Returns a list of option for an popup menu, contained in file ../electronicForms/common/entry-Name.txt

            If the name is a path, takes its title ( e.g., \a\b\c\entry-toto.txt -> toto )
            
            """

        # takes the last part of the name
        
        name = self.pathTitle( name )

        # builds a path to electronicForms/common/entry-*.txt

        path = self.entryListPath( name )

        # reads

        text = self.fileRead( path )

        if bool( instantiate ) : text = self.instantiate( text, default = "" )

        return self.asciiToLines( text )



    def filterOwners (

        self,
        items = None,
        owners = None,
        header = None
        ) :

        """ Returns a filtered list woth items corresponding to owners and having a given header """

        if items is None : return [ ]
        
        # checks all configuration directories

        files = [ ]
        
        for item in items :

            if not self.checkFilePrefix(
                item,
                prefix = owners,
                header = header) : continue

            files.append( item )

        return files

        


    def getFilePrefix (
        
        self,
        path = None,
        prefixes = None,
        header = None,
        default = ""
        ) :

        """ Gets the prefix of a file from a list

            case insensitive.

            Returns "" if prefix not in list

            Default prefix is "" """

        index = self.getFilePrefixIndex( path, prefixes, header )

        if index < 0 : return default

        else : return prefixes[ index ]



    def getFilePrefixIndex (
        
        self,
        path = None,
        prefixes = None,
        header = None
        ) :

        """ Returns the index of the prefix of a file in a list

            Header is an optional header, before prefix **EF

            case insensitive.

            Returns -1 if prefix not in list

            Default prefix is "" """

        # no file
        
        if path is None : return -1

        # normalizes header
        
        if self.isEmpty( header ) : header = ""

        else : header = self.string( header, format = "lower" )
        
        
        # normalizes list of prefixes 
        
        if self.isEmpty( prefixes ) : return -1

        elif type( prefixes ) == str : prefixes = [ prefixes ]

        elif not type( prefixes ) == list : return -1
        

        # gets the file name
        
        name = self.pathLastNameWithExtension( path ).lower()

        # loop on allowed prefixes
        
        for index in range( len( prefixes ) ) :
           
            if name.startswith( header + prefixes[ index ].lower() ) : return index

            if name.startswith( prefixes[ index ].lower() ) : return index

        return -1





        
        
    def getType (

        self,
        identifier = None,
        strict = True,
        backwards = False
        ) :

        """ Gets a type (new types) from its identifier.

            identifier can be an index, a TypeNode object ( returns this object ), or a string

            reference is a bibtex category

            if strict is True, looks for a type with this name, else looks for a type that corresponds to the prefix
            
            Returns a TypeNode object or None

            """


        if self.context is None : return None

        try :

            return self.context.getType(
                identifier = identifier,
                strict = strict,
                backwards = backwards
                )

        except Exception, exception :

            return None
    



       

    
    def getTemplate (

        self,
        text = None
        ) :

        """ Returns the template corresponding to the text ( description ), i.e., a path

            Searches a template with this description in self.template*List
            Returns None in case of problems

            """

        if self.context is None : return None

        try :

            return self.context.getTemplate( text = text )

        except Exception, exception :

            return None


    def isProcedure (

        self,
        path = None
        ) :

        """ returns True iff the path is a procedure

            - directory
            - parent = procedures* OR
            - name = procedure* OR
            - contains execute.pyw

            """

        if self.isEmpty( path ) : return False

        if not path.endswith( os.sep ) : return False

        directory = self.pathDirectory( path )

        parent = self.pathName( directory )

        name = self.pathName( path )

        if name.startswith( "procedure_" ) : return True

        if parent.startswith( "procedures"  ) : return True

        if self.filePresent( path + "execute.pyw" ) : return True

        return False
        

    def isType (

        self,
        identifier = None,
        ) :

        """ Returns true iff identifier is a type (name, index or object) """


        if self.context is None : return False

        try :

            return self.context.isType( identifier = identifier )

        except Exception, exception :

            return False
    
            
        
    def parseDirectoryName (
        
        self,
        path = None,
        prefixes = None
        ) :
        
        """ Parses the name of "path" and returns its prefix (e.g., libPython), name and date

            By default looks for the prefix in the list of phases (libPython, exp, study...)

            The argument prefixes overrides the standard prefixes, e.g., developments instead of phases.

            If path is a single name, takes this name

        """
        
        if path is None : return None, None, None

        # gets the name of current directory
        
        remainder, name = os.path.split( path )
        
        if len( name ) <= 0 : name = remainder

        # removes standard prefix ( "" if present)
        
        prefix = self.getFilePrefix(
            name,
            prefixes = prefixes )
        
        # removes prefix
        
        name = name[ len( prefix ) : ]
        
        # takes date as 8 last digits
        
        date = ""
        
        if name[ -8 : ].isdigit() :
            
            date = name[ -8 : ]
            
            name = name[ : -8 ]

        # removes final and initial "-"
        
        name = name.strip('-')

        return prefix, name, date




    def pathCategory (

        self,
        path = None,
        index = None,
        reserved = None,
        parent = None
        ) :

        """ Returns the category of the path, under the form of a prefix """

        if self.isEmpty( path ) : return "none"

        elif path.endswith( os.sep ) : return "directory"

        else : return "file"
        

    def pathTimeBackuped (

        self,
        path = None
        ) :

        """ time of last backup of the path """

        backupsDirectory = self.backupsDirectory ( path )

        if self.isEmpty( backupsDirectory ) : return 0

        else : return self.fileTimeModified( backupsDirectory + "date.txt" )

    

    def popVariable (

        self,
        identifier = None
        ) :

        """ Gets the previous value of a variable, does nothing if there is none

            if argument is a list, pops all the variables contained in the list

            returns True if popped something, False otherwise (for a list, True is popped all )
            
            """

        if self.context is None : return None

        try :
            
            return self.context.popVariable( identifier )

        except Exception, exception :

            return None


    def popVariables (

        self,
        variableList = None
        ) :

        """ Gets the previous value of a list of variables, does nothing if there is none

            returns True if popped all, False otherwise
            
            """

        if self.context is None : return None

        try :
            
            return self.context.popVariables( variableList )

        except Exception, exception :

            return None


    def procedureDirectory (

        self,
        path = None
        ) :

        """ Returns the procedure that contains path """

        if path is None : return None

        path = self.normalizePath( path, normalize = False )

        while True :

            if self.isProcedure( path ) : return path

            directory = self.pathDirectory( path )

            if directory == path : break

            path = directory

        # not found
        
        return None



    def proceduresDirectory (

        self,
        path = None
        ) :

        """ Returns the local procedures directory.

            If the path is .../procedures, path itself, otherwise local/procedures/

            """

        if path is None : return None

        path = self.normalizePath( path, normalize = False )

        if self.pathLastNameWithExtension( path ) == "procedures" : return path

        local = self.localDirectory( path )

        if self.isEmpty( path ) : return None

        return local + "procedures" + os.sep



    def pushVariable (

        self,
        identifier = None
        ) :

        """ Pushes the value of context.identifierValue, i.e., adds it to the list context.identifierPrevious

           if argument is a list, pushes all the variables contained in the list

            returns True if could push, False otherwise (for a list, True iff pushed all )
            
            """

        if self.context is None : return None

        try :

            return self.context.pushVariable( identifier )

        except Exception, exception :

            return None


    def pushVariables (

        self,
        variableList = None
        ) :

        """ Pushes the value of a list of variables

            returns True if pushed all, False otherwise
            
            """

        if self.context is None : return None

        try :

            return self.context.pushVariables( variableList )

        except Exception, exception :

            return None



    def readVariables (

        self,
        path = None,
        text = None,
        instantiate = None,
        push = None
        ) :

        """ Reads the context variables from a file (default = ../_persistence/context.txt ) or a text buffer

            if instantiate is True. variables are instantiated e.g., file contains toto,(user) -> toto=current user

            if push is true, previous values of variables are stored

            returns the list of identifiers of variables that were read
                       
            
            """

        if self.context is None : return None

        try :

            return self.context.readVariables(
                path = path,
                text = text,
                instantiate = instantiate,
                push = push
                )

        except Exception, exception :

            return None


    def selectedDirectory (

        self,
        path = None
        ) :

        """ Returns the selected directory (selectedValue), assuming that we are somewhere in the local directory """

        if path is None : return None

        path = self.normalizePath( path, normalize = False )

        # the path itself may be the selected object
        
        if path.endswith( os.sep ) : result = path

        else : result = None

        while True :

            directory = self.pathDirectory( path )

            if directory == path : break

            name = self.pathName( path )

            # with a subdirectory  "_x" , name to find is "x" and the result cannot be the original path itself

            if name.startswith( "_" ) :

                name = name.lstrip( "_" )

                result = None

            # we are in .../_x/, looks for .../x*.*
                
            items = self.directoryContent( directory, annotate = True )

            for item in items :

                # first, tries the directory ../x/
            
                if item == name + os.sep  : return directory + item

                # then , if there is an item ../x*.*, returns the directory itself

                if self.pathLastNameWithoutExtension( item ) == name : return directory + item

            path = directory

        # not found, but the path itself does not contain "_" : it may be the selected object
        
        return result



    def selectedPath (

        self,
        path = None
        ) :

        """ Returns the selected object (selectedValue), assuming that we are somewhere in the local directory """

        if path is None : return None

        path = self.normalizePath( path, normalize = False )

        # the path itself may be the selected object
        
        if path.endswith( os.sep ) : result = path

        else : result = None

        while True :

            directory = self.pathDirectory( path )

            if directory == path : break

            name = self.pathName( path )

            # with a subdirectory  "_x" , name to find is "x" and the result cannot be the original path itself

            if name.startswith( "_" ) :

                name = name.lstrip( "_" )

                result = None

            # we are in .../_x/, looks for .../x*.*
                
            items = self.directoryContent( directory, annotate = True )

            for item in items :

                # tries the name itself

                if item == name : return directory + item

                # first, tries the directory ../x/
            
                if item == name + os.sep  : return directory + item

                # then , if there is an item ../x*.*, returns the directory itself

                if self.pathLastNameWithoutExtension( item ) == name : return directory + item


            path = directory

        # not found, but the path itself does not contain "_" : it may be the selected object
        
        return result




    def typeDirectory (

        self,
        index = None
        ) :

        """ Returns the directory of creation of the type of objects "index" """

        if self.context is None : return None

        try :
            
            return self.context.typeDirectory( index )
    
        except Exception, exception :

            return None

        

    def updateVariables ( self ) :

        """ Updates dependent variables """

        if self.context is None : return 

        try :
            
            self.context.updateVariables()

        except Exception, exception :

            return None

        


    def writeVariables (

        self,
        path = None,
        text = None
        ) :

        """ Writes the variables to a file ( default is ../persistence/context.txt ) or into a text buffer of tableFile

            returns the list of identifiers of variables that were written
            
            """

        if self.context is None : return None

        try :
            
            return self.context.writeVariables(
                path = path,
                text = text
                )

        except Exception, exception :

            return None
    
        
        






