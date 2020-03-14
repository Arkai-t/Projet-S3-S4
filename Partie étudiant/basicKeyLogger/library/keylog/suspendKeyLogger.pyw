

""" Suspends the key logger by sending a virtual key to windows """


# no action if imported from interpretor or other module

def main ( ) :

    """ so that can be executed from application launcher """

    from KeyLogger import *

    keyLogger.key( keyLogger.keySuspendLogger )

    
if __name__ == "__main__" :

    import __init__

    main()

