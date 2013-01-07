##The range of zoom levels we are normally looking for
from math import sin, pi, log, tan

DEFAULT_ZOOM_LEVELS=range(9,22)

class MercatorProjection:
    def __init__(self, zoom=0):
        self.west=-180
        self.east=180
        self.north=90
        self.south=-90
        self.setZoom(zoom)
        self.pixels=256
        
    def setZoom(self,zoom):
        if zoom<0:
            raise ValueError
        else:
            self.zoom=zoom
            ##self.latDiv=85.0511/2**zoom
            self.latDiv=90.0/2**zoom
            self.lonDiv=180.0/2**zoom

    def getTileBoundBox(self, x,y):
        if self.zoom==0:
            ##Base Case is one big box
            return ((self.north,self.west),(self.south, self.east))
        else:
            lon=(x+0.5)*(360.0/2**self.zoom)-180
            #r=1-(2*pi*float(y)/(2**self.zoom))
            #2*r=log((1+sin(lat))/(1-sin(lat)))
            return ((self.north-(((y+y+1)*self.latDiv)-self.latDiv), self.west+(((x+x+1)*self.lonDiv)-self.lonDiv)),
                    (self.north-(((y+y+1)*self.latDiv)+self.latDiv), self.west+(((x+x+1)*self.lonDiv)+self.lonDiv)))

    def project(self, lat, lon, x, y, zoom):
        self.setZoom(zoom)
        #x,y=self.findTile(lat,lon)
        #top,bottom=self.getTileBoundBox(x,y)
        #return self.projectToTile(top, bottom, (lat,lon))
        pixX=(180+lon)*(float(2**zoom)/360)*256
        #print pixX
        #print x*256
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
        
    
    def projectToTile(self, top, bottom, loc, height=256, width=256):
        ##Split the data sets
        latTop, lonTop = top
        latBottom, lonBottom = bottom
        latLoc, lonLoc = loc
        ##Get the size of the tile
        heightBox=latTop-latBottom
        widthBox=lonBottom-lonTop
        ##Determine pixels per degrees
        heightOffset=height/(latTop-latBottom)
        widthOffset=width/(lonBottom-lonTop)
        ##Calculate position
        x=widthOffset*abs(lonLoc-lonTop)
        y=heightOffset*abs(latTop-latLoc)
        return (x,y)


    def findTile(self, lat, lon, z=None):
        if not z:
            z=self.zoom
        else:
            self.setZoom(z)
        x=1
        y=1
        if self.zoom==0:
            return (0,0)
        else:
            ## while self.north-(((y+y+1)*self.latDiv)+self.latDiv) >= lat:
            ##     y+=1
            ## while self.west+(((x+x+1)*self.lonDiv)+self.lonDiv) <= lon:
            ##     x+=1
            #x=int(round(float(180+lon)/(360.0/2**self.zoom)))
            x=int(float(180+lon)/(360.0/2**self.zoom))
            if lat>90:
                lat-=180
            if lat<-90:
                lat+=180
            lat=pi*lat/180
            r=0.5*log((1+sin(lat))/(1-sin(lat)))
            y=int(((1-r/pi)/2)*(2**self.zoom))
            ##y=int(round(float(90-lat)/(180.0/2**self.zoom)))

        return (x,y)

    def getZoomTileSet(self, lat, lon, zoomLevels=DEFAULT_ZOOM_LEVELS):
        tileHash={}
        for each in zoomLevels:
            x,y=self.findTile(lat, lon, each)
            tileHash[each]=(x,y)
        return tileHash

