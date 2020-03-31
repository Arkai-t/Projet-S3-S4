""" Contains the standard formal variables.

    These variables are used for instance in templates.

    In files or file names, they are noted (x).

    In the scripts, variables are identified as context.xxxVariable, e.g., context.nameVariable

    Variables may be overwritten from a file (eventually new variables may be added)


    """


import os

from api.Utilities import *

from api.Clock import *

from api.TableFile import *



class Variables :


    """ Contains the standard formal variables.

        These variables are used for instance in templates.

        In files or file names, they are noted (x).

        In the scripts, variables are identified as context.xxxVariable, e.g., context.nameVariable

        Variables may be overwritten from a file (eventually new variables may be added)

            """

    # loads standard, then tries the redefined file and if fails, reloads original

    from variable_configuration import *

    try :

        from configuration.variable_configuration import *

    except Exception, exception :

        from variable_configuration import *


    # list of patterns

    patternList = None

    # work variable to detect changes in selected object

    selected = None

    # list of variables associated to current selection

    selectedList = None
    
    # list of variables
    
    variableList = None

    # prefixes of variables

    variablePrefixList = [
        "__",   # backups directory
        "_",    # local directory
        "1_",   # first word
        "-1_",  # last word
        "c_",   # class format capitalized no spaces
        "d_",   # directory of a path
        "e_",   # extension of a path
        "f_",   # content of a file (all lines)
        "fl_",  # content of a file (last line)
        "i_",   # identifier format, no spaces
        "in_",  # initials (for path, of name)
        "l_",   # lower case
        "l1_",  # uncapitalized, 1 letter lower case remainder unchanged
        "n_",   # name of a path
        "ne_",  # name and extension of a path
        "s_",   # sentence, words, 1st capitalized
        "t_",   # title, capitalized words
        "u_",   # upper case
        "ut_",  # upper case words
        "u1_",  # capitalized, 1 letter upper case remainder unchanged
        "uu_",  # underscored-separated words
        ]

    




    def clearSelected ( self ) :

        """ Clears variables that depends on selectedValue """

        for variable in self.selectedList :

            self.setVariable( variable, "" )

        
        
    def completeVariables ( self ) :

        """ Adds an attributes self.xValue for each self.xVariable """


        attributes = self.variableList

        # selects strings whose name ends with "Variable"
        
        for index in range( len( self.variableList ) ) :

            attribute = self.variableList[ index ]

            value = self.patternList[ index ]

            # this is a variable. Reads its pattern and adds NameVariable and name_Variable
            
             # looks for  1st letter case letter in pattern
            
            iLetter = 0

            for iLetter in range( len( value ) ) :

                if value[ iLetter ].isalpha() : break

            # pattern contains no alphabetical : no way of capitalizing the pattern or creating an underscored pattern

            if iLetter >= len( value ) : continue
            

            # capitalized name
            
            # capitalized pattern, only if 1st letter is is lower case

            if not value[ iLetter ].isupper() :
              
                self.loadVariable(
                    attribute[ 0 ].upper() + attribute[ 1 : ],
                    value[ : iLetter ] + value[ iLetter ].upper() + value[ iLetter + 1 : ]
                    )


            # upper case pattern, only if not already in upper case

            if not value.isupper() :

                self.loadVariable(
                    attribute.upper(),
                    value.upper()
                    )

            # creates patterns for all possible prefixes

            for prefix in self.variablePrefixList :

                if not value.startswith( "(" + prefix ) :
                    
                    self.loadVariable(
                        prefix + attribute,
                        "(" + prefix + value[ 1 : ]
                        )

        # list of variables that depends on current selection
        
        self.selectedList = [
            "author",
            "description",
            "shared",
            "title",
            "type",
            "year",
            ]


    def getPattern (

        self,
        attribute = None,
        default = ""
        ) :

        """ Gets the pattern of variable "attribute"

            Method accepts simple names , e.g., "user", or complete names, "userValue"

            Returns None if absent

            """

        if type( attribute ) == int :

            if utilities.isIndex( attribute, self.patternList ) : return self.patternList[ attribute ]

            else : return default

        if utilities.isEmpty( attribute ) : return default

        # attribute already ends with "Value", determines its name ( string before suffix )

        if attribute.endswith( "Value" ) : attribute = attribute[ : -len( "Value" ) ]

        # not in variable list ? no pattern

        if utilities.isEmpty( self.variableList ) : return default

        if utilities.isEmpty( self.patternList ) : return default

        index = utilities.index( self.variableList, attribute )

        if index < 0 : return default

        else : return self.patternList[ index ]





        
    def getVariable (

        self,
        attribute = None,
        default = ""
        ) :

        """ Gets the value of variable "attribute"

            Method accepts simple names , e.g., "user", or complete names, "userValue"

            Returns None if absent

            """

        if type( attribute ) == int :

            if not utilities.isIndex( attribute, self.variableList ) : return default

            attribute = self.variableList[ attribute ]

            
        if utilities.isEmpty( attribute ) : return default

        # attribute already ends with "Value", determines its name ( string before suffix )

        if attribute.endswith( "Value" ) : attribute = attribute[ : -len( "Value" ) ]


        # format of variable
        
        prefix = utilities.prefix( attribute, self.variablePrefixList )

        if not utilities.isEmpty( prefix ) :

            attribute = attribute[ len( prefix ) : ]

        
        # is it upper ?

        elif attribute.isupper() :

            prefix = "ut_"

            attribute = attribute.lower()

            # patch: upper case: finds a variable that may match ( e.g., ELECTRONICFORMS electronicForms )

            for item in self.variableList :

                if item.lower() == attribute :

                    attribute = item

                    break
            

        elif attribute[ 0 ].isupper():

            prefix = "t_"

            attribute = attribute[ 0 ].lower() + attribute[ 1 : ]
        

        # no name  ( e.g., pure suffix ) : nothing to do

        if len( attribute ) <= 0 : return default
        
            
        try :

            value = getattr( self, attribute + "Value" )

            # date untouched
            
            if attribute == "date" :

                value = clock.today()

                self.dateValue = value

            # elapsed time

            elif attribute == "elapsed" :

                value = clock.secondsToString( clock.timeS() - clock.startS )

                self.elapsedValue = value
        
            # time untouched
            
            elif attribute == "time" :

                value = clock.hour()

                self.timeValue = value

            # empty string

            elif utilities.isEmpty( value ) : value = ""

            # 1st word

            elif prefix == "1_" :
 
                  value = utilities.split( utilities.pathLastName( value ) )

                  value = utilities.textToWords( value )

