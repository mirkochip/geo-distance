"""
example of request:
https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins=+++Catania&destinations=Acireale&mode=transit&departure_time=1475485200&key=AIzaSyBJkkOc9OYc7ZGw6hdfm2HZC7O-FF8UrG4

example of response:
{
   u'destination_addresses':[
      u'95024 Acireale,
      Province of Catania,
      Italy'
   ],
   u'origin_addresses':[
      u'Catania,
      Province of Catania,
      Italy'
   ],
   u'rows':[
      {
         u'elements':[
            {
               u'distance':{
                  u'text':u'14.7 km',
                  u'value':14746
               },
               u'duration':{
                  u'text':u'48 mins',
                  u'value':2892
               },
               u'status':u'OK'
            }
         ]
      }
   ],
   u'status':u'OK'
}
"""