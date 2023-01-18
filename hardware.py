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


    def allDevicesOn(self):
        self.plug1.turnOn()
        self.plug2.turnOn()
        self.bulb.turnOn()

    def allDevicesOff(self):
        self.plug1.turnOff()
        self.plug2.turnOff()
        self.bulb.turnOff()

    def deviceToggle(self, deviceName):
        if deviceName == "p1":
            self.plug1.toggleState()
        elif deviceName == "p2":
            self.plug2.toggleState()
        elif deviceName == "b":
            self.bulb.toggleState()

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

    def showEnergyUsage(self):
        plug1Energy = self.plug1.getEnergyUsage()["result"]
        plug2Energy = self.plug2.getEnergyUsage()["result"]

        plug1Runtime = int(plug1Energy["month_runtime"]) // 60
        plug2Runtime = int(plug2Energy["month_runtime"]) // 60

        energy = "plug one has used " + str(plug1Energy["month_energy"]) + " watts this month and " + \
                 "plug two has used " + str(plug2Energy["month_energy"]) + " watts this month. Plug one has been running for " + \
                 str(plug1Runtime) + "hours and plug two has been running for " + str(plug2Runtime) + "hours"

        return energy