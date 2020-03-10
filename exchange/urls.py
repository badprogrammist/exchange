from django.urls import path

from . import views

urlpatterns = [
    path('rates/<str:base_ccy>',
         views.rates,
         name='rates'),
    path('convert/<str:base_ccy>/<str:to_ccy>/<str:amount>',
         views.convert,
         name='convert'),
]
