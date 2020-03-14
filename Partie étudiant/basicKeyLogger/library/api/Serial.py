
""" Wraps the serial.py module. Serial is whimsical to load (requires pywintype24.dll in original directory )

   
    """


import sys

import os

    
class Serial :

    """ Wraps the serial.py module. Serial is whimsical to load (requires pywintype24.dll in original directory )

       
        """

    # saves current directory, goes to python installation (required otherwise serial.py cannot find pywintype24.dll

    directory = os.getcwd()

    try :

        os.chdir( sys.libraryPath + "python" )

        from serial import *

    except Exception, exception :

        print str( exception )

    os.chdir( directory )



# -----------------------------------
# creates a global singleton if not already here
#

if not "serial" in globals() : serial = Serial()
         
        
