# -*- coding: cp1252 -*-

# previous - * - c o d i n g : utf-8 - * -

#
# format information
#

import os

# list of extended alpha codes - all cases

alphaList = "aàâäãAÀÂÀÃ@bBcCdDeéèêëEÉÈÊËfFgGhHiîïìIÎÏÌjJkKlLmMnñNÑoôöõòOÔÖÕÒpPqQrRsStTuûüùUÛÜÙvVwWxXyYzZ"


# table of recoding of characters

characterTable = [
    "aàâäãAÀÂÀÃ@",
    "bB",
    "cC",
    "dD",
    "eéèêëEÉÈÊË",
    "fF",
    "gG",
    "hH",
    "iîïìIÎÏÌ",
    "jJ",
    "kK",
    "lL",
    "mM",
    "nñNÑ",
    "oôöõòOÔÖÕÒ",
    "pP",
    "qQ",
    "rR",
    "sS",
    "tT",
    "uûüùUÛÜÙ",
    "vV",
    "wW",
    "xX*",
    "yY",
    "zZ",
    "AÀÂÀÃ@",
    "B",
    "C",
    "D",
    "EÉÈÊË",
    "F",
    "G",
    "H",
    "IÎÏÌ",
    "J",
    "K",
    "L",
    "M",
    "NÑ",
    "OÔÖÕÒ",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "UÛÜÙ",
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
    "&iexcl;", "¡",
    "&cent;", "¢",
    "&pound;", "£",
    "&curren;", "¤",
    "&yen;", "¥",
    "&brvbar;", "¦",
    "&sect;", "§",
    "&uml;", "¨",
    "&copy;", "©",
    "&ordf;", "ª",
    "&laquo;", "«",
    "&not;", "¬",
    "&reg;", "®",
    "&macr;", "¯",
    "&deg;", "°",
    "&plusmn;", "±",
    "&sup2;", "²",
    "&sup3;", "	³",
    "&acute;", "´",
    "&micro;", "µ",
    "&para;", "¶",
    "&middot;", "·",
    "&cedil;", "¸",
    "&sup1;", "¹",
    "&ordm;", "º",
    "&raquo;", "»",
    "&frac14;", "¼",
    "&frac12;", "½",
    "&frac34;", "¾",
    "&iquest;", "¿",
    "&Agrave;", "À",
    "&Aacute;", "Á",
    "&Acirc;", "Â",
    "&Atilde;", "Ã",
    "&Auml;", "Ä",
    "&Aring;", "Å",
    "&AElig;", "Æ",
    "&Ccedil;", "Ç",
    "&Egrave;", "È",
    "&Eacute;", "É",
    "&Ecirc;", "Ê",
    "&Euml;", "Ë",
    "&Igrave;", "Ì",
    "&Iacute;", "Í",
    "&Icirc;", "Î",
    "&Iuml;", "Ï",
    "&ETH;", "Ð",
    "&Ntilde;", "Ñ",
    "&Ograve;", "Ò",
    "&Oacute;", "Ó",
    "&Ocirc;", "Ô",
    "&Otilde;", "Õ",
    "&Ouml;", "Ö",
    "&times;", "×",
    "&Oslash;", "Ø",
    "&Ugrave;", "Ù",
    "&Uacute;", "Ú",
    "&Ucirc;", "Û",
    "&Uuml;", "Ü",
    "&Yacute;", "Ý",
    "&THORN;", "Þ",
    "&szlig;", "ß",
    "&agrave;", "à",
    "&aacute;", "á",
    "&acirc;", "â",
    "&atilde;", "ã",
    "&auml;", "ä",
    "&aring;", "å",
    "&aelig;", "æ",
    "&ccedil;", "ç",
    "&egrave;", "è",
    "&eacute;", "é",
    "&ecirc;", "ê",
    "&euml;", "ë",
    "&igrave;", "ì",
    "&iacute;", "í",
    "&icirc;", "î",
    "&iuml;", "ï",
    "&eth;", "ð",
    "&ntilde;", "ñ",
    "&ograve;", "ò",
    "&oacute;", "ó",
    "&ocirc;", "ô",
    "&otilde;", "õ",
    "&ouml;", "ö",
    "&divide;", "÷",
    "&oslash;", "ø",
    "&ugrave;", "ù",
    "&uacute;", "ú",
    "&ucirc;", "û",
    "&uuml;", "ü",
    "&yacute;", "ý",
    "&thorn;", "þ",
    "&yuml;", "ÿ",
    "&euro;", "€",
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

lowerList = "aàâäã@bcdeéèêëfghiîïìjklmnñoôöõòpqrstuûüùvwxyz"

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

upperList = "AÀÂÀÃ@BCDEÉÈÊËFGHIÎÏÌJKLMNÑOÔÖÕÒPQRSTUÛÜÙVWXYZ"



# all recognized delimiters

wordDelimiterList = [
    " ",
    ",",
    "\t",
    "="
    ]

# xml encoder. Defines the characters that can be copied-pasted from clipboard and external documents

xmlFormat = "UTF-8"


