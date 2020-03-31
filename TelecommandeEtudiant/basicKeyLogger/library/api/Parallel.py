
""" Wraps the parallel.py module.  This class is here for compatibility with Serial (from api.Parallel import * ), but it is not strictly necessary

   
    """


import sys

import os

    
class Parallel :

    """ Wraps the parallel.py module.  This class is here for compatibility with Serial (from api.Parallel import * ), but it is not strictly necessary

       
        """

    # saves current directory, goes to python installation (required otherwise serial.py cannot find pywintype24.dll

    directory = os.getcwd()

    try :

        os.chdir( sys.libraryPath + "python" )

        from parallel import *

    except Exception, exception :

        print str( exception )

    os.chdir( directory )



# -----------------------------------
# creates a global singleton if not already here
#

if not "parallel" in globals() : parallel = Parallel()
         
        
