
""" Class for installation & deinstallation

    """


import sys

import os

if sys.platform == "win32" :

    from win32com.shell import shell
    
    import win32api
    
    import pythoncom


from api.Context import *

from gui.DialogBox import *




class Setup :

    """ Class for installation & deinstallation

        """

    # error (text composed of identifiers )
    
    error = None

    

    def __init__ ( self ) :

        """ constructor """

        self.error = ""



    def createShortcutWindows (

        self,
        path,
        target,
        arguments = "",
        directory = "",
        icon = "",
        description = ""
        ) :

        """ creates a shortcut

            from http://www.xxxxxxxxxx
            
            """

        # captures exceptions
        
        try :

            # Get the shell interface.
            
            sh = pythoncom.CoCreateInstance(
                shell.CLSID_ShellLink,
                None, 
                pythoncom.CLSCTX_INPROC_SERVER,
                shell.IID_IShellLink
                )

            # Get an IPersist interface
            
            persist = sh.QueryInterface( pythoncom.IID_IPersistFile )

            # Set the data
            
            sh.SetPath( target )
            
            sh.SetDescription( description )
            
            sh.SetArguments( arguments )
            
            sh.SetWorkingDirectory( directory )
            
            sh.SetIconLocation( icon, 0 )    

            # Save the link itself.
            
            persist.Save( path, 1 )

            return True

        except Exception, exception :

            self.error = self.error + " " + "windows" + "(" + str( exception ) + ")"

            return False
        

##
##if __name__ == "__main__":
##	TempDir = os.environ["TEMP"]
##	WinRoot = os.environ["windir"]
##
##	Path        =  WinRoot    + "\\Profiles\\All Users\\Desktop\\New
##Link.lnk"
##	Target      =  Pythonroot + "pythonw.exe "
##	Arguments   =  TempDir + "\\test.py"
##	StartIn     =  TempDir
##	Icon        = (Pythonroot + "\\py.ico", 0)
##	Description = "New Link"
##
##	CreateShortCut(Path,Target,Arguments,StartIn,Icon,Description)
##
##









    def install ( self ) :

        """ installs the application : adds links on desktop, option to right click menu & (for windows) an uninstaller """


##        print "Setup.install"

        self.error = ""


        dialogBox.display(
            text = utilities.getMessage( "setupStart" ),
            buttonOk = utilities.getMessage( "continue" ),
            buttonBack = utilities.getMessage( "cancel" ),
            position = "center"
            )

        if dialogBox.command == "back" : return False
        

        # now, go
        
        if sys.platform == "win32" : ok = self.installWindows()

        elif sys.platform == "linux2" : ok = self.installLinux()

        else : return False

        if utilities.isEmpty( self.error ) :

            text = utilities.getMessage( "installed" )

        else :

            text = utilities.getMessage( "partiallyInstalled" ) + "\n"

            if "desktop" in self.error : text = text + utilities.getMessage( "setupDesktop" ) + "\n"

            if "windows" in self.error : text = text + utilities.getMessage( "setupWindows" ) + "\n"

            if "shortcut" in self.error : text = text + utilities.getMessage( "setupIcon" ) + "\n"

            if "reg1" in self.error : text = text + utilities.getMessage( "setupReg" ) + "\n"

            if "right" in self.error : text = text + utilities.getMessage( "setupRight" ) + "\n"

            if "reg2" in self.error : text = text + utilities.getMessage( "setupReg" ) + "\n"
            
            if "windir" in self.error : text = text + utilities.getMessage( "setupWindir" ) + "\n"
            
            if "uninstall" in self.error : text = text + utilities.getMessage( "setupUninstall" ) + "\n"


        dialogBox.display(
            text = text,
            button = utilities.getMessage( "continue" ),
            position = "center"
            )

                                             
        return ok





    def installDesktopIconLinux ( self ) :

        """ adds a desktop icon """

        if not sys.platform == "linux2" : return False

        directory = utilities.instantiate ( "(procedures)_common/linux2/", default = "_" )

        source = directory + "desktop.txt"

        program = utilities.getVariable( "program" )

        home = utilities.normalizePath( "~" + os.sep )

        target = home + "Desktop" + os.sep + program

        # does not exist (weird desktop name: copies link here

        if not utilities.directoryPresent( target ) :

            target = directory + program

            self.error = self.error + " " + "desktop"

        ok = utilities.fileCopy(
            source,
            target,
            instantiate = True
            )

        if not ok : self.error = self.error + " " + "shortcut"

        return True




    def installDesktopIconWindows ( self ) :

        """ adds a desktop icon """

        if not sys.platform == "win32" : return False

