from django.urls import path

from .views import (
    dashboard,
    create_complaint,
    my_complaints,
    edit_complaint,
    register,
    login_view,
    logout_view,
    staff_dashboard,
)


urlpatterns = [

    # Login
    path(
        'login/',
        login_view,
        name='login'
    ),

    # Create account
    path(
        'register/',
        register,
        name='register'
    ),

    # Logout
    path(
        'logout/',
        logout_view,
        name='logout'
    ),

    # User dashboard
    path(
        '',
        dashboard,
        name='dashboard'
    ),

    # Create complaint
    path(
        'complaint/new/',
        create_complaint,
        name='create_complaint'
    ),

    # My complaints
    path(
        'complaints/',
        my_complaints,
        name='my_complaints'
    ),

    # Edit complaint
    path(
        'complaint/<int:complaint_id>/edit/',
        edit_complaint,
        name='edit_complaint'
    ),

    # Staff dashboard
    path(
        'staff/',
        staff_dashboard,
        name='staff_dashboard'
    ),
]