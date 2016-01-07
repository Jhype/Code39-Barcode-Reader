#Code39 barcode decoder

import sys
import json
from PIL import Image
from argparse import ArgumentParser

COLORS = {

    '1' : 'black',
    '0' : 'white',
}

SHORTHAND_MAP = {
    'nw' : ' ',
    'ww' : '-',
    'nb' : '0',
    'wb' : '1',
}

CHAR_TABLE = {
    '100-01' : 'A',
    '010-01' : 'B',
    '110-00' : 'C',
    '001-01' : 'D',
    '101-00' : 'E',
    '011-00' : 'F',
    '000-11' : 'G',
    '100-10' : 'H',
    '010-10' : 'I',
    '001-10' : 'J',
    '1000-1' : 'K',
    '0100-1' : 'L',
    '1100-0' : 'M',
    '0010-1' : 'N',
    '1010-0' : 'O',
    '0110-0' : 'P',
    '0001-1' : 'Q',
    '1001-0' : 'R',
    '0101-0' : 'S',
    '0011-0' : 'T',
    '1-0001' : 'U',
    '0-1001' : 'V',
    '1-1000' : 'W',
    '0-0101' : 'X',
    '1-0100' : 'Y',
    '0-1100' : 'Z',
    '01-100' : '0', 
    '010-01' : '1', 
    '110-00' : '2', 
    '001-01' : '3', 
    '101-00' : '4', 
    '011-00' : '5', 
    '000-11' : '6', 
    '100-10' : '7', 
    '10-010' : '8', 
    '001-10' : '9', 
    '0-0011' : '-', 
    '1-0010' : '.', 
    '0-1010' : ' ',
    '0-0110' : '*',
}

def get_options():

    parser = ArgumentParser()

    parser.add_argument('--barcode', dest='barcode', type=str, required=True, help='Load barcode image')

    return parser.parse_args().__dict__


class Barcode(object):

    def __init__(self, filename):

        barcodeImage = Image.open(filename)
        self.binary = self.barcodeToBinary(barcodeImage)

        self.detailed = [{
                    'color' : COLORS[bar[0]],
                    'binary' : bar[0],
                    'length' : len(bar),
               } for bar in self.binary.split()]

        self._calibrate_reader()

        for bar in self.detailed:

            bar['type'] = 'narrow' if bar['length'] < self.high_min else 'wide'
            bar['shorthand'] = '%s%s' % (bar['type'][0], bar['color'][0])
            bar['symbol'] = SHORTHAND_MAP[bar['shorthand']]

        self.code39 = ''.join([bar['symbol'] for bar in self.detailed])
        self.shorthand = ' '.join([bar['shorthand'] for bar in self.detailed])
        self._decoded = self._decode(self.code39)

    @staticmethod
    def _decode(line):
        line = line.replace(' ', '')
        n = 6
        groups = [line[i:i+n] for i in range(0, len(line), n)]

        decoded = []
        for g in groups:
            decoded.append(CHAR_TABLE[g])

        return ''.join(decoded)

    def decode(self):
        return self._decoded

            

    def print_details(self):
        print json.dumps(self.detailed, indent=4, sort_keys=True)
    
    @staticmethod
    def barcodeToBinary(barcodeImage):
    
        barcodeBinary = []
        lastChar = ''
        width = barcodeImage.size[0]
        for pixel in range(width-1):
    
            r, g, b = barcodeImage.getpixel((pixel,5))
            if (r, g, b) == (255, 255, 255):
                currentChar = '0'
            elif (r, g, b) == (0, 0, 0):
                currentChar = '1'
            else:
                continue
    
            if currentChar != lastChar:
                barcodeBinary.append(' ')
            barcodeBinary.append(currentChar)
            lastChar = currentChar
    
        return ''.join(barcodeBinary)

    def _calibrate_reader(self):

        bar_list = self.detailed
    
        sorted_bar_list = sorted(bar_list, key=lambda k: k['length'])
    
        max_difference = index_of_max_difference = -1
    
        for i in xrange(len(sorted_bar_list)-1):
    
            current_bar = sorted_bar_list[i]
            next_bar = sorted_bar_list[i+1]
            difference = abs(next_bar['length'] - current_bar['length'])
            if difference > max_difference:
    
                index_of_max_difference = i
                max_difference = difference
    
        self.low_range = sorted_bar_list[:index_of_max_difference]
        self.high_range = sorted_bar_list[index_of_max_difference+1:]
    
        self.low_min = self.low_range[0]['length']
        self.high_min = self.high_range[0]['length']

    def __str__(self):
        return self.code39
    
if __name__ == '__main__':

    options = get_options()

    barcode = Barcode(options['barcode'])
    
    print barcode.decode()

