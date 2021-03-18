function initMap() {

	const centerPos = { lat: 52.52, lng: 13.41 };
	// map options: https://developers.google.com/maps/documentation/javascript/reference#MapOptions
	const map = new google.maps.Map(document.getElementById("map"), {
		zoom: 13,
		minZoom: 6,
		maxZoom: 19,
		center: centerPos,
		mapTypeControl: false,
		streetViewControl: false
	});

	// fetch addresses of requests/offers from the API (backend)

	const fetchUpdateAddresses = async (center) => {
		const URL = ``;
		const response = await fetch(URL);
		return response.json();
	}

	const request = {
		query: "Alexanderplatz",
		fields: ["name", "geometry"]
	}

	service = new google.maps.places.PlacesService(map);
	service.findPlaceFromQuery(request, (results, status) => {
		if (status === google.maps.places.PlacesServiceStatus.OK && results) {
			console.dir(results);
			for (let i = 0; i < results.length; i++) {
				createMarker(results[i]);
			}
			map.setCenter(results[0].geometry.location);
		}
	})
	
	// const uluru = new google.maps.Marker({
	// 	position: { lat: -25.344, lng: 131.036 },
	// 	map: map,
	// });
	
	function createMarker(place) {
		lat = place.geometry.location.lat();
		lng = place.geometry.location.lng();
		console.log(lat, lng);

		const contentString = "<div>" + 
		"<strong>" + place.name + "</strong><br>" +
		"<span>Latitude: " + lat + "</span><br>" +
		"<span>Longitude: " + lng + "</span>" +
		"</div>";
		
		const infowindow = new google.maps.InfoWindow({
			content: contentString
		});
		
		if (!place.geometry || !place.geometry.location) return;
		const marker = new google.maps.Marker({
			map,
			position: place.geometry.location,
			title: place.name
		});
	
		marker.addListener("click", () => {
			infowindow.open(map, marker);
		})
	}
}
