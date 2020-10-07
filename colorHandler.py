#Color Replacement Dependencies
#Hex not loading, refer to next commit
from skimage import io, img_as_float
import urllib.request
import io as sysio
import requests

def getAverageColor(url):
    image = io.imread(sysio.BytesIO(urllib.request.urlopen(url).read()))
    image = img_as_float(image)
    r,g,b = 0, 0, 0
    for row in image:
        for pixel in row:
            x,y,z = pixel[:3]
            r += x
            g += y
            b += z
    scale = 255 / (len(image) * len(image[0]))
    color = 65536 * int(r * scale) + 256 * int(g * scale) + int(b * scale)
    return color