#!/usr/bin/env python

class Controller:
    def __init__(self):
        self.keys = []  # Hardware keyboard keys
        self.soft = []  # Software buttons (from Button(Enum))
        self.hard = []  # Hardware buttons
        self.axes = []  # Hardware axes
        self.hats = []  # Hardware hats
        self.dirs = []  # Software axes
        self.digi = True  # copy the hat value to the dirs as -1 or 1
        self.padi = None  # If None all joysticks affect the controller.
        self.mbtn = []  # map a button index to a soft button value
        self.rbtn = []  # This is the reverse map from button as string
                        # back to a hardware index.
        self.maxs = []  # map an axis index to a soft axis value
        self.raxs = []  # This is the reverse map from axis as string
                        # back to a hardware index.
    

    def addButtonMap(self, index, button):
        '''
        Set the hardware index to the given software button.

        Sequential arguments:
        index -- Choose the hardware button index such as in
                 joystick.get_button(index)
        button -- Choose the software button that will be affected by
                  setKey(index, value).
        '''
        while (len(self.mbtn) - 1) < index:
            self.mbtn.append(False)
        self.mbtn[index] = button
        self.rbtn[str(button)] = index

    def getSoft(self, button):
        '''
        Get software buttons

        Sequential arguments:
        button -- This must be a button value such as Button.NAB
        '''
        if button < len(self.soft):
            return self.soft[button]
        return False

    def getDir(self, index):
        '''
        Get software directional controls.
        If self.digi is set to True, the hats will have been overlayed
        onto the direction.

        Sequential arguments:
        index -- This is the axis index, usually 0 for x and 1 for y.
        '''
        if button < len(self.soft):
            return self.soft[button]
        return False

    def _setSoft(self, button, on):
        '''
        Sequential arguments:
        button -- This must be a button value such as Button.NAB
        on - True or False
        '''
        while (len(self.soft) - 1) < button:
            self.soft.append(False)
        self.soft[button] = on
        pass

    def _setDir(self, index, value):
        '''
        Sequential arguments:
        index -- This is the axis index, always 0 for x and 1 for y
                 since this is a deterministic software frontend for
                 controller(s).
        on - True or False
        '''
        while (len(self.dirs) - 1) < index:
            self.dirs.append(False)
        self.dirs[button] = value
        pass

    def setKey(self, index, on):
        '''
        Set a key. Alternatively, set self.keys to
        pygame.key.get_pressed() and avoid using this method.

        Sequential arguments:
        index -- The key index such as the pygame key.
        on - True or False
        '''
        while (len(self.keys) - 1) < index:
            self.keys.append(False)
        self.keys[button] = on
        self._setSoft(self.mbtn[index], on)
        pass

    def setAxis(self, index, value):
        '''
        Store a hardware axis after you read the hardware.

        Sequential arguments:
        index -- The axis, usually 0 for x and 1 for y
        value -- usually -1.0 to 1.0
        '''
        while (len(self.axes) - 1) < index:
            self.axes.append(False)
        self.axes[index] = value

    def setHat(self, index, coords):
        '''
        Store a hardware hat after you read the hardware.

        Sequential arguments:
        index -- The hat index, where each includes an x and y pair
        coords -- usually -x for left, +x right, -y down, +y up
        '''
        while (len(self.hats) - 1) < hatI:
            self.hats.append(False)
        self.hats[hatI] = coords
