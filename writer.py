# -*- coding: utf-8 -*-

import argparse
from stegano import lsb

class writer:

    def __init__(self, filePath, output):
        self.filePath = filePath
        self.output = output
        print(self.filePath)
        print(self.output)

    def openAndHide(self, identifier):
        secret = lsb.hide(self.filePath, identifier)
        secret.save(self.output)

    def openAndReveal(self):
        clearMessage = lsb.reveal(self.output)
        print(clearMessage)
        return (clearMessage)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', metavar='f',
                        help='Path to file to write')
    parser.add_argument('output', metavar='o',
                        help='outpute filename')
    args = parser.parse_args()
    objWrite = writer(args.file, args.output)
    objWrite.openAndHide('TEST')
    objWrite.openAndReveal()

if __name__ == "__main__":
    main()
