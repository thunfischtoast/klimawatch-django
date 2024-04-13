from django.db import models


class Kommune(models.Model):
    # Name of the municipality
    name = models.CharField(max_length=200)

    # Slugified version of the name, for use in URLs
    slug = models.SlugField(max_length=200, unique=True)

    # Population of the municipality, optional
    population = models.IntegerField(null=True)

    # Geographic coordinates of the municipality, optional. We use the WGS 84 coordinate system.
    latitude = models.FloatField(
        null=True
    )  # Latitude, in degrees, between -90 and 90. East of the prime meridian is positive.
    longitude = models.FloatField(
        null=True
    )  # Longitude, in degrees, between -180 and 180. North of the equator is positive.
