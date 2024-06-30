from django.urls import path

from . import views

urlpatterns = [
    path("kommunen/<slug:municipality_slug>/", views.kommune_detail, name="kommunen"),
    path("paris-limits/", views.paris_limits, name="paris-limits"),
    path("anleitung/", views.anleitung, name="anleitung"),
    path(
        "spreadsheet/<slug:municipality_slug>/", views.spreadsheet, name="spreadsheet"
    ),
    path(
        "api/emission_data/<slug:municipality_slug>/",
        views.emission_data,
        name="emission_data",
    ),
    path(
        "actions/<slug:municipality_slug>/<int:field_id>/",
        views.field_actions,
        name="field_actions",
    ),
    path("actions/<slug:municipality_slug>/", views.actions, name="actions"),
    path("", views.index, name="index"),
]
