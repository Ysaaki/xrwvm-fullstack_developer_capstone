from django.urls import path
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # Paths for authentication actions
    path(route='login', view=views.login_user, name='login'),
    path(route='logout', view=views.logout_request, name='logout'),
    path(route='register', view=views.registration, name='register'),
    
    # Path for database inventory vehicles list
    path(route='get_cars', view=views.get_cars, name='getcars'),

    # Paths for Dealership interactions (Fixed to handle both path structures)
    path(route='get_dealers', view=views.get_dealerships, name='get_dealers'),
    path(route='get_dealers/', view=views.get_dealerships, name='get_dealers_slash'), 
    path(route='get_dealers/<str:state>', view=views.get_dealerships, name='get_dealers_by_state'),
    
    # Paths for Dealer detail and Review profiles
    path(route='dealer/<int:dealer_id>', view=views.get_dealer_details, name='dealer_details'),
    path(route='reviews/dealer/<int:dealer_id>', view=views.get_dealer_reviews, name='dealer_reviews'),
    path(route='add_review', view=views.add_review, name='add_review'),
]