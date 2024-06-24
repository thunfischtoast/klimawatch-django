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

    def __str__(self):
        return f"{self.name} ({self.slug}) - ID: {self.id}"


class MarkdownContent(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

    kommune = models.ForeignKey(Kommune, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Markdown content"

    def __str__(self):
        return f"{self.title} - ID: {self.id} - Kommune: {self.kommune.name} ({self.kommune.slug} - ID: {self.kommune.id})"


class EmissionData(models.Model):
    # The municipality this data is about
    kommune = models.OneToOneField(Kommune, on_delete=models.CASCADE)

    # the emission data, in JSON format
    emissions = models.JSONField()

    # last updated timestamp
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Emission data for {self.kommune.name} ({self.kommune.slug}) - ID: {self.id}"


class ActionSource(models.Model):
    # Name of the source
    name = models.CharField(max_length=500)

    # URL of the source
    url = models.URLField(null=True)

    def __str__(self):
        return f"{self.name} - ID: {self.id}"


class ActionField(models.Model):
    # Name of the field
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name} - ID: {self.id}"


class Action(models.Model):
    # The municipality this data is about
    kommune = models.ForeignKey(Kommune, on_delete=models.CASCADE)

    # The source of the action
    source = models.ForeignKey(ActionSource, on_delete=models.CASCADE, null=True)

    # The field of the action
    field = models.ForeignKey(ActionField, on_delete=models.CASCADE, null=True)

    # Title of the action
    title = models.CharField(max_length=500, null=True)

    # Short title of the action
    short_title = models.CharField(max_length=200, null=True) 

    # The action
    action = models.TextField()

    def __str__(self):
        return f"Action for {self.kommune.name} ({self.kommune.slug}) - ID: {self.id} - Source: {self.source.name} - Field: {self.field.name}"
