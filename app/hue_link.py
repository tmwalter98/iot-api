import time
from colour import Color
import math
from phue import Bridge
from phue import PhueRegistrationException
from rgbxy import GamutC
from rgbxy import Converter

class HueLink:
    def __init__(self, bridge_ip):
        linked = False
        while(linked == False):
            try:
                self.bridge = Bridge(bridge_ip)
                self.bridge.connect()
                linked = True
            except PhueRegistrationException:
                print('Bridge Unregistered -> Must push button on bridge.')
                time.sleep(5)
            

        self.palette = self.create_palette()

    def create_palette(self):
        gradient_steps = 100
        gradient = list( Color("red").range_to(Color("green"), gradient_steps))
        converter = Converter(GamutC)
        return [converter.rgb_to_xy(color.red, color.green, color.blue) for color in gradient]

    # Function to change color of lightstrip under bed upon phone plugged in
    def bed_phone_indicator_on_plugin(self, battery_level):
        bed = self.bridge.get_light('Bed')
        bed_0 = bed['state']
    
        # If the light is on, perform battery indicator routine
        if(bed_0['on'] == True):
            palette = self.palette
            command = {'xy': palette.pop()}
            self.bridge.set_light(bed['name'], command)
            time.sleep(2)

            if(battery_level < 80):
                color_rgb = palette[math.floor((battery_level / 100) * len(palette))]
                command = {'xy': color_rgb, 'transitiontime': 1}
                self.bridge.set_light(bed['name'], command)
                time.sleep(2)
        
            bed_0 = {'xy': bed_0['xy']}
            bed_0['transitiontime'] = 18
            self.bridge.set_light(bed['name'], bed_0)

    def bed_phone_indicator_on_unplug(self, battery_level):
        bed = self.bridge.get_light('Bed')
        bed_0 = bed['state']

        # If the light is on, perform battery indicator routine
        if(bed_0['on'] == True):
            palette = self.palette
            color_rgb = palette[math.floor((battery_level / 100) * len(palette))]
            command = {'xy': color_rgb}
            self.bridge.set_light(bed['name'], command)
            time.sleep(2)

            bed_0 = {'xy': bed_0['xy']}
            bed_0['transitiontime'] = 18
            self.bridge.set_light(bed['name'], bed_0)
