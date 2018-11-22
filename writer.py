# -*- coding: utf-8 -*-

import argparse
from stegano import lsb

def openAndHide(filepath, identifier, output):
    secret = lsb.hide(filepath, identifier)
    secret.save(output)

def openAndReveal(filepath):
    clearMessage = lsb.reveal(filepath)
    print(clearMessage)
    return (clearMessage)

# def main():
#     parser = argparse.ArgumentParser()
#     parser.add_argument('file', metavar='f',
#                         help='Path to file to write')
#     parser.add_argument('output', metavar='o',
#                         help='outpute filename')
#     args = parser.parse_args()
#     openAndHide(args.file, "BONJOUR", "./output.png")
#     openAndReveal("./output.mp3")
# if __name__ == "__main__":
#     main()
