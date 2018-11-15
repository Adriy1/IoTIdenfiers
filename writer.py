# -*- coding: utf-8 -*-

import argparse
from stegano import lsb

def openAndHide(self, filepath, identifier):
    secret = lsb.hide(filepath, identifier)
    secret.save(self.output)

def openAndReveal(self, filepath):
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
#     objWrite = writer(args.file, args.output)
#     objWrite.openAndReveal()
#
# if __name__ == "__main__":
#     main()