##                  print "variables getvariable 1_", value

                  if len( value ) > 0 : value = value[ 0 ].lower()

                  else : value = ""

            # last word

            elif prefix == "-1_" :
 
                  value = utilities.split( utilities.pathLastName( value ) )


                  value = utilities.textToWords( value )

##                  print "variables getvariable -1_", value


                  if len( value ) > 0 : value = value[ -1 ].lower()

                  else : value = ""

            # capitalized simple
            
            elif prefix == "c_" : value = utilities.string( utilities.pathLastName( value ), format = "class" )
            
            # directory of a path
            
            elif prefix == "d_" : value = utilities.pathDirectory( value )
            
            # extension of a path
            
            elif prefix == "e_" :

                if value.endswith( os.sep ) : value = os.sep

                else : value = "." + utilities.pathExtension( value )

            # content of a file, all lines

            elif prefix == "f_" :

                value = utilities.fileRead( value )

                if utilities.isEmpty( value ) : value = ""

                
            # content of a file, last line

            elif prefix == "fl_" :

                value = utilities.fileRead( value )

                if utilities.isEmpty( value ) : value = ""

                else : value = value.strip( " \t\n" )

                if "\n" in value : value = value[ value.rfind( "\n" ) + 1 : ]
            
            # identifier
            
            elif prefix == "i_" : value = utilities.string( utilities.pathLastName( value ), format = "identifier" )

            # initials

            elif prefix == "in_" :

