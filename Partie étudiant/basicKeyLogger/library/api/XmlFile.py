
""" XML files and tree manager.Read/write and access XML files

    See on wikipedia for information on  XML format
   
 
    """


import xml.dom.minidom

from api.Utilities import *


class XmlFile :
    
    """ XML files and tree manager.Read/write and access XML files

        See on wikipedia for information on  XML format
   
        The basic internal representation is a tree.

        """

    # error

    error = None
    
    # file name
    
    path = ""

    # text to write to file and/or written from file

    text = None

    # xml tree for a document

    tree = None


    def __init__ ( self ) :

        """ Constructor. Does absolutely nothing
           
            """

        self.resetData()


    def addNode (

        self,
        node = None,
        to = None
        ) :

        """ Adds a node to the tree and/or some subnode """

        if to is None : to = self.tree
        
        try :

            # checks whether destination is a tree, in this case takes its document element

            if isinstance( to, xml.dom.minidom.Document ) : to = to.documentElement

            elif not isinstance( to, xml.dom.minidom.Node ) : return False
            
        
            # checks whether node is a tree, in this case takes its document element
            
            if isinstance( node, xml.dom.minidom.Document ) : node = node.documentElement
        
            if not isinstance( node, xml.dom.minidom.Node ) : return False

            # appends

            to.appendChild( node )

            
        except Exception, exception :

            utilities.error = "addNode - error : " + str( exception )

            return False

        return True

        

        return True

    
    def fileToText (

        self,
        path = None,
        text = None,
        ) :

        """ Reads a bib file "path" and initializes self.attributeList, self.valueList and self.text from file.
           
            
            """

        ok = self.read( path = path, text = text )

        if not ok : return None

        else : return self.text
        

    def read (

        self,
        path = None,
        text = None,
        ) :

        """ Reads a bib file "path" and initializes self.attributeList, self.valueList and self.text from file.
           
            
            """

        utilities.error = ""

        if path is None : path = self.path

        if not utilities.isEmpty( path ) :

            self.path = utilities.normalizePath( path, normalize = False )

            text = utilities.fileRead( self.path ).replace( "\r", "" )

        if utilities.isEmpty( text ) : return False

        self.text = utilities.string( text )

##        print "XMLFILE READ TYPE SELF TEXT ", utilities.pathName( path ), type( self.text )

        if not self.tree is None : self.tree.unlink()
        
        self.tree = self.textToTree( self.text )

        if self.tree is None :

            self.text = None

            return False

        return True


    def resetData ( self ) :

        """ Empties the data structure """

        utilities.error = None
        
        self.path = None

        if not self.tree is None : self.tree.unlink()
               
        self.tree = None

        self.text = None


                
    def textToTree (

        self,
        text = None
        ) :

        """ Checks that a text is a valid XML and builds self.tree. Otherwise, sets error and does nothing
            
            """

        if utilities.isEmpty( text ) : text = self.text

        elif utilities.isEmpty( text ) : return None

        else : text = utilities.stringToUnicode( text, encoder = utilities.xmlFormat )
        
        try :

            tree = xml.dom.minidom.parseString( text )

##            if not self.tree is None : self.tree.unlink()
##            
##            self.tree = tree
##
##            self.text = utilities.string( text )
            
            return tree

        except Exception, exception :

            utilities.error = "textToTree - error : " + str( exception )

            return None

        return 



    
                
    def treeToText (

        self,
        tree = None
        ) :

        """ Converts a tree into a text in XML format.
            
            """

        if tree is None : tree = self.tree

        if tree is None : return ""
        
        try :

            text = utilities.string( tree.toxml() )

            self.text = text
            
            return text

        except Exception, exception :

            utilities.error = "treeToText - error : " + str( exception )

            return ""

        return 



    


    def write (
        
        self,
        path = None,
        text = None,
        tree = None,
        ) :

        """ Alias for write table Writes a matrix of values, i.e. a table file
      
            Returns True/False

            """

        utilities.error = ""

        if path is None : path = self.path

        if utilities.isEmpty( path ) : return False

        if not text is None : None

        elif not tree is None : text = self.treeToText( tree )

        elif not self.tree is None : text = self.treeToText( self.tree )

        elif not self.text is None : text = self.text

        if not text is None : self.text = text

        if not tree is None :

            if not self.tree is None : self.tree.unlink()
        
            self.tree = tree

        ok = utilities.fileWrite( path, text )

        return ok






# creates the global singleton object if not already here

if not "xmlFile" in globals() : xmlFile = XmlFile()
         
        

