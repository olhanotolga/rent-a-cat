let addressAutocomplete;
let input;

// event handler
const onPlaceChanged = () => {
	let place = addressAutocomplete.getPlace();
	console.log('place', place);
	console.log('geometry', place.geometry);
	console.log('formatted_address', place.formatted_address);
	console.log('name', place.name);

	if (!place.geometry) {
		input.placeholder = "Enter your address!!!";
	} else {
		document.getElementById("lat").value = place.geometry.location.lat();
		document.getElementById("lng").value = place.geometry.location.lng();
		input.value = place.geometry.formatted_address;
	}	
}

function initAutocomplete() {
	console.log('Hello from autocomplete!!!');
	// center at Alexanderplatz, Berlin
	const centerPos = { lat: 52.52, lng: 13.41 };
	// bounds at 100km from center in all directions
	const defaultBounds = {
		north: centerPos.lat + 1,
		south: centerPos.lat - 1,
		east: centerPos.lng + 1,
		west: centerPos.lng - 1,
	};
	// query restrictions
	const options = {
		bounds: defaultBounds,
		componentRestrictions: {country: "de"},
		fields: ["address_components", "geometry", "name"],
		strictBounds: true,
		origin: centerPos
	}

	// the HTML input element
	input = document.getElementById("acAddress");

	addressAutocomplete = new google.maps.places.Autocomplete(input, options);

	// 'on input change' event listener
	addressAutocomplete.addListener("place_changed", onPlaceChanged);
}