##                print "Variables getvariable in", value

                value = utilities.string( utilities.pathLastName( value ), format = "initials" )
            
            # lower
            
            elif prefix == "l_" : value = utilities.string( utilities.pathLastName( value ), format = "lower" )

            # uncapitalized

            elif prefix == "l1_" : value = utilities.string( utilities.pathLastName( value ), format = "uncapitalize" )

          
            # name of a path, without extension
            
            elif prefix == "n_" : value = utilities.pathLastNameWithoutExtension( value )

            # name of a path, includes extension
            
            elif prefix == "ne_" :

                isDirectory = value.endswith( os.sep )

                value = utilities.pathLastNameWithExtension( value )

                if isDirectory : value = value + os.sep

            # sentence
            
            elif prefix == "s_" : value = utilities.string( utilities.pathLastName( value ), format = "sentence" )

            # capitalized
            
            elif prefix == "t_" : value = utilities.string( utilities.pathLastName( value ), format = "title" )

            # upper prefixed

            elif prefix == "u_" : value = utilities.string( utilities.pathLastName( value ), format = "upper" )

            # capitalized

            elif prefix == "u1_" : value = utilities.string( utilities.pathLastName( value ), format = "capitalize" )

            # upper capitalized

            elif prefix == "ut_" : value = utilities.string( utilities.pathLastName( value ), format = "title" ).upper()

            # title underscore-separated

            elif prefix == "uu_" : value = utilities.string( utilities.pathLastName( value ), format = "underscore" )
            
            # local path of variable
            
            elif prefix == "__" : value = utilities.backupsDirectory( value )

            # local path of variable
            
            elif prefix == "_" : value = utilities.localDirectory( value )
            
            if ( ( utilities.isEmpty( value ) ) or ( value == utilities.voidCode ) ) : value = default         

        except Exception, exception :

            value = default

        return value




    def isPattern (

        self,
        attribute = None
        ) :

        """ Returns true iff the attribute is the pattern of some variable """

        if utilities.isEmpty( attribute ) : return False

        return attribute in self.patternList

        
        
    def isVariable (

        self,
        attribute = None,
        ) :

        """ Returns True iff the attribute is a variable name

            Method accepts simple names , e.g., "user", or complete names, "userValue"

            Returns None if absent

            """

        if utilities.isEmpty( attribute ) : return False

        # attribute already ends with "Value", determines its name ( string before suffix )

        if attribute.endswith( "Value" ) : attribute = attribute[ : -len( "Value" ) ]



        # checks prefix
        
        prefix = utilities.prefix( attribute, self.variablePrefixList )

        if not utilities.isEmpty( prefix ) : attribute = attribute[ len( prefix ) : ]


        # is it upper ?

        elif attribute.isupper() : name = attribute.lower()

        # it is capitalized ?
        
        elif attribute[ 0 ].isupper(): attribute = attribute[ 0 ].lower() + attribute[ 1 : ]
        
        # it is x_ ( local directory, the corresponding variable is named x_Variable )

        elif attribute.endswith( "_" ) : attribute = attribute[ : -1 ]

        try :

            value = getattr( self, attribute + "Value" )

            return True

        except Exception, exception :

            return False




    def loadVariable (

        self,
        identifier = None,
        pattern = None
        ) :

        """ Adds a variable and its pattern to the lists """

        # problem on attribute ? ( weird )

        if utilities.isEmpty( identifier ) : return False

        if identifier.endswith( "Value" ) : identifier = identifier[ : - len( "Value" ) ]

        # pattern is default : (identifier)
        
        if utilities.isEmpty( pattern ) : pattern = "(" + identifier + ")"
        
        # add to list of variables

        self.variableList.append( identifier )

        # adds to list of patterns

        self.patternList.append( pattern )

        return True

        




    def loadVariables ( self ) :

        """ Initializes variables from the attributes that end with "Value" """

        self.variableList = [ ]

        self.patternList = [ ]

        for item in dir( self ) :

            if item.startswith( "_" ) : continue

            if not item.endswith( "Value" ) : continue

            if callable( getattr( self, item ) ) : continue

            self.loadVariable( item )




    def patternIndex (

        self,
        pattern = None
        ) :

        """ returns the index of some pattern """

        index = utilities.index( self.patternList, pattern )

        if index < 0 : return None

        else : return index





    def patternVariable (

        self,
        pattern = None
        ) :

        """ returns the variable of some pattern """

        if not self.isPattern( pattern ) : return None

        index = self.patternList.index( pattern )

        return self.variableList[ index ]

    
        

    def popVariable (

        self,
        identifier = None
        ) :

        """ Gets the previous value of a variable, does nothing if there is none

            if argument is a list, pops all the variables contained in the list

            returns True if popped something, False otherwise (for a list, True is popped all )
            
            """

        # list : pops content

        if type( identifier ) == list :

            result = True

            for name in identifier :

                ok = self.popVariable( name )

                result = result and ok

            return result




        if utilities.isEmpty( identifier ) : return False

        # normalizes the name of the identifier
        
        if identifier.endswith( "Value" ) : identifier = identifier[ : - len( "Value" ) ]

        else : None

        # gets the list of previous values

        try :

            previousList = getattr( self, identifier + "Previous" )

            # a single value instead of a list : break

            if not type( previousList ) == list : return False

        except Exception, exception :

            previousList = [ ]

        # no previous value

        if utilities.isEmpty( previousList ) : return False

        
        # assigns first value of the previous list to variable

        try :

            if not getattr( self, identifier + "Value" ) == previousList[ -1 ] : utilities.changeMs = clock.clockMs()

            setattr( self, identifier + "Value", previousList[ -1 ] )

            setattr( self, identifier + "Previous", previousList[ : -1 ]  )


        except Exception, exception :

            return False

        return True
        


    def popVariables (

        self,
        variableList = None
        ) :

        """ Gets the previous value of a list of variables, does nothing if there is none

            returns True if popped all, False otherwise
            
            """

        if not type( variableList ) == list : return False

        return self.popVariable( variableList )

        


    def pushVariable (

        self,
        identifier = None
        ) :

        """ Pushes the value of context.identifierValue, i.e., adds it to the list context.identifierPrevious

            if argument is a list, pushes all the variables contained in the list

            returns True if could push, False otherwise (for a list, True iff pushed all )
            
            """

        # list : pushes content

        if type( identifier ) == list :

            result = True

            for name in identifier :

                ok = self.pushVariable( name )

                result = result and ok

            return result

        

        if utilities.isEmpty( identifier ) : return False

        # normalizes the name of the identifier
        
        if identifier.endswith( "Value" ) : identifier = identifier[ : - len( "Value" ) ]


        # tries to read the value of the variable
        
        try :
            
            value = getattr( self, identifier + "Value" )

        except Exception, exception :

            return False

        # gets the list of previous values

        try :

            previousList = getattr( self, identifier + "Previous" )

            # a single value instead of a list : break

            if not type( previousList ) == list : previousList = [ ]

        except Exception, exception :

            previousList = [ ]

        # adds value to previous list and assigna

        try :

            setattr( self, identifier + "Previous", previousList + [ value ] )

        except Exception, exception :

            return False

        return True

        

    def pushVariables (

        self,
        variableList = None
        ) :

        """ Pushes the value of a list of variables

            returns True if pushed all, False otherwise
            
            """

        if not type( variableList ) == list : return False

        return self.pushVariable( variableList )


        

            

            
        

    def readVariables (

        self,
        path = None,
        text = None,
        instantiate = None,
        push = None
        ) :

        """ Alias for readVariableValues. Reads the context variables from a file
            (default = ../_persistence/context.txt ) or a text buffer

            if instantiate is True. variables are instantiated e.g., file contains toto,(user) -> toto=current user

            if push is true, previous values of variables are stored

            returns the list of identifiers of variables that were read
            
            
            

            """


        return self.readVariableValues(
            path = path,
            text = text,
            instantiate = instantiate,
            push = push
            )


        

    def readVariableValues (

        self,
        path = None,
        text = None,
        instantiate = False,
        push = False
        ) :

        """ Reads the context variables from a file (default = ../_persistence/context.txt ) or a text buffer

            returns the list of identifiers of variables that were read        

            """


        if ( ( utilities.isEmpty( path ) ) and ( utilities.isEmpty( text ) ) ) :

            path = self.workPath + os.sep + "variables.txt" 
                

        identifiers, values = tableFile.readAttributeValueList(
            path = path,
            text = text,
            strict = False
            )

        variableList = [ ]
        
        for index in range( len( identifiers ) ) :

            identifier = identifiers[ index ]

            if len( identifier ) <= 0 : continue

            if identifier in self.variableList : None

            elif identifier in self.patternList : identifier = self.variableList[ self.patternList.index( identifier ) ]

            else : continue

            # this is a formatted variable _xxx, Xxx, etc : cannot assign value
            
            if identifier.find( "_" ) >= 0 : continue

            if not identifier[ 0 ].islower() : continue

            # checks the value and converts lists into strings

            value = values[ index ]

            if type( value ) == list : value = utilities.linesToAscii( value )

            # removes starting and trailing spaces
            
            value = value.strip()

            # specific case : <void> is replaced by ""

            if value == utilities.voidCode : value = ""

            # instantiates if required

            if bool( instantiate ) :

                # the value is a file

                if value.startswith( utilities.fileHeader ) :

                    value = utilities.fileRead( utilities.instantiate( value ) )

                #  instantiates
                    
                value = utilities.instantiate( value, default = "" )


            # push previous value

            if bool( push ) : self.pushVariable( identifier )

            # assigns

            try :

                if not getattr( self, identifier + "Value" ) == value : utilities.changeMs = clock.clockMs()

                setattr( self, identifier + "Value" , value )

            except Exception, exception :

                continue

            variableList.append( identifier )

        # updates the dependent variables

        self.updateVariables()

        return variableList



    def readWorkVariables ( self ) :

        """ reads the persistent values of variables in work/variables.txt .


            """

