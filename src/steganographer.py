import pypng.code.png as png
import subprocess
import sys

class Steganographer:

    def __init__(self, myFile, message):
        '''Constructor method'''

        self.file = myFile
        self.message = message
        self.loadPicture()


    def loadPicture(self):
        '''Load all data from the picture into the object'''

        try:
            f = open(self.file, 'rb')
            r = png.Reader(file = f)
        except IOError:
            sys.exit('Image not accessible')

        self.width, self.height, rows, self.info = r.read()
        self.data = list(rows).copy()
        f.close()

        if (self.width*self.height*self.info["planes"])/8 < len(self.message)*8:
            sys.exit('Message is too long for the selected picture')


    def write(self):
        '''Write the specified message into a copy of the file'''

        messageAsBytes = str.encode(self.message)
        messageCounter = 0
        byteWritted = 0
        newData = []

        for row in range(self.height):
            pixelRow = []
            for col in range(self.width):
                for i in range(self.info["planes"]):
                    if messageCounter < len(messageAsBytes):
                        pixel = bin(self.data[row][col*self.info["planes"]+i])[2:].zfill(8)
                        pixel = pixel[:-1]
                        pixel += (bin(messageAsBytes[writeCounterMessage])[2:].zfill(8))[byteWritted]
                        byteWritted += 1
                        if byteWritted > 7:
                            byteWritted = 0
                            messageCounter += 1
                    pixelRow.append(int(pixel, 2))
            newData.append(tuple(pixelRow))

        newName = self.file[:self.file.find('.png')] + "Copy" + self.file[self.file.find('.png'):]
        f = open(newName, 'wb')
        if 'palette' in self.info.keys():
            w = png.Writer(width = self.width, height = self.height, greyscale = self.info["greyscale"], alpha = self.info["alpha"], bitdepth = self.info["bitdepth"], palette = self.info["palette"])
        else:
            w = png.Writer(width = self.width, height = self.height, greyscale = self.info["greyscale"], alpha = self.info["alpha"], bitdepth = self.info["bitdepth"])
        w.write(f, newData)
        f.close()


    def read(self):
        '''Read the specified file as bytes and '''

        tmpBinary = ""
        message = ""

        for row in range(self.height):
            for col in range(self.width):
                for i in range(self.info["planes"]):
                    pixel = bin(self.data[row][col*self.info["planes"]+i])[2:].zfill(8)
                    tmpBinary += pixel[7]
                    if len(tmpBinary) > 7:
                        message += chr(int(tmpBinary, 2))
                        tmpBinary = ""
        file = open("msg.txt", "w", encoding="utf-8")
        file.write(message)
        file.close()
        strings = subprocess.Popen(['strings', 'msg.txt'])