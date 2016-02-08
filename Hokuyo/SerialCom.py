# -*- coding: utf8 -*-
__author__ = 'adrie_000'

from math import pi
from time import sleep
import glob
import numpy
from serial import *


class GeneralSerialCom:
    def __init__(self, port=None, specific_test_request=None, specific_test_answer=None):
        self.port = port
        if port is None:
            possible_ports = find_ports()
            valid_port = test_port(possible_ports, specific_test_request, specific_test_answer)
            if valid_port is None:
                quit('Error : no serial port openable for request ' + specific_test_request
                     + ' and answer ' + specific_test_answer)
            self.port = valid_port
        self.com = Serial(self.port)

    def write(self, message):
        self.com.write(message)
        self.com.flush()

    def read(self):
        return self.com.read()

    def close(self):
        self.com.close()

def find_ports():
    """ Lists serial ports
    :raises EnvironmentError:
        On unsupported or unknown platforms
    :returns:
        A list of available serial ports
    """

    if sys.platform.startswith('win'):
        ports = ['COM' + str(i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this is to exclude your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    # Try opening ports to find used ones.
    result = []
    for portID in ports:
        try:
            s = Serial(portID)
            s.close()
            result.append(portID)
        except (OSError, SerialException):
            pass
        
    return result

def test_port(possible_ports, specific_test_request, specific_test_answer):
    # TODO : ouvrir chaque connexion série possible, lui envoyer specific_test_request, verifier si elle renvoie specific_test_answer
    return 0

class HokuyoCom(GeneralSerialCom):

    undesirables_limits=[40, 4000]

    def __init__(self, port=None, specific_test_request=None, specific_test_answer=None):
        GeneralSerialCom.__init__(self, port, specific_test_request, specific_test_answer)


    def get_fresh_data(self):
        """ Return new data from the Hokuyo
        :return: [range, angle]
            range = [int, int, int, ...]
            angle = [double, double, double, ...]
        """

        start = 44
        end = 725
        # Returns [arraylist of millimeters,arraylist of corresponding rads]
        self.write('M')
        self.write('S')

        s = [chr(0x30+start/1000), chr(0x30+((start/100) % 10)), chr(0x30+((start/10) % 10)), chr(0x30+ (start % 10))]
        e = [chr(0x30+(end/1000)), chr(0x30+((end/100) % 10)), chr(0x30+((end/10) % 10)), chr(0x30 + (end % 10) )]
       
        cluster = 1
        cc = [chr(0x30 + ((cluster / 10) % 10)), chr(0x30 + (cluster % 10))]
        si = chr(0x30)
        sn = [chr(0x30), chr(0x31)]
        self.write(''.join(b for b in s))
        self.write(''.join(b for b in e))
        self.write(''.join(b for b in cc))
        self.write(''.join(b for b in si))
        self.write(''.join(b for b in sn))
        self.write(''.join(b for b in LF))

        sleep(0.1) # 0.25
        ret = []
        mes_count = 0
        count = 0
        possible_end = False

        while self.com.inWaiting() > 0:
            c1 = self.com.read()                         # Read first char
            count += 1
            if not possible_end or c1 != LF:
                c2 = self.com.read()                     # Read second char
                count += 1
                # Skip the echo send by the Hokuyo
                if c1 == 'M' and c2 == 'S':
                    for k in range(47):
                        self.com.read()
                # Get data from respond
                elif c1 != '?' and c2 != LF:
                    mes_count += 1
                    data = ((ord(c1) - 0x30) << 6) | (ord(c2) - 0x30)
                    ret.append(data)
                # Detect end of message
                else:
                    count = 0
                    possible_end = True

            else:
                possible_end = False

        n = len(ret)
        # Create the Angle tab
        doub = [-k*4*pi/3/n + 2*pi/3 for k in range(n)]
        return [ret, doub]

    def clean_data(self, ret, doub):
        """ Supprime les valeurs abérentes
        :param ret: [int, int, int, ...]
        :param doub: [double, double, double, ...]
        :return: [range, angle], range = [int, int, int, ...], angle = [double, double, double, ...]
        """
        range_cleaned = []
        angle_cleaned = []
        for k in range(len(ret)):
            if not (ret[k] < HokuyoCom.undesirables_limits[0] or ret[k]>HokuyoCom.undesirables_limits[1]):
                range_cleaned.append(ret[k])
                angle_cleaned.append(doub[k])
        return [angle_cleaned, range_cleaned]