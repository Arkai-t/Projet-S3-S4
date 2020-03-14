
""" Wraps the I2C.py module. I2C is whimsical (requires pywintype24.dll in original directory )

   
    """


import sys

import os

    
class I2c :

    """ Wraps the I2C.py module. I2C is whimsical  (requires pywintype24.dll in original directory )

       
        """

    # saves current directory, goes to python installation (required otherwise serial.py cannot find pywintype24.dll

    directory = os.getcwd()

    try :

        os.chdir( sys.libraryPath + "python" )

        from I2C import *

    except Exception, exception :

        print str( exception )

    os.chdir( directory )



# -----------------------------------
# creates a global singleton if not already here
#

if not "i2c" in globals() : i2c = I2c()
         
        
