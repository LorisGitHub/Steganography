import argparse
import subprocess
import pypng.code.png as png

myFile = None
writeMode = False
text = None


def set_arguments():

    global myFile
    global writeMode
    global text

    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("-w", "--write", help="programs run in writting mode", action="store_true")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-f", "--filename", help="use filename as text", action="store_true")
    group.add_argument("-t", "--text", help="specify your own text as an argument", type=str)
    args = parser.parse_args()

    myFile = args.file

    if args.write:
        writeMode = True
    if args.filename:
        text = myFile[2:myFile.find('.png')]
    elif args.text:
        print('t mode is on', args.text)
        text = args.text
    else:
        print('default input')
        text = "default"


def loadPicture():
    try:
        f = open(myFile, 'rb')
        r = png.Reader(file = f)
    except IOError:
        sys.exit('Image not accessible')
    width, height, rows, info = r.read()
    numberChanel = info["planes"]
    alpha = info["alpha"]
    bitdepth = info["bitdepth"]
    greyscale = info["greyscale"]
    palette = None
    if 'palette' in info.keys():
        palette = info["palette"]
    data = list(rows).copy()
    f.close()
    return width, height, data, numberChanel, alpha, bitdepth, greyscale, palette
    

def write():
    width, height, data, numberChanel, alpha, bitdepth, greyscale, palette = loadPicture()
    message = text + "\n"
    messageAsBytes = str.encode(message)
    numberMessageAsBytes = len(messageAsBytes)*8

    writeCounterMessage = 0
    byteCounter = 0

    newData = []
    for heightRead in range(height):
        pixelRow = []
        for widthRead in range(width):
            for i in range(numberChanel):
                pixel = bin(data[heightRead][widthRead*numberChanel+i])[2:].zfill(8)
                if(writeCounterMessage < len(messageAsBytes)):
                    pixel = pixel[:-1]
                    pixel += (bin(messageAsBytes[writeCounterMessage])[2:].zfill(8))[byteCounter]
                    byteCounter += 1
                    if(byteCounter > 7):
                        byteCounter = 0
                        writeCounterMessage += 1
                pixelRow.append(int(pixel, 2))
        newData.append(tuple(pixelRow))

    newName = myFile[:myFile.find('.png')] + "Copy" + myFile[myFile.find('.png'):]
    f = open(newName, 'wb')
    if(palette):
        w = png.Writer(width = width, height = height, greyscale = greyscale, alpha = alpha, bitdepth = bitdepth, palette = palette)
    else:
        w = png.Writer(width = width, height = height, greyscale = greyscale, alpha = alpha, bitdepth = bitdepth)
    w.write(f, newData)
    f.close()
    print("Sucessful writing.")


def read():
    width, height, data, numberChanel, alpha, bitdepth, greyscale, palette = loadPicture()
    tmpBinary = ""
    message = ""

    for heightRead in range(height):
        for widthRead in range(width):
            for i in range(numberChanel):
                pixel = bin(data[heightRead][widthRead*numberChanel+i])[2:].zfill(8)
                tmpBinary += pixel[7]
                if(len(tmpBinary) > 7):
                    message += chr(int(tmpBinary, 2))
                    tmpBinary = ""
    file = open("msg.txt", "w", encoding="utf-8")
    file.write(message)
    file.close()
    strings = subprocess.Popen(['strings', 'msg.txt'])


if __name__ == "__main__":
    set_arguments()
    if writeMode:
        write()
    else:
        read()
