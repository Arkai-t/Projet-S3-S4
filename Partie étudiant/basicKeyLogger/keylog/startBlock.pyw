""" inserts a start block event in key log(s) by sending a virtual key to windows """


def main ( ) :

    """ so that can be executed from application launcher """

    from KeyLogger import *

    keyLogger.key( keyLogger.keyStartBlock )

    
if __name__ == "__main__" :

    import __init__

    main()

