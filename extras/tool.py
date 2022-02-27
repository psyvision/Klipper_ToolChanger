# Tool support
#
# Copyright (C) 2022  Andrei Ignat <andrei@ignat.se>
#
# This file may be distributed under the terms of the GNU GPLv3 license.
import logging

class Tool:
    def __init__(self, config, extruder_num):
        self.printer = config.get_printer()
        #self.name = config.get_name().split()[-1]
        self.name = config.get_name().split(' ')[1]

        if not unicode(self.name, 'utf-8').isnumeric():
            raise config.error(
                    "Name of section '%s' contains illegal characters. Use only integer tool number."
                    % (config.get_name()))

        # ToolType, defaults to 0. Check if tooltype is defined.
        self.tooltype = 'tooltype ' + str(config.getint('tool_type', 0))
        if config.has_section(self.tooltype):
            self.tooltype = self.printer.lookup_object(self.tooltype)
        else:
            raise config.error(
                    "Tooltype of '%s' is not defined. It must be configured before the tool."
                    % (config.get_name()))

        self.type = self.tooltype.Physical
        self.ercf_physical_tool = 0             # Physical tool for the ERCF. This is parent tool and can be same as virtual. Requred on virtual tool and on physical tool holding virtual tools.
        #self.zone_x = 0                         # X to do a fast approach for when parked. Requred on Physical tool
        #self.zone_y = 0                         # Y to do a fast approach for when parked. Requred on Physical tool
        #self.park_x = 0                         # X to do a slow approach for when parked. Requred on Physical tool
        #self.park_y = 0                         # Y to do a slow approach for when parked. Requred on Physical tool
        #self.offset_x = 0                       # Nozzle offset to probe. Requred on Physical tool
        #self.offset_y = 0                       # Nozzle offset to probe. Requred on Physical tool
        #self.offset_z = 0                       # Nozzle offset to probe. Requred on Physical tool
        #self.fan = "none"           # Name of general fan configuration connected to this tool as a part fan. Defaults to "none".
        #self.extruder = "none"              # Name of extruder connected to this tool. Defaults to "none".
        #self.meltzonelength = 0                # Length of the meltzone for retracting and inserting filament on toolchange. 18mm for e3d Revo
        #self.heater_state = 0                   # 0 = off, 1 = standby temperature, 2 = active temperature. Placeholder. Requred on Physical tool.
        #self.heater_active_temp = 0             # Temperature to set when in active mode. Placeholder. Requred on Physical and virtual tool if any has extruder.
        #self.heater_standby_temp = 0            # Temperature to set when in standby mode.  Placeholder. Requred on Physical and virtual tool if any has extruder.
        #self.idle_to_standby_time = 30          # Time in seconds from being parked to setting temperature to standby the temperature above. Use 0.1 to change imediatley to standby temperature. Requred on Physical tool
        #self.idle_to_powerdown_time = 600       # Time in seconds from being parked to setting temperature to 0. Use something like 86400 to wait 24h if you want to disable. Requred on Physical tool.
        #self.wipe_type = 0                      # 0 = none, 1= Only load filament, 2= Wipe in front of carriage, 3= Pebble wiper, 4= First Silicone, then pebble. Defaults to 0.
        ##self.wipe_silicone_park_side = ""   # Position on the side near parking spot of the silicone flap.  Must include X or Y. Requred on Physical tool if Wipe Type = 2 or 4.
        ##self.wipe_silicone_print_side = ""  # Position on the side near printing side of the silicone flap. Must include X or Y. Requred on Physical tool if Wipe Type = 2 or 4.
        #self.placeholder_standby_temp = 0       # Required placeholder if this tool has virtual tools. Holds last used standby temp of physical heater.

        #self.printer = printer
        #self.eventtime = eventtime
        #self.printer = config.get_printer()

        # G-Code macros
        gcode_macro = self.printer.load_object(config, 'gcode_macro')



        self.custom_select_gcode_template = gcode_macro.load_template(config, 'custom_select_gcode', '')
        self.custom_deselect_gcode_template = gcode_macro.load_template(config,
                                                          'custom_deselect_gcode', '')

        # Register commands
        gcode = config.get_printer().lookup_object('gcode')
        gcode.register_command("T" + self.name, self.cmd_SelectTool, desc=self.cmd_SelectTool_help)
        gcode.register_command("T49", self.cmd_SelectTool49, desc=self.cmd_SelectTool49_help)


    cmd_SelectTool_help = "Select T49"
    def cmd_SelectTool(self, gcmd):
        gcmd.respond_info("T" + self.name + " Selected.") # + self.get_status()['state'])
        

    cmd_SelectTool49_help = "Select T49"
    def cmd_SelectTool49(self, gcmd):
        gcmd.respond_info("T-" + self.tname + "Selected.") # + self.get_status()['state'])

######################################################################
# Load Config
#####################################################################
def load_config_prefix(config):
    #printer = config.get_printer()
    #for i in range(99):
    #    section = 'tool %d' % (i,)
    #    if not config.has_section(section):
    #        continue
    #    pt = Tool(config.getsection(section), i)
    #    printer.add_object(section, pt)
    return Tool(config)
