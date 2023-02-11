from PyP100 import PyP110, PyL530

class Hardware():
    def __init__(self, plugIP1, plugIP2, bulbIP, email, password):
        super().__init__()

        try:
            self.plug1 = PyP110.P110(plugIP1, email, password)
            self.plug1.handshake()
            self.plug1.login()

            self.plug2 = PyP110.P110(plugIP2, email, password)
            self.plug2.handshake()
            self.plug2.login()

            self.bulb = PyL530.L530(bulbIP, email, password)
            self.bulb.handshake()
            self.bulb.login()
        except:
            print("Some of your devices may not work as you have not entered an ip address into the application")

    def getDeviceStatus(self, device_name):
        if device_name == "p1":
            result = self.plug1.getDeviceInfo()["result"]
            status = result["device_on"]
            return status
        if device_name == "p2":
            result = self.plug2.getDeviceInfo()["result"]
            status = result["device_on"]
            return status
        if device_name == "b":
            result = self.bulb.getDeviceInfo()["result"]
            status = result["device_on"]
            return status

    def allDevicesOn(self):
        self.plug1.turnOn()
        self.plug2.turnOn()
        self.bulb.turnOn()

    def allDevicesOff(self):
        self.plug1.turnOff()
        self.plug2.turnOff()
        self.bulb.turnOff()

    def deviceToggle(self, deviceName, turnOn):
        if deviceName == "p1":
            if turnOn == True:
                self.plug1.turnOn()
                print("Plug 1 has been turned on")
            elif turnOn == False:
                self.plug1.turnOff()
                print("Plug 1 has been turned off")
            else:
                self.plug1.toggleState()
                print("Plug 2 has been toggled")
        elif deviceName == "p2":
            if turnOn == True:
                self.plug2.turnOn()
                print("Plug 2 has been turned on")
            elif turnOn == False:
                self.plug2.turnOff()
                print("Plug 2 has been turned off")
            else:
                self.plug2.toggleState()
                print("Plug 1 has been toggled")
        elif deviceName == "b":
            if turnOn == True:
                self.bulb.turnOn()
                print("Bulb has been turned on")
            elif turnOn == False:
                self.bulb.turnOff()
                print("Bulb has been turned off")
            else:
                self.bulb.toggleState()
                print("Bulb has been toggled")

    def increaseHue(self):
        try:
            result = self.bulb.getDeviceInfo()["result"]
            hue = int(result["hue"]) + 10
            saturation = int(result["saturation"])
            self.bulb.setColor(hue, saturation)
            return "Hue has been increased by 10"
        except:
            return "Hue cannot be increased further"

    def decreaseHue(self):
        try:
            result = self.bulb.getDeviceInfo()["result"]
            hue = int(result["hue"]) - 10
            saturation = int(result["saturation"])
            self.bulb.setColor(hue, saturation)
            return "Hue has been decreased by 10"
        except:
            return "Hue cannot be decreased further"

    def increaseSaturation(self):
        try:
            result = self.bulb.getDeviceInfo()["result"]
            hue = int(result["hue"])
            saturation = int(result["saturation"]) + 10
            self.bulb.setColor(hue, saturation)
            return "Saturation has been increased by 10"
        except:
            return "Saturation cannot be increased further"

    def decreaseSaturation(self):
        try:
            result = self.bulb.getDeviceInfo()["result"]
            hue = int(result["hue"])
            saturation = int(result["saturation"]) - 10
            self.bulb.setColor(hue, saturation)
            return "Saturation has been decreased by 10"
        except:
            return "Saturation cannot be decreased further"

    def changeLightSettings(self, hue, brightness, saturation, colour_temperature):
        try:
            self.bulb.setColor(hue, saturation)
            self.bulb.setBrightness(brightness)

            if colour_temperature == "invalid":
                result = self.bulb.getDeviceInfo()["result"]
                colour_temperature = int(result["color_temp"])

            self.bulb.setColorTemp(colour_temperature)
            print("The colours have been changed")
        except:
            return "Could not perform action"

    def showEnergyUsage(self):
        plug1Energy = self.plug1.getEnergyUsage()["result"]
        plug2Energy = self.plug2.getEnergyUsage()["result"]

        plug1Runtime = int(plug1Energy["month_runtime"]) // 60
        plug2Runtime = int(plug2Energy["month_runtime"]) // 60

        energy = "plug one has used " + str(plug1Energy["month_energy"]) + " watts this month and " + \
                 "plug two has used " + str(plug2Energy["month_energy"]) + " watts this month. Plug one has been running for " + \
                 str(plug1Runtime) + "hours and plug two has been running for " + str(plug2Runtime) + "hours"

        return energy