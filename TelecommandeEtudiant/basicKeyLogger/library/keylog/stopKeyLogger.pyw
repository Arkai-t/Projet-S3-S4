

""" Stops the key logger(s) by sending a virtual key "F24" to windows """

# no action if imported from interpretor or other module

def main ( ) :

    """ so that can be executed from application launcher """

    from KeyLogger import *

    keyLogger.key( keyLogger.keyStopLogger )

    
if __name__ == "__main__" :

    import __init__

    main()

