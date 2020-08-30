#!/usr/bin/env python3
#    Copyright (C) 2020  ArisuTheWired
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
# 
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from sys import argv
import shutil, os
from imagesort.imageres import GetResolution

def main():
    #0 script, 1 -offset,2 argv ,3 W res, 4 H res, 5 range's second W, 6 range's second H
    # -m -d [equal | min | max | range] [ 5760 1080 | 1920 1080 | 400 400 | 800 600 1920 1080]

    # '-m' + [ equal | min | max | range ] WIDTH HEIGHT if range WIDTH HEIGHT
    # '-d' + [ equal | min | max | range ] WIDTH HEIGHT if range WIDTH HEIGHT
    # '-f' Folder name for saving / moving files that are not within the parameter
    # '-ar' + 16 9  Will only accept images of a certain aspect ratio
    #
    #TODO
    #Optimizations
    #More filetype support
    #failsafe checking with both argv and file list
    #filetype specific sorting
    #Add help flag

    #Maybe make this bit a dictionary
    files = []
    mode = ""
    #             mode res   ar     o     fs (MB)  mode fs
    condition = ["default", [0,0], "none", [0.0,0.0], "default"]
    offset = 0
    inputres = []
    overarg = 0
    folder = "bad/"

    for i in range(1, len(argv)):
        if overarg != 0:
          overarg -= 1
          continue
        if argv[i] == "-m" or argv[i] == "-d":
            mode = argv[i]
            if i != (len(argv)-1): #optimize before next release
                if str(argv[i+1]) == "range":
                    condition[0] = argv[i+1]
                    inputres.append(int(argv[i+2]))
                    inputres.append(int(argv[i+3]))
                    inputres.append(int(argv[i+4]))
                    inputres.append(int(argv[i+5]))
                    overarg += 5
                else:
                    for x in ["equal", "min", "max"]:
                        if str(argv[i + 1]) == x:
                            condition[0] = argv[i+1]
                            inputres.append(int(argv[i+2]))
                            inputres.append(int(argv[i+3]))
                            overarg += 3
        elif argv[i] == "-f":
            folder = argv[i + 1] + '/'
            overarg += 1
        elif argv[i] == "-ar":
            condition[1][0] = int(argv[i + 1])
            condition[1][1] = int(argv[i + 2])
            overarg += 2
        elif argv[i] == "-o":
            condition[2] = argv[i + 1]
            overarg += 1
        elif argv[i] == "-fs": #optimize before next release
            if str(argv[i+1]) == "range":
                condition[4] = argv[i+1]
                condition[3][0] = float(argv[i+2])
                condition[3][1] = float(argv[i+3])
                overarg += 3
            else:
                for x in ["min", "max"]:
                    if str(argv[i + 1]) == x:
                        condition[4] = argv[i+1]
                        condition[3][0] = float(argv[i+2])
                        overarg += 2
        else:
            files.append(argv[i])
    resolution = []
    for i in range(0, len(files)):
        isbad = 0
        statinfo = os.stat(files[i])
        filesize = (((int(statinfo.st_size) / 1024) / 1024))
        resolution = GetResolution(files[i])
        if mode > "": #optimize before next release
            if resolution[0] < 0:
               continue
            elif condition[0] == "min" and resolution[0] > inputres[0] and resolution[1] > inputres[1]:
                pass
            elif condition[0] == "max" and resolution[0] < inputres[0] and resolution[1] < inputres[1]:
                pass
            elif condition[0] == "range" and resolution[0] > inputres[0] and resolution[1] > inputres[1] and resolution[0] < inputres[2] and resolution[1] < inputres[3]:
                pass
            elif condition[0] == "equal" and resolution[0] == inputres[0] and resolution[1] == inputres[1]:
                pass
            else:
              isbad += 1
        if condition[1][0] != 0:
            if (condition[1][0] / condition[1][1]) == (resolution[0] / resolution[1]):
                pass
            else:
                isbad += 1
        if condition[2] != "none":
            if condition[2] == "widescreen":
                if resolution[0] > resolution[1]:
                    pass
                else:
                    isbad += 1
            elif condition[2] == "portrait":
                if resolution[0] < resolution[1]:
                    pass
                else:
                    isbad += 1
        if condition[4] == "min" and filesize > condition[3][0]:
            pass
        elif condition[4] == "max" and filesize < condition[3][0]:
            pass
        elif condition[4] == "range" and filesize > condition[3][0] and filesize < condition[3][1]:
            pass
        elif condition[4] == "default":
            print(str(filesize) + " MB")
        else:
            isbad += 1
        if isbad != 0:
            print((files[i] + "\nFailed %d tests!\n") % (isbad))
            if not os.path.exists(folder) and mode == "-m":
                os.makedirs(folder)
                shutil.move(files[i], folder)
            elif os.path.exists(folder) and mode == "-m":
                shutil.move(files[i], folder)
            elif mode == "-d":
                os.remove(files[i])
        else:
            print((files[i] + "\nImage " + str(i) + " is %d x %d\n") % (resolution[0],resolution[1]))

    return 0
if __name__ == "__main__":
    main()
