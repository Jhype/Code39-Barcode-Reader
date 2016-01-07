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

    print barcode
    print barcode.shorthand

    barcode.print_details()
