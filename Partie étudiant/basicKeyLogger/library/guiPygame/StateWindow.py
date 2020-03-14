#!

""" window that behaves like a finite-state automaton. In Pygame """

import os

import sys

import time

import pygame


class StateWindow :

    """ window that behaves like a finite-state automaton. In Pygame """


    # list of background colors for each state

    backgroundList = None

    # error message

    error = None
    
    # font used for messages

    font = None

    # list of text colors for each state

    foregroundList = None

    # list of window icons for each state

    iconList= None

    # program name

    program = None

    # initial icon

    startIcon = None

    # list of state names

    stateList = None

    # list of internal texts for each state

    textList = None

    # title of window

    title = None

    # version

    version = None

    # window displayed when logger active

    window = None

    # size of window

    windowSize = None

    # initial state

    windowState = None

    # identifier of event source in the window manager

    windowManagerIdentifier = None
    


    def __init__ ( self ) :


        """ Constructor """

        self.setTitle()

        self.loadIcons()




    def createWindow ( self ) :

        """ creates the window

            captures exceptions, in case another application uses SDL in exclusive mode

            """
        
        try :

            # window title and icon BEFORE the window is created otherwise icon does not appear in maximized window

            pygame.display.set_caption( self.title )

            pygame.display.set_icon( self.startIcon )

            # creates the window and displays it. May fail if another application uses SDL in exclusive mode

            self.window = pygame.display.set_mode( self.windowSize )

            return True

        except Exception, exception :

            return False

        

    def directoryContent (

        self,
        path = None
        ) :

        """ returns the content of the directory (entry names without path or empty list ) """

        path = self.normalizePath( path )

        if path is None : return [ ]

        if not os.path.isdir( path ) : return [ ]

        return os.listdir( path )

    
            
    def directoryCreate (

        self,
        path = None
        ) :

        """ creates a directory. returns True iff ok """
        
        if path is None : return False

        if self.directoryPresent( path ) : return True

        try :

            os.makedirs( path )

            return True

        except Exception, exception :

            return False



        
    def directoryPresent (

        self,
        path = None
        ) :

        """ Checks whether the directory "path" is here. Version of os.path.isdir that handles empty or void arguments.

            Returns True if present False if absent or any other problem

            """
        
        if path is None : return False

        elif path == "" : return True
        
        else : return os.path.isdir( path ) 




    def displayWindow (

        self,
        state = None
        ) :

        """ Creates a main window and minimizes it """


        # identifier of the current window in the OS window manager
        
        self.windowManagerIdentifier = "?"

        # tries to initialize display

        ok = self.initDisplay()

        if not ok : return False
        
        # creates the window

        ok = self.createWindow()

        if not ok : return False

        # configures it in desired state

        if state is None : state = "start"

        ok = self.setWindow( state )
        
        if not ok : return False

        # captures exceptions, in case another application uses SDL in exclusive mode
        
        try :

            # no uncaptured closing of the window

            pygame.event.set_blocked( pygame.QUIT )

            # identifier in the window manager

            self.windowManagerIdentifier = pygame.display.get_wm_info()[ "window" ]

        except Exception, exception :

            return False
        

        return True


    

    def endDisplay ( self ) :

        """ ends the display, i.e., pygame """
        try :

            pygame.quit()

            return True

        except Exception, exception :

            return False






    def fileClose (

        self,
        fileHandler = None
        ) :
        

        """ Version of file.close() that throws no exception and accepts void arguments.

            Returns True is OK, false if any exception or problem occurred.
        
            """

        if fileHandler is None : fileHandler = self.fileHandler
        
        if fileHandler is None : return True
        
        try :

            fileHandler.close()

        except Exception, exception :
            
            return False

        return True




    def fileOpen (
        
        self,
        path = None,
        mode = None
        ) :
        
        """ Version of file() or open() that throws no exception, and accepts empty or undefined arguments.

            Returns None or the file handle

            
        """

        if path is None : path = self.logPath
        
        if path is None : return None
        
        if mode is None : mode = "r"
            
        try :

            fileHandler = file( path, mode )

        except Exception, exception :
            
            return None

        return fileHandler




    def filePresent (
        
        self,
        path = None
        ) :

        """ Checks whether the file "path" is here. Version of os.path.isfile that accepts empty or void arguments.

            Returns True if present False if absent or any other problem

            """

        
        if self.isEmpty( path ) : return False
        
        return os.path.isfile( path )






    def fileRead (
        
        self,
        path = None
        ) :

        """ Reads the file "path"

            Returns the content as a string

            """

        
        handler = self.fileOpen( path, "rb" )

        if handler is None : return ""

        try :

            text = handler.read()

        except Exception, exception :

            text = ""

        self.fileClose( handler )
        
        return text


                



    def loadIcon (

        self,
        path = None
        ) :

        """ loads an icon from a path.

            Returns a Pygame Surface or None in case of problem or the argument if it is not a string (e.g., already loaded )

            """

        if not type( path ) == str : return path

        path = self.normalizePath(path )

        if path is None : return None

        try :

            return pygame.image.load( path )

        except Exception, exception :

            return None

        



    def loadIcons ( self ) :

        """ loads the icons from the paths contained in the list """

        if self.iconList is None : self.iconList = [ ]

        if self.stateList is None : self.stateList = [ ]

        ok = True

        for index in range( len( self.iconList ) ) :

            self.iconList[ index ] = self.loadIcon( self.iconList[ index ] )

            if self.iconList[ index ] is None : ok = False

        # determines start icon

        self.startIcon = None

        try :

            self.startIcon = self.iconList[ self.stateList.index( "start" ) ]

        except Exception, exception :

            if len( self.iconList ) > 0 : self.startIcon = self.iconList[ 0 ]

            else : ok = False
            

        return ok
                   
        


        

    def initDisplay ( self ) :

        """ initializes pygame 3 attempts """

        count = 8

        while True :

            try :

                pygame.init()

                if not bool( pygame.display.get_init() ) : continue

                if not bool( pygame.joystick.get_init() ) : continue

                if not bool( pygame.font.get_init() ) : continue

                return True

            except Exception, exception :

                return False

            count = count - 1

            if count <= 0 : return False

            time.sleep( 0.2 )

        return False





    def isEmpty (

        self,
        text = None
        ) :

        """ Returns True iff the argument is a non empty string or sequence """

        if text is None : return True

        try :

            return len( text ) <= 0

        except Exception, exception :

            return True




    
    def isIndex (

        self,
        index = None,
        text = None
        ) :

        """ Returns True iff the first argument is a correct index of the second, list/string, or sequence """

        if not type( index ) == int : return False

        if self.isEmpty( text ) : return False

        if index < 0 : return False

        if index >= len( text ) : return False

        return True



    def mouseHandler (

        self,
        name = None,
        origin = None
        ) :

        """ processes a mouse event, i.e., empties the thread of the window

            if event needs to close the application, returns True otherwise False

            """
        
