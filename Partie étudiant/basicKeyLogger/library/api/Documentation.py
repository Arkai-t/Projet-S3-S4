""" builds the documentation of a python directory.

    Creates files in different format and allows on line consultation

    use:

    from Documentation import *

    documentation.build() to create documentation in memory (can be consulted on line)

        by default,  builds documentation of application, extenal dependencies and built in functions used here.

        to select, ...build( origin = xxx ), xxx being "external", "internal", "builtin" or any sentence composed with
        these 3 words.

    on disk : documentation is in ../_x/*.html etc.

        it is divided in 3 x 3 files :
        - internal (within application directory), external (dependencies),  builtin Python.
        - txt format (ascii), tsv (tab-separated value), html

        file names are : documentation_origin.format

    documentation.write() writes current documentation from memory
    
    documentation.check() to refresh and write if documentation files are not here

    documentation.refresh() to build and write

    ----------------------
    
    on line consultation :

    documentation.build()

    print documentation.itemHelp( my variable ).

        my variable may be an item (e.g., class, python instance, method..) ,
        a complete name, e.g., "api.Documentation.documentation",
        an index (item number)


    """

import sys

import os

import re



class Documentation :

    """ builds the documentation of a python directory.

        Creates files in different format and allows on line consultation

        use:

        from Documentation import *

        documentation.build() to create documentation in memory (can be consulted on line)

            by default,  builds documentation of application, extenal dependencies and built in functions used here.

            to select, ...build( origin = xxx ), xxx being "external", "internal", "builtin" or any sentence composed with
            these 3 words.

        on disk : documentation is in ../_x/*.html etc.

            it is divided in 3 x 3 files :
            - internal (within application directory), external (dependencies),  builtin Python.
            - txt format (ascii), tsv (tab-separated value), html

            file names are : documentation_origin.format

        documentation.write() writes current documentation from memory
        
        documentation.check() to refresh and write if documentation files are not here

        documentation.refresh() to build and write

        ----------------------
        
        on line consultation :

        documentation.build()

        print documentation.itemHelp( my variable ).

            my variable may be an item (e.g., class, python instance, method..) ,
            a complete name, e.g., "api.Documentation.documentation",
            an index (item number)


        """

    from documentation_configuration import *

    try :

        from configuration.documentation_configuration import *

    except Exception, exception :

        from documentation_configuration import *


    
    # text of documentation

    asciiText = None

    # list of classes internal/external

    classBuiltinList = None
    
    classExternalList = None

    classInternalList = None

    classList = None

    # source directory
    
    directory = None

    # list of directories used by application, classified internal/external

    directoryExternalList = None

    directoryInternalList = None

    directoryBuiltinList = None

    directoryList = None

    # list of exceptions

    exceptionList = None

    # text of list of errors

    exceptionText = None

    

    # list of files, classified internal/external

    fileExternalList = None

    fileInternalList = None

    fileBuiltinList = None

    fileList = None
    
    # text of documentation

    htmlText = None

    # list of items

    itemList = None
    
    # matrix of items with their features

    itemMatrix = None

    # root directory in lower case

    lowerDirectory = None

    # list of paths

    pathList = None

    # text of read mes

    readmeText = None

    # text of documentation

    tsvText = None

    # list of variables (pairs [ (pattern), value ] ) for header and footer

    variableList = None

    

    def __init__ ( self ) :


        """ Constructor - by default works on the current directory """

        self.setDirectory()

        self.resetData()

        self.setPatterns()




    def add (

        self,
        identifier = None,
        item = None,
        container = None,
        path = None,
        origin = None,
        ) :

        """ adds an item to the lists

            origin is None ( no control, takes anything) or a string that contains "builtin", "external", "internal"
            
            """

        # control that can access item

        try :

            str( item )

        except Exception, exception :

            text = "documentation - add cannot access item " + str( exception )

            print text

            self.exceptionList.append( text )

            return False


        # needs an identifier (if absent tries to find it in the item )

        if identifier is None : identifier = self.itemName( item )
        
        if identifier is None : return False
           
        # checks identifier : word after last point must not be reserved
        
        if identifier[ identifier.rfind( "." ) + 1 : ] in self.reservedNameList : return False

        # category of item
       
        category = self.itemTypeName( item )

        # builtin

        if category in self.builtinTypeList : return False


        # basic type : no control of presence

        elif category in self.basicTypeList : pass

        # already here (control only for non-basic objects)

        elif item in self.itemList : return True

        print "build - items ", len( self.itemMatrix ), " paths", len( self.pathList )
        
        # original file

        pathIndex = self.itemPathIndex( item, path )

        if not pathIndex is None : path = self.pathList[ pathIndex ]

        else : path = None
        
        if pathIndex is None :

            itemOrigin = self.keywordBuiltin

            path = None

        else :

            path = self.pathList[ pathIndex ]

            lowerPath = path.lower() + os.sep   # to compare adequately with the root directory

            if lowerPath.startswith( self.lowerDirectory ) : itemOrigin = self.keywordInternal

            else : itemOrigin = self.keywordExternal

        # filters according to origin

        if origin is None : None

        elif itemOrigin in origin : None

        else : return False

        # documentation (string )

        docstring = self.itemDocstring( item )
       
        # super classes and parent classes ( the whole hierarchy ) - objects

        superclass = self.itemSuperclass( item )

        hierarchyList, hierarchyText = self.itemHierarchy( item )

        # sublists 
        
        moduleList, classList, functionList, fieldList, referenceList = self.itemComponents( item )

        # modules of origin of imported items

        importList = self.itemImported( item )

        # inserts item

        # list of items

        self.itemList.append( item )

        # matrix 

        self.itemMatrix.append( [
            itemOrigin,
            identifier,
            category,
            pathIndex,                  # index in fileList
            hierarchyText,
            self.toString( importList, size = 8, separator = ", " ),
            self.toString( referenceList, size = 8, separator = ", " ),       
            self.toString( moduleList, size = 8, separator = ", "  ),         
            self.toString( classList, size = 8, separator = ", "  ),         
            self.toString( functionList, size = 8, separator = ", "  ),         
            self.toString( fieldList, size = 8, separator = ", "  ), 
            docstring,
            len( self.itemList ) - 1,   # index in itemList
            ] )

        

        # adds subitems recursively (updates module and container if the item plays these roles for its content)

        # add subitems, except for callable items

        if category in self.callableTypeList : contentList = [ ]

        else : contentList = moduleList + classList + functionList + fieldList
                                   
        for key in contentList :

            if key in self.reservedNameList : continue

            try :

                subitem = getattr( item, key )

            except Exception, exception :

                text = "documentation - add cannot access subitem " +  str(key) + " - " + str( exception )

                print text

                self.exceptionList.append( text )

                continue

            self.add(
                identifier = identifier + "." + key,
                item = subitem,
                path = path,
                origin = origin,
                )


        # importe modules
        
        for module in importList  :

            self.add(
                item = module,
                origin = origin,
                )
            
        return True

        

    def addReadme (

        self,
        path = None,
        ) :

        """ adds a readme file to the current buffer self.readmeText """


        if path is None : return

        path = os.path.abspath( os.path.expanduser( path ) ) 

        # gets directory, name extension
        
        directory, name = os.path.split( path )

        name, extension = os.path.splitext( name )

        # inserts title and link

        # part of title is relative path from root
        
        parent = directory[ len( self.directory ) : ]

        if len( parent ) == 0 : parent = self.keywordRoot

        title = parent.replace( "\\", " " ).replace( "/", " " ) + " /"

        name = name[ len( self.keywordReadme ) : ]

        name = name.strip( " _" ).replace( "_", " " )

        if len( name ) > 0 : title = name

        if len( name ) > 0 : text = self.subsectionHtml

        else : text = self.sectionHtml

        # transforms path into relative from local directory of file:///xxx

        text = text.replace( "(1)", title ).replace( "(2)", self.htmlPath( path ) )

        self.readmeText = self.readmeText + text

        # now, reads content
        
        content = self.fileRead( path )

        if content is None : return

        # if .html, .html, .shtml, truncates to body

        if "htm" in extension :

            iStart = content.find( "<body>" )

            if iStart >= 0 : content = content[ iStart + len( "<body>" ) : ]

            iEnd = content.find( "</body>" )

            if iEnd >= 0 : content = content[ : iEnd ]

        # this is a text content : recodes
        
        else :

            for pair in self.codeHtml : content = content.replace( str( pair[ 0 ] ), str( pair[ 1 ] ) )

        # appends the content            

        self.readmeText = self.readmeText + "<br><br>\n" + content + "<br><br>\n"
        


    def addSeeAlso (

        self,
        path = None,
        ) :

        """ adds a link (see also) to potential doc file """

        self.readmeText = self.readmeText + self.linkHtml.replace( "(1)", self.htmlPath( path ) )


        
        
        

    def build (

        self,
        identifier = None,
        origin = None,
        path = None,
        ) :

        """ builds the matrix of items
        
            identifier is an item or a list of items, defined directly or by identifier, e.g.,
            build( x ) or build ( "module.x" )

            origin is a filter on external, internal builtin (default = adds all). it is a string that contains
            the desired keywords, e.g., "internal external"

            path = the path to the application directory. anything in this is considered internal, otherwise external

            
            """

        # sets the application directory and the local directory
        
        if not path is None : self.setDirectory( path )
        
        self.resetData()

        # verifies and eventually creates the documentation directory
        
        ok = self.setDocumentation()

        if not ok : return False

        # looks for the item with the given identifier or documents everything in current execution


        # all modules and packages

        dictionary = {}

        dictionary.update( sys.modules )

        self.buildDictionary(
            dictionary = dictionary,
            identifier = identifier,
            origin = origin,
            )

        # sorts the items

        self.itemMatrix.sort()

        # builds the list of paths

        self.buildLists()

        return True




    def buildDictionary (

        self,
        dictionary = None,
        identifier = None,
        origin = None,
        ) :

        """ builds the items of a dictionary (adds to previous items)
        
            identifier is an item or a list of items, defined directly or by identifier, e.g.,
            build( x ) or build ( "module.x" )

            origin is a filter on external, internal builtin (default = adds all). it is a string that contains
            the desired keywords, e.g., "internal external"

            the path to the application directory is self.directory

            """

        if dictionary is None : return 


        # normalizes the identifier to document : None, a list or an item

        if identifier is None :

            item = None

        elif type( identifier ) == list :

            item = None

        elif type( identifier ) == str :

            identifier = [ identifier ]

            item = None

        else :

            item = self.itemModule( identifier )

            identifier = None

        # loop on items of the dictionary
        
        for key in dictionary :

            if ( ( not identifier is None ) and ( not key in identifier ) ) : continue

            value = dictionary[ key ]

            if ( ( not item is None ) and ( not value is item ) ) : continue

            self.add(
                identifier = key,
                item = value,
                origin = origin,
                path = self.directory,
                )



    def buildErrors ( self ) :

        """ writes the list of errors in HTML format, generates self.errorText """

        self.errorsText = self.errorsHtml

        if self.exceptionList is None : return True

        if len( self.exceptionList ) <= 0 : return True

        for item in self.exceptionList :

            self.errorsText = self.errorsText + item + "<br>"

        self.errorsText = self.errorsText + self.bottomHtml

        

    def buildLists ( self ) :

        """ builds the lists of paths to internal/external files and directories """

        self.classList = [ ]
        
        self.classBuiltinList = [ ]
        
        self.classExternalList = [ ]

        self.classInternalList = [ ]

        self.directoryList = [ ]

        self.directoryExternalList = [ ]

        self.directoryInternalList = [ ]

        self.fileList = [ ]

        self.fileExternalList = [ ]

        self.fileInternalList = [ ]

        # internal builtin

        directory, dummy = os.path.split( sys.executable )

        self.fileBuiltinList = [ sys.executable ]

        self.directoryBuiltinList = [ directory ]

        # loop on documentation items. constructs class lists, file and directory lists, solves reference to files

        for line in self.itemMatrix :

            origin = line[ 0 ]

            identifier = line[ 1 ]

            # class lists

            if line[ 2 ] == "classobj" :

                # the class (and its directory) are already in list
                
                if identifier in self.classList : continue

                self.classList.append( identifier )

                if origin == self.keywordInternal : self.classInternalList.append( identifier )

                elif origin == self.keywordExternal : self.classExternalList.append( identifier )
 
                else : self.classBuiltinList.append( identifier )
                    
            # path

            path = line[ 3 ]

            if path is None : continue

            path = self.pathList[ path ]

            if sys.platform == "win32" : path = path.lower()

            directory, name = os.path.split( path )

            directory = directory + os.sep

            name, extension = os.path.splitext( name )

            if os.path.exists( directory + name + ".py" ) : path = directory + name + ".py"

            elif os.path.exists( directory + name + ".pyw" ) : path = directory + name + ".pyw"
            
            # resolves reference

            line[ 3 ] = path

            # already here

            if path in self.fileList : continue

            self.fileList.append( path )

            
            # internal lists

            if origin == self.keywordInternal : self.fileInternalList.append( path )

            
            # external lists

            elif origin == self.keywordExternal : self.fileExternalList.append( path )

            # directory already here

            if directory in self.directoryList : continue

            self.directoryList.append( directory )
            
            # internal lists

            if origin == self.keywordInternal : self.directoryInternalList.append( directory )
            
            # external lists

            elif origin == self.keywordExternal : self.directoryExternalList.append( directory )

            
        # sorts

        self.classList.sort()
        
        self.classBuiltinList.sort()
        
        self.classExternalList.sort()

        self.classInternalList.sort()

        self.directoryList.sort()

        self.directoryExternalList.sort()

        self.directoryInternalList.sort()

        self.fileList.sort()

        self.fileExternalList.sort()

        self.fileInternalList.sort()

       


    def buildReadme (

        self,
        path = None,
        target = None
        ) :

        """ builds a readme text (html) by collecting all the readmes files

            creates sections according to subdirectory, e.g., path/api/readme.txt -> section api

            creates subsections with the name of the readme file e.g. readme_users_manual.txt -> sub section users manual

            accepts html and texts

            path = the path to the application directory. anything in this is considered internal, otherwise external

            target is the directory where the files should be written (default is local = _path/). Used for relative links

            """

        ok = self.setDocumentation( target )

        if not ok : return False

        # directory to document

        if not path is None : self.setDirectory( path )

        if self.directory is None : return

        self.readmeText = self.readmeHtml

        # instantiates

        self.buildVariables(
            origin = self.keywordInternal,
            anchorPattern = self.anchorHtml,
            linkPattern = self.linkHtml,
            html = True
            )

        for variable in self.variableList :

            identifier = str( variable[ 0 ] )

            field = str( variable[ 1 ] )

            self.readmeText = self.readmeText.replace( identifier, field )        

        # recursive walk through directory to include readme files
                
        walk = os.walk( self.directory )
       
        for parent, directories, files in walk :

            # expands the readme files

            for item in files :

                name, extension = os.path.splitext( item )

                # this is a read me
                   
                if not name.startswith( self.keywordReadme ) : continue

                if ( ( not "txt" in extension ) and ( not "htm" in extension ) ) : continue

                # file name with path relative to sourceDirectory 
                
                path = os.path.abspath( os.path.expanduser( parent + os.sep + item ) )

                self.addReadme( path )

        # recursive walk through directory to include see also links

        # prepares the search patterns for see also (additional links)

        patternList = list(
            str( item ).replace( "\\", "\\\\" ).replace( ".", "\\." ).replace( "*", ".*" ) + "$"
            for item in self.seeAlsoList
            )

        text = self.sectionHtml.replace( "(1)", "Links" ).replace( "(2)", self.htmlPath( self.directory ) ) + "<br><br>"
                
        self.readmeText = self.readmeText + text

        # new walk, does not work with the old one (it is an iterator )
        
        walk = os.walk( self.directory )
       
        for parent, directories, files in walk :

            # adds see also (links to possible doc files )

            for item in files :

                # file name with path relative to sourceDirectory 
                
                path = os.path.abspath( os.path.expanduser( parent + os.sep + item ) )

                # there is a match or not

                ok = max( not re.search( pattern, path ) is None for pattern in patternList )

                if ok : self.addSeeAlso( path )
                
        self.readmeText = self.readmeText + self.bottomHtml

        





    def buildVariables (
        
        self,
        origin = None,
        anchorPattern = None,
        linkPattern = None,
        html = False
        ) :

        """ builds a variable list to be used in text outputs

            origin = origin of the item :  "internal" "external" or "builtin"

            anchorPattern and linkPattern are patterns for internal and external links respectively

            html is a flag: if true, the paths are transformed intotml with / and file:/// before global paths
            
            """

        if origin == self.keywordBuiltin :

            classes = self.classBuiltinList

            directories = self.directoryBuiltinList

            files = self.fileBuiltinList

        elif origin == self.keywordExternal :

            classes = self.classExternalList

            directories = self.directoryExternalList

            files = self.fileExternalList

        elif origin == self.keywordInternal :
            
            classes = self.classInternalList

            directories = self.directoryInternalList

            files = self.fileInternalList

        else :

            origin = ""

            classes = self.classList

            directories = self.directoryList

            files = self.fileList

        # creates lists of instantiated patterns from the classes, files and directories

        classText = ""

        for item in classes : classText = classText + anchorPattern.replace( "(1)", self.toString( item ) )
        
        directoryText = ""

        for item in directories :

            item = self.toString( item )

            if bool( html ) : item = self.htmlPath( item )

            directoryText = directoryText + linkPattern.replace( "(1)", item )
        
        fileText = ""

        for item in files :

            item = self.toString( item )

            if bool( html ) : item = self.htmlPath( item )

            fileText = fileText + linkPattern.replace( "(1)", item )
            
        
        self.variableList = [
            [ "(" + self.keywordClasses +")", classText ],
            [ "(" + self.keywordDirectories +")", directoryText ],
            [ "(" + self.keywordFiles +")", fileText ],
            [ "(" + self.keywordOrigin + ")", origin ],
            ]

        



    def check ( self ) :

        """ if documentation files do not exist, create them """


        path = self.documentationPath + "documentation_internal.txt"

        if not os.path.exists( path ) :

            self.directoryCreate( self.documentationPath )

            self.refresh()




    def directoryCreate (

        self,
        path = None
        ) :

        """ creates recursively a directory """

        if path is None : return True
       
        # makes directory
        
        try :
            
            os.makedirs( path )

        except Exception, exception :
            
            None

        return os.path.isdir( path )


        
    def fileRead (

        self,
        path = None
        ) :

        """ reads the content of a file. Returns None or the content (ascii) """
        
        try :

            handler = open( path, mode = "r" )

            text = handler.read()

            handler.close()

            return text

        except Exception, exception :

            return None



    def fileWrite (

        self,
        path = None,
        text = None
        ) :

        """ writes the text into a file . returns True/False and prints error message if there is a pb """

        if not type( text ) == str : text = str( text )
        
        try :

            handler = open( path, mode = "w" )

            handler.write( text )

            handler.close()

            return True

        except Exception, exception :

            text = "documentation - " + str( exception )

            print text

            self.exceptionList.append( text )

            return False



         

    def get (

        self,
        item = None,
        ) :

        """ returns a line of information on some item. The item is a (compound) string """


        if not type( item ) == str :

            identifier = None
            
        else :

            identifier = item

            item = None


        found = None            

        for line in self.itemMatrix :

            if ( ( not item is None ) and ( self.itemList[ line[ -1 ] ] == item ) ) : return line

            if not identifier is None :

                if line[ 1 ] == identifier : return line

                if line[ 1 ].endswith( identifier ) : found = line

        return found



    def htmlPath (

        self,
        path = None
        ) :

        """ returns a html path relative path from target directory if possible, file:///path  otherwise """

        if path is None :

            path = os.curdir

            isDirectory = True

        else :

            isDirectory = path.endswith( os.sep ) 

        path = os.path.abspath( os.path.expanduser( path ) )

        # normalizes the final /
        
        if ( ( isDirectory ) and ( not path.endswith( os.sep ) ) ) : path = path + os.sep

        # ends with None (dummy file) : removes

        if ( ( path.endswith( "none" ) ) or ( path.endswith( "None" ) ) ) : path = path[ : - len( "none" ) ]

        # no target directory

        if self.documentationPath is None :

            if not path.startswith( "file:///" ) : path = "file:///" + path

            return path


        # relative is the parent directory of target
        
        relative, dummy = os.path.split( self.documentationPath[ : -1 ] )

        if sys.platform == "win32" :

            relative = relative.lower()

            path = path.lower()

        if path.startswith( relative ) :  path = os.pardir + path[ len( relative ) : ]

        elif not path.startswith( "file:///" ) : path = "file:///" + path

        return path.replace( os.sep, "/" )

        



        
    def itemCallExpression (

        self,
        item = None
        ) :

        """ returns the function call of a callable item or "" """

        try :

            if not type( item ).__name__ in self.callableTypeList : return ""

        except Exception, exception :

            return ""
        

        try :

            # object is a function
            
            if type( item ).__name__ == "function" : function = item

            # object is a method, gets its function
            
            else : function = item.im_func

            defaults = function.func_defaults

            if defaults is None : defaults = ""

            sizeDefault = len( defaults )

            code = function.func_code

            sizeArgument = code.co_argcount

            arguments = code.co_varnames

            if arguments is None : arguments = ""

            name = code.co_name

            text = name + " (\n"

            for i in range ( sizeArgument ) :

                text = text + "\t" + str( arguments[ i ] )

                if i >= sizeArgument - sizeDefault :

                    text = text + " = " + str( defaults[ i - sizeArgument + sizeDefault ] )

                text = text + "," + "\n"

            text = text + "\t" + ")" + "\n\n"

            return text

        except Exception, exception :

            return ""
    

        
    def itemComponents (

        self,
        item = None,
        path = None
        ) :

        """ returns the content of the item classified into sublists ( of identifiers )

            returns lists of
            modules defined here
            classes defined here
            functions and methods defined here
            other fields defined here
            items defined elsewhere and forming part of the name space
            
            for basic or reserved items, returns 5 empty lists
            
            """

        # item is basic

        if type( item ).__name__ in self.basicTypeList : return [], [], [], [], []
        