##        print "Variables.readWorkVariables", sys.workPath +  "variables.txt"

        self.readVariableValues( path = sys.workPath +  "variables.txt" )
        

    def setVariable (

        self,
        attribute = None,
        value = None
        ) :

        """ Sets the value of variable "attribute"

            Method accepts simple names , e.g., "user", or complete names, "userValue"

            Returns True/False

            """

        if attribute is None : return False

        if not self.variablePresent( attribute ) : return

        if not attribute.endswith( "Value" ) : attribute = attribute + "Value"

        if not type( value ) == str : value = utilities.string( value )

        try :

            if not getattr( self, attribute ) == value : utilities.changeMs = clock.clockMs()
            
            setattr( self, attribute, value )

        except Exception, exception :

            None






        
        
    def updateSelected ( self ) :

        """ updates the variables that depend on selection, self.selectedList """

        utilities.changeMs = clock.clockMs()

        # first, clears variables
        
        self.clearSelected()

        # year of the document ( takes date at the end of the name ) *****

        category, author, description, year, initials = utilities.parseShared( self.selectedValue )

        if category is None : return

        self.typeValue = category

        self.authorValue = author

        self.descriptionValue = description

        self.yearValue = year

        title = utilities.string( initials, format = "upper", default = "" )

        self.titleValue = utilities.string ( title, format = "title" )

        

    def updateShared ( self ) :

        """ Updates the path etc of the shared item (on doc server ) """


       
        typeObject = utilities.getType( self.typeValue )

        if typeObject is None : 

            self.sharedValue = None

            return

            
        # determines the normalized name and the path on the document server

        prefix = utilities.string( self.typeValue, default = "" )

        author = utilities.string( self.authorValue, default = "" )

        description = utilities.string( self.descriptionValue, default = "" )

        title = utilities.string( self.titleValue, default = "" )

        year = utilities.string( self.yearValue, default = "" )

        if self.selectedValue.endswith( os.sep ) : extension = os.sep

        else : extension = "." + utilities.pathExtension( self.selectedValue )
        
        bookcase = utilities.string( self.bookcaseValue, default = "" )


        # normalized name

        self.sharedValue = utilities.pathShared(
            category = prefix,
            author = author,
            description = description,
            year = year,
            title = title,
            extension = extension,
            directory = bookcase
            )
        



        
        
    def updateVariables ( self ) :

        """ Updates dependent variables. Relationships are hard coded """

        # variables that depend on the selected file or directory

        emptySelected = utilities.isEmpty( self.selectedValue )

        if emptySelected : self.clearSelected()

        elif not self.selected == self.selectedValue : self.updateSelected()


        # data directory, depends on current procedure and selected object (local)/procedures/_(procedure)/data/

        
        self.dataValue = utilities.executionDataDirectory(
            script = self.scriptValue,
            procedure = self.procedureValue,
            selected = self.selectedValue
            )

        # updates the path etc of the shared item

        self.updateShared()

        # variables related to templates, copies etc ( source = a path )

        # nothing if the templates are not loaded yet

        if not type( self.templateList ) == list  :

            None
        
        elif ( ( utilities.isEmpty( self.templateValue ) ) or
             ( utilities.isEmpty( self.selectedValue ) ) or
             ( utilities.isEmpty( self.instanceValue ) )
             ) :

            self.sourceValue = None

            self.targetValue = None

        else :

            self.sourceValue = utilities.getTemplate( self.templateValue )

            if self.sourceValue in self.templateList : directory = self.selectedValue

            else : directory = ""

            name = utilities.string( self.instanceValue, format = "strictunderscore", default = "_" )

            extension = utilities.pathExtension( self.sourceValue )

            self.targetValue = directory + name

            if utilities.isEmpty( self.sourceValue ) : self.targetValue = None

            elif self.sourceValue.endswith( os.sep ) : self.targetValue = self.targetValue + os.sep

            elif not utilities.isEmpty( extension ) : self.targetValue = self.targetValue + "." + extension

            
            
        # codes

        executionCode = utilities.string(
            utilities.flatToAscii( self.executionCodeValue ),
            format = "strictunderscore",
            default = ""
            )


        personCode = utilities.string(
            utilities.flatToAscii( self.personCodeValue ),
            format = "strictunderscore",
            default = "" )

        if ( ( utilities.isEmpty( personCode ) ) or ( utilities.isEmpty( executionCode ) ) ) : separator = ""

        else : separator = "_"

        self.codeValue = executionCode + separator + personCode

        # keeps track of selected value

        self.selected = self.selectedValue






    def variableIndex (

        self,
        attribute = None
        ) :

        """ returns the index of some variable """

        if utilities.isEmpty( attribute ) : return None

        if attribute.endswith( "Value" ) : attribute = attribute[ : -len( "Value" ) ]

        index = utilities.index( self.variableList, attribute )

        if index < 0 : return None

        else : return index



        
    def variablePresent (

        self,
        attribute = None
        ) :

        """ Checks whether the current object contains the attribute

            Method accepts simple names , e.g., "user", or complete names, "userValue"

            Returns True/False
            
            """

        if utilities.isEmpty( attribute ) : return False

        if not attribute.endswith( "Value" ) : attribute = attribute + "Value"
           
        
        try :

            x = getattr( self, attribute  )
            
            return True

        except Exception, exception :

            return False



        
        
    def writeVariables (

        self,
        path = None,
        text = None
        ) :

        """ Alias for writeVariableValues. Writes the variables to a file
            ( default is ../persistence/context.txt ) or into a text buffer of tableFile

            returns the list of identifiers of variables that were written

            """

        return self.writeVariableValues(
            path = path,
            text = text
            )
        



    def writeVariableValues (

        self,
        path = None,
        text = None,
        ) :

        """ Writes the variables to a file ( default is ../persistence/context.txt ) or into a text buffer of tableFile

            returns the list of identifiers of variables that were written
            

            """

        if utilities.isEmpty( path ) : path = self.workPath + os.sep + "variables.txt" 

        # updates the dependent variables

        self.updateVariables()

        # loads attribute-value lists from variables
        
        identifiers = [ ]

        values = [ ]

        for variable in self.variableList :

            identifier = variable

            if len( identifier ) <= 0 : continue

            if not identifier[ 0 ].islower() : continue

            try :

                value = getattr( self, identifier + "Value" )

                if not value is None : value = utilities.string( value )

            except Exception, exception :

                value = ""

            if utilities.isEmpty( value ) : continue

            if value == utilities.voidCode : value = "" # will be reconverted

            identifiers.append( identifier )

            values.append( value )


        tableFile.writeAttributeValueList(
            path = path,
            text = text,
            identifiers = identifiers,
            values = values )

        return identifiers


                   
    def writeWorkVariables ( self ) :

        """ writes the values of variables in the work directory work/variables.txt (percistent values).

            if the file configuration/variable_configuration.py has been modified more recently than the work variables
            
            erases the work variables and does not save

            """

        workPath = sys.workPath +  "variables.txt"

        configurationPath = sys.configurationPath + "variable_configuration.py"

        configurationTime = utilities.fileTimeModified( configurationPath )

##        print "Variables.writeWorkVariables conf time", configurationTime, "start ", clock.startS, "delete", int( configurationTime ) >= int( clock.startS )

        # the configuration file has been modified since the beginning of the session : does not save the work variables

        if int( configurationTime ) >= int( clock.startS ) : utilities.fileDelete( workPath )

        else :  self.writeVariableValues( path = workPath )