##        print "Setup.installDesktopIconWindows"

        directory = utilities.getVariable( "procedure" )

        program = utilities.getVariable( "program" )

        desktop = os.environ[ "ALLUSERSPROFILE" ] + os.sep + "Desktop" + os.sep

        # if desktop not presept (e.g., fucking windows mixes languages like "all users/Escritorio") copies link here

        if not utilities.directoryPresent( desktop ) :

            desktop = directory 

            self.error = self.error + " " + "desktop"

        desktop = desktop + program + ".lnk"

        target = directory + "pythonw.exe"

        arguments = "pop.pyw"

        icon = utilities.instantiate( "(procedures)_common/pictures/doc.ico", default = "_" )

        ok = self.createShortcutWindows(
            path = utilities.normalizePath( desktop, normalize = False),
            target = utilities.normalizePath( target, normalize = False ),
            arguments = arguments,
            directory = utilities.normalizePath( directory, normalize = False ),
            icon = utilities.normalizePath( icon, normalize = False ),
            description = program
            )

        if not ok : self.error = self.error + " " + "shortcut"

        return True





    def installLinux ( self ) :

        """ installs for linux : desktop icon, right click option (in submenu script ) """


        if not sys.platform == "linux2" : return False

##        print "installLinux"

        self.installDesktopIconLinux()

        self.installRightClickOptionLinux()

        utilities.fileCreate( sys.rootPath + "installed.txt" )

        return True
    





    def installRightClickOptionLinux ( self ) :

        """ adds a right click option """

        if not sys.platform == "linux2" : return False

        source = utilities.instantiate( "(procedures)_common/linux2/right_click.txt", default = "_" )

        program = utilities.getVariable( "program" )

        home = utilities.normalizePath( "~" + os.sep )

        target = home + ".gnome2" + os.sep + "nautilus-script" + os.sep + program

        ok = utilities.fileCopy(
            source,
            target,
            instantiate = True,
            )

        if not ok : self.error = self.error + " " + "right"

        return True



    def installRightClickOptionWindows ( self ) :

        """ adds a right click option """

        if not sys.platform == "win32" : return False

        # normalizes the current procedure for the registries (\\ delimited)

        directory = utilities.currentDirectory()
        
        utilities.setVariable( "procedure", directory )

        utilities.setVariable( "work", directory.replace( "\\", "\\\\" ) )

##        print "Setup.installRightClickOptionWindows", directory
        
        # copies and instantiates the registry files (right click for files & folders, uninstall)

        names = [
            "ftkdoc_right_click_files_add.reg",
            "ftkdoc_right_click_files_remove.reg",
            "ftkdoc_right_click_folders_add.reg",
            "ftkdoc_right_click_folders_remove.reg",
            ]

        
        source = utilities.instantiate( "(procedures)_common/win32/", default = "_" )

        target = utilities.instantiate( "(procedure)", default = "_" )

        result = True
        
        for name in names :
        
            ok = utilities.fileCopy(
                source + name,
                target + name,
                instantiate = True,
##                filter = True,
                )

            if not ok :

                self.error = self.error + " " + "reg1"

                result = False

        if not result : self.error = self.error + " " + "right"
        
        
        # adds registers (uses .system instead of executePath because regedit /s is an incorrect command prefix)
        
        external.system( "regedit.exe /s " + target + "ftkdoc_right_click_files_add.reg" )

        external.system( "regedit.exe /s " + target + "ftkdoc_right_click_folders_add.reg" )

        
        return True





    def installUninstallerWindows ( self ) :

        """ adds an uninstaller:
            a file ftkdoc_uninstall.exe to C:/WINDOWS,
            a windows registry for add/remove programs

            """

        if not sys.platform == "win32" : return False

##        print "Setup.installUninstallerWindows"

        if not sys.platform == "win32" : return False

        # prepares variables

        directory = utilities.currentDirectory()
        
        utilities.setVariable( "procedure", directory )

        # normalizes the current procedure for the registries (\\ delimited)

        utilities.setVariable( "work", directory.replace( "\\", "\\\\" ) )

