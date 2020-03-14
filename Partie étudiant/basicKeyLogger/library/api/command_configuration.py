#
# file extension - commands associations for execute, open, edit and view.
# os dependent
#

import sys

import os


# edit in external window

if sys.platform == "win32" : editCommandList = [
"bat", "notepad",
"c", "",
"cpp", "",
"csv", "",
"tsv", "",
"java", "",
"doc", "",
"htm", "",
"html", "",
"pdf", "",
"ppt", "",
"reg", "notepad",
"sav", "",
"sh", "notepad",
"shtml", "",
"spo", "",
"txt", "",
"xls", "",
"xml", "",
"py", "notepad",
"pyw", "notepad",
"directory", "explorer",
]

elif sys.platform == "linux2"  : editCommandList = [
"bat", "gedit",
"c", "gedit",
"cpp", "gedit",
"csv", "openoffice",
"tsv", "openoffice",
"java", "gedit",
"doc", "openoffice",
"htm", "gedit",
"html", "gedit",
"pdf", "",
"ppt", "openoffice",
"sav", "",
"sh", "gedit",
"shtml", "gedit",
"spo", "",
"txt", "gedit",
"xls", "openoffice",
"xml", "",
"py", "gedit",
"pyw", "gedit",
"directory", "nautilus",
]



else : editCommandList = [
"bat", "",
"c", "",
"cpp", "",
"csv", "",
"tsv", "",
"java", "",
"doc", "",
"htm", "",
"html", "",
"pdf", "",
"ppt", "",
"sav", "",
"sh", "",
"shtml", "",
"spo", "",
"txt", "",
"xls", "",
"xml", "",
"py", "",
"pyw", "",
"directory", "",
]



# execute in external thread

if sys.platform == "win32" : executeCommandList = [
"class", "java", 
"exe", "", 
"java", "javac", 
"py", "(library)python/python.exe",
"pyc", "(library)python/python.exe",
"pyo", "(library)python/python.exe",
"pyw", "(library)python/python.exe",
"reg", "regedit.exe",
## "pyw", "'(library)python/python.exe' %1 '--(library)'",
"directory", "explorer",
]

elif sys.platform == "linux2" : executeCommandList = [
"class", "java", 
"exe", "", 
"java", "javac", 
"py", "(library)python/python",
"pyc", "(library)python/python",
"pyo", "(library)python/python",
"pyw", "(library)python/python",
"sh", "bash",
"directory", "nautilus",
]

else : executeCommandList = [
"class", "", 
"exe", "", 
"java", "", 
"py", "",
"pyc", "",
"pyo", "",
"pyw", "",
"directory", "",
]



# open in external window

if sys.platform == "win32" : openCommandList = [
"bat", "notepad",
"c", "",
"cpp", "",
"csv", "",
"tsv", "",
"java", "",
"doc", "",
"htm", "",
"html", "",
"pdf", "",
"ppt", "",
"reg", "notepad",
"sav", "",
"sh", "notepad",
"shtml", "",
"spo", "",
"txt", "",
"xls", "",
"xml", "",
"py", "notepad",
"pyw", "notepad",
"directory", "explorer",
]


elif sys.platform == "linux2" : openCommandList = [
"bat", "gedit",
"c", "gedit",
"cpp", "gedit",
"csv", "openoffice",
"tsv", "openoffice",
"java", "gedit",
"doc", "openoffice",
"htm", "firefox",
"html", "firefox",
"pdf", "",
"ppt", "openoffice",
"sav", "",
"sh", "gedit",
"shtml", "firefox",
"spo", "",
"txt", "gedit",
"xls", "openoffice",
"xml", "",
"py", "gedit",
"pyw", "gedit",
"directory", "nautilus",
]

else : openCommandList = [
"bat", "",
"c", "",
"cpp", "",
"csv", "",
"tsv", "",
"java", "",
"doc", "",
"htm", "",
"html", "",
"pdf", "",
"ppt", "",
"sav", "",
"sh", "",
"shtml", "",
"spo", "",
"txt", "",
"xls", "",
"xml", "",
"py", "",
"pyw", "",
"directory", "",
]


