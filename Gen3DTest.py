# TODO HEADER
#
# Questions:
#
#   How hard to vary layer height?
#   - if I vary layer height what else varies?
#           Going from a .2 layer to a .1 layer:
#               - for every "G1 Z" command the Z value is halved
#               - for every "G1 X<val> Y<val> E" the extraction ("E") value is halved
#               - *HARD* when layer height is changed, total number of layers required to get original height
#                 changes, so to get the same height model, I would have to either subtract existing or add new
#                 layers (HARD), BUT...who cares if the original height is maintained? The original intent is to
#                 compare the *print quality*, so I may just add a caveat to the layer height

import ConfigParser
import os

# constants - shouldn't need to change any of these
CONFIG_FILE_PATH = r'RTGen.cfg'
TEMPLATE_FILE = ''

# globals
# template file characteristics
total_line_count = 0
layer_count = 0
layer_height = 0
ext_temp = 0
bed_temp = 0
retract_dist = 0
retract_speed = 0

# user settings (from config file)
base_height = 0

#
#
# Printing examples
#
# print "Welcome to Python!"
# print "Welcome",
# print "to Python!"
# print "Welcome\nto\n\nPython!"
#
#
# Console input examples
#
# read strings and convert to integers
# integer1 = raw_input("Enter first integer: ")
# integer1 = int(integer1)
# integer2 = raw_input("Enter second integer: ")
# integer2 = int(integer2)
# # compute, assign and print sum
# theSum = integer1 + integer2
# print "Sum is", theSum
#
#
# Read settings
#

# if ( !( $file = fopen( "fig29_17.txt",
# "append" ) ) ) {
# // print error message and terminate script
# // execution if file cannot be opened
# print( "<title>Error</title></head><body>
# Could not open password file
# </body></html>" );
# die();
# }


# def read_settings():
#     if 1 != os.path.exists(settingsFilename):
#         print("\nError: settings file:"),
#         print("\"" + settingsFilename + "\" not found."),
#         print("exiting...\n")
#         exit(1)
#     for settings_line in open(settingsFilename).xreadlines():
#         if settings_line[0] != "#":
#             tokens = settings_line.strip().split()
#             print("comment")
#         else:
#             print(settings_line)
#
#
# read_settings()


def analyze_template_file():
    global TEMPLATE_FILE
    global retract_dist
    global retract_speed
    global ext_temp
    global bed_temp
    global total_line_count
    global layer_count
    global layer_height

    print("\nTemplate file is \"%s\"" % TEMPLATE_FILE)
    print("\nAnalyzing...\n")
    total_line_count = 0
    for template_line in open(TEMPLATE_FILE).xreadlines():
        total_line_count += 1
        # skip comment lines
        if template_line.startswith(";", 0):
            continue
        # extruder temperature
        elif -1 != template_line.find("M104") or -1 != template_line.find("M109"):
            # parse line and read temp value
            temp_arg = template_line.split()[1]
            temp = int(temp_arg[1:])
            if temp > 0:
                ext_temp = temp
        # bed temperature
        elif -1 != template_line.find("M140") or -1 != template_line.find("M190"):
            # parse line and read temp value
            temp_arg = template_line.split()[1]
            temp = int(temp_arg[1:])
            if temp > 0:
                bed_temp = temp
        # Z-axis movement (e.g., layer)
        elif -1 != template_line.find("G1 Z"):
            layer_count += 1
        elif -1 != template_line.find("G1 E-"):
            temp_arg = template_line.split()[1]
            retract_dist = float(temp_arg[2:])
        elif -1 != template_line.find("G1 E"):
            temp_arg = template_line.split()[2]
            retract_speed = int(temp_arg[1:])


def print_model_info():
    global retract_dist
    global retract_speed
    global ext_temp
    global bed_temp
    global total_line_count
    global layer_count
    global layer_height

    print("        Total lines: %d" % total_line_count)
    print("   Number of layers: %d" % layer_count)
    print("      Extruder temp: %d" % ext_temp)
    print("           Bed temp: %d" % bed_temp)
    print("   Retraction speed: %d mm/min" % retract_speed),
    print("(%.2f mm/sec)" % (retract_speed / 60.0))
    print("Retraction distance: %.2f mm" % retract_dist)


def read_settings():
    global TEMPLATE_FILE
    global base_height

    print("\nInitializing...\n")
    if 1 != os.path.exists(CONFIG_FILE_PATH):
        print("\nError: configuration file:"),
        print("\"" + CONFIG_FILE_PATH + "\" not found."),
        print("exiting...\n")
        exit(1)
    config_parser = ConfigParser.RawConfigParser()
    config_parser.read(CONFIG_FILE_PATH)
    TEMPLATE_FILE = config_parser.get("MainOpts", "TemplateFile").strip()
    if 1 != os.path.exists(TEMPLATE_FILE):
        print("\nError: Can't find template G-code file:"),
        print("\"" + TEMPLATE_FILE + "\"!"),
        print("exiting...\n")
        exit(1)
    base_height = config_parser.get("MainOpts", "baseHeight").strip()
    # if 1 != os.path.exists(settingsFilename):
    #     print("\nError: settings file:"),
    #     print("\"" + settingsFilename + "\" not found."),
    #     print("exiting...\n")
    #     exit(1)
    # for settings_line in open(settingsFilename).xreadlines():
    #     if settings_line[0] != "#":
    #         tokens = settings_line.strip().split()
    #         print("comment")
    #     else:
    #         print(settings_line)
#


read_settings()
analyze_template_file()
print_model_info()
# confirm_settings()
# preview_settings()
