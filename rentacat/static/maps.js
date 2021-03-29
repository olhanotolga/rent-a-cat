let map;

function initMap() {
	// fetch URL variables:
	const fetchURLBase = "http://localhost:5000/";
	const username = document.getElementById("username").innerText;
	const updates = document.getElementById("updates").innerText;
	
	const getUpdatesFunction = async () => {

		const URL = `${fetchURLBase}api/${username}/updates/requests`;
		console.log(URL);
		try {

			const response = await fetch(URL, { mode: "cors" });
			// console.log(response.headers.values());
			const updatesAndLocation = await response.json();
			console.log(updatesAndLocation);
			
			const userLocation = updatesAndLocation.location;

			// Might want to center either on user's location or Siegessäule in Tiergarten
			const centerPos = { lat: 52.514444, lng: 13.35 };

			// map options: https://developers.google.com/maps/documentation/javascript/reference#MapOptions

			map = new google.maps.Map(document.getElementById("map"), {
				zoom: 13,
				minZoom: 6,
				maxZoom: 19,
				center: userLocation || centerPos,
				mapTypeControl: false,
				streetViewControl: false
			});

			// get each update and make a marker out of it!
			updatesAndLocation.data.map(update => {
				createMarker(update)
			})
			
			function createMarker(place) {
				console.log(place);
				lat = place.location.lat;
				lng = place.location.lng;
		
				const contentString = "<div>" + 
				"<strong>" + place.title + "</strong><br>" +
				"<span>Latitude: " + lat + "</span><br>" +
				"<span>Longitude: " + lng + "</span>" +
				"</div>";
				
				const infowindow = new google.maps.InfoWindow({
					content: contentString
				});
				
				const marker = new google.maps.Marker({
					map,
					position: place.location,
					title: place.title
				});
			
				marker.addListener("click", () => {
					infowindow.open(map, marker);
				})
			}

		} catch(err) {
			console.log(err);
		}
	}


	getUpdatesFunction();
}
