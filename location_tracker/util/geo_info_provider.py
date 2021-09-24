import os
from typing import Dict, Any

import requests

from location_tracker.models import GeoLocation

GEO_URL_BASE = "http://api.geonames.org/searchJSON"
MAX_RESULT_COUNT_DEFAULT = 3
API_USERNAME_DEFAULT = "dimagi"


def get_env(name, default=None):
    return os.environ.get(name, default)


class GeoInfoProvider(object):

    def __init__(self):
        self.max_rows = get_env("MAX_RESULT_COUNT", MAX_RESULT_COUNT_DEFAULT)
        self.api_user = get_env("API_USERNAME", API_USERNAME_DEFAULT)

    def get_geo_data(self, location_query: str):
        location_obj = GeoLocation.objects.filter(
            location_name__icontains=location_query).first()
        if not location_obj:
            print("fetching geo data")
            params = {'q': location_query,
                      'maxRows': self.max_rows,
                      'username': self.api_user}
            resp = requests.get(url=GEO_URL_BASE, params=params)
            location_obj = GeoInfoProvider.create_geo_object(resp)
        return location_obj

    @staticmethod
    def create_geo_object(resp_obj):
        response_json = resp_obj.json()
        print(response_json)
        geo_names = response_json.get("geonames")
        if not geo_names:
            raise Exception("Location not found")
        geo_data: Dict[str, Any] = geo_names[0]
        print(geo_data)
        country_name = geo_data.get("countryName")
        location_name = geo_data.get("name")
        location_id = geo_data.get("geonameId")
        return GeoLocation.objects.create(location_id=location_id,
                                          location_name=location_name,
                                          country_name=country_name)
