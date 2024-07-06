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

    # icon of the field
    icon = models.CharField(max_length=200, default="fa-suitcase")

    def __str__(self):
        return f"{self.name} - ID: {self.id}"


class KommuneActionField(models.Model):
    # The municipality this data is about
    kommune = models.ForeignKey(Kommune, on_delete=models.CASCADE)

    # The field
    field = models.ForeignKey(ActionField, on_delete=models.CASCADE)

    # a description
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Action field for {self.kommune.name} ({self.kommune.slug}) - ID: {self.id} - Field: {self.field.name}"


class ActionStatus(models.TextChoices):
    UNBEKANNT = "unbekannt"
    NICHT_BEGONNEN = "nicht begonnen"
    BEGONNEN = "begonnen"
    TEILWEISE_UMGESETZT = "teilweise umgesetzt"
    UMGESETZT = "umgesetzt"
    VERSCHOBEN = "verschoben"


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

    # status of the action
    status = models.CharField(
        max_length=50,
        choices=ActionStatus.choices,
        default=ActionStatus.UNBEKANNT,
    )

    def __str__(self):
        return f"Action for {self.kommune.name} ({self.kommune.slug}) - ID: {self.id} - Title: {self.short_title} - Field: {self.field.name}"


class ActionProgress(models.Model):
    # The action this progress is about
    action = models.ForeignKey(Action, on_delete=models.CASCADE)

    # The progress
    progress = models.TextField()

    # the title
    title = models.CharField(max_length=500, null=True, blank=True)

    # the old status of the action
    old_status = models.CharField(
        max_length=50,
        choices=ActionStatus.choices,
    )

    # the new status of the action
    new_status = models.CharField(
        max_length=50,
        choices=ActionStatus.choices,
    )

    # The date of the progress
    date = models.DateField()

    # the reporting user
    user = models.CharField(max_length=200, null=True, blank=True)

    # the source of the progress
    source = models.CharField(max_length=1000, null=True, blank=True)

    # whether the source is a link
    source_is_link = models.BooleanField(default=False)

    def __str__(self):
        return f"Progress for action {self.action.title} - ID: {self.id} - Date: {self.date}"