##        if type( item ).__name__ in self.callableTypeList : return [], [], [], [], []
        
        # gets the extended dictionary (full reference space)
        
        try :
            
            dictionary = dir( item )

        except Exception, exception :

            return [], [], [], [], []

        # gets the items DEFINED here
        
        items = self.itemContent( item )

        path = self.itemPath( item, path )
        
        # sublists 
        
        moduleList = [ ]

        classList = [ ]

        functionList = [ ]

        fieldList = [ ]

        referenceList = [ ]

        # loop on complete dictionary ( name space includes items, except for functions & methods )

        referenceList = list( key for key in dictionary \
                              if ( ( not key in self.reservedNameList ) and ( not key in items ) )
                              )
        

##        for key in dictionary :
##
##            if key in self.reservedNameList : continue
##
##            if key in items : continue
##
##            # not defined here : imported
##
##            referenceList.append( key )

        # callable item : the content are local variables and getattr( funct, localVar ) does not exist

        if type( item ).__name__ in self.callableTypeList :

            fieldList = items

            return moduleList, classList, functionList, fieldList, referenceList
        
        # non callable item
        
        for key in items :

            if key in self.reservedNameList : continue

            try :

                value = getattr( item, key )

            except Exception, exception :

                continue

            category = self.itemTypeName( value )

            # not from here, external reference

            if not self.itemPath( value, path ) == path : referenceList.append( key )

            # otherwise, classified by category

            elif category == "module" : moduleList.append( key )

            elif category == "module" : moduleList.append( key )

            elif category == "classobj" : classList.append( key )

            elif callable( value ) : functionList.append( key )

            else : fieldList.append( key )


        return moduleList, classList, functionList, fieldList, referenceList




        
        

        
    def itemContent (

        self,
        item = None
        ) :

        """ returns the directory of subitems (identifiers) """

        category = type( item ).__name__

        # for basic elements, nothing
        
        if category in self.basicTypeList : return [ ]

        # for callable elements, returns the list of local variables
        
        if ( ( category == "function" ) or ( category == "instancemethod" ) ) : return self.itemLocalVariables( item )


        # gets the directory
        
        try :

            items = item.__dict__.keys()

        except Exception, exception :

            return [ ]


        # filters reserved names
        
        content = list( item for item in items if not item in self.reservedNameList )

        # ... and sorts
        
        return sorted( content )



    def itemDocstring (

        self,
        item = None
        ) :

        """ returns the documentation string of the item """

        # it is a callable item generates a function call

        text = self.itemCallExpression( item )

        

        # doc string is the generic one: don't care
        
        try :

            if ( ( text == "" ) and ( item.__doc__ == type( item ).__doc__ ) ) : return ""

        except Exception, exception :

            None           

        try :

            return text + item.__doc__

        except Exception, exception :

            return text

        




    def itemHelp (

        self,
        item = None,
        path = None
        ) :

        """ returns a text information on some item. The item is a (compound) string """

        if len( self.itemMatrix ) == 0 : self.build( path = None )

        line = self.get( item )

        if line is None : return ""

        return self.toAscii( line )




    def itemHierarchy (

        self,
        item = None,
        level = 0
        ) :

        """ ancestor class (es) or type of the item. Category (item's type) and parent can be predefined

            returns a pair list - text, composed of indented lines
            
            """

        parent = self.itemSuperclass( item )

        if parent is None : return [ ], ""

        if not type( parent ) == list : parent = [ parent ]

        ancestor = [ ]

        text = ""

        for item in parent :

            ancestor.append( item )

            text = text + level * "\t" + self.itemName( item ) + "\n"

            itemParent = self.itemSuperclass( item )

            if itemParent is None : continue

            if not type( itemParent ) == list : itemParent = [ itemParent ]

            for subitem in itemParent :

                # checks end of hierarchy: types are their own types
                
                if subitem == item : continue

                itemAncestor, itemText = self.itemHierarchy(
                    subitem,
                    level = level + 1
                    )

                ancestor.extend( itemAncestor )

                text = itemText + text

        
        return ancestor, text



    def itemImported (

        self,
        item = None
        ) :

        """ returns the list of modules used by the item (direct or indirect import ) """

        try :

            content = dir( item )

        except Exception, exception :

            return [ ]

        itemModule = self.itemModule( item )
        
        moduleList = [ ]
        
        for key in content :

            module = self.itemModule( getattr( item, key ) )

            if module is None : continue

            if module == itemModule : continue

            if module in moduleList : continue

            moduleList.append( module )

        return moduleList



        
    def itemLocalVariables (

        self,
        item = None
        ) :

        """ returns the list of local variables of callable elements """

        try :

            if not type( item ).__name__ in self.callableTypeList : return [ ]

        except Exception, exception :

            return [ ]
        

        try :

            # object is a function
            
            if type( item ).__name__ == "function" : function = item

            # object is a method, gets its function
            
            else : function = item.im_func

            code = function.func_code

            content = code.co_varnames

        except Exception, exception :

            return [ ]

        # filters reserved names
        
        content = list( item for item in content if not item in self.reservedNameList )

        # ... and sorts
        
        return sorted( content )
        



    def itemModule (

        self,
        item = None,
        ) :

        """ module where an item is defined. For modules & packages, the item's name. """

        # it is a module : returns itself

        try :
            
            if type( item ).__name__ == "module" : return item

        except Exception, exception :

            None

        # instance, class, function
        
        try :

            return sys.modules[ item.__module__ ]

        except Exception, exception :

            None

        # instance of method
        
        try :

            return sys.modules[ item.im_class.__module__ ]

        except Exception, exception :

            None

        return None
        
        

    def itemName (

        self,
        item = None
        ) :

        """ returns the name of the item or by default type_xxx """

        # doc string is the generic one: don't care
        
        try :

            return item.__name__

        except Exception, exception :

            return type( item ).__name__ + str( len( self.itemList ) )

        

    def itemPackage (

        self,
        item = None,
        module = None,
        package = None
        ) :

        """ package where an item is defined. For modules & packages, the item's name. """

        if module is None : module = self.itemModule( item )

        if module is None : return None

        name = self.itemName( module )

        if not "." in name : return None

        try :

            return sys.modules[ name[ : name.rfind( "." ) ] ]

        except Exception, exception :

            None

        if type( package ).__name__ == "module" : return package

        try :

            return sys.modules[ package ]

        except Exception, exception :

            None

        return None
        

        

    def itemPath (

        self,
        item = None,
        path = None
        ) :

        """ returns the path to the file where the item is defined """

        module = self.itemModule( item )

        # there is a module (true except if defined directly in main script )

        if not module is None : 

            # tries to get the module's file

            try :

                path = module.__file__

                path = os.path.abspath( os.path.expanduser( path ) )
                
            except Exception, exception :

                return None

        return path
    



    def itemPathIndex (

        self,
        item = None,
        path = None
        ) :

        """ returns the index of the path where the item is defined in the list self.pathList

            adds to the list if not here

            """

        path = self.itemPath( item, path )

        # no path
        
        if path is None : return None

        # tries to find the path given as argument in list

        path = os.path.abspath( os.path.expanduser( path ) )

        if path in self.pathList : return self.pathList.index( path )

        # not here : appends

        self.pathList.append( path )

        return len( self.pathList ) - 1

    
    

    def itemSuperclass (

        self,
        item = None,
        category = None,
        ) :

        """ parent class (es) or type of the item. Category (item's type) and parent can be predefined

            returns None, a string or a list

            """

        if category is None : category = type( item ).__name__

        if category == "classobj" :

            parent = list( item.__bases__ )

        elif category == "instance" :

            parent = item.__class__

        else :

            parent = type( item )


        return parent

            
        
    def itemTypeName (

        self,
        item = None
        ) :

        """ returns the category of an item """

        try :

            name = type( item ).__name__

        except Exception, exception :

            return None

        # specific cases

        # module with path = package

        if name == "module" :

            try :

                path = item.__path__

                name = "package"

            except Exception, exception :

                None

        return name





        
    def refresh (

        self,
        path = None
        ) :

        """ builds and writes """

        self.build( path = path )

        self.write()






    def resetData ( self ) :

        """ resets the matrix of items """


        self.itemList = [ ]

        self.itemMatrix = [ ]

        self.pathList = [ ]

        self.classList = [ ]

        self.classBuiltinList = [ ]

        self.classExternalList = [ ]

        self.classInternalList = [ ]

        self.directoryList = [ ]

        self.directoryBuiltinList = [ ]

        self.directoryExternalList = [ ]

        self.directoryInternalList = [ ]

        self.exceptionList = [ ]

        self.fileList = [ ]

        self.fileExternalList = [ ]

        self.fileInternalList = [ ]

        self.fileBuiltinList = [ ]

        self.asciiText = ""

        self.htmlText = ""

        self.tsvText = ""



    def setDirectory (

        self,
        directory = None
        ) :

        """ sets the source and local directory, where the documentation is placed """

        # default = current
        
        if directory is None : directory = os.curdir
        
        # replaces \\ and // by os.sep

        else : directory = directory.replace( "\\", os.sep ).replace( "/", os.sep )

        # normalizes the name
        
        self.directory = os.path.abspath( os.path.expanduser( directory ) )

        if not self.directory.endswith( os.sep ) : self.directory = self.directory + os.sep

        # to speed up recognition of internal items
        
        self.lowerDirectory = self.directory.lower()




    def setDocumentation (

        self,
        path = None
        ) :

        """ sets/resets the documentation path. creates if required """


        if path is None : path = self.documentationPath

        if not os.path.isdir( path ) :

            ok = self.directoryCreate( path )

            if not ok : return False

        path = os.path.abspath( os.path.expanduser( path ) ) + os.sep

        self.documentationPath = path.replace( os.altsep, os.sep ).replace( os.sep + os.sep, os.sep )
        
        return True
        


    def setPatterns ( self ) :

        """ initializes the patterns from files, in same directory than this module """

        path = self.itemPath( self )

        directory, dummy = os.path.split( path )

        directory = directory + os.sep

        # headers

        pattern = self.fileRead( directory + "documentation_header.txt" )

        if not pattern is None : self.headerAscii = pattern
            
        pattern = self.fileRead( directory + "documentation_header.html" )

        if not pattern is None :

            # truncates

            iStart = pattern.find( "<body>" )

            if iStart >= 0 : pattern = pattern[ iStart + len( "<body>" ) : ]
            
            iEnd = pattern.find( "</body>" )

            if iEnd >= 0 : pattern = pattern[  : iEnd ]

            self.headerHtml = pattern
            
        pattern = self.fileRead( directory + "documentation_header.tsv" )

        if not pattern is None : self.headerTsv = pattern
            
        
        # patterns for items

        pattern = self.fileRead( directory + "documentation_pattern.txt" )

        if not pattern is None : self.patternAscii = pattern
            
        pattern = self.fileRead( directory + "documentation_pattern.html" )

        if not pattern is None :

            # truncates
            
            iStart = pattern.find( "<body>" )

            if iStart >= 0 : pattern = pattern[ iStart + len( "<body>" ) : ]
            
            iEnd = pattern.find( "</body>" )

            if iEnd >= 0 : pattern = pattern[  : iEnd ]

            self.patternHtml = pattern
            
        pattern = self.fileRead( directory + "documentation_pattern.tsv" )

        if not pattern is None : self.patternTsv = pattern

        
        # patterns for basic items

        pattern = self.fileRead( directory + "documentation_basic.txt" )

        if not pattern is None : self.basicAscii = pattern
            
        pattern = self.fileRead( directory + "documentation_basic.html" )

        if not pattern is None :

            # truncates
            
            iStart = pattern.find( "<body>" )

            if iStart >= 0 : pattern = pattern[ iStart + len( "<body>" ) : ]
            
            iEnd = pattern.find( "</body>" )

            if iEnd >= 0 : pattern = pattern[  : iEnd ]

            self.basicHtml = pattern
            
        pattern = self.fileRead( directory + "documentation_basic.tsv" )

        if not pattern is None : self.basicTsv = pattern

        
        # footers

        pattern = self.fileRead( directory + "documentation_footer.txt" )

        if not pattern is None : self.footerAscii = pattern
            
        pattern = self.fileRead( directory + "documentation_footer.html" )

        if not pattern is None :

            # truncates

            iStart = pattern.find( "<body>" )

            if iStart >= 0 : pattern = pattern[ iStart + len( "<body>" ) : ]

            self.footerHtml = pattern
            
        pattern = self.fileRead( directory + "documentation_footer.tsv" )

        if not pattern is None : self.footerTsv = pattern
        

        
        # error fils

        pattern = self.fileRead( directory + "documentation_errors.html" )

        if not pattern is None :
            
            # truncates
            
            iStart = pattern.find( "<body>" )

            if iStart >= 0 : pattern = pattern[ iStart + len( "<body>" ) : ]
            
            iEnd = pattern.find( "</body>" )

            if iEnd >= 0 : pattern = pattern[  : iEnd ]

            self.errorsHtml = pattern


        # read me for html file

        pattern = self.fileRead( directory + "documentation_readme.html" )

        if not pattern is None :

            # truncates
            
            iStart = pattern.find( "<body>" )

            if iStart >= 0 : pattern = pattern[ iStart + len( "<body>" ) : ]
            
            iEnd = pattern.find( "</body>" )

            if iEnd >= 0 : pattern = pattern[  : iEnd ]

            self.readmeHtml = pattern

        
                           
    def toAscii (

        self,
        line = None,
        index = None,
        item = None,
        origin = None,
        ) :

        """ converts the matrix ( or a single line ) of items into a flat text

            line, index, item and origin are filters that selects
            - 1 line of the matrix
            - 1 specific line number,
            - the line of an item ( see get()
            - lines from a given origin (internal, external..)

            if no unique line is defined, the text contains a header, all lines from the 'origin' and a footer

            recodes the characters according to 'code' : a list of pairs [ [ "xx", "new xx" ] .. ]

            """
            

        return self.toFormat(
            line = line,
            index = index,
            item = item,
            origin = origin,
            header = self.headerAscii,
            pattern = self.patternAscii,
            basic = self.basicAscii,
            footer = self.footerAscii,
            anchor = self.anchorAscii,
            link = self.linkAscii,
            void = self.voidAscii,
            code = self.codeAscii
            )
    



    def toFormat (

        self,
        line = None,
        index = None,
        item = None,
        origin = None,
        header = None,
        pattern = None,
        basic = None,
        footer = None,
        anchor = None,
        link = None,
        void = None,
        code = None,
        html = False
        ) :

        """ returns a pattern filled with one line and/or all the documentation lines (if line is undefined)

            line, index, item and origin are filters that selects
            - 1 line of the matrix
            - 1 specific line number,
            - the line of an item ( see get()
            - lines from a given origin (internal, external..)

            if no unique line is defined, the text contains a header, all lines from the 'origin' and a footer

            recodes the characters according to 'code' : a list of pairs [ [ "xx", "new xx" ] .. ]

            html is a flag: if true the paths are transformed into html syntax file:/// etc.
                        
            """

        # tries to determine a specific line from arguments

        # index defined
        
        if not line is None :

            None

        elif type( index ) == int  :

            try :

                line = self.itemMatrix[ index ]

            except Exception, exception :

                None

        # item (or attribute ) defined

        elif not item is None :

            line = self.get( item )

        
        # no specific line : text covers all        
            
        if line is None :

            # builds variable list to instantiate header and footer

            self.buildVariables(
                origin,
                anchorPattern = anchor,
                linkPattern = link,
                html = html
                )

            # instantiates header and footer
            # no need to recode the values, they come from a  type-dependent pattern , link or anchor

            for variable in self.variableList :

                identifier = str( variable[ 0 ] )

                field = str( variable[ 1 ] )

                header = header.replace( identifier, field )

                footer = footer.replace( identifier, field )

            text = header

            for line in self.itemMatrix :

                # filters according to origin
                
                if ( ( not origin is None ) and ( not line[ 0 ] == origin ) ) : continue

                text = text + \
                       self.toFormat(
                            line = line,
                            pattern = pattern,
                            basic = basic,
                            void = void,
                            code = code,
                            html = html,
                            )


            text = text + footer

            return text

        # error of type

        if ( ( not type( line ) == list ) or ( len( line ) < 13 ) ) : return ""

        line = list( str( x ) for x in line )

        # type of pattern : normal or basic

        if line[ 2 ] in self.basicTypeList : text = basic

        else : text = pattern
        
        # resolves the file

        path = line[ 3 ]

        if not path is None :

            if sys.platform == "win32" : path = path.lower()

            prefix, extension = os.path.splitext( path )

            if os.path.exists( prefix + ".py" ) : extension = ".py"

            elif os.path.exists( prefix + ".pyw" ) : extension = ".pyw"

            path = prefix + extension

            if bool( html ) : path = self.htmlPath( path )

            line[ 3 ] = path

