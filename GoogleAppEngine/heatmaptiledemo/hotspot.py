from PIL import Image, ImageChops, ImageDraw,  ImageFilter
import random
from mercator import MercatorProjection
import StringIO

def test():
    main=Image.new("L",(256,256),255)
    for x in range(256):
        aPoint=(random.randint(0,256),random.randint(0,256))
        im=Image.new("L",(256,256),255)
        d=ImageDraw.Draw(im)
        d.ellipse([aPoint,(aPoint[0]+10,aPoint[1]+10)],fill=160)
        im=im.filter(ImageFilter.SMOOTH_MORE)
        main=ImageChops.multiply(main,im)

    oldData=main.getdata()
    newData=[]
    for pix in oldData:
        print pix
        newData.append(colors[pix])
    result=Image.new("RGBA",(256,256),None)
    result.putalpha(0)
    result.putdata(newData)
    result.save("/Users/tiberius/Documents/tmp/foo.png","PNG")
    

class HotSpot:
    def __init__(self):
        self.colors=[]
        ##Blue to Teal
        self.colors+=[(0,x,255) for x in range(0,256,4)]
        ##Teal to Green
        self.colors+=[(0,255,255-x) for x in range(0,256,4)]
        ##Green to Yellow
        self.colors+=[(x,255,0) for x in range(0,256,4)]
        ##Yellow to Red
        self.colors+=[(255,255-x,0) for x in range(0,256,4)]
        self.colors.reverse()
        self.colors[-1]=(0,0,0,0)

        self.locs=[]
        self.buffer=StringIO.StringIO()
        self.buffer.seek(0)
        
    def addPoint(self, lat, lon, x, y, zoom):
        mp=MercatorProjection()        
        self.locs.append(mp.project(lat,lon,x,y,zoom))
        
    def getPNG(self):
        main=Image.new("L",(256,256),255)
        ##main.putalpha(0)
        for aPoint in self.locs:
            im=Image.new("L",(256,256),255)
            d=ImageDraw.Draw(im)
            d.ellipse([aPoint,(aPoint[0]+10,aPoint[1]+10)],fill=160)
            im=im.filter(ImageFilter.SMOOTH_MORE)
            main=ImageChops.multiply(main,im)

        oldData=main.getdata()
        newData=[]
        for pix in oldData:
            newData.append(self.colors[pix])

        result=Image.new("RGBA",(256,256),None)
        result.putalpha(0)
        result.putdata(newData)
        self.buffer=StringIO.StringIO()
        self.buffer.seek(0)
        result.save(self.buffer,"PNG")
        return self.buffer.getvalue()

