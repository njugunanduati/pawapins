from django.urls import path, include

from pins.views import BatchView, AddBatchView, ShowPinsView, move_to_live, print_csv

app_name = "pins"

urlpatterns = [
    path("batch/", BatchView.as_view(), name="batch"),
    path("addbatch/", AddBatchView.as_view(), name="add_batch"),
    path("showpinbatch/<int:id>/", ShowPinsView.as_view(), name="show_pins"),
    path("movetolive/<int:id>/", move_to_live, name="move_to_live"),
    path("print_csv", print_csv, name="print_csv"),
]
