##The range of zoom levels we are normally looking for
from math import sin, pi, log, tan

DEFAULT_ZOOM_LEVELS=range(9,22)

class MercatorProjection:
    def __init__(self):
        self.west=-180
        self.east=180
        self.north=90
        self.south=-90
        self.pixels=256
        

    def project(self, lat, lon, x, y, zoom):
        pixX=(180+lon)*(float(2**zoom)/360)*256
        if lat>90:
            lat-=180
        if lat<-90:
            lat+=180
        lat=pi*lat/180
        r=0.5*log((1+sin(lat))/(1-sin(lat)))
        pixY=((1-r/pi)/2)*(2**zoom*256)
        pixX-=256*x
        pixY-=256*y
        return (pixX, pixY)
        

    def findTile(self, lat, lon, zoom):
        if zoom==0:
            return (0,0)
        else:
            x=int(float(180+lon)/(360.0/2**zoom))
            if lat>90:
                lat-=180
            if lat<-90:
                lat+=180
            lat=pi*lat/180
            r=0.5*log((1+sin(lat))/(1-sin(lat)))
            y=int(((1-r/pi)/2)*(2**zoom))
        return (x,y)

    def getZoomTileSet(self, lat, lon, zoomLevels=DEFAULT_ZOOM_LEVELS):
        tileHash={}
        for each in zoomLevels:
            x,y=self.findTile(lat, lon, each)
            tileHash[each]=(x,y)
        return tileHash

