#Code39 barcode decoder

import sys
from PIL import Image
from argparse import ArgumentParser

MIN_THICK_WIDTH = 8
MAX_THIN_WIDTH = 2


def get_options():

    parser = ArgumentParser()

    parser.add_argument('--barcode', dest='barcode', type=str, required=True, help='Load barcode image')

    return parser.parse_args().__dict__

#Get pixel barcodeImage.getpixel(xy) 
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

def binaryToSymbols(binary):

    #take the barcode binary
    print "binary", binary
    #atm just a test print to check it's working.
    #compare it to symbols, find matches
        #for line thingy
    final = ''

    for line in barcodeBinary.split():
        #to grab first character of line line[1] 
        if line[0] == '0':
        # if first character is white
            print "white"
            final += str('W') 
        elif line[0] == '1':
        # if first character is black
            print "black"
            final += str('B')
    
        if len(line) >= MIN_THICK_WIDTH:
            print "large"
            final += str('L')
        elif len(line) <= MAX_THIN_WIDTH: 
            print "small"
            final += str('S')
    print final
    return final

#TO DO: take final string, match each pair to a number. 
#       take the number string and match to the
#       letters/numbers of code39
    
if __name__ == '__main__':

    options = get_options()

    print options

    barcodeImage = Image.open(options['barcode'])

    barcodeBinary = barcodeToBinary(barcodeImage)

    binarySymbols = binaryToSymbols(barcodeBinary)
