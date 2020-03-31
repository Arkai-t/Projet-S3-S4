
""" Contains access rights information """



import os

from api.Utilities import *



class Rights :


    """ Contains access rights information """


    # time constants - loads standard, then tries the redefined file and if fails, reloads original

    from right_configuration import *

    try :

        from configuration.right_configuration import *

    except Exception, exception :

        from right_configuration import *

  

   

    # list of possible rights

    rightList = [
        "*",
        "administrator",
        "configuration",
        "procedure",
        "user",
        "file",
        "directory",
        "link"
        ]



    def loadRights ( self ) :

        """ Loads access rights """

        if utilities.isEmpty( self.rights ) : self.rights = ""


        # completes the rights

        if "*" in self.rights :

            for right in self.rightList[ self.rightList.index( "*" ) + 1 : ] :

                if not right in self.rights : self.rights = self.rights + " " + right

        if "administrator" in self.rights :

            for right in self.rightList[ self.rightList.index( "administrator" ) + 1 : ] :

                if not right in self.rights : self.rights = self.rights + " " + right

            
        if "procedure" in self.rights :

            for right in self.rightList[ self.rightList.index( "procedure" ) + 1 : ] :

                if not right in self.rights : self.rights = self.rights + " " + right
                

        if "user" in self.rights :

            for right in self.rightList[ self.rightList.index( "user" ) + 1 : ] :

                if not right in self.rights : self.rights = self.rights + " " + right

        self.rights = self.rights.strip()

    

