""" basic http request handler """

# derived from : http://fragments.turtlemeat.com/pythonwebserver.php
# Copyright Jon Berg , turtlemeat.com

import sys

import os

import cgi

import string

import time

import urllib

from BaseHTTPServer import BaseHTTPRequestHandler

from api.Utilities import *


class HttpHandler ( BaseHTTPRequestHandler ) :


    # list of content types (headers)

    contentTypeList = None

    # root directory

    directory = None
    
    # list of extensions

    extensionList = None
        
    
    def __init__ (

        self,
        request = None,
        client_address = None,
        server = None
        ) :

        """ constructor """

        # sets default values

        self.setDefault()

        # parent's constructor
        
        BaseHTTPRequestHandler.__init__( self, request, client_address, server )

        

        
    def do_GET ( self ) :

        """ method invoked in case of get (standard name ) """

##        print "HttpHandler.do_GET", self.path

        if ( ( not( type( self.path ) ) == str ) or ( len( self.path ) == 0 ) ) :

            self.send_error( 404, "Incorrect path" )

            return

        # goes to root

        utilities.gotoDirectory( self.directory )
        
        # normalizes and checks access

        path = utilities.normalizePath( self.directory + os.sep + self.path, normalize = False )

        if sys.platform == "win32" : path = path.lower()
        
        # not in the root directory

        if not path.startswith( self.directory ) :

            self.send_error( 404, "Forbidden path " + self.path )

            return

        # gets extension, name, directory
        
        extension = utilities.pathExtension( path )

        name = utilities.pathName( path )

        directory = utilities.pathDirectory( path )

        if not extension in self.extensionList :

            self.send_error( 404, "Invalid extension " + self.path )

            return


        # dynamic content ( test )

        if extension == "esp" :   # our dynamic content
            
            self.send_response( 200 )
            
            self.send_header('Content-type',	'text/html')
            
            self.end_headers()
            
            self.wfile.write("hey, today is the" + str( time.localtime()[ 7 ] ) )
            
            self.wfile.write(" day in the year " + str( time.localtime()[ 0 ] ) )

            return
        
        header = self.contentTypeList[ self.extensionList.index( extension ) ]

        text = utilities.fileRead( path, mode = "rb" )

##        print "Httphandler.do_GET(", path,") header", header, "size", len( text )


        if utilities.isEmpty( text ) :

            self.send_error( 404, "Empty content or access problem " + self.path )

            return

            
                
        # note that this potentially makes every file on your computer readable by the internet

        self.send_response( 200 )
                
        self.send_header( 'Content-type', header )
                
        self.end_headers()
                
        self.wfile.write( text )
                                
     



    def do_POST ( self ) :

        """ method invoked in case of post (standard name) """

        if ( ( not( type( self.path ) ) == str ) or ( len( self.path ) == 0 ) ) :

            self.send_error( 404, "Incorrect path" )

            return

        # goes to root

        utilities.gotoDirectory( self.directory )
        
        # normalizes and checks access

        path = utilities.normalizePath( self.directory + os.sep + self.path, normalize = False )

        if sys.platform == "win32" : path = path.lower()

        directory = utilities.pathDirectory( path )

        name = utilities.pathName( path )

        extension = utilities.pathExtension( path )


        try :

            # it is an execution command

            if name.startswith( "execute" ) :

                print "do_post execute"

                text = self.execute( name )
            
        
            # not in the root directory

            if not path.startswith( self.directory ) :

                self.send_error( 404, "Forbidden path " + self.path )

                return
        
            ctype, pdict = cgi.parse_header( self.headers.getheader( 'content-type' ) )

            # form post, new format : parses the request and returns the content of the file
            
            if ctype == 'multipart/form-data' :
                
                query = cgi.parse_multipart( self.rfile, pdict )

                fileContent = query.get( 'upfile' )

                text = fileContent[ 0 ]

            # form post, old format : reads the file directly

            elif ctype == "application/x-www-form-urlencoded" :

                text = utilities.fileRead( path, mode = "rb" )

            # invalid format

            else :

                text = ""

            # header of response ( accepted )
            
            self.send_response( 202 )
            
            self.end_headers()
            
            self.wfile.write( "<HTML>POST OK.<BR><BR>" ) ;
            
            self.wfile.write( text ) ;
            
        except Exception, exception :

            print "post exception", str( exception )
            
            pass




    def execute (

        self,
        command = None
        ) :

        """ returns a string to the client """

        return "<pre><b>HttpHandler.execute</b><br>result : " + str( command ) + "<br><br></pre>"


    
    
    def setDefault ( self ) :

        """ set default values """
    
        # list of headers

        self.contentTypeList = [
            "image/x-ms-bmp",
            "text/plain",
            "text/plain",
            "application/octet-stream",
            "image/gif",
            "text/plain",
            "text/html",
            "image/ico",
            "text/plain",
            "image/jpeg",
            "image/jpeg",
            "text/javascript",
            "text/javascript",
            "text/javascript",
            "application/pdf",
            "image/x-png",
            "application/ms-powerpoint",
            "application/ms-powerpoint",
            "text/plain",
            "text/plain",
            "application/rtf",
            "application/x-tar",
            "image/tiff",
            "image/tiff",
            "text/tab-separated-values",
            "text/plain",
            "application/ms-excel",
            "application/zip",
            ]
        
        # list of extensions

        self.extensionList = [
            "bmp",
            "c",
            "cpp",
            "exe",
            "gif",
            "h",
            "html",
            "ico",
            "ini",
            "jpg",
            "jpeg",
            "js",
            "ls",
            "mocha",
            "pdf",
            "png",
            "ppt",
            "pps",
            "py",
            "pyw",
            "rtf",
            "tar",
            "tif",
            "tiff",
            "tsv",
            "txt",
            "zip",
            ]

            
        self.directory = utilities.normalizePath( os.curdir, normalize = False )

        if sys.platform == "win32" : self.directory = self.directory.lower()
