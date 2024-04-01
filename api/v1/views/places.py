#!/usr/bin/python3
"""
route for handling Place objects and operations
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage, State, City, Place, Amenity


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """
    Search for places based on request body JSON data.
    """
    try:
        search_data = request.get_json()
    except ValueError:
        abort(400, "Not a JSON")

    if not search_data:
        # If the request body is empty, retrieve all places
        places = storage.all(Place).values()
        return jsonify([place.to_dict() for place in places])

    # Extract search parameters
    states_ids = search_data.get('states', [])
    cities_ids = search_data.get('cities', [])
    amenities_ids = search_data.get('amenities', [])

    if not any([states_ids, cities_ids, amenities_ids]):
        # If all lists are empty, retrieve all places
        places = storage.all(Place).values()
        return jsonify([place.to_dict() for place in places])

    # Initialize set to store place ids
    place_ids = set()

    # If states list is not empty, retrieve places for each state
    for state_id in states_ids:
        state = storage.get(State, state_id)
        if state:
            for city in state.cities:
                place_ids.update({place.id for place in city.places})

    # Retrieve places for each city id in cities list
    for city_id in cities_ids:
        city = storage.get(City, city_id)
        if city:
            place_ids.update({place.id for place in city.places})

    # If amenities list is not empty, filter places based on amenities
    if amenities_ids:
        amenities = storage.get(Amenity, amenities_ids)
        place_ids = filter_places_by_amenities(place_ids, amenities)

    # Retrieve places using the filtered place_ids
    places = [storage.get(Place, place_id) for place_id in place_ids if storage.get(Place, place_id)]

    return jsonify([place.to_dict() for place in places])


def filter_places_by_amenities(place_ids, amenities):
    """
    Filter places based on the provided amenities.
    """
    filtered_place_ids = set(place_ids)

    for place_id in place_ids:
        place = storage.get(Place, place_id)
        if place:
            place_amenities = {amenity.id for amenity in place.amenities}
            if not amenities.issubset(place_amenities):
                filtered_place_ids.remove(place_id)

    return filtered_place_ids
