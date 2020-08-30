#!/usr/bin/env python3

# Author: Trev32198
# 1/2/2017
# Implementation of a webm resolution finder.
# GPL licensed

def getWebMRes(fname):
    """Gets the resolution of a given webm file with the filename fname.\
    Will return (-1,-1) if an error occurs in reading the file."""
    with open(fname,'rb') as filehandle: # Open file in such a way that it will be closed automatically
        filehandle.seek(278) # Discard first chunk of data
        data = bytearray(filehandle.read(512)) # Read 512 bytes of data
    w, h = -1, -1 # Set both w and h to -1 for error handling by caller
    for i in range(len(data)): # Loop over webm data
        if (i+7 < len(data)): # Prevent index errors
            if data[i] == 0xb0: # Start of width data
                if data[i+1] == 0x82: # Width is 2 bytes
                    if data[i+4] == 0xba: # Start of height data
                        if data[i+5] == 0x82: # Height is 2 bytes
                            w = (data[i+2]*256)+data[i+3] # Read 2 bytes for width data
                            h = (data[i+6]*256)+data[i+7] # Read 2 bytes for height data
                        elif data[i+5] == 0x81: # Height is 1 byte
                            w = (data[i+2]*256)+data[i+3] # Read 2 bytes for width data
                            h = data[i+6] # Read 1 byte for height data
                elif data[i+1] == 0x81: # Width is 1 byte
                    if data[i+3] == 0xba: # Start of height data
                        if data[i+4] == 0x82: # Height is 2 bytes
                            w = data[i+2] # Read 1 byte for width data
                            h = (data[i+5]*256)+data[i+6] # Read 2 bytes for height data
                        elif data[i+4] == 0x81: # Height is 1 byte
                            w = data[i+2] # Read 1 byte for width data
                            h = data[i+5] # Read 1 byte for height data
            if w != -1 and h != -1: # Values found, break
                break
        else: # The loop reaches the end of the byte array without finding resolution data, break
            break
    return [w,h] # Return the values of w and h

def main():
    """Obtains the resolutions of the webm files that are passed as arguments to the script."""
    from sys import argv # Required for processing arguments
    if len(argv) < 2: # Invalid number of arguments
        print("USAGE: python webm_resolution.py [webm filename 1] [webm filename 2] [webm filename 3] ...") # Print usage data
    else: # There is at least one webm file in the argument list
        for i in range(1,len(argv)): # For each webm file name in the list, find the resolution
            try: # Attempt to get the resolution of a single webm file
                w,h = getWebMRes(argv[i]) # Call function to get resolution and store result
                if w == -1 or h == -1: # If an error occurs in the retrieval of the resolution
                    print('(',i,'/',len(argv)-1,') -> ',argv[i],' - Error retrieving resolution...') # Print that there was an error
                else: # If there is no error
                    print('(',i,'/',len(argv)-1,') -> ',argv[i],' - ',w,'x',h) # Print the resolution of the webm
            except IOError: # If there is an error in opening / reading the file
                print('(',i,'/',len(argv)-1,') -> ',argv[i],' - I/O Error...') # Inform the user of the error

if __name__ == "__main__": # If program is not being used as a module, call main
    main()
