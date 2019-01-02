# TODO HEADER
#
# Questions:
#
#   How hard to vary layer height?
#   - if I vary layer height what else varies?
#           Test by comparing G-code files: going from a .2 layer to a .1 layer:
#               - for every "G1 Z" command the Z value is halved
#               - for every "G1 X<val> Y<val> E" the extraction ("E") value is halved
#               - *HARD* when layer height is changed, total number of layers required to get original height
#                 changes, so to get the same height model, I would have to either subtract existing or add new
#                 layers (HARD), BUT...who cares if the original height is maintained? The original intent is to
#                 compare the *print quality*, so I may just add a caveat to the layer height

import ConfigParser
import os

# constants - shouldn't need to change any of these
from math import ceil

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
num_sections = 0
vary_retract_dist = "disabled"
vary_retract_speed = "disabled"
nozzle_temp_mode = "disabled"
nozzle_temp_values = []

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
    global num_base_layers

    model_layer_height = 0
    last_z_position = 0

    print("\nTemplate file is \"%s\"" % TEMPLATE_FILE)
    print("Analyzing...\n")
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
            z_position = float(template_line.split()[1][1:])
            if 0 == last_z_position: # first Z movement
                # last_layer_movement = float(z_position)
                last_z_position = float(z_position)
            else:
                layer_height = z_position - last_z_position
                last_z_position = z_position
                if 0 == model_layer_height:  # once determined, the layer height must never change in the template file
                    model_layer_height = layer_height
                elif abs(model_layer_height - layer_height) > 0.00001:
                    exit(1)     # TODO: Add error handler: "inconsistent layer height in template file"
            layer_count += 1
        elif -1 != template_line.find("G1 E-"):
            temp_arg = template_line.split()[1]
            retract_dist = float(temp_arg[2:])
        elif -1 != template_line.find("G1 E"):
            temp_arg = template_line.split()[2]
            retract_speed = int(temp_arg[1:])


def set_nozzle_temps(temp_mode, num_sections, **kwargs):
    global nozzle_temp_values

    if "discrete" == temp_mode:
        nozzle_temp_values = kwargs["discrete_values"].split()
        if (num_sections != len(nozzle_temp_values)):
            print("\n\nERROR:\nNumber of discrete nozzle temperature values"),
            print("is different than the number of sections to be generated.\n")
            print("Please check the configuration file. Exiting...")
            exit(4)
    elif "range" == temp_mode:
        min_value = int(kwargs["min"])
        max_value = int(kwargs["max"])
        step = float((int(max_value) - int(min_value)) / float((num_sections - 1)))
        nozzle_temp_values = [float(min_value + step * x) for x in range(num_sections)]
        print nozzle_temp_values


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
    print("       Layer height: %.2f mm" % layer_height)


def read_settings():
    global TEMPLATE_FILE
    global base_height
    global num_sections
    global nozzle_temp_mode
    #
    #
    # get config file
    #
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
    #
    #
    # get height (mm) of model base and desired number of test sections
    #
    base_height = float(config_parser.get("MainOpts", "BaseHeight").strip())
    num_sections = int(config_parser.get("MainOpts", "NumTestSections").strip())
    if 2 > num_sections:
        print("\n\nERROR:\nYou must specify at least 2 test sections,"),
        print("or else why bother using this program?")
        print("Please check the configuration file. Exiting...")
        exit(2)
    nozzle_temp_mode = config_parser.get("MainOpts", "VaryNozzleTemp")
    if "discrete" == nozzle_temp_mode:
        try:
            nozzle_temps = config_parser.get("MainOpts", "NozzleTemps")
            set_nozzle_temps(nozzle_temp_mode, num_sections, discrete_values = nozzle_temps)
        except ConfigParser.NoOptionError:
            print("\n\nERROR:\nVaryNozzleTemp is set to \"discrete\" but no setting containing"),
            print("the desired values was found.\n")
            print("Please check the configuration file. Exiting...")
            exit(3)
    elif "range" == nozzle_temp_mode:
        try:
            nozzle_temp_min = config_parser.get("MainOpts", "NozzleTempMin")
            nozzle_temp_max = config_parser.get("MainOpts", "NozzleTempMax")
            set_nozzle_temps(nozzle_temp_mode, num_sections, min = nozzle_temp_min, max = nozzle_temp_max)
        except ConfigParser.NoOptionError:
            print("\n\nERROR:\nVaryNozzleTemp is set to \"range\" but the desired min"),
            print("and max settings were not found.\n")
            print("Please check the configuration file. Exiting...")
            exit(5)





    vary_retract_dist = config_parser.get("MainOpts", "VaryRetractionDistance")
    vary_retract_speed = config_parser.get("MainOpts", "VaryRetractionSpeed")
    vary_print_speed = config_parser.get("MainOpts", "VaryPrintSpeed")
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


def confirm_settings():
    global num_base_layers

    print("\nSettings: \n")
    num_base_layers = int(ceil(base_height / layer_height))
    print("             Base height: %.2f mm" % base_height),
    print("(%d layers)" % num_base_layers)
    print(" Number of test sections: %d" % num_sections)
    layers_per_section = (layer_count - num_base_layers) / num_sections
    print("      Layers per section: %d" % layers_per_section)
    print("        Vary nozzle temp: %s" % nozzle_temp_mode)
    print("Vary retraction distance: %s" % vary_retract_dist)
    print("   Vary retraction speed: %s" % vary_retract_speed)
    print("        Vary print speed: %s" % vary_retract_speed)
    print("Test Generator Settings")
    print("=======================")
    if len(nozzle_temp_values) > 0:
        print("Extruder temp values:"),
        print nozzle_temp_values


    # print("        Total lines: %d" % total_line_count)
    # print("   Number of layers: %d" % layer_count)
    # print("      Extruder temp: %d" % ext_temp)
    # print("           Bed temp: %d" % bed_temp)
    # print("   Retraction speed: %d mm/min" % retract_speed),
    # print("(%.2f mm/sec)" % (retract_speed / 60.0))
    # print("Retraction distance: %.2f mm" % retract_dist)
    # print("       Layer height: %.2f mm" % layer_height)


read_settings()
analyze_template_file()
print_model_info()
confirm_settings()
