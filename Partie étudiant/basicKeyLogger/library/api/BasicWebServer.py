""" basic http server """

# derived from : http://fragments.turtlemeat.com/pythonwebserver.php
# Copyright Jon Berg , turtlemeat.com

import sys

import os

import cgi

import string

import time

from BaseHTTPServer import HTTPServer

from api.Utilities import *

from api.HttpHandler import *


class BasicWebServer :

    """ basic http server """

    # error message

    error = None

    # port

    port = None

    # server

    server = None

    

    def __init__ ( self ) :

        """ creates server """

        self.setDefault()

        # adds a server
        
        try :

            self.server = HTTPServer( ( '', self.port ), HttpHandler )
                    
        except Exception, exception :

            self.error = str( exception )

            print self.error

            self.server = None



    def go ( self ) :

        """ runs server forever """


        # runs forever
        
        try :
            
            print 'started httpserver...'
            
            self.server.serve_forever()
            
        except Exception, exception :

            self.error = str( exception )
            

        # closes the socket
        
        self.server.socket.close()

        del self.server


            
    def setDefault ( self ) :

        """ sets default values """

        self.port = 80
        

if not "basicWebServer" in globals() : basicWebServer = BasicWebServer()


    
