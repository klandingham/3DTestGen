#
# Edit this file to change settings
#
# vary_distance:
#   true => vary the retraction distance during the print
#   false => do not modify any distance values
#
# vary_speed:
#   true => vary the retraction speed during the print
#   false => do not modify any distance values
#
# values_mode:
#   range:
#       vary value between min and max
#   discrete:
#       use discrete values from ZZZZZZZZZZZZZZZZZZZZZZZZZZZz
#
RTconfig = dict(
    template_file='RetractionTestTemplate',
    vary_distance='true',
    vary_speed='false',
    values_mode='range',
    min_distance=1.0,
    max_distance=10.0,
    min_speed=1800,
    max_speed=1899
)
