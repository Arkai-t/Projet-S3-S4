""" Class that handles external applications
 
   
    """


import sys

import os

import ctypes

import imp

import array

import struct

from subprocess import *

import webbrowser

if sys.platform == "linux2" : import fcntl

from api.Utilities import *


class External :


    """ Class that handles external applications
  
        """


    # file extension - command association - load standard, then tries the redefined file and if fails, reloads original

    from command_configuration import *

    try :

        from configuration.command_configuration import *

    except Exception, exception :

        from command_configuration import *


    # list of arguments

    argumentList = None
    
    # child process
    
    childProcess = None

    # current command line

    commandLine = None

##    # communication directory for semaphors
##
##    communicationDirectory = os.curdir
    
    # execution directory
    
    directory = None

    # error message

    error = None

##    # path to error message
##
##    errorPath = None
     

    # handlers of opened files ( must be managed when a subprocess is called )

    handlerList = None

    # path in execution

    path = None

    # previous directory
    
    previousDirectory = None

##    # private stderr object to capture messages
##
##    stderr = None
##

    # lists of contents to update

    updateScriptList = [ ]
        

    

    
    def __init__ (

        self,
        frame = None,
        directory = None,
        ) :

        """ Constructor """

        self.directory = directory

        # empties the handler list (used to maintain the open files blocked, see activate)

        self.handlerList = [ ]

        



    def activate (
        
        self,
        name = None
        ) :

        """ Activates the process "name", 

            opens a file self.directory\\name.ini that cannot be deleted until the end of the process

            returns None if problem or process already active fileHandler otherwise

            Use deactivate to free the file

            """


        if utilities.isEmpty( name ) : return None

        try :

            directory = sys.workPath

            if utilities.isEmpty( directory ) : return None

            fileHandler = utilities.fileOpen( directory + name + ".ini", "wb" )

            if sys.platform == "linux2" : fcntl.lockf( fileHandler, fcntl.LOCK_EX | fcntl.LOCK_NB )

            # adds handler to list of open handlers, so that it has a global reference, and is only freed at exit
            
            self.handlerList.append( fileHandler )

            return fileHandler


        except Exception, exception :

            return None

               


        

    def closeHandlers ( self ) :

        """ Closes all the handlers that are already open """

        if utilities.isEmpty( self.handlerList ) : return

        for handler in self.handlerList :

            try :

                handler.close()

            except Exception, exception :

                continue




    def deactivate (
        
        self,
        name = None
        ) :

        """ Deactivates the process "name", 

            looks in the list of open handlers for the name and close the corresponding one.
            
            returns None if problem or not found, the closed handler otherwise


            """
        
        if utilities.isEmpty( name ) : return None

        directory = sys.workPath

        if utilities.isEmpty( directory ) : return None

        path = directory + name + ".ini"

        if utilities.isEmpty( self.handlerList ) : return None

        for handler in self.handlerList :

            if not handler.name == path : continue

            try :

                handler.close()

                return handler

            except Exception, exception :

                return None

        return None

        

    def deleteMessage (

        self,
        name = None,
        ) :

        """ deletes message in the communication directory for process 'name'

            message is a file self.directory\\name.txt

            deletes it when read

            returns message if OK, None if problem or no message

            """


        if utilities.isEmpty( name ) : return False

        try :

            directory = sys.workPath

            if utilities.isEmpty( directory ) : return False

        except Exception, exception :

            return False

        path = directory + name + ".txt"

        if not utilities.filePresent( path ) : return True

        ok = False

        count = 0

        while True :
               
            ok = utilities.fileDelete( path )

            if ok : break

            count = count + 1

            clock.sleepMs( 100 )

            if count >= 3 :

                utilities.error = "external - deleteMessage failed"

                break

        return ok


        
    def editFile (

        self,
        path = None,
        wait = False
        ) :

        """ Edits a file (document) """

        command = self.pathCommand( path, self.editCommandList )

        if not utilities.isEmpty( utilities.error ) : return False

        result = self.launch(
            command = command,
            wait = wait
            )
            
        return result

        

        

    def executeFile (

        self,
        path = None,
        argument = None,
        wait = False
        ) :

        """ Executes a file 

            Uses executeCommandList to select program

            """

        command = self.pathCommand( path, self.executeCommandList )

        if not utilities.isEmpty( utilities.error ) : return False

        argument = utilities.string( argument )

        if not utilities.isEmpty( argument ) : command = command + ' "' + argument + ' "' # space to avoid escape sequences

        result = self.launch(
            command = command,
            wait = wait
            )

        return result


        

    def executePath (

        self,
        path = None,
        argument = None,
        script = None,
        wait = False
        ) :

        """ Executes a file or the script execute.py* (default) of a directory in an external window """

        # no path
        
        path = utilities.normalizePath( path, normalize = False )
        
        if utilities.isEmpty( path ) : return False

        # this is an URL: opens in browser
        
        if utilities.isUrl( path ) :

            result = self.openUrl( path = path )

            return result

        if utilities.filePresent( path ) :

            script = utilities.pathLastName( path )

            directory = utilities.pathDirectory( path )

        elif utilities.directoryPresent( path ) :

            directory = path

            if utilities.isEmpty( script ) : script = "execute.pyw"

            if not utilities.filePresent( path + os.sep + script ) : return False #**EF was script = execute.pyw

            path = path + os.sep + script

        # path absent
        
        else :

            return False

        # script is execute*.* : completes to make the directory executable

        if script.startswith( "execute" ) : self.updateExecuteFiles( directory )

        # executes

        currentDirectory = utilities.currentDirectory()

        if not currentDirectory == directory : utilities.gotoDirectory( directory )
        
        result = self.executeFile(
            path = path,
            argument = argument,
            wait = wait
            )

        if not currentDirectory == directory : utilities.gotoDirectory( currentDirectory )
        

            
        return result




    def finished (

        self,
        ) :

        """ Checks that the child process is finished, back to previous directory """

        if self.childProcess is None : return True

        poll = self.childProcess.poll()

        if poll is None : return False

        # deletes previous child process
        
        self.childProcess = None
             
        # back to previous directory

        utilities.gotoDirectory( self.previousDirectory )
        
        return True





    def gotoDirectory (

        self,
        directory = None
        ) :

        """ goes to new directory """

        if utilities.isEmpty( directory ) : directory = self.directory

        self.previousDirectory = ""

        if utilities.isEmpty( directory ) : return True

        self.previousDirectory = utilities.currentDirectory()

        ok = utilities.gotoDirectory( directory )

        if not ok :

            self.logMethod(
                software = "External.gotoDirectory",                
                exception = "Could not find path - " + directory,
                )

        return ok

        
