import logging

from django.http import HttpResponse
from django.urls import reverse
from django.views.generic.edit import FormView

from location_tracker.forms import LocationAddForm, LocationQueryForm
from location_tracker.models import UserLocation
from location_tracker.util.geo_info_provider import GeoInfoProvider

logger = logging.getLogger(__name__)


class LocationTrackerFormView(FormView):
    form_class = LocationAddForm
    template_name = "location_tracker/location_add.html"
    success_url = "/new/"

    def __init__(self):
        self.location_provider = GeoInfoProvider()
        super(LocationTrackerFormView, self).__init__()

    def form_valid(self, form: LocationAddForm):
        form_data = form.cleaned_data
        logger.info(form_data)
        try:
            email = form_data.get("email")
            location_query = form_data.get("location")
            geo_data = self.location_provider.get_geo_data(location_query)
            logger.info("geo data", geo_data)
            UserLocation.objects.create(email=email, location=geo_data)
            logger.info("user data added/updated")
            return super(LocationTrackerFormView, self).form_valid(form)
        except Exception as e:
            logger.error(e)
            return super(LocationTrackerFormView, self).form_invalid(form)


class LocationQueryView(FormView):
    form_class = LocationQueryForm
    template_name = "location_tracker/location_query.html"
    success_url = "/search/"

    def form_valid(self, form: LocationAddForm):
        form_data = form.cleaned_data
        logger.info(form_data)
        try:
            email = form_data.get("email")
            user = UserLocation.objects.filter(email=email).order_by("-added_time")
            logger.info("user data received")
            if user:
                return HttpResponse(user[0])
            return super(LocationQueryView, self).form_valid(form)
        except Exception as e:
            logger.error(e)
            return super(LocationQueryView, self).form_invalid(form)
