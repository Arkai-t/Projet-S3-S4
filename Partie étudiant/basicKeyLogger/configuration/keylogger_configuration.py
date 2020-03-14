#
# configuration of KeyLogger
#



# uses absolute time stamps ( 1 ) or relative time stamps, starting from 0

absoluteFlag = 1 


# size of events buffer (eventList is incremented by blocks of this size )

##bufferSize = 16384


# converts buttons releases to C ( 1 ) or does not generate C operations for button release ( 0, default )

buttonReleaseFlag = 0

# daily start time (S) 0 = None

##dayStartS = 0

# daily stop time (S) 0 = None

##dayStopS = 0


# maximal time between consecutive events  of the same type (e.g. mouse move, mouse wheel ) to accept continuity

# continuityThresholdS = 0.100


# field delimiter in logs (tab \t or comma)

fieldDelimiter = "\t"


# converts key release to K ( 1 ) or does not generate K operations for key release release ( 0, default )

keyReleaseFlag = 0


# constants : numerical values of keys associated to predefined events

##keyStopLogger = 240
##
##keySynchronization = 241
##
##keySynchronization1 = 242
##
##keySynchronization2 = 243
##
##keyStartSession = 232
##
##keyStopSession = 233
##
##keyStartBlock = 234
##
##keyStopBlock = 235
##
##keyStartTrial = 236
##
##keyStopTrial = 237
##
##keySuspendLogger = 238
##
##keyResumeLogger = 239
##
##keyStartWrite = 244
##
##keyStopWrite = 245
##




# path to processed log ( KPC file )

kpcPath = "(root)/data/kpc_log.tsv"


# path to log

logPath = "(root)/data/key_log.tsv"



# threshold for detecting pauses

##pauseThresholdS = 1.


# sampling period in milliseconds

##samplingPeriodS = 0.010


# write mode for logs : append or write (overwrites previous log

##writeMode = "append"

# period to write log to disk ( 0 means at the end of session )

##writePeriodS = 0

