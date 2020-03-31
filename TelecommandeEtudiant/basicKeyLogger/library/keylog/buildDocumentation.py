
""" Builds the documentation  """


def main ( ) :

    """ so that can be executed from application launcher """

    from KeyLogger import *

    from api.Documentation import *

    documentation.write()

    

    
if __name__ == "__main__" :

    import __init__

    main()

    