##            else : line[ 3 ] = ""

        for i in range( len( line ) ) :

            field = line[ i ]

            if ( ( field is None ) or ( field == "" ) ) : field = str( void )
            
            for pair in code : field = field.replace( str( pair[ 0 ] ), str( pair[ 1 ] ) )

            text = text.replace( "(" + str( i + 1 ) + ")", field )

            # particular case (html): in links, ( ) are often recoded %28 %29

            text = text.replace( "%28" + str( i + 1 ) + "%29", field )

        return text

        


    def toHtml (

        self,
        line = None,
        index = None,
        item = None,
        origin = None,
        ) :

        """ converts the matrix ( or a single line ) of items into a html text

            line, index, item and origin are filters that selects
            - 1 line of the matrix
            - 1 specific line number,
            - the line of an item ( see get()
            - lines from a given origin (internal, external..)

            if no unique line is defined, the text contains a header, all lines from the 'origin' and a footer

            recodes the characters according to 'code' : a list of pairs [ [ "xx", "new xx" ] .. ]
            
            
            """

        return self.toFormat(
            line = line,
            index = index,
            item = item,
            origin = origin,
            header = self.headerHtml,
            pattern = self.patternHtml,
            basic = self.basicHtml,
            footer = self.footerHtml,
            anchor = self.anchorHtml,
            link = self.linkHtml,
            void = self.voidHtml,
            code = self.codeHtml,
            html = True
            )

            
        
        return text


    def toString (

        self,
        item = None,
        size = None,
        indent = None,
        prefix = None,
        separator = None,
        ) :

        """ returns the name of an item (string ) or of a list of items (in this case, space-separated words """

        if type( item ) == list :

            text = ""

            i = 0

            if size is None : size = 1

            if indent is None : indent = 0

            if separator is None : separator = ""

            if prefix is None : prefix = ""

            for x in item :

                text = text + prefix

                text = text + self.toString( x, size = size, indent = indent, separator = separator )

                text = text + separator

                i = i + 1

                if not ( i % size ) : text = text + "\n" + indent * "\t"

            return text.strip()

        # none object
        
        if item is None : return ""

        # string : itself

        if type( item ) == str : return item

        # others : finds name

        try :

            return item.__name__

        except Exception, exception :

            return ""
        


    def toTsv (

        self,
        line = None,
        index = None,
        item = None,
        origin = None,
        ) :

        """ converts the matrix ( or a single line ) of items into a tab-separated text
            line, index, item and origin are filters that selects
            - 1 line of the matrix
            - 1 specific line number,
            - the line of an item ( see get()
            - lines from a given origin (internal, external..)

            if no unique line is defined, the text contains a header, all lines from the 'origin' and a footer

            recodes the characters according to 'code' : a list of pairs [ [ "xx", "new xx" ] .. ]
            
            
            """

        return self.toFormat(
            line = line,
            index = index,
            item = item,
            origin = origin,
            header = self.headerTsv,
            pattern = self.patternTsv,
            basic = self.basicTsv,
            footer = self.footerTsv,
            anchor = self.anchorTsv,
            link = self.linkTsv,
            void = self.voidTsv,
            code = self.codeTsv
            )



        


    def write (

        self,
        identifier = None,
        origin = None,
        path = None,
        target = None
        ) :

        """ writes all the documentation in .../_x/

            by default takes current documentation and if it does not exist, builds it.

            when arguments are defined, rebuilds
            
            identifier is an item or a list of items, defined directly or by identifier, e.g.,
            build( x ) or build ( "module.x" )

            origin is a filter on external, internal builtin (default = adds all). it is a string that contains
            the desired keywords, e.g., "internal external"

            path = the path to the application directory. anything in this is considered internal, otherwise external

            target is the target directory where the doc is written


            """

        ok = self.setDocumentation( target )
        
        if not ok : return False

        # full path for documentation

        if ( ( len( self.itemMatrix ) == 0 ) or
             ( not identifier is None ) or
             ( not origin is None ) or
             ( not path is None )
             ) :

            self.build(
                identifier = identifier,
                origin = origin,
                path = path,
                )


        self.writeAscii( self.keywordBuiltin )

        self.writeAscii( self.keywordExternal )

        self.writeAscii( self.keywordInternal )

        self.writeHtml( self.keywordBuiltin )

        self.writeHtml( self.keywordExternal )

        self.writeHtml( self.keywordInternal )

        self.writeTsv( self.keywordBuiltin )

        self.writeTsv( self.keywordExternal )

        self.writeTsv( self.keywordInternal )

        self.writeReadme()

        self.writeErrors()
        

        
    def writeAscii (

        self,
        origin = None
        ) :

        """ writes the ascii file for all items of a given origin

            if origin is "internal", "external", "builtin", creates file ../x/origin.txt

            else places items of any origin in ../x/documentation.txt
            
            """

        if type( origin ) == str : name = self.keywordDocumentation + "_" + origin

        else : name = self.keywordDocumentation

        self.fileWrite(
            self.documentationPath + name + ".txt",
            self.toAscii( origin = origin )
            )
            

        
    def writeErrors ( self ) :


        """ build the text of exceptions and writes it
            
            """

        name = self.keywordDocumentation + "_" + self.keywordErrors

        self.buildErrors()

        self.fileWrite(
            self.documentationPath + name + ".html",
            self.errorsText
            )


        
    def writeHtml (

        self,
        origin = None
        ) :

        """ writes the html file for all items of a given origin

            if origin is "internal", "external", "builtin", creates file ../x/origin.html

            else places items of any origin in ../x/documentation.html
            
            """

        if type( origin ) == str : name = self.keywordDocumentation + "_" + origin

        else : name = self.keywordDocumentation

        self.fileWrite(
            self.documentationPath + name + ".html",
            self.toHtml( origin = origin )
            )
            

        
    def writeReadme (

        self,
        path = None,
        target = None,
        ) :

        """ collects all the readme_* files within the directory and build a single documentation_readme.html

            else places items of any origin in ../x/documentation.html
            
            """

        name = self.keywordDocumentation + "_" + self.keywordReadme

        self.buildReadme(
            path = path,
            target = target
            )

        self.fileWrite(
            self.documentationPath + name + ".html",
            self.readmeText
            )




    def writeTsv (

        self,
        origin = None
        ) :

        """ writes the tab-separated file for all items of a given origin

            if origin is "internal", "external", "builtin", creates file ../x/origin.tsv

            else places items of any origin in ../x/documentation.tsv
            
            """

        
        if type( origin ) == str : name = self.keywordDocumentation + "_" + origin

        else : name = self.keywordDocumentation

        self.fileWrite(
            self.documentationPath + name + ".tsv",
            self.toTsv( origin = origin )
            )
        
        

        
        
        
        

