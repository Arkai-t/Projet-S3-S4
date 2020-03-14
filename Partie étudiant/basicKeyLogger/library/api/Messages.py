
""" Contains the standard messages.

    In the scripts, messages are identified as context.xxxMessage, e.g., context.redMessage

    Messages may be overwritten from a file (eventually new color variables may be added)


    """


import os

from api.Utilities import *


class Messages :


    """ Contains the standard messages.

        In the scripts, messages are identified as self.context.xxxMessage, e.g., self.context.redMessage

        Messages may be overwritten from a file (eventually new color variables may be added)

        """

    # loads standard, then tries the redefined file and if fails, reloads original

    from message_configuration import *

    try :

        from configuration.message_configuration import *

    except Exception, exception :

        from message_configuration import *

 

    def addCapitalizedMessages ( self ) :

        """ Adds capitalized versions of the keywords """

        attributes = dir( self )

        # selects strings whose name ends with "Color"
        
        for attribute in attributes :

            # lower cases only
            
            if not attribute[ 0 ].islower() : continue

            if attribute.startswith( "_" ) : continue

            if not attribute.endswith( "Message" ) : continue

            value = getattr( self, attribute )
            
            if not type( value ) == str : continue

            if len( value ) <= 0 : continue
            
            setattr( self, utilities.firstLetterUpper( attribute ), utilities.firstLetterUpper( value ) )
        


    def getMessage (

        self,
        attribute = None,
        default = None
        ) :

        """ Gets the value of message "attribute"

            Method accepts simple names , e.g., "user", or complete names, "userMessage"

            Returns None if absent

            """

        if utilities.isEmpty( attribute ) : return default

        # attribute already ends with "Value", determines its name ( string before suffix )

        if not attribute.endswith( "Message" ) : attribute = attribute + "Message"
            
        try :

            value = getattr( self, attribute )

        except Exception, exception :

            value = default

        return value

        

    def messagePresent (

        self,
        attribute = None
        ) :

        """ Checks whether the current object contains the attribute """

        if utilities.isEmpty( attribute ) : return False

        if not attribute.endswith( "Message" ) : attribute = attribute + "Message"
        
        try :

            x = getattr( self, attribute  )
            
            return True

        except Exception, exception :

            return False


                
