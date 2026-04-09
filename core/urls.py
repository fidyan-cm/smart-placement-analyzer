from django.urls import path
from . import views

urlpatterns = [
    path('',                views.predict_placement, name='predict'),
    path('history/',        views.history,           name='history'),
    path('download-report/', views.download_report,  name='download_report'),  # ← add this
]