##    def getError ( self ) :
##
##        """ gets the error messages """
##
##        try :
##        
##            self.stderr.close()
##
##            self.error = utilities.fileRead( self.errorPath )
##
##        except Exception, exception :
##
##            None
##

    def instantiate (

        self,
        text = None
        ) :

        """ returns the text instantiated, i.e., variables replaced by their value

            """

        if utilities.isEmpty( text ) : return ""

        try :

            text = text.\
                    replace( "(root)", sys.rootPath ).\
                    replace( "(library)", sys.libraryPath ).\
                    replace( "(configuration)", sys.configurationPath )

        except Exception, exception :

            None

        text = text.\
                replace( os.altsep, os.sep ).\
                replace( os.sep + os.sep, os.sep )

        return text



    def isActive (
        
        self,
        name = None
        ) :


        """ Checks whether a script identified by its name is launched

            verifies whether there is a file directory\\_name.ini that is currently blocked
            ( cannot be deleted )


            """

        if utilities.isEmpty( name ) : return False

        try :

            directory = sys.workPath

            if utilities.isEmpty( directory ) : return False

        except Exception, exception :

            return False
       
        path = directory + os.sep + name + ".ini" 

        if not utilities.filePresent( path ) : return False

        # linux : tries to lock the file

        if sys.platform == "linux2" :

            try :

                fileHandler = file( path, "w" )

                fcntl.lockf( fileHandler, fcntl.LOCK_EX | fcntl.LOCK_NB )

                fcntl.lockf( fileHandler, fcntl.LOCK_UN )

                return False

            except Exception, exception :

                return True

        # windows : tries to delete

        else : 
        
            result = utilities.fileDelete( path )

            return not result


              



    def launch (

        self,
        command = None,
        wait = False
        ) :

        """ Launches a path and/or executes a command """

        if not self.finished() :

            self.logMethod(
                software = "External.launch",                
                exception = "previous process not finished",
                )

            return False
            
            
        if utilities.isEmpty( command ) : command = ""

        # no child process for now

        self.childProcess = None

        # parses the command line

        self.parseCommand( command )

        if utilities.isEmpty( self.argumentList ) :

            self.logMethod(
                software = "External.launch",                
                exception = "Empty command line",
                )

            return False


        # space in first argument (name of executable file) : not allowed

        if " " in self.argumentList[ 0 ] :

            self.logMethod(
                software = "External.launch",
                exception = "space in file name not allowed - " + self.argumentList[ 0 ]
                )

            return False

        # this is a URL

        if utilities.isUrl( self.path ) : result = self.launchUrl()

        # this is a command

        else : result = self.launchCommand( wait = wait )

        return result

        



    def launchCommand (

        self,
        commandLine = None,
        directory = None,
        wait = False
        ) :

        """ launches a command in the given directory """

        if utilities.isEmpty( commandLine ) : commandLine = self.commandLine

        if utilities.isEmpty( directory ) : directory = self.directory
        
        # changes to new directory

        ok = self.gotoDirectory( directory )

        if not ok : return False

        # closes the open handlers during the call, so that they are not shared by the child process

        self.closeHandlers()

        # clears the cache (some files may be modified externally)

        dircache.reset()


        # executes (and captures any exception )

##        print "External.launchCommand dir", directory, "\n    command", commandLine

        try :

            childProcess = Popen(
                commandLine,
                shell = True,
                )

            result = True           

        except Exception, exception :

            self.logMethod(
                software = "External.launch",                
                exception = exception,
                )

            result = False

        # reopens the file handlers

        self.openHandlers()

        # back to former directory if there is one

        ok = self.restoreDirectory()

        if not ok : return False
                    
        # if required, keeps track of the external process
        
        if bool( wait ) : self.childProcess = childProcess
      
        return result



    def launchUrl (

        self,
        url = None
        ) :

        """ opens a URL in an external browser """

        if utilities.isEmpty( url ) : url = self.path

        try :

            webbrowser.open( url, new = 1 )

            return True

        except Exception, exception :

            self.logMethod(
                software = "External.launch",                
                exception = exception,
                )

            return False
    

        
    def loadLibrary (

        self,
        path = None,
        call = "c"
        ) :

        """ loads a library from a C dynamic library (.dll or .so file)

            The default calling convention is cdll (libraries generated typically from ansi C).

            The other convention is stdcall (typically C++ files)
            
            """

        path = utilities.pathDirectoryName( path )

        if utilities.isEmpty( path ) : return None

        # extension depends on OS (for linux: SO ; for windows: DLL, automatic)

        if sys.platform == "linux2" : path = path + ".so"

        elif sys.platform == "win32" : path = path + ".dll"

        # loader depends on call convention, default = cdecl

        # cdecl convention

        if call == "c" : loader = ctypes.cdll

        elif call == "win" : loader = ctypes.windll

        elif call == "ole" : loader = ctypes.oledll

        else : loader = ctypes.cdll

        try :

            library = loader.LoadLibrary( path )

        except Exception, exception :

            self.logMethod(
                software = "External.loadLibrary",                
                exception = exception,
                )

            return None

        return library

    

        
    def loadModule (
        
        self,
        path = None,
        identifier = None
        ) :

        """ Loads a module from a file and imports it, i.e. adds it to sys.module

            identifier is the name of the module in sys.modules. By default it is the file name, 
    
            Returns the module  or None in case of problem

            Remark. The internal name of the module is the name of the file, this is invisible from outside.
        
            Example of use :

            myModule = loadModule( "c:\\toto\\titi.py" )
        
            myModule.go() or eval ("titi" ).go()

            del ( myModule )

            """


        utilities.error = ""

        path = utilities.normalizePath( path, normalize = False )

        if path is None : return None

        if identifier is None : identifier = utilities.pathName( path )

        # filters identifier as valid module name (submodules a.b.c are  paths a/b/c/, not xxx/a.b.c.py)

        for char in identifier :

            if ( ( not char.isalnum() ) and ( not char == "_" ) ) : identifier = identifier.replace( char, "_" )

        identifier = utilities.string( identifier, format = "strictunderscore" )

        extension = utilities.pathExtension( path )

        if not extension.startswith( "py" ) : return None

        if not utilities.filePresent( path ) : return None

        try :

            module = imp.load_source( identifier, path )

        except Exception, exception :

            self.logMethod(
                software = "External.loadModule",                
                exception = exception,
                )

            return None

        return module

    
        


    def logMethod (

        self,
        software = "External",
        exception = None
        ) :

        """ Writes an error in log, sets error message """

        utilities.error = str( exception )





    def openDirectory (

        self,
        path = None,
        wait = False
        ) :

        """ Loads a directory with explorer in a new shell. Uses self.openCommandList to select program  """


        path = utilities.normalizePath( path, normalize = False )
       
        if utilities.isEmpty( path ) : return False

        if utilities.filePresent( path ) : path = utilities.pathDirectory( path )

        command = self.pathCommand(
            path,
            commands = self.openCommandList,
            extension = "directory"
            )

        if not utilities.isEmpty( utilities.error ) : return False

        result = self.launch(
            command = command,
            wait = wait
            )
            
        return result



        
    def openFile (

        self,
        path = None,
        wait = False
        ) :

        """ Loads a file (document) in a new shell. Uses openCommandList to select program  """

        command = self.pathCommand( path,self.openCommandList )

        if not utilities.isEmpty( utilities.error ) : return False

        result = self.launch(
            command = command,
            wait = wait
            )
                    
        return result




    def openHandlers ( self ) :

        """ Re-opens all the handlers that are already open """

        if utilities.isEmpty( self.handlerList ) : return

        for index in range( len( self.handlerList ) ) :

            handler = self.handlerList[ index ]

            try :

                path = handler.name

                mode = handler.mode

                self.handlerList[ index ] = open( path, mode )

            except Exception, exception :

                None



    def openPath (

        self,
        path = None,
        wait = False
        ) :

        """ Loads a file (document) in a new shell. Uses openCommandList to select program  """

        path = utilities.normalizePath( path, normalize = False )
        
        if utilities.isEmpty( path ) : return False

        if utilities.isUrl( path ) :

            result = self.openUrl( path = path )

        elif utilities.filePresent( path ) :

            result = self.openFile(
                path = path,
                wait = wait )

        else :

            result = self.openDirectory(
                path = path,
                wait = wait )

            
        return result




    def openUrl (

        self,
        path = None
        ) :

        """ Loads a url in default browser. Does not wait  """

        result = self.launch( command = path )
                    
        return result



    def pack (

        self,
        value = None,
        result = None,
        size = None,
        ) :

        """ prepares a byte-wise array for calling a C function (see loadLibrary ).

            the array will be used by the C function to place its result.

            the size of the array is 'size' or by default, the size of value in bytes (it cannot be smaller than that).

            The array contains the argument "value" ( a list, or transformed into a list), bytewise

            The argument "result" can point on a preexisting array, so that there is no memory allocation

            returns a pointer to an array of "size"  bytes containing the values of the list "value"

            

            """

        if value is None : value = [ ]

        elif not isinstance( value, list ) : value = [ value ]

        packed = ""

        for item in value :

            if type( item ) == str : None

            elif type( item ) == bool : item = struct.pack( "i", item )

            elif type( item ) == int : item = struct.pack( "i", item )

            elif type( item ) == float : item = struct.pack( "d", item )

            else : continue

            packed = packed + item

        # array of bytes large enough to contain the value

        sPacked = len( packed )
            
        size = utilities.integer( size, default = sPacked )

        size = max( size, sPacked )

        # tries whether the argument result is an array, sufficiently large

        try :
            
            pointer, sResult = result.buffer_info()

        except Exception, exception :

            sResult = 0

        if sResult < size :

            result = array.array( "c", size * [ chr( 0 ) ] )
            
            pointer, sResult = result.buffer_info()


        # copies the value

        for index in range( sPacked ) :

            result[ index ] = packed[ index ]
            

        return pointer, size


        


    def parseCommand (

        self,
        command = None
        ) :

        """ parses the command and builds a command line, a list of arguments, an execution directory and a path to execute

            returns self.directory (where to execute) self.commandLine, self.argumentList, self.path

            """

        self.directory = ""

        self.argumentList = [ ]

        self.commandLine = ""

        self.path = ""

        # parses the command into words. quotes are separate words


        words = self.textToWords( command )

        if utilities.isEmpty( words ) : return

        for word in words :

            word = word.strip( " \"'" )

            if " " in word : self.argumentList.append( '"' + word + '"' )

            else : self.argumentList.append( word )

        # special case for word[ 0 ]

        self.path = utilities.normalizePath( self.argumentList[ 0 ].strip( " \"'" ), normalize = False )

        # this is a URL: nothing more
        
        if utilities.isUrl( self.path ) : return

        # the file exists : will execute it in the same directory ( avoids trouble with spaces in path name )
        
        if utilities.filePresent( self.path ) :

            self.directory = utilities.pathDirectory( self.path )

            self.path = os.curdir + os.sep + utilities.pathLastNameWithExtension( self.path )

        # otherwise (e.g., path = "explorer.exe" that is anywhere ) "goes as close as possible"
        
        else :

            self.directory = utilities.closestDirectory( self.path )

            # truncates the path to the file name
            
            self.path = self.path[ len( self.directory ) : ]

        # first argument = name of file

        self.argumentList[ 0 ] = self.path

        # flattens the command again
            
        self.commandLine = utilities.wordsToText( self.argumentList )
        

      

        
    def pathCommand (

        self,
        path = None,
        commands = None,
        extension = None
        ) :

        """ Returns the command corresponding to the extension of path in the list """

        utilities.error = ""
        
        if utilities.isEmpty( path ) : return None

        path = path.strip( " \"'" )

        # dafault commands = open
        
        if utilities.isEmpty( commands ) : commands = self.openCommandList

        if utilities.isEmpty( commands ) : return None

        # url

        if utilities.isUrl( path ) : return path

        # look for extension in the list of commands

        path = utilities.normalizePath( path, normalize = False )
       
        if extension is None : extension = utilities.pathExtension( path )

        if " " in path : path = '"' + path + '"'

        index = utilities.index( commands, extension )

        if index < 0 : return path

        prefix = utilities.osPath( self.instantiate( commands[ index + 1 ] ) )

        if utilities.isEmpty( prefix ) : return path

        # normalizes the quotes of prefix, separates them from the words
        
        prefix = prefix.replace( "'", '"' ).replace( '"', ' " ' )

        # adds the path or replaces in the command line

        if "%1" in prefix : command = prefix.replace( "%1", " " + path + " " )

        else : command = prefix + " " + path

        return command
        


    def receiveMessage (

        self,
        name = None,
        ) :

        """ receives message in the communication directory for process 'name'

            message is a file self.directory\\name.txt

            deletes it when read

            returns message if OK, None if problem or no message

            """


        if utilities.isEmpty( name ) : return None

        try :

            directory = sys.workPath

            if utilities.isEmpty( directory ) : return None

        except Exception, exception :

            return None


        path = directory + name + ".txt"

        if not utilities.filePresent( path ) : return None
               
        text = utilities.fileRead( path )

        ok = self.deleteMessage( name )

        if not ok : return None
        
        return text



    def repeatScript (

        self,
        path = None,
        result = None
        ) :

        """ repeats a python script while the result is "result" (default 3).

            the result is given by the exit instruction, sys.exit() or os._exit()

            with normal exit ( 0 ), the script is not repeated

            WARNING: path must not contain spaces, special characters or quotes

            """

        if not utilities.pathPresent( path ) : return result

        result = utilities.integer( result, default = 3 )

        # directory, name of the current python interpreter
        
        directory, name = os.path.split( sys.executable )

        while True :
    
            value = os.spawnv( os.P_WAIT, sys.executable, [ name, path ] )

            if not value == result : return value

        # normally, never goes here
        
        return result



        
    def reset ( self ) :

        """ Clears persistence, resets child process """

        self.childProcess = None



    def restoreDirectory ( self ) :

        """ back to original directory if there is one """

        if utilities.isEmpty( self.previousDirectory ) : return True

        ok = utilities.gotoDirectory( self.previousDirectory )

        if not ok :

            self.logMethod(
                software = "External.launch",                
                exception = "Could not find directory - " + self.previousDirectory,
                )

        return ok
        


    def sendMessage (

        self,
        name = None,
        text = None
        ) :

        """ sends a message in the communication directory to the process 'name'

            creates a file self.directory\\name.txt

            returns True if creation is ok

            """


        if utilities.isEmpty( name ) : return False

        try :

            directory = sys.workPath

            if utilities.isEmpty( directory ) : return False

        except Exception, exception :

            return False

        ok = False

        count = 0

        while True :
               
            ok = utilities.fileWrite( directory + name + ".txt", utilities.string( text, default = "" ) )

            if ok : break

            count = count + 1

            clock.sleepMs( 100 )

            if count >= 3 :

                utilities.error = "external - sendMessage failed 3 attempts"

                break

