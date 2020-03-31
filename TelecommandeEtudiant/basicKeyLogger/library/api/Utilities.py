
""" API that contains miscellaneous methods for strings, files, etc.

    """


import os

import sys

from api.Clock import *

from api.Classes import *

from api.Texts import *

from api.PathNames import *

from api.Files import *

from api.Items import *


class Utilities ( Classes, Texts, PathNames, Files, Items ) :


    """ API that contains miscellaneous methods for strings, files, etc.

        methods are called as  " utilities.xxx( ... ) "

        there is a reverse link from utilities to the singleton context, utilities.context


        """


    # file formats - loads standard file extension - command association, then tries the redefined file and if fails, reloads original

    from format_configuration import *
    
    try :

        from configuration.format_configuration import *

    except Exception, exception :

        from format_configuration import *



    # time of last change

    changeMs = 0

    # context that contains variables
    
    context = None

    # error

    error = None


    def __init__ ( self ) :

        """ constructor """

        # updates clock formats

        try :
        
            clock.dateFormat = self.dateFormat
                
            clock.timeFormat = self.timeFormat
            
            clock.dayFormat = self.dayFormat
            
            clock.fileDayFormat = self.fileDayFormat
            
            clock.fileDateFormat = self.fileDateFormat

        except Exception, exception :

            None
        


        
# creates the global singleton object if not already here

if not "utilities" in globals() : utilities = Utilities()
         




