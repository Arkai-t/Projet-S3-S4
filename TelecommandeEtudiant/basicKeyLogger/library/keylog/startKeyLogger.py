
""" Starts a key logger. To stop it, click in the window or use stopKeyLogger.py* """

def main ( ) :

    """ so that can be executed from application launcher """

    from KeyLogger import *

    keyLogger.startLogger()

    
if __name__ == "__main__" :

    import __init__

    main()

    
