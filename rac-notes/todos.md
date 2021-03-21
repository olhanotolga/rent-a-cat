# TO DO

## Week of 8 March +

- [ ] update / create skeletons for the basic templates
  - [x] landing page
  - [x] registration
  - [x] login
  - [x] dashboard
  - [x] create profile
  - [x] new request
  - [ ] new offer
  - [ ] list view
  - [ ] map view
- [x] logout route
- [x] test login/registration pages
- [ ] see if I got the models right
- [ ] add map view
  - [ ] render Google Map on page
  - [ ] create markers
- [ ] update routes with the necessary info, so that it all aligns with the DB
- [ ] allow offers / requests
  - [ ] format date displayed
  - [ ] enable offers or requests depending on the profile type
- [ ] display offers and requests
  - [ ] in the dashboard
  - [ ] on the map
- [ ] basic styling

## Week of 15 March

- [ ] templates:
  - [ ] profile (private)
  - [ ] profile (public)
  - [ ] update profile
  - [ ] view offer / request
  - [ ] edit offer / request
  - [ ] delete offer / request
- [ ] styling:
  - [ ] style offers and requests on the map
  - [ ] create prototypes

### Display posts as markers in the map

- [x] Get the coordinates via profile creation form
  - [x] Create an Autofill object with Google Maps API
  - [x] Attach the Autofill functionality to the input field
  - [x] Add 2 hidden fields for collecting latitude and longitude
- [ ] Save the location to the DB (as profile property)
  - [x] Create a DB Geometry Column in the Profile model
  - [ ] Convert the coordinates into a DB-digestible format
  - [ ] Add the Geometry data to the Profile instance
  - [ ] Test with SQLiteStudio
- [ ] Reset the map center to the user's profile address/coordinates
  - [ ] Convert Geometry into coordinates
  - [ ] Set the center if user is logged in/has address
- [ ] Show markers for relevant posts on the map
  - [ ] Serve an array of coordinates from backend:
    - [ ] Create a route where posts are queried
    - [ ] Convert Geometry of respective profiles into coordinates
    - [ ] Send the array as a response
  - [ ] Fetch the array of coordinates in the frontend
  - [ ] Loop through coordinates and create markers for each of them

lat = form.lat.data
lng = form.lng.data
profile_location = point_rep(lat, lng)

```python
def point_rep(longitude, latitude):
	point = f'POINT({longitude} {latitude})'
	srid = 4326
	wkt_el = WKTElement(point, srid)
	return wkt_el
```