##        print "external.sendMessage(",text,") ", ok #**EF

        return ok





    def system (

        self,
        commandLine = None,
        directory = None,
        ) :

        """ launches a command in the given directory """

        if utilities.isEmpty( commandLine ) : commandLine = self.commandLine

        if utilities.isEmpty( directory ) : directory = self.directory

        # clears the cache (some files may be modified externally)

        dircache.reset()

        # changes to new directory

        ok = self.gotoDirectory( directory )

        if not ok : return False

        # executes (and captures any exception )

        try :

            os.system( commandLine )

            result = True           

        except Exception, exception :

            self.logMethod(
                software = "External.system",                
                exception = exception,
                )

            result = False

        # back to former directory if there is one
        
        ok = self.restoreDirectory()

        if not ok : return False

        return result




    def textToWords (

        self,
        command = None
        ) :

        """ Converts a command into a list of arguments. the command may contain quotes """

        if utilities.isEmpty( command ) : return [ ]

        # normalizes the quotes within the command line ( only ", and separated by spaces )
        
        command = command.replace( "'", '"' ).replace( '"', ' " ' )
        
        # splits into words, the quotes are now separate words
        
        items = command.split()

        word = ""

        quote = False

        words = [ ]

        # parses and groups the words within quotes.
        
        for item in items :

            item = item.strip()

            # empty word

            if utilities.isEmpty( item ) : continue

            # a quote : writes current word ( if not empty ) and toggles state

            if item == '"' :

                word = word.strip()

                if not utilities.isEmpty( word ) : words.append( word )

                word = ""

                quote = not quote                

            # normal word within a quote : appends to current word, does not append to list yet

            elif bool( quote ) :

                word = word + " " + item

            # normal word out of a quote, appends a new word to list

            else :

                word = ""

                words.append( item )


        return words




    def unpack (

        self,
        value = None,
        result = None,
        ) :

        """ gets a list of values from a byte-wise array 'result' produced by a C function (see loadLibrary)

            uses the same variable value to store the results, so that there is no memory allocation

            returns value (normally, a pointer to the argument)
            

            """

        if result is None : return [ ]

        if value is None : return [ ]

        if not isinstance( value, list ) : value = [ value ]

        iResult = 0

        for iList in range( len( value ) ) :

            item = value[ iList ]

            if type( item ) == str :

                length = len( item )

                format = str( length ) + "s"

            elif type( item ) == int :

                length = struct.calcsize( "i" )

                format = "i"

            elif type( item ) == float :
            
                length = struct.calcsize( "d" )

                format = "d"

            else : continue

            try :

                value[ iList ] = struct.unpack( format, result[ iResult : iResult + length ] )[ 0 ]

            except Exception, exception :

                None
                
            iResult = iResult + length

        return value

                



    def updateExecuteFiles (

        self,
        path = None,
        forced = False,
        delete = False
        ) :

        """ updates the files of a procedure """

