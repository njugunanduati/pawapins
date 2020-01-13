from django.urls import path, include

from pins.views import BatchView, AddBatchView, ShowPinsView, GetPinCsvView, move_to_live

app_name = "pins"

urlpatterns = [
    path("batch/", BatchView.as_view(), name="batch"),
    path("addbatch/", AddBatchView.as_view(), name="add_batch"),
    path("showpinbatch/<int:id>/", ShowPinsView.as_view(), name="show_pins"),
    path("movetolive/<int:id>/", move_to_live, name="move_to_live"),
    path("get_csv", GetPinCsvView.as_view(), name="get_csv"),
]