##        print "StateWindow.mouseHandler", name, origin

        try :
        
            # no window initialized

            if not pygame.display.get_init() : return False

            # dispatches the pygame events ( otherwise overflow )

            pygame.event.pump()

            # this is NOT in the basic lab book window

            if not self.windowManagerIdentifier == origin : return False

            # this is NOT a mouse click

            if not name.endswith( "up" ) : return False

            # this is NOT a mouse click in the display region

            x, y = pygame.mouse.get_pos()

            if ( x <= 0 ) or ( y <= 0 ) : return False

            # here, must close the window
            
            return True

        except Exception, exception :

            return False


        


    def normalizePath (

        self,
        path = None
        ) :

        """ normalizes a path,

            replaces variables (root), (library) and (configuration) and makes the path absolute

            returns a normalized path or None in case of problem

            """

        try :

            path = str( path ).\
                        replace( "(root)", sys.rootPath ).\
                        replace( "(library)", sys.libraryPath ).\
                        replace( "(configuration)", sys.configurationPath ).\
                        replace( os.altsep, os.sep ).\
                        replace( os.sep + os.sep, os.sep )

            path = os.path.abspath( os.path.expanduser( path ) )
            
        except Exception, exception :

            path = None

        return path

        

        


    def setTitle ( self ) :


        """ sets the title of the window from program and version """

        if self.program is None : self.program = ""

        if self.version is None : self.version = ""

        self.title = self.program + " " + self.version

        return True
    
        
        
        
    def setWindow (

        self,
        state = None,
        ) :

        """ sets the background color, icon and internal text of the window as a function of the state.

            uses the state argument to find color, icon, text and whether iconified or not in lists.


            captures exceptions, in case another application uses SDL in exclusive mode

            """


        if self.window is None : return False

        if self.stateList is None : return False

        if not state in self.stateList : return False

        index = self.stateList.index( state )

        ok = True
        
        # iconifies or not

        if self.isIndex( index, self.minimizeList ) :  minimize = self.minimizeList[ index ]

        else : minimize = None


        # icon
    
        if self.isIndex( index, self.iconList ) : icon = self.iconList[ index ]

        else : icon = None


        # background color
    
        if self.isIndex( index, self.backgroundList ) : background = self.backgroundList[ index ]

        else : background = None

        # text

        if self.isIndex( index, self.textList ) :

            text = self.textList[ index ]

            # instantiates. uses truncated version of the paths and error message.

            if self.error is None : error = ""

            else : error = str( self.error )

            if len( error ) > 40 : error = error[ : 40 ] + "..." 

            rootPath = sys.rootPath

            if len( rootPath ) > 40 : rootPath = rootPath[ : 20 ] + "..." + rootPath[ -20 : ]

            libraryPath = sys.libraryPath

            if len( libraryPath ) > 40 : libraryPath = libraryPath[ : 20 ] + "..." + libraryPath[ -20 : ]
            
            configurationPath = sys.configurationPath

            if len( configurationPath ) > 40 : configurationPath = configurationPath[ : 20 ] + "..." + configurationPath[ -20 : ]

            text = text.\
                replace( "(error)", error ).\
                replace( "(root)", rootPath ).\
                replace( "(library)", libraryPath ).\
                replace( "(configuration)", configurationPath ).\
                replace( os.altsep, os.sep ).\
                replace( os.sep + os.sep, os.sep )


        else :

            text = None

        # foreground color

        if self.isIndex( index, self.foregroundList ) : foreground = self.foregroundList[ index ]

        else : foreground = None
        

        # iconifies if required
        
        try :        

            if bool( minimize ) : pygame.display.iconify()

        except Exception, exception :

            ok = False


        # sets icon
        
        try :
            
            if not icon is None : pygame.display.set_icon( icon )

        except Exception, exception :

            ok = False
            

        # sets background color
        
        try :
                            
            if not background is None : self.window.fill( background )

        except Exception, exception :

            ok = False

        try :

            if not text is None :

                if self.font is None : self.font = pygame.font.SysFont( self.fontName, self.fontSize, self.fontBold, self.fontItalic )

                if background is None : background = [ 0, 0, 0 ]

                if foreground is None : foreground = [ 255, 255, 255 ]

                text = self.font.render( str( text ), 1, foreground, background )

                self.window.blit( text, [ 16, 0 ] )

        except Exception, exception :

            ok = False

        # refreshes display
        
        try :

            pygame.display.update()

        except Exception, exception :

            ok = False

        return True

        

    


    def waitClick (

        self,
        close = False,
        ) :

        """ waits for a click.

            If close is True, exits

            else returns the event type (integer, see pygame.events )

            """

        try :

            # no uncaptured closing of the window

            pygame.event.set_allowed( pygame.QUIT )

            while True :

                for event in pygame.event.get() :

                    if not bool( close ) : return event.type

                    if ( event.type == pygame.MOUSEBUTTONUP ) or ( event.type == pygame.QUIT ) :

                        pygame.quit()

                        sys.exit( 0 )

                # frees the CPU
                
                time.sleep( 0.05 )

                    

        except Exception, exception :

            if bool( close ) : sys.exit( 0 )
            

        return False


    def waitDelay (

        self,
        close = False
        ) :

        """ waits for warningS seconds, then closes application if required """


        time.sleep( self.warningS )

        if bool( close ) :

            pygame.quit()

            sys.exit( 0 )
        




