# System imports
import abc
import os
import sys
import time

# Local imports
from mtda.keyboard.controller import KeyboardController

class HidKeyboardController(KeyboardController):

    def __init__(self, mtda):
        self.dev  = None
        self.fd   = None
        self.mtda = mtda

    def configure(self, conf):
        self.mtda.debug(3, "keyboard.hid.configure()")

        """ Configure this keyboard controller from the provided configuration"""
        if 'device' in conf:
           self.dev = conf['device']
           self.mtda.debug(4, "keyboard.hid.configure(): will use %s" % str(self.dev))

    def probe(self):
        self.mtda.debug(3, "keyboard.hid.probe()")

        result = False
        if self.dev is None:
            self.mtda.debug(1, "keyboard.hid.probe(): %s not configured" % str(self.dev))
        elif os.path.exists(self.dev) == False:
            self.mtda.debug(1, "keyboard.hid.probe(): %s not found" % str(self.dev))
        else:
            result = True

        self.mtda.debug(3, "keyboard.hid.probe(): %s" % str(result))
        return result

    def write_report(self, report):
        self.mtda.debug(3, "keyboard.hid.write_report()")

        return self.fd.write(report.encode())
 
    def press(self, key, mod=0x00, repeat=1):
        self.mtda.debug(3, "keyboard.hid.press()")

        NULL_CHAR = chr(0)
        try:
            if self.fd is None:
                self.mtda.debug(4, "keyboard.hid.press(): opening %s" % self.dev)
                self.fd = open(self.dev, mode="r+b", buffering=0)
        except:
            self.mtda.debug(0, "keyboard.hid.press(): failed to open %s" % self.dev)
            return False

        result = True
        while repeat > 0:
            repeat = repeat - 1
            try:
                written = self.write_report(chr(mod) + NULL_CHAR + chr(key) + NULL_CHAR * 5)
                time.sleep(0.1)
                self.write_report(NULL_CHAR * 8)
                if repeat > 0:
                    time.sleep(0.1)
                if written < 8:
                    result = False
                    break
            except:
                self.write_report(NULL_CHAR * 8)
                result = False
                break
        return result

    def enter(self, repeat=1):
        self.mtda.debug(3, "keyboard.hid.enter()")

        return self.press(0x28, 0, repeat)

    def esc(self, repeat=1):
        self.mtda.debug(3, "keyboard.hid.esc()")

        return self.press(0x29, 0, repeat)

    def down(self, repeat=1):
        self.mtda.debug(3, "keyboard.hid.down()")

        return self.press(0x51, 0, repeat)

    def left(self, repeat=1):
        self.mtda.debug(3, "keyboard.hid.left()")

        return self.press(0x50, 0, repeat)

    def right(self, repeat=1):
        self.mtda.debug(3, "keyboard.hid.right()")

        return self.press(0x4f, 0, repeat)

    def up(self, repeat=1):
        self.mtda.debug(3, "keyboard.hid.up()")

        return self.press(0x52, 0, repeat)

    def write(self, str):
        self.mtda.debug(3, "keyboard.hid.write()")

        lower_keys = {
            'a': 0x04, 'b': 0x05, 'c': 0x06, 'd': 0x07, 'e': 0x08, 'f': 0x09,
            'g': 0x0a, 'h': 0x0b, 'i': 0x0c, 'j': 0x0d, 'k': 0x0e, 'l': 0x0f,
            'm': 0x10, 'n': 0x11, 'o': 0x12, 'p': 0x13, 'q': 0x14, 'r': 0x15,
            's': 0x16, 't': 0x17, 'u': 0x18, 'v': 0x19, 'w': 0x1a, 'x': 0x1b,
            'y': 0x1c, 'z': 0x1d, '1': 0x1e, '2': 0x1f, '3': 0x20, '4': 0x21,
            '5': 0x22, '6': 0x23, '7': 0x24, '8': 0x25, '9': 0x26, '0': 0x27,
            '!': 0x1e, '@': 0x1f, '#': 0x20, '$': 0x21, '%': 0x22, '^': 0x23,
            '&': 0x24, '*': 0x25, '(': 0x26, ')': 0x27, ' ': 0x2c, '-': 0x2d,
            '_': 0x2d, '+': 0x2e, '=': 0x2e
        }
        for k in str:
            if k in lower_keys:
                self.press(lower_keys[k])

def instantiate(mtda):
   return HidKeyboardController(mtda)