##        print "Setup.installUninstallerWindows", utilities.getVariable( "root" )
##        print "                               ", utilities.getVariable( "procedure" )
##        print "                               ", utilities.getVariable( "work" )
        
        # copies and instantiates the registry files (right click for files & folders, uninstall)

        names = [
            "ftkdoc_uninstall_add.reg",
            "ftkdoc_uninstall_remove.reg",
            "ftkdoc_remove.bat",
            ]

        
        source = utilities.instantiate( "(procedures)_common/win32/" , default = "_" )

        target = utilities.instantiate( "(procedure)", default = "_" )
            
        for name in names :
        
            ok = utilities.fileCopy(
                source + name,
                target + name,
                instantiate = True,
##                filter = True,
                )

            if not ok : self.error = self.error + " " + "reg2" 

        # adds registers (uses .system instead of executePath because regedit /s is an incorrect command prefix)
        
        external.system( "regedit.exe /s " + target + "ftkdoc_uninstall_add.reg" )

        # copies uninstaller in windows directory
        
        windows = os.environ[ "WINDIR" ] + os.sep

##        print "Setup.installUninstallerWindows", windows
##        print "     ", source + "ftkdoc_uninstall.exe", utilities.filePresent( source + "ftkdoc_uninstall.exe" )
##        print "     ", target + "ftkdoc_remove.bat", utilities.filePresent( target + "ftkdoc_remove.bat" )

        # copies the executable batch file ftkdoc_uninstall that calls ftkdoc_remove, and ftkdoc_remove
        
        ok1 = utilities.fileCopy(
            source + "ftkdoc_uninstall.exe",
            windows + "ftkdoc_uninstall.exe"
            )
        
        ok2 = utilities.fileCopy(
            target + "ftkdoc_remove.bat",
            windows + "ftkdoc_remove.bat",
            )

        ok = ok1 and ok2

        if not ok : self.error = self.error + " " + "windir"

        return True


    


    def installWindows ( self ) :

        """ installs for windows : desktop icon, right click option for files and folders, uninstaller """


        if not sys.platform == "win32" : return False

##        print "install windows"

        self.installDesktopIconWindows()

        self.installRightClickOptionWindows()

        self.installUninstallerWindows()

        utilities.fileCreate( sys.rootPath + "installed.txt" )
        
        return True



    

    def uninstall ( self ) :

        """ uninstalls the application ( normally completed by a bat or sh file )

            does not work if we are in the common directory
            
            """

        directory = utilities.currentDirectory()

        if directory.startswith( sys.rootPath ) :

            dialogBox.display(
                text = utilities.getMessage( "inroot" ),
                button = utilities.getMessage( "continue" ),
                position = "center"
                )

            return False

        dialogBox.display(
            text = utilities.getMessage( "uninstallStart" ),
            buttonOk = utilities.getMessage( "continue" ),
            buttonBack = utilities.getMessage( "cancel" ),
            position = "center"
            )

        return False

        if dialogBox.command == "back" : return False
        
                

##        print "Setup.install"

        if sys.platform == "win32" : ok = self.uninstallWindows()

        elif sys.platform == "linux2" : ok = self.uninstallLinux()

        else : return False

        dialogBox.display(
            text = utilities.getMessage( "uninstalled" ),
            button = utilities.getMessage( "continue" ),
            position = "center"
            )
        
        return ok




    def uninstallLinux ( self ) :

        """ installs for linux : deletes """

        #**EF TODO


        if not sys.platform == "linux2" : return False

        return True


        

    def uninstallWindows ( self ) :

        """ installs for windows : runs uninstalled in WINDOWS """


        if not sys.platform == "win32" : return False

        # copies uninstaller in windows directory
        
        windows = os.environ[ "WINDIR" ] + os.sep

##        print "Setup.installUninstallerWindows", windows
##        print "     ", source + "ftkdoc_uninstall.exe", utilities.filePresent( source + "ftkdoc_uninstall.exe" )
##        print "     ", target + "ftkdoc_remove.bat", utilities.filePresent( target + "ftkdoc_remove.bat" )

        # executes the executable version of ftkdoc_uninstall.bat, calls WINDOWS/ftkdoc_remove.bat
        
        external.executeFile( windows + "ftkdoc_uninstall.exe" )


        return True

            
        
# -----------------------------------
# creates the global singleton object if not already here
#

if not "setup" in globals() : setup = Setup()
    
