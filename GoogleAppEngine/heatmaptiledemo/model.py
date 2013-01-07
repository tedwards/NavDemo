from google.appengine.ext import db

##GeoHit
### latlon Lattitude and Longitude of geolocation
### hitCount Number of times the geolocation has been tagged by a user
### zoom Zoom level (used for geo bounding box)
### tileX X coordinate for tile (used for geo bounding box)
### tileY Y coordinate for tile (used for geo bounding box)

class GeoHit (db.Model):
    latlon = db.GeoPtProperty()
    hitCount = db.IntegerProperty()
    zoom = db.IntegerProperty()
    tileX = db.IntegerProperty()
    tileY = db.IntegerProperty()
    
