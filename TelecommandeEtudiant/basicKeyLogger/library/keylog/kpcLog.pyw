
""" Builds a KPC log from current key log """


def main ( ) :

    """ so that can be executed from application launcher """

    from KeyLogger import *

    keyLogger.writeKpc()

    
if __name__ == "__main__" :

    import __init__

    main()

    

