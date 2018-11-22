# -*- coding: utf-8 -*-

import argparse
# Use wave package (native to Python) for reading the received audio file
import wave

def openAndHideAudio(filepath,identifier,output):
    # read wave audio file
    song = wave.open(filepath, mode='rb')
    # Read frames and convert to byte array
    frame_bytes = bytearray(list(song.readframes(song.getnframes())))

    # The "secret" text message
    # string='Peter Parker is the Spiderman!'
    # Append dummy data to fill out rest of the bytes. Receiver shall detect and remove these characters.
    # string = identifier + int((len(frame_bytes)-(len(identifier)*8*8))/8) *'#'
    string = 3*'#' + identifier + 3 *'#'
    # Convert text to bit array
    bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in string])))

    # Replace LSB of each byte of the audio data by one bit from the text bit array
    for i, bit in enumerate(bits):
        frame_bytes[i] = (frame_bytes[i] & 254) | bit
    # Get the modified bytes
    frame_modified = bytes(frame_bytes)

    # Write bytes to a new wave audio file
    with wave.open(output, 'wb') as fd:
        fd.setparams(song.getparams())
        fd.writeframes(frame_modified)
    song.close()
    print("MESSAGE HIDDEN")

def openAndRevealAudio(filepath):
    decoded = ""
    song = wave.open(filepath, mode='rb')
    # Convert audio to byte array
    frame_bytes = bytearray(list(song.readframes(song.getnframes())))

    prefix = "".join(chr(int("".join(map(str,[frame_bytes[j] & 1 for j in range(0,8)])),2)) for i in range(3))
    if(prefix != '###'):
        print("No message hidden")
    else:
        c = 0
        i = 24
        l = len(frame_bytes)
        string = ""
        while(c<3 and i<l-8):
            extracted = [frame_bytes[j] & 1 for j in range(i,i+8)]
            string += "".join(chr(int("".join(map(str,extracted)),2)))
            if (string[-1]=="#"):
                c += 1
            else:
                c = 0
            i += 8
        # Extract the LSB of each byte
        # extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
        # Convert byte array back to string
        # string = "".join(chr(int("".join(map(str,extracted[i:i+8])),2)) for i in range(0,len(extracted),8))
        # Cut off at the filler characters
        decoded = string.split("###")[0]

        # Print the extracted text
        print("Sucessfully decoded: "+decoded)
    song.close()
    return decoded


def main():
    openAndHide("BBB.wav","HELLO##AAA","CCC.wav")
    openAndReveal("CCC.wav")

if __name__ == "__main__":
    main()
