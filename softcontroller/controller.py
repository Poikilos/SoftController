#!/usr/bin/env python

_verbose_controller_stats = True
_show_controller_stats = False

def set_controller_stats(on):
    '''
    Enable all controller messages continuously.

    Sequential arguments:
    on -- True for on, False for off
    '''
    global _verbose_controller_stats
    _verbose_controller_stats = on

class Controller:
    '''
    Each button, axis, hat, or key is mapped to a single sid (software
    id) identifying a virtual actuator. In the case of a key, it can
    add a specific value to the sid. Each sid is a string that is a key
    in the self._states dict. The value is any number, such as 0 for
    not pressed, 1 for pressed, or -1 for the opposite direction.

    The state of each virtual actuator can be affected by multiple
    types of hardware actuators and up to two keyboard keys. If 4 keys
    are necessary such as for a hat, then you must add two sids such
    as 'x' and 'y' (use the addKeyAsAxisValue twice for each sid but
    with a different keycode and value--See addKeyAsAxisValue).

    Create the controller(s) in a different file. Call all of the add
    methods on the controller before your program calls any other
    methods on the controller.
    '''

    # region initialization

    def __init__(self):
        self.deadZone = .2
        self._states = {}  # The state of each virtual actuator, usually
                           # -1.0 to 1.0 (or 0 or 1 for buttons, or any
                           # number of keyboard keys can affect it)

        self._btn_to_sid = {}  # map joystick button [str(num)] to sid
        self._sid_to_btn = {}  # reverse: [str(sid)] = button [str(num)]

        self._kc_to_sid = {}  # map keyboard [keycode] to sid
        self._sid_to_kcs = {}  # reverse map: [sid] to multiple keycodes
        self._kc_value = {}  # make the keycode set a specific value

        self._ax_to_sid = {}  # map joystick [axisIndex] to sid
        self._sid_to_ax = {}  # reverse map: [str(axis)] sid

        self._hat_to_sids = {}  # hat [hatID] values to sids: (sid, sid)
        self._sid_to_hat = {}  # reverse map: either axis sid to hatID


    def addKeyAsAxisValue(self, keycode, sid, value):
        '''
        keycode -- Set the keycode value.
        sid -- Choose a new/existing virtual actuator.
        value -- Set the axis to this value (such as: Make a down
                 arrow key set the axis value to 1)
        '''
        try:
            tmp = sid.strip()
        except AttributeError:
            raise TypeError("The sid must be some kid of string")
        self._kc_to_sid[str(keycode)] = sid
        self._sid_to_kcs[sid] = keycode
        self._kc_value[str(keycode)] = value

    def addAxis(self, axisIndex, sid):
        '''
        Sequential arguments:
        axisIndex -- an actual joystick axis number
        sid -- Choose a new/existing virtual actuator.
        '''
        try:
            tmp = sid.strip()
        except AttributeError:
            raise TypeError("The sid must be some kid of string")
        self._ax_to_sid[str(axisIndex)] = sid
        self._sid_to_ax[sid] = axisIndex

    def addButton(self, button, sid):
        '''
        Sequential arguments:
        button -- an actual joystick button number
        sid -- Choose a new/existing virtual actuator.
        '''
        try:
            tmp = sid.strip()
        except AttributeError:
            raise TypeError("The sid must be some kid of string")
        self._btn_to_sid[str(button)] = sid
        self._sid_to_btn[sid] = button

    def addKey(self, keycode, sid):
        '''
        Sequential arguments:
        keycode -- a hardware keycode
        sid -- Choose a new/existing virtual actuator.
        '''
        self._kc_to_sid[str(keycode)] = sid
        if self._sid_to_kcs.get(sid) is None:
            self._sid_to_kcs[sid] = []
        self._sid_to_kcs[sid].append(keycode)

    # endregion initialization

    # region runtime

    def getBool(self, sid):
        '''
        Get the value as True if > 0, otherwise False.

        Sequential arguments:
        sid -- Choose an existing virtual actuator.
        '''
        got = self._states.get(sid)
        if got is None:
            raise KeyError("{} is not a registered controller sid"
                           "".format(sid))
        return got > 0

    def getRaw(self, sid):
        '''
        Sequential arguments:
        sid -- Choose an existing virtual actuator.
        '''
        got = self._states.get(sid)
        if got is None:
            raise KeyError("{} is not a registered controller sid"
                           "".format(sid))
        return got

    def getInt(self, sid):
        '''
        Get the value as -1, 0, or 1 (It will be 0 unless
        abs(self._states[sid]) > self.deadZone).

        Sequential arguments:
        sid -- Choose an existing virtual actuator.
        '''
        got = self._states.get(sid)
        if got is None:
            raise KeyError("{} is not a registered controller sid"
                           "".format(sid))
        if abs(got) > self.deadZone:
            if got > 0:
                return 1
            else:
                return -1
        else:
            if _show_controller_stats:
                print("sid {}: abs({})"
                      " didn't get outside of self.deadZone"
                      "".format(sid, got))
        return 0

    def toKeys(self):
        '''
        Get a list of keys where the index is the keycode and the
        value is True or False for whether it is pressed. This only
        works for keys mapped using addKey and set using setKey.
        '''
        pressed = []
        count = 0
        for sid, kcs in self._sid_to_kcs.items():
            for kc in kcs:
                if (kc + 1) > count:
                    count = kc + 1
        for kc in range(count):
            keyValue = self._kc_value.get(str(kc))
            if keyValue is None:
                keyValue = 1
            stateValue = self._states[self._kc_to_sid[str(kc)]]
            if abs(stateValue) > self.deadZone:
                # Determine which key affected the the sid
                # since the key may set the sid to a certain
                # value such as left and right arrows both affecting
                # a sid called 'x':
                if (keyValue > 0) and (stateValue > 0):
                    pressed.append(True)
                elif (keyValue < 0) and (stateValue < 0):
                    pressed.append(True)
                else:
                    pressed.append(False)
            else:
                pressed.append(False)
        return pressed

    def setKey(self, keycode, on):
        '''
        Sequential arguments:
        keycode -- a hardware keycode such as pygame.key.* constants
        on -- True for pressed, False for released. If the key was
              defined using addKeyAsAxisValue, then a True value
              becomes the value you set at that time.
        '''
        value = 0
        if on:
            value = self._kc_value.get(str(keycode))
            if value is None:
                value = int(on)
        self._states[self._kc_to_sid[str(keycode)]] = value

    def setAxis(self, axis, value):
        '''
        Set the value at the sid that you defined by addAxis
        (However, not set a value unless abs(value) > self.deadZone).

        Sequential arguments:
        axis -- The axis number must already be mapped using
                addAxis so this method knows which sid to affect.
        value -- The raw value is usually -1.0 to 1.0 but it doesn't
                 matter. You can get it later with any "get" method
                 that gets a single value.
        '''
        if abs(value) > self.deadZone:
            try:
                tmp = float(value)
            except ValueError:
                print("The value for axis {} should be a number"
                      " but is {}."
                      "".format(axis, value))
            self._states[self._ax_to_sid[str(axis)]] = value
            if this_show_stats:
                print("joystick axis {} = {}"
                      "".format(axis, value))

    def setButton(self, button, on):
        '''
        Sequential arguments:
        button -- Set a hardware gamepad button number such as from a
                  pygame joystick. It must be already mapped using
                  addButton so that this method knows what virtual
                  actuator sid to affect.
        on -- True for pressed, False for released (converted to 0 or 1
              if True or False, otherwise the integer is preserved but
              other values are not supported)
        '''
        sid = self._btn_to_sid[str(button)]
        self._states[sid] = int(on)

    def setHat(self, hat, values):
        '''
        Set a hat such as a d-pad (any hardware actuator with two axes).

        Sequential arguments:
        hat -- Specify the hat index from the hardware controller. This
               hat must already be mapped using addHat in order for this
               method to know which virtual actuator sid to affect.
        values -- The tuple containing the values of the hat, usually
                  two coordinates, each of which can be -1, 0, or 1.
                  Only a two-long tuple is supported.
        '''
        if len(values) != 2:
            raise ValueError("The hat values argument must be a tuple"
                             " or list that has two elements.")
        sid0, sid1 = self._hat_to_sids[str(hat)]
        self._states[sid0] = values[0]
        self._states[sid1] = values[1]

    def addHat(self, hat, sids):
        '''
        Sequential arguments:
        hat -- Specify the hat index from the hardware controller.
        sids -- Specify a tuple containing two sids to affect since a
                hat (such as a d-pad) has two values, usually
                interpreted as x and y.
        '''
        if len(sids) != 2:
            raise ValueError("The hat sids argument must be a tuple"
                             " or list that has two elements.")
        self._hat_to_sids[str(hat)] = (sids[0], sids[1])
        self._sid_to_hat[sids[0]] = hat
        self._sid_to_hat[sids[1]] = hat
        # ^ Both sids point to the same hat.

    def clearPressed(self):
        for sid in self._states.keys():
            self._states[sid] = 0


# endregion runtime


