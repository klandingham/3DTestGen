# TODO HEADER
import ConfigParser
import os

# constants - shouldn't need to change any of these
CONFIG_FILE_PATH = r'RTGen.cfg'
TEMPLATE_FILE = ''

# globals
layer_count = 0
ext_temp = 0
bed_temp = 0


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
    global ext_temp
    global bed_temp

    print("Template file is \"%s\" ...analyzing..." % TEMPLATE_FILE)
    total_line_count = 0
    comment_line_count = 0
    for template_line in open(TEMPLATE_FILE).xreadlines():
        total_line_count = total_line_count + 1
        # skip comment lines
        if template_line.startswith(";", 0):
            comment_line_count = comment_line_count + 1
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
    print("      Total lines: %d" % total_line_count)
    print("     G-code lines: %d\n" % (total_line_count - comment_line_count))


def preview_settings():
    print("Template file is "),
    print(TEMPLATE_FILE),
    print("n")


def read_settings():
    global TEMPLATE_FILE
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
# preview_settings()
