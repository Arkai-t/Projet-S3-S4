#
# configuration of KeyLogger's window
#


# background color of internal panel for each state of the window

backgroundList = [
[ 208, 0, 0 ],
[ 128, 128, 128 ],
[ 208, 0, 0 ],
[ 0, 228, 228 ],
[ 0, 228, 228 ],
[ 0, 0, 192 ]
]

# font features

fontName = "Arial"

fontSize = 14

fontBold = True

fontItalic = False

# foreground color of messages for each state of the window

foregroundList = [
[ 255, 255, 255 ],
[ 0, 0, 0 ],
[ 255, 255, 255 ],
[ 0, 0, 0 ],
[ 0, 0, 0 ],
[ 255, 255, 255 ]
]

# icons for each state of the window

iconList = [
"(library)/keylog/error.png",
"(library)/keylog/halt.png",
"(library)/keylog/error.png",
"(library)/keylog/record.png",
"(library)/keylog/record.png",
"(library)/keylog/record.png"
]


# initial configuration maximized or minimized (true) for each state

minimizeList = [
False,
False,
False,
True,
True,
False
]

# program name

program = "Basic Key Logger"

# states of the window

stateList = [
"error",
"halt",
"present",
"record",
"start",
"stop"
]


# texts for each state of the window

textList = [
"Sorry. Windows only",
"Halted. Click to finish",
"Already running",
"Recording... Click to finish",
"",
"Writing logs..."
]

# version of program

version = "2011-03-01"

# duration of warnings in seconds

warningS = 3.

# size

windowSize = [ 480, 16 ]

