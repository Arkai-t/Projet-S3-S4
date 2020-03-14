""" Class that determines execution context, organization, lists, etc.

    Based on self-detection in order to avoid environment variables and complex setups
 
   
    """

# graphical toolkit ( default is tkinter ) or none

try :

    import Tkinter
    
except Exception, exception :

    None
    

# standard python modules

import os

import imp

import glob

import random

import sys

import time

# API

from api.Utilities import *

# singletons

from api.Archiver import *

from api.BibFile import *

from api.Clock import *

from api.External import *

from api.Logger import *

from api.Statistics import *

from api.Librarian import *

from api.TableFile import *

from api.XmlFile import *

from api.Html import *


# superclasses

from api.Paths import *

from api.Messages import *

from api.Rights import *

from api.Types import *

from api.Variables import *


  
class Context ( \
    Paths,  # must go first (initializes attributes before calling constructor )
    Messages,
    Rights,
    Types,
    Variables 
    ) :


    """ Class that determines execution context, organization, lists, etc.

        Based on self-detection in order to avoid environment variables and complex setups

        """

    # error message

    error = None

        
    # general configuration - loads standard, then tries the redefined file and if fails, reloads original

    from context_configuration import *

    try :

        from configuration.context_configuration import *

    except Exception, exception :

        from context_configuration import *



    # general information - loads standard, then tries the redefined file and if fails, reloads original

    from information_configuration import *

    try :

        from configuration.information_configuration import *

    except Exception, exception :

        from information_configuration import *




    # time constants - loads standard, then tries the redefined file and if fails, reloads original

    from time_configuration import *

    try :

        from configuration.time_configuration import *

    except Exception, exception :

        from time_configuration import *



        
   
    def __init__ ( self ) :

        """ Constructor. finds the organization and the root path

            root and keywords are optional. They overwrite the root path and the path to keywords file, respectively.
            
            """

        # links utilities to current context singleton and to clock singleton
        
        utilities.context = self 


        # creates a frame, a label a button

        self._createBootWindow()


        try :

            utilities.driveList = self.driveList

        except Exception, exception :

            None


        # inserts variables with capitalized messages
        
        self.addCapitalizedMessages()





        # access rights
        
        utilities.error = None

        self.loadRights()
        
        if not utilities.isEmpty( utilities.error ) : self._bootError( utilities.error )


        # types
        
        self.loadTypes()
        
        if not utilities.isEmpty( utilities.error ) : self._bootError( utilities.error )


        # time constants

        try :
        
            clock.defaultPeriodMs = self.clockPeriodMs

            clock.periodMs = self.clockPeriodMs

        except Exception, exception :

            None





        # variables

        # loads variables and completes list
        
        self.loadVariables()

        self.completeVariables()

        if not utilities.isEmpty( utilities.error ) : self._bootError( utilities.error )

        # reads variables value from persistence file
        
        self.readWorkVariables()

        utilities.error = ""    # resets, in case the file does not exist

        # sets variables from the constants & parameters

        self.setConfigurationVariables()
      
        # end of init : deletes message window

        self._deleteBootWindow()

        # random seed

        random.seed( clock.clockMs() )

        




    def _bootError (

        self,
        text = None
        ) :

        self._message( "Error : " + text, dots = False )

        # graphical interface : enters the main loop of popup. Goes out only when button is pressed

        if not self._popup is None :
            
            self._popup.button.grid(
                padx = 5,
                pady = 5
                )
            
            self._popup.mainloop()
        
        # no graphical interface : waits for a character

        else :

            raw_input( "press any key" )
            


    def _bootPressButton ( self ) :

        """ Handler of button """

        sys.exit( 1 )

          


        






        
        
    def _createBootWindow ( self ) :

        """ A simple popup window """

        # creates a frame and gets its top level window (if we create directly toplevel, it will appear decorated)

        self._popup = None

        # tries to create a popup window
        
        try :
            
            frame = Tkinter.Frame( )

            self._popup = frame.winfo_toplevel()
            
            # configurates top level
            
            self._popup.config(
                border = 2,
                background = "grey",
                relief = "groove"
                )

            # decorations ( title, close buttons, etc. ) are removed

            self._popup.overrideredirect( 1 )

            # shifted towards the center

            self._popup.geometry( "+256+256" )          
                        
            self._popup.label = Tkinter.Label(
                frame,
                font = "Arial 10",
                background = "#C8C8C8C8F8F8",   # light blue
                wraplength = 64,                # max chars per line
                text = "..."
                )

            self._popup.label.grid(
                padx = 32,
                pady = 32
                )


            self._popup.button = Tkinter.Button(
                frame,
                text = "Press me",
                background = "cyan",
                font = "Arial 10 bold",
                command = self._bootPressButton
                )

            # places the frame in top level

            frame.grid()

        except Exception, exception :

            None


        

        
    def clearPersistenceFiles ( self ) :

        """ Deletes the persistence files. """

        self._clearTypePersistenceFile()



       

    def _deleteBootWindow ( self ) :

        """ Deletes the message window and its components """

        if not self._popup is None :

            self._popup.destroy()

            self._popup = None
        
        


    def end ( self ) :

        """ Ends execution. Called when main window is closed """

        # stops all timers
        
        clock.stopAll()

        # saves context variables into persistence file.

        self.writeWorkVariables()

        # closes handlers

        external.closeHandlers()
        



        
    def _message (

        self,
        text = None,
        dots = True
        ) :

        """ Message in boot window """

        if utilities.isEmpty( text ) : return


        # sets text in label

        text = utilities.string( self.program + " - " + text, format = "title" )

        if dots : text = text.rstrip( "." ) + " ..."

        # there is a graphical window : updates label, lifts window above stack, updates window

        if not self._popup is None :
            
            self._popup.label.config( text = text )

            self._popup.label.update()
            
            self._popup.lift()

            self._popup.update()


        # no graphical window : console
        
        else :

            print text





    def setConfigurationVariables ( self ) :

        """ Sets context variables from configuration parameters """



        # os

        self.osValue = utilities.string( sys.platform, format = "join" )

        # predefined variables

        # paths

        self.commonValue = sys.rootPath

        self.configurationValue = sys.configurationPath

        self.proceduresValue = sys.proceduresPath

        self.libraryPythonValue = sys.libraryPath

        self.typesValue = sys.typesPath

        self.pendingValue = sys.pendingPath 

        self.notesValue = sys.notesPath

        self.pendingValue = sys.pendingPath

        # execution line

        self.scriptValue = utilities.pathName( sys.argv[ 0 ] )

        # general information

        self.copyrightValue = self.copyright

        # self.licenseValue = self.licenseMessage # done at the end of Init, when messages are read
        
        self.emailValue = self.email

        self.organizationValue = self.organization

        self.programValue = self.program
        
        self.versionValue = self.version

        self.webValue = self.web

        # computer information

        self.cpuValue = self.cpu

        self.bookcaseValue = self.bookcase

        self.classifyValue = self.classify

        self.exportValue = self.export

        self.rightsValue = self.rights

        self.drivesValue = self.driveList

##        self.hostValue = self.host
       

        # void variable, and work variables for interface

        self.voidValue = ""

        # license, composed from lines (at the end so that can be instantiated)

        self.licenseMessage = utilities.instantiate( self.licenseMessage )

        self.licenseValue = self.licenseMessage



        


        
                
       
# creates the singleton "context" if not already here

if not "context" in globals() : context = Context()






       
        
    
