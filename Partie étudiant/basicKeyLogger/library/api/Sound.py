
""" Class that plays sound files (wav, for now)

   
    """


# captures exceptions, in case there are some missing components (e.g., nokia tablet)

import pygame


from api.Utilities import *

    
class Sound :


    """ Class that plays sound files (wav, for now)

        Uses pygames
   
        """

    
    # default values

    defaultChannels = 2

    defaultFrequency = 16000
    

    # flag to avoid multiple levels of interruption
    
    busy = None

    # number of channels

    channels = None

    # allowed extensions

    extensionList = [ "wav" ]

    # sampling frequency

    frequency = None
    
    # handler for sound
    
    handler = None

    # current file

    path = None
    



    def __init__ ( self ) :

        """ Constructs the object, does not do anything else

            """

        None



    def busy ( self ) :

        """ player is busy """

        try :

            return pygame.mixer.music.get_busy()

        except Exception, exception :

            return False

    
    def play (

        self,
        path = None,
        frequency = None,
        channels = None
        ) :

        """ plays a file """

        if not utilities.filePresent( path ) : return None

        if not utilities.pathExtension( path ) in self.extensionList : return None

        self.path = path

        self.resetMixer( frequency, channels )

        pygame.mixer.music.load( path )

        pygame.mixer.music.play()



    def pause ( self ) :

        """ pauses the player """

        try :
            
            pygame.mixer.music.pause()

            return True

        except Exception, exception :

            return False

        

    def resetMixer (

        self,
        frequency = None,
        channels = None
        ) :

        """ resets the mixer with the given parameters """

        if frequency is None : self.frequency = self.defaultFrequency

        else : self.frequency = utilities.integer( frequency )

        if channels is None : self.channels = self.defaultChannels

        else : self.channels = utilities.integer( channels )

        # ends with previous setup        

        try :

            pygame.mixer.quit()

        except Exception, exception :

            None

        # reinitializes the mixer

        try :

            pygame.mixer.init( 16000 )

            return True

        except Exception, exception :

            return False
        




    def rewind ( self ) :

        """ rewinds the player """


        try :
            
            pygame.mixer.music.rewind()

            return True

        except Exception, exception :

            return False
        



    def stop ( self ) :

        """ ends the player """


        try :
            
            pygame.mixer.music.stop()

            return True

        except Exception, exception :

            return False
        

    def volume (

        self,
        value = None
        ) :

        """ gets or sets the volume of the player """

        value = utilities.float( value )


        try :

            if type( value ) == float : pygame.mixer.music.set_volume( max( value, 0. ) )

            value = pygame.mixer.music.get_volume()

        except Exception, exception :

            value = -1.

        return value

                                                                      

# -----------------------------------
# creates the global singleton object if not already here
#

if not "sound" in globals() : sound = Sound()

    
         
        
