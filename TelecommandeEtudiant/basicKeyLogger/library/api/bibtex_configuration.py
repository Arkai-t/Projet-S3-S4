# -*- coding: cp1252 -*-

# previous - * - c o d i n g : cp1252 - * -

#
# elements of BibTeX syntax
#

import os





# table of deaccentuation of characters

accentTable = [
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


# list of aliases for fields

aliasDictionary = {
"authors" : "author",
"book" : "booktitle",
"chap" : "chapter",
"ed" : "editor",
"editors" : "editor",
"eds" : "editor",
"date" : "year",
"mm" : "month",
"months" : "month",
"pp" : "pages",
"pub" : "publisher",
"publishers" : "publisher",
"num" : "number",
"vol" : "volume",
"years" : "year",
"yy" : "year",
}

    


# comment delimiter

commentDelimiter = "#"

# field delimiter

fieldDelimiter = ","

# special characters in latex/bibtex (limited to accented letters and usual foreign letters)

escapeTable = [
"{\\`A}", "�",
"{\\'A}", "�",
"{\\^A}", "�",
"{\\~A}", "�",
'{\\"A}', "�",
"{\\AA}", "�",
"{\\AE}", "�",
"{\\cC}", "�",
"{\\`E}", "�",
"{\\'E}", "�",
"{\\^E}", "�",
'{\\"E}', "�",
"{\\`I}", "�",
"{\\'I}", "�",
"{\\^I}", "�",
'{\\"I}', "�",
"{\\~N}", "�",
"{\\`O}", "�",
"{\\'O}", "�",
"{\\^O}", "�",
"{\\~O}", "�",
'{\\"O}', "�",
"{\\O}", "�",
"{\\`U}", "�",
"{\\'U}", "�",
"{\\^U}", "�",
'{\\"U}', "�",
"{\\'Y}", "�",
"{\\cc}", "�",
"{\\~n}", "�",
"{\\ss}", "�",
"{\\`a}", "�",
"{\\'a}", "�",
"{\\^a}", "�",
"{\\~a}", "�",
'{\\"a}', "�",
"{\\aa}", "�",
"{\\ae}", "�",
"{\\`e}", "�",
"{\\'e}", "�",
"{\\^e}", "�",
'{\\"e}', "�",
"{\\`i}", "�",
"{\\'i}", "�",
"{\\^i}", "�",
'{\\"i}', "�",
"{\\`o}", "�",
"{\\'o}", "�",
"{\\^o}", "�",
"{\\~o}", "�",
'{\\"o}', "�",
"{\\o}", "�",
"{\\`u}", "�",
"{\\'u}", "�",
"{\\^u}", "�",
'{\\"u}', "�",
"{\\'y}", "�",
'{\\"y}', "�",

"{\\`{A}}", "�",
"{\\'{A}}", "�",
"{\\^{A}}", "�",
"{\\~{A}}", "�",
'{\\"{A}}', "�",
"{\\A{A}}", "�",
"{\\A{E}}", "�",
"{\\c{C}}", "�",
"{\\`{E}}", "�",
"{\\'{E}}", "�",
"{\\^{E}}", "�",
'{\\"{E}}', "�",
"{\\`{I}}", "�",
"{\\'{I}}", "�",
"{\\^{I}}", "�",
'{\\"{I}}', "�",
"{\\~{N}}", "�",
"{\\`{O}}", "�",
"{\\'{O}}", "�",
"{\\^{O}}", "�",
"{\\~{O}}", "�",
'{\\"{O}}', "�",
"{\\{O}}", "�",
"{\\`{U}}", "�",
"{\\'{U}}", "�",
"{\\^{U}}", "�",
'{\\"{U}}', "�",
"{\\'{Y}}", "�",
"{\\c{c}}", "�",
"{\\~{n}}", "�",
"{\\s{s}}", "�",
"{\\`{a}}", "�",
"{\\'{a}}", "�",
"{\\^{a}}", "�",
"{\\~{a}}", "�",
'{\\"{a}}', "�",
"{\\a{a}}", "�",
"{\\a{e}}", "�",
"{\\`{e}}", "�",
"{\\'{e}}", "�",
"{\\^{e}}", "�",
'{\\"{e}}', "�",
"{\\`{i}}", "�",
"{\\'{i}}", "�",
"{\\^{i}}", "�",
'{\\"{i}}', "�",
"{\\`{o}}", "�",
"{\\'{o}}", "�",
"{\\^{o}}", "�",
"{\\~{o}}", "�",
'{\\"{o}}', "�",
"{\\{o}}", "�",
"{\\`{u}}", "�",
"{\\'{u}}", "�",
"{\\^{u}}", "�",
'{\\"{u}}', "�",
"{\\'{y}}", "�",
'{\\"{y}}', "�",
## "{\\textasciitilde{}}", "~", # pointless in bibtex, and tilde is used for initials
"{\\#}", "#",
"{\\textdollar{}}", "$",
"{\\%}", "%",
"{\\^{}}", "^",
"{\\&}", "&",
"{\\{}", "{",
"{\\}}", "}",
"{\\textbackslash{}}", "\\",
"{\\textvert{}}", "|",
## "{\\_}", "_", # pointless in bibtex
"{\\textless{}}", "<",
"{\\textgreater{}}", ">",
"{\\textexclamdown{}}", "�",
"{\\textcent{}}", "�", 
"{\\textsterling{}}", "�",
"{\\textcurrency{}}", "�",
"{\\textyen{}}", "�",
"{\\textbrokenbar{}}", "�",
"{\\textsection{}}", "�",
"{\\textasciidieresis{}}", "�",
"{\\textcopyright{}}", "�",
"{\\textordfeminine{}}", "�",
"{\\guillemotleft{}}", "�",
"{\\textregistered{}}", "�",
"{\\textasciimacron{}}", "�", 
"{\\textdegree{}}", "�", 
"{\\textasciiacute{}}", "�",

# invalid syntax found in some bibtex from scholar
"{\\\\`A}", "�",
"{\\\\'A}", "�",
"{\\\\^A}", "�",
"{\\\\~A}", "�",
'{\\\\"A}', "�",
"{\\\\AA}", "�",
"{\\\\AE}", "�",
"{\\\\cC}", "�",
"{\\\\`E}", "�",
"{\\\\'E}", "�",
"{\\\\^E}", "�",
'{\\\\"E}', "�",
"{\\\\`I}", "�",
"{\\\\'I}", "�",
"{\\\\^I}", "�",
'{\\\\"I}', "�",
"{\\\\~N}", "�",
"{\\\\`O}", "�",
"{\\\\'O}", "�",
"{\\\\^O}", "�",
"{\\\\~O}", "�",
'{\\\\"O}', "�",
"{\\\\O}", "�",
"{\\\\`U}", "�",
"{\\\\'U}", "�",
"{\\\\^U}", "�",
'{\\\\"U}', "�",
"{\\\\'Y}", "�",
"{\\\\cc}", "�",
"{\\\\~n}", "�",
"{\\\\ss}", "�",
"{\\\\`a}", "�",
"{\\\\'a}", "�",
"{\\\\^a}", "�",
"{\\\\~a}", "�",
'{\\\\"a}', "�",
"{\\\\aa}", "�",
"{\\\\ae}", "�",
"{\\\\`e}", "�",
"{\\\\'e}", "�",
"{\\\\^e}", "�",
'{\\\\"e}', "�",
"{\\\\`i}", "�",
"{\\\\'i}", "�",
"{\\\\^i}", "�",
'{\\\\"i}', "�",
"{\\\\`o}", "�",
"{\\\\'o}", "�",
"{\\\\^o}", "�",
"{\\\\~o}", "�",
'{\\\\"o}', "�",
"{\\\\o}", "�",
"{\\\\`u}", "�",
"{\\\\'u}", "�",
"{\\\\^u}", "�",
'{\\\\"u}', "�",
"{\\\\'y}", "�",
'{\\\\"y}', "�",

"{\\\\`{A}}", "�",
"{\\\\'{A}}", "�",
"{\\\\^{A}}", "�",
"{\\\\~{A}}", "�",
'{\\\\"{A}}', "�",
"{\\\\A{A}}", "�",
"{\\\\A{E}}", "�",
"{\\\\c{C}}", "�",
"{\\\\`{E}}", "�",
"{\\\\'{E}}", "�",
"{\\\\^{E}}", "�",
'{\\\\"{E}}', "�",
"{\\\\`{I}}", "�",
"{\\\\'{I}}", "�",
"{\\\\^{I}}", "�",
'{\\\\"{I}}', "�",
"{\\\\~{N}}", "�",
"{\\\\`{O}}", "�",
"{\\\\'{O}}", "�",
"{\\\\^{O}}", "�",
"{\\\\~{O}}", "�",
'{\\\\"{O}}', "�",
"{\\\\{O}}", "�",
"{\\\\`{U}}", "�",
"{\\\\'{U}}", "�",
"{\\\\^{U}}", "�",
'{\\\\"{U}}', "�",
"{\\\\'{Y}}", "�",
"{\\\\c{c}}", "�",
"{\\\\~{n}}", "�",
"{\\\\s{s}}", "�",
"{\\\\`{a}}", "�",
"{\\\\'{a}}", "�",
"{\\\\^{a}}", "�",
"{\\\\~{a}}", "�",
'{\\\\"{a}}', "�",
"{\\\\a{a}}", "�",
"{\\\\a{e}}", "�",
"{\\\\`{e}}", "�",
"{\\\\'{e}}", "�",
"{\\\\^{e}}", "�",
'{\\\\"{e}}', "�",
"{\\\\`{i}}", "�",
"{\\\\'{i}}", "�",
"{\\\\^{i}}", "�",
'{\\\\"{i}}', "�",
"{\\\\`{o}}", "�",
"{\\\\'{o}}", "�",
"{\\\\^{o}}", "�",
"{\\\\~{o}}", "�",
'{\\\\"{o}}', "�",
"{\\\\{o}}", "�",
"{\\\\`{u}}", "�",
"{\\\\'{u}}", "�",
"{\\\\^{u}}", "�",
'{\\\\"{u}}', "�",
"{\\\\'{y}}", "�",
'{\\\\"{y}}', "�",
## "{\\textasciitilde{}}", "~", # pointless in bibtex, and tilde is used for initials
"{\\\\#}", "#",
"{\\\\textdollar{}}", "$",
"{\\\\%}", "%",
"{\\\\^{}}", "^",
"{\\\\&}", "&",
"{\\\\{}", "{",
"{\\\\}}", "}",
"{\\\\textbackslash{}}", "\\",
"{\\\\textvert{}}", "|",
## "{\\_}", "_", # pointless in bibtex
"{\\\\textless{}}", "<",
"{\\\\textgreater{}}", ">",
"{\\\\textexclamdown{}}", "�",
"{\\\\textcent{}}", "�", 
"{\\\\textsterling{}}", "�",
"{\\\\textcurrency{}}", "�",
"{\\\\textyen{}}", "�",
"{\\\\textbrokenbar{}}", "�",
"{\\\\textsection{}}", "�",
"{\\\\textasciidieresis{}}", "�",
"{\\\\textcopyright{}}", "�",
"{\\\\textordfeminine{}}", "�",
"{\\\\guillemotleft{}}", "�",
"{\\\\textregistered{}}", "�",
"{\\\\textasciimacron{}}", "�", 
"{\\\\textdegree{}}", "�", 
"{\\\\textasciiacute{}}", "�",

]


# matrix of fields allowed for each type

fieldMatrix = [
[ "owner", "author", "title", "journal", "volume", "number", "pages", "year", "month", "url", "copyright" ], # article
[ "owner", "author", "title", "editor", "publisher", "year", "isbn", "url", "copyright" ], # book
[ "owner", "author", "title", "year", "month", "url", "copyright" ], # booklet  not used in this API
[ "owner", "title", "year" ] , # collection, not used in this API
[ "owner", "author", "title", "editor", "publisher", "booktitle", "chapter", "pages", "year", "month", "url", "copyright" ], # conference ~inproceedings            
[ "owner", "author", "title", "editor", "publisher", "booktitle", "chapter", "pages", "year", "url", "copyright" ], #inbook
[ "owner", "author", "title", "year", "month", "url", "copyright" ], #incollection, not used in this API
[ "owner", "author", "title", "editor", "publisher", "booktitle", "chapter", "pages", "year", "month", "url", "copyright" ], # inproceedings
[ "owner", "author", "title", "institution", "year", "month", "url", "copyright" ], # manual
[ "owner", "author", "school", "title", "year", "month", "url", "copyright" ], # mastersthesis
[ "owner", "author", "title", "number", "year", "url" ], # patent
[ "owner", "author", "school", "title", "year", "month", "url", "copyright" ], # phdthesis
[ "owner", "title", "editor", "publisher", "year", "month", "isbn", "url", "copyright" ], #proceedings
[ "owner", "author", "institution", "title", "pages", "year", "month", "url", "copyright" ], # techreport
[ "owner", "author", "title", "year", "month", "url", "copyright" ], # unpublished, not used in this API
[ "owner", "author", "title", "institution", "year", "url", "copyright" ], # misc, here, limited to non-documents
[ "owner", "author", "title", "school", "institution", "year", "month", "url", "copyright" ], # course 
[ "owner", "author", "title", "institution", "year", "month", "url", "copyright" ], # dataset
[ "owner", "author", "title", "institution", "year", "month", "url", "copyright" ], # document
[ "owner", "author", "school", "title", "year", "month", "url", "copyright" ], # studentreport
[ "owner", "author", "title", "institution", "year", "month", "url", "copyright" ], # poster
[ "owner", "author", "title", "institution", "year", "month", "url", "copyright" ], # presentation 
[ "owner", "author", "title", "institution", "year", "month", "url", "copyright" ], # protocol
[ "owner", "author", "title", "institution", "year", "month", "url", "copyright" ], # software 
[ "owner", "author", "title", "institution", "year", "month", "url", "copyright" ], # tutorial
]
       
# list of months names

monthList = [
"jan",
"feb",
"mar",
"apr",
"may",
"jun",
"jul",
"aug",
"sep",
"oct",
"nov",
"dec"
]



# list of words that can be omitted from publication name (journal booktitle)

omissionList = [
"&",
"a",
"al",
"als",
"am",
"an",
"and",
"at",
"au",
"auf",
"aus",
"aux",
"con",
"d",
"da",
"das",
"de",
"dei",
"del",
"dell",
"delle",
"della",
"dem",
"den",
"der",
"des",
"di",
"die",
"do",
"du",
"e",
"el",
"en",
"et",
"foer",
"for",
"fra",
"from",
"fur",
"i",
"im",
"in",
"it",
"its",
"ja",
"kai",
"l",
"la",
"las",
"le",
"les",
"los",
"no",
"och",
"of",
"og",
"om",
"on",
"over",
"para",
"part",
"parts",
"pour",
"serie", 
"series",
"sowie",
"sur",
"the",
"their",
"to",
"uber",
"und",
"van",
"volume",
"volumes",
"von",
"vor",
"with",
"y",
"zu",
"zum",
"zur",
]

# fields required for each type

requiredMatrix = [
[ "author", "journal", "title", "year" ], # article
[ "author", "publisher", "title", "year" ], # book
[ "author", "title", "year" ], # booklet  not used in this API
[ "title", "year" ] , # collection, not used in this API
[ "booktitle", "title", "year" , "booktitle" ], #conference
[ "author", "booktitle", "pages", "publisher", "title", "year" ], #inbook
[ "author", "booktitle", "publisher", "title", "year" ], #incollection, not used in this API
[ "author", "title", "year", "booktitle" ], # inproceedings
[ "author", "title", "year" ], # manual
[ "author", "school", "title", "year" ], # mastersthesis
[ "author", "title", "year" ], # patent
[ "author", "school", "title", "year" ], # phdthesis
[ "title", "year" ], #proceedings
[ "author", "institution", "title", "year" ], # techreport
[ "author", "title", "year" ], # unpublished, not used in this API
[ "author", "title", "year" ], # misc, here, limited to non-documents
[ "author", "title", "year" ], # course 
[ "author", "title", "year" ], # dataSet
[ "author", "title", "year" ], # document
[ "author", "school", "title", "year" ], # studentreport
[ "author", "title", "year" ], # poster
[ "author", "title", "year" ], # presentation 
[ "author", "title", "year" ], # protocol
[ "title", "year" ], # software 
[ "author", "title", "year" ], # tutorial
]


# bibtex types

typeList = [
"article",
"book",
"booklet",  # not used in this API
"collection",  # not used in this API, equivalent to inproceedings (roughly)
"conference",  # equivalent to inproceedings; not used in this API
"inbook",
"incollection", # not used in this API
"inproceedings",
"manual",
"mastersthesis",
"patent",
"phdthesis",
"proceedings",
"techreport",
"unpublished",  # not used in this API
"misc", # here, limited to non-documents
"course", # added in this API
"dataset", # added in this API
"document", # added in this API
"studentreport", # added in this API
"poster", # added in this API
"presentation", # added in this API
"protocol", # added in this API
"software", # added in this API
"tutorial", # added in this API
]
