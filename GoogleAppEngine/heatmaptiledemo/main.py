#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#Local Imports
from mercator import MercatorProjection
from hotspot import HotSpot
#Python Native Imports
import os
import logging
import re
#GAE Imports
import model
import webapp2
from google.appengine.ext import db

class MainHandler(webapp2.RequestHandler):
    def get(self):
        p = self.request.path
        p=p.replace('/','',1)
        self.response.write('Hello world!')

class TileHandler(webapp2.RequestHandler):
    def get(self):
        paramCheck=True
        for each in ('x','y','zoom'):
            if not self.request.params.has_key(each):
                logging.debug("%s not found" %each)
                paramCheck=False
                self.error(400)
                self.response.out.write("Missing Parameters")
        if paramCheck:
            try:
                zoom=int(self.request.params.get('zoom'))
                x=int(self.request.params.get('x'))
                y=int(self.request.params.get('y'))
            except StandardError:
                logging.debug("Zoom x or y not ints %s,%s,%s" %(self.request.params.get('zoom'),
                                                                self.request.params.get('x'),
                                                                self.request.params.get('y')))
                self.error(400)
                self.response.out.write("Ivalid Parameters")
            ## Return a null for a blank tile if the zoom is too far out
            if zoom<9:
                self.response.out.write("null")
            else: ## Otherwise find the hits for the given tile and make a picture
                heatmap=HotSpot()
                q= db.GqlQuery("SELECT * from GeoHit WHERE zoom = :1 and tileX = :2 and tileY = :3",
                               zoom,x,y)
                geohits= q.fetch(1000)
                if geohits:
                    for each in geohits:
                        logging.debug(dir(each.latlon))
                        heatmap.addPoint(each.latlon.lat, each.latlon.lon, each.tileX, each.tileY, zoom)

                    self.response.headers['Content-Type'] = "image/png"
                    img=heatmap.getPNG()
                    self.response.out.write(img)
                else:
                    self.response.out.write("null")
                    
class GeoHitHandler(webapp2.RequestHandler):
    def get(self):
        paramCheck=True
        for each in ('lat','lon'):
            if not self.request.params.has_key(each):
                logging.debug("%s not found" %each)
                paramCheck=False
                self.error(400)
                self.response.out.write("Missing Parameters")
        if paramCheck:
            try:
                lat=float(self.request.params.get('lat'))
                lon=float(self.request.params.get('lon'))
            except StandardError:
                logging.debug("Lat/Lon wouldn't convert to float")
                self.error(400)
                self.response.out.write("Invalid Parameters")

            latlon=db.GeoPt(lat,lon)
            q = db.GqlQuery("SELECT * FROM GeoHit WHERE latlon = :1", latlon)
            geohits = q.fetch(25)
            if geohits:
                for gh in geohits:
                    gh.hitCount+=1
                    gh.put()
            else:
                mp=MercatorProjection()
                tiles=mp.getZoomTileSet(lat,lon)
                for zoom in tiles.keys():
                    geohit=model.GeoHit(latlon=latlon, hitCount=1,
                                        zoom=zoom, tileX=tiles[zoom][0],
                                        tileY=tiles[zoom][1])
                    geohit.put()
            self.response.out.write("ok")
        
            
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/tile', TileHandler),
    ('/geohit', GeoHitHandler)
    ], debug=True)
