
""" PDF files manager.Read/write and access PDF files

    See on wikipedia for information on  PDF format
   
 
    """


from api.Utilities import *



class PdfFile :
    
    """ PDF files manager.Read/write and access PDF files

        See on wikipedia for information on  PDF format
       
     
        """


    def __init__ ( self ) :

        """ Constructor. Does absolutely nothing
           
            """

        None

        



        


# -----------------------------------
# creates the global singleton object if not already here
#

if not "pdfFile" in globals() : pdfFile = PdfFile()
         
        

