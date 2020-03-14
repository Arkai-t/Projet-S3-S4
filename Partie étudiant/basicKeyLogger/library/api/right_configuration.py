# Access rights. place the desired access rights in one single string, space (or whatever delimiter)separated
#

rights = "administrator"


#
# possible access rights are 
#
#   * : all rights
#   administrator: all rights
#
#   configuration: edit configuration files, edit popup lists used in entry fields and menus. Automatic restart in case
#	of change
#
#   procedure: edit procedures directories and procedures files. Automatic update of current procedure in case of change.
#     also, procedures have the rights of 'file', 'directory' and 'link'.
#
#   user : edit files, open paths and directories, open links (rights 'file', 'directory' and 'link' )
#   
#   file: can edit files displayed in widgets.
#
#   link: can open links displayed in wiki texts
#
#   directory: can open paths (files and/or directories) displayed in directory lists.
#