# creates a singleton

if not "documentation" in globals() : documentation = Documentation()



# wrappers for documentation's methods


def build (
    
    item = None,
    origin = None,
    path = None,
    ) :

    """ builds the documentation

        wrapper for documentation's method

        """

    documentation.build( item, origin, path )
    

    
def callExpression ( item ) :

    """ returns the call expression the item (string composed of indented lines )

        wrapper for documentation's method

        """

    return documentation.itemCallExpression( item )




def components ( item ) :

    """ returns the components of the item, i.e., 5 lists: modules, classes, functions, fields, import

        wrapper for documentation's method

        """

    return documentation.itemComponents( item )



def content ( item ) :

    """ returns the content of the item ( list of identifiers )

        wrapper for documentation's method

        """

    return documentation.itemContent( item )




def docstring ( item ) :

    """ returns the in line documentation of the item

        wrapper for documentation's method

        """

    return documentation.itemDocstring( item )



def help ( item ) :

    """ returns a help string on the item.

        wrapper for documentation's method

        """

    return documentation.itemHelp( item )




def hierarchy ( item ) :

    """ returns the hierarchy  ( string composed of indented lines )

        wrapper for documentation's method

        """

    return documentation.itemHierarchy( item )




def imported ( item ) :

    """ returns the imported modules (direct, import xxx or indirect, i.e., uses some item from the module)

        wrapper for documentation's method

        """

    return documentation.itemImported( item )


def localVariables ( item ) :

    """ returns the local variables of the item (for functions and methods items only )

        wrapper for documentation's method

        """

    return documentation.itemLocalVariables( item )

        

def module ( item ) :

    """ returns the module of the item 

        wrapper for documentation's method

        """

    return documentation.itemModule( item )



def name ( item ) :

    """ returns the name of the item.

        wrapper for documentation's method

        """

    return documentation.itemName( item )



def package ( item ) :


    """ returns the package that contains the item 

        wrapper for documentation's method

        """

    return documentation.itemPackage( item )



def path ( item ) :

    """ returns the path to the file where the item is defined ( list of identifiers )

        wrapper for documentation's method

        """

    return documentation.itemPath( item )




def typeName ( item ) :

    """ returns the name of the type of the item.

        wrapper for documentation's method

        """

    return documentation.itemTypeName( item )


def write (
    
    item = None,
    origin = None,
    path = None,
    target = None,
    ) :

    """ writes the documentation to files

        wrapper for documentation's method

        """

    documentation.write( item, origin, path, target )
    
