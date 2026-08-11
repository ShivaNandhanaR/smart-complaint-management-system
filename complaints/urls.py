from django.urls import path

from .views import (
    dashboard,
    create_complaint,
    my_complaints,
    edit_complaint,
)


urlpatterns = [

    path(
        '',
        dashboard,
        name='dashboard'
    ),

    path(
        'complaint/new/',
        create_complaint,
        name='create_complaint'
    ),

    path(
        'complaints/',
        my_complaints,
        name='my_complaints'
    ),

    path(
        'complaint/<int:complaint_id>/edit/',
        edit_complaint,
        name='edit_complaint'
    ),

]