# list of files that make a procedure (folder) executable

if sys.platform == "win32" : procedureFileList = [
"findLibrary.py", "(library)api/findLibrary.py",
"findLibrary.txt", "(library)findLibrary.txt",
##"execute.pyw", "(library)widgets/executeTemplate.pyw",  pointless, used to detect executable directories
"tutorial.pyw", "(library)widgets/tutorialTemplate.pyw", 
"execute.bat", "(procedures)_common/scripts/execute.bat", 
"tutorial.bat", "(procedures)_common/scripts/tutorial.bat",
"python.exe", "(library)python/python.exe",
"pythonw.exe", "(library)python/pythonw.exe",
"copy_reg.py",  "(library)python/Lib/copy_reg.py",
"ntpath.py",  "(library)python/Lib/ntpath.py",
"os.py",  "(library)python/Lib/os.py",
"stat.py",   "(library)python/Lib/stat.py",
"types.py",   "(library)python/Lib/types.py",
"UserDict.py",   "(library)python/Lib/UserDict.py",
"python24.dll",  "(library)python/python24.dll",
"pythoncom24.dll",  "(library)python/pythoncom24.dll",
"pywintypes24.dll",  "(library)python/pywintypes24.dll",


]


elif sys.platform == "linux2" : procedureFileList = [
"findLibrary.py", "(library)api/findLibrary.py",
"execute.pyw", "(library)widgets/executeTemplate.pyw", 
##"tutorial.pyw", "(library)widgets/tutorialTemplate.pyw", pointless: used to detect executable directories
"execute.sh", "(procedures)_common/scripts/execute.sh", 
"tutorial.sh", "(procedures)_common/scripts/tutorial.sh",
"python", "(library)python/python",
"copy_reg.py",  "(library)python/copy_reg.py",
"os.py",  "(library)python/os.py",
"os2emxpath.py",  "(library)python/os2emxpath.py",
"posixpath.py",  "(library)python/posixpath.py",
"stat.py",   "(library)python/stat.py",
"types.py",   "(library)python/types.py",
"UserDict.py",   "(library)python/UserDict.py",

]

else : procedureFileList = [
"findLibrary.py", "(library)api/findLibrary.py",
"execute.pyw", "(library)widgets/executeTemplate.pyw", 
"tutorial.pyw", "(library)widgets/tutorialTemplate.pyw", 
]


# list of files that make a procedure (folder) standalone

standaloneFileList = [
"findLibrary.txt", "(types)_standalone/findLibrary.txt",
"software/configuration", "(configuration)",
"software/procedures/_common/", "(procedures)_common/", 
"software/libraryPython/", "(library)", 
]




# view in external window

if sys.platform == "win32" : viewCommandList = [
"bat", "notepad",
"c", "",
"cpp", "",
"csv", "",
"tsv", "",
"java", "",
"doc", "",
"shtml", "",
"htm", "",
"html", "",
"pdf", "",
"ppt", "",
"reg", "notepad",
"sav", "",
"sh", "notepad",
"shtml", "",
"spo", "",
"txt", "",
"xls", "",
"xml", "",
"py", "notepad",
"pyw", "notepad",
"directory", "explorer",
]

elif sys.platform == "linux2" : viewCommandList = [
"bat", "gedit",
"c", "gedit",
"cpp", "gedit",
"csv", "openoffice",
"tsv", "openoffice",
"java", "gedit",
"doc", "openoffice",
"htm", "firefox",
"html", "firefox",
"pdf", "",
"ppt", "openoffice",
"sav", "",
"sh", "gedit",
"shtml", "firefox",
"spo", "",
"txt", "gedit",
"xls", "openoffice",
"xml", "",
"py", "gedit",
"pyw", "gedit",
"directory", "nautilus",
]

else : viewCommandList = [
"bat", "", 
"c", "",
"cpp", "",
"csv", "",
"tsv", "",
"java", "",
"doc", "",
"htm", "",
"html", "",
"pdf", "",
"ppt", "",
"sav", "",
"sh", "",
"shtml", "",
"spo", "",
"txt", "",
"xls", "",
"xml", "",
"py", "",
"pyw", "",
"directory", "",
]


