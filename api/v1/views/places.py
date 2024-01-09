#!/usr/bin/python3
"""Places view for API v1"""

from flask import jsonify, abort, request, make_response
from models.place import Place
from models.city import City
from models.user import User
from models.state import State
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places_list = [place.to_dict() for place in city.places]
    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    body = request.get_json()
    if not body:
        abort(400, 'Not a JSON')
    if 'user_id' not in body:
        abort(400, 'Missing user_id')
    user = storage.get(User, body['user_id'])
    if user is None:
        abort(404)
    if 'name' not in body:
        abort(400, 'Missing name')
    body['city_id'] = city_id
    new_place = Place(**body)
    storage.new(new_place)
    storage.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    body = request.get_json()
    if not body:
        abort(400, 'Not a JSON')
    for key, value in body.items():
        if key not in ['id', 'user_id', 'city_id',
                       'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict())


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """Retrieves all Place objects
    depending on the JSON in the body of the request."""
    body = request.get_json()
    if body is None:
        abort(400, 'Not a JSON')

    # If the JSON body is empty or each list of all keys are empty,
    # retrieve all Place objects.
    if not body or all(not body.get(key) for
                       key in ['states', 'cities', 'amenities']):
        places = storage.all(Place).values()
    else:
        places = []

        # If states list is not empty,
        # include all Place objects for each State id listed
        if body.get('states'):
            for state_id in body['states']:
                state = storage.get(State, state_id)
                if state:
                    for city in state.cities:
                        places.extend(city.places)

        # If cities list is not empty,
        # include all Place objects for each City id listed
        if body.get('cities'):
            for city_id in body['cities']:
                city = storage.get(City, city_id)
                if city and city not in [place.city for place in places]:
                    places.extend(city.places)

        # Remove duplicates
        places = list(set(places))

        # If amenities list is not empty, filter Place objects by amenities
        if body.get('amenities'):
            amenities_ids = body['amenities']
            places = [place for place in places if
                      all(amenity.id in amenities_ids
                          for amenity in place.amenities)]

    # Return the results
    places_list = [place.to_dict() for place in places]
    return jsonify(places_list)