##        libraryModifiedTime = 0

        if utilities.isEmpty( self.procedureFileList ) : return False

        if not utilities.directoryPresent( path ) : return False

        previousSelected = utilities.getVariable( "selected", default = "" )

        utilities.setVariable( "selected", utilities.normalizePath( path + os.sep, normalize = False ) )

##        print "external.update execute files"
        
        for i in range( 0, len( self.procedureFileList ), 2 ) :

            target = path + os.sep + self.instantiate( self.procedureFileList[ i ] )

            if bool( delete ) :

                utilities.pathDelete( target )

            elif ( ( bool( forced ) ) or ( not utilities.pathPresent( target ) ) ) :

                source = self.instantiate( self.procedureFileList[ i + 1 ] )

    ##            print "  ", utilities.pathName( source ), target

                utilities.pathCopy(
                    source,
                    target,
                    filter = True
                    )
        
        # restores the selected value

        utilities.setVariable( "selected", previousSelected )

        return True





    def updateStandaloneFiles (

        self,
        path = None,
        forced = False,
        delete = False,
        ) :

        """ copies or removes the files that make a procedure standalone """

##        libraryModifiedTime = 0

        if utilities.isEmpty( self.standaloneFileList ) : return False

        if not utilities.directoryPresent( path ) : return False

        previousSelected = utilities.getVariable( "selected", default = "" )

        utilities.setVariable( "selected", utilities.normalizePath( path + os.sep, normalize = False ) )

##        print "external.update execute files"
        
        for i in range( 0, len( self.standaloneFileList ), 2 ) :

            target = path + os.sep + self.instantiate( self.standaloneFileList[ i ] )

            if bool( delete ) :

                utilities.pathDelete( target )

                continue

            elif ( ( bool( forced ) ) or ( not utilities.pathPresent( target ) ) ) :

                source = self.instantiate( self.standaloneFileList[ i + 1 ] )

##            print "  ", utilities.pathName( source ), target

                utilities.pathCopy(
                    source,
                    target,
                    filter = True
                    )
        

        # restores the selected value

        utilities.setVariable( "selected", previousSelected )


        

    def viewFile (

        self,
        path = None,
        wait = False
        ) :

        """ Loads a file in a viewer

            Uses viewCommandList to select program

            """


        command = self.pathCommand( path, self.viewCommandList )

        if not utilities.isEmpty( utilities.error ) : return False

        result = self.launch(
            command = command,
            wait = wait
            )
            
        return result


        

    def wait ( self ) :

        """ Waits until external process is finished """

        while not self.finished() :

            clock.sleepMs( 100 )

            
        
# -----------------------------------
# creates the global singleton object if not already here
#

if not "external" in globals() : external = External()
         
        
