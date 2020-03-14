# -*- coding: cp1252 -*-

# previous - * - c o d i n g : utf-8 - * -

#
# format information
#

import os

# list of extended alpha codes - all cases

alphaList = "a����A����@bBcCdDe����E����fFgGhHi���I���jJkKlLmMn�N�o����O����pPqQrRsStTu���U���vVwWxXyYzZ"


# table of recoding of characters

characterTable = [
    "a����A����@",
    "bB",
    "cC",
    "dD",
    "e����E����",
    "fF",
    "gG",
    "hH",
    "i���I���",
    "jJ",
    "kK",
    "lL",
    "mM",
    "n�N�",
    "o����O����",
    "pP",
    "qQ",
    "rR",
    "sS",
    "tT",
    "u���U���",
    "vV",
    "wW",
    "xX*",
    "yY",
    "zZ",
    "A����@",
    "B",
    "C",
    "D",
    "E����",
    "F",
    "G",
    "H",
    "I���",
    "J",
    "K",
    "L",
    "M",
    "N�",
    "O����",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U���",
    "V",
    "W",
    "X",
    "Y",
    "Z",
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "_-",
    ]



# comment delimiter

commentDelimiter = "#"

# recognized command delimiters

commentDelimiterList =[
    "#",
    "\n"
    ]

# date of the day (short)

dayFormat = "%Y %m %d"

# long date

dateFormat = "%Y %m %d - %H:%M:%S"

# list of extensions that can be executed

executeExtensionList = [
    "exe",
    "bat",
    "sh",
    "",
    ]


# in wiki and xwiki, the symbol that cuts a text stream

featureDelimiter = "|"

# in TSV file, delimiter between fields

fieldDelimiter = "\t"

# formats for dates in file name

fileDayFormat = "%Y%m%d"

# format for data in file name

fileDateFormat = "%Y%m%d%H%M%S"

# html format

htmlFormat = "ISO-8859-1"

# table of recoding for html

htmlTable = [
    "&quot;", '"',
    "&amp;", "&",
    "&lt;", "<", 
    "&gt;", ">",
    "&nbsp;", " ",
    #DOES NOT WORK **EF 2008 06 09 &shy;	_
    "&iexcl;", "�",
    "&cent;", "�",
    "&pound;", "�",
    "&curren;", "�",
    "&yen;", "�",
    "&brvbar;", "�",
    "&sect;", "�",
    "&uml;", "�",
    "&copy;", "�",
    "&ordf;", "�",
    "&laquo;", "�",
    "&not;", "�",
    "&reg;", "�",
    "&macr;", "�",
    "&deg;", "�",
    "&plusmn;", "�",
    "&sup2;", "�",
    "&sup3;", "	�",
    "&acute;", "�",
    "&micro;", "�",
    "&para;", "�",
    "&middot;", "�",
    "&cedil;", "�",
    "&sup1;", "�",
    "&ordm;", "�",
    "&raquo;", "�",
    "&frac14;", "�",
    "&frac12;", "�",
    "&frac34;", "�",
    "&iquest;", "�",
    "&Agrave;", "�",
    "&Aacute;", "�",
    "&Acirc;", "�",
    "&Atilde;", "�",
    "&Auml;", "�",
    "&Aring;", "�",
    "&AElig;", "�",
    "&Ccedil;", "�",
    "&Egrave;", "�",
    "&Eacute;", "�",
    "&Ecirc;", "�",
    "&Euml;", "�",
    "&Igrave;", "�",
    "&Iacute;", "�",
    "&Icirc;", "�",
    "&Iuml;", "�",
    "&ETH;", "�",
    "&Ntilde;", "�",
    "&Ograve;", "�",
    "&Oacute;", "�",
    "&Ocirc;", "�",
    "&Otilde;", "�",
    "&Ouml;", "�",
    "&times;", "�",
    "&Oslash;", "�",
    "&Ugrave;", "�",
    "&Uacute;", "�",
    "&Ucirc;", "�",
    "&Uuml;", "�",
    "&Yacute;", "�",
    "&THORN;", "�",
    "&szlig;", "�",
    "&agrave;", "�",
    "&aacute;", "�",
    "&acirc;", "�",
    "&atilde;", "�",
    "&auml;", "�",
    "&aring;", "�",
    "&aelig;", "�",
    "&ccedil;", "�",
    "&egrave;", "�",
    "&eacute;", "�",
    "&ecirc;", "�",
    "&euml;", "�",
    "&igrave;", "�",
    "&iacute;", "�",
    "&icirc;", "�",
    "&iuml;", "�",
    "&eth;", "�",
    "&ntilde;", "�",
    "&ograve;", "�",
    "&oacute;", "�",
    "&ocirc;", "�",
    "&otilde;", "�",
    "&ouml;", "�",
    "&divide;", "�",
    "&oslash;", "�",
    "&ugrave;", "�",
    "&uacute;", "�",
    "&ucirc;", "�",
    "&uuml;", "�",
    "&yacute;", "�",
    "&thorn;", "�",
    "&yuml;", "�",
    "&euro;", "�",
    ]

# list of extensions that can be instantiated

instantiateExtensionList = [
    "bat",
    "csv",
    "htm",
    "html",
    "ini",
    "py",
    "pyw",
    "reg",
    "rtf",
    "sh",
    "shtml",
    "tsv",
    "txt",
    "xml",
    ]

# delimiters used in file formats

lineDelimiter = "\n"

# list of extensions that contain links

linkExtensionList = [ "to" ]

# list of extended alpha codes - lower case

lowerList = "a����@bcde����fghi���jklmn�o����pqrstu���vwxyz"

# maximal size of files ( e.g., for zip etc., 64 mb )

maxFileSizeKb = 64000.

# special characters accepted in paths

pathCharacterList = [
    " ",
    "!",
    "@",
    "#",
    "$",
    "%",
    "",
    "&",
    "*",
    "(",
    ")",
    "/",
    "\\",
    ":",
    ".",
    "_",
    "-",
    "~",
    os.sep
    ]

# punctuation signs

punctuationList = [
    ',',
    '.',
    ';',
    ':',
    '?',
    '!',
    '[',
    ']',
    '(',
    ')'
    ]

# list of prefix of reserved files/folders

reservedPrefixList = [ "_", ".", "~" ]

# hour

timeFormat = "%H:%M:%S"

# unicode encoder for strings. Defines the characters that can be displayed

unicodeFormat = "Latin-1"

# list of extended alpha codes - upper case

upperList = "A����@BCDE����FGHI���JKLMN�O����PQRSTU���VWXYZ"



# all recognized delimiters

wordDelimiterList = [
    " ",
    ",",
    "\t",
    "="
    ]

# xml encoder. Defines the characters that can be copied-pasted from clipboard and external documents

xmlFormat = "UTF-8"


