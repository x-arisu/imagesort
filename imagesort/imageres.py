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

from imagesort.WebMResolution import getWebMRes

def GetResolution(imagename):
    try:
        image = open(imagename, "rb")
    except:
        pass
    hplus, wplus, isgif = 0,0,0
    if "jpg" in imagename[-4:] or "jpeg" in imagename[-4:]:
        image.seek(163)  #bytes 164-166
    elif "png" in imagename[-4:]:
        image.seek(18)   #bytes 19-21
        hplus = 2
    elif "gif" in imagename[-4:]:
        image.seek(6)    #bytes 7-10
        isgif = 1
    elif "webm" in imagename[-4:]:
        webmres = getWebMRes(imagename)
        return webmres
    else:
        return [-1,-1]
    decs = image.read(2 + hplus)#PNGs HxW consist of 8 total bytes for their values?
    val1 = (decs[0 + isgif] << 8) + decs[1 - isgif]#GIFS flipped the byte shift
    decs = image.read(2)
    val2 = (decs[0 + isgif] << 8) + decs[1 - isgif]
    image.close()
    """
    JPEG     PNG      GIF
    W=val2   W=val1   W=val1
    H=val1   H=val2   H=val2
    """
    if "jpg" in imagename[-4:] or "jpeg" in imagename[-4:]:
        return [val2, val1]
    elif "png" in imagename[-4:]:
        return [val1, val2]
    elif "gif" in imagename[-4:]:
        return [val1, val2]
