import argparse
from src.steganographer import *

def set_arguments():

    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("-w", "--write", help="programs run in writting mode", action="store_true")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-f", "--filename", help="use filename as text", action="store_true")
    group.add_argument("-t", "--text", help="specify your own text as an argument", type=str)
    args = parser.parse_args()

    myFile = args.file
    text = ""
    writeMode = False

    if args.write:
        writeMode = True
        if args.filename:
            text = myFile[2:myFile.find('.png')]
        elif args.text:
            text = args.text
        else:
            text = input("Enter your text: ")

    steganographer = Steganographer(myFile, text)
    if writeMode:
        steganographer.write()
    else: 
        steganographer.read()


if __name__ == "__main__":
    set_arguments()
