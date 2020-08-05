from django.urls import path, include

from pins.views import BatchView, AddBatchView, ShowPinsView, move_to_live, get_csv

app_name = "pins"

urlpatterns = [
    path("batch/", BatchView.as_view(), name="batch"),
    path("addbatch/", AddBatchView.as_view(), name="add_batch"),
    path("showpinbatch/<int:id>/", ShowPinsView.as_view(), name="show_pins"),
    path("movetolive/<int:id>/", move_to_live, name="move_to_live"),
    path("get_csv/<int:id>/", get_csv, name="get_csv"),
]
