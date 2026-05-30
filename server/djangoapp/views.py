from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.http import JsonResponse

import json
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt

from .models import CarMake, CarModel
from .populate import initiate
from .restapis import get_request, post_review, analyze_review_sentiments

# Get an instance of a logger
logger = logging.getLogger(__name__)


@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    username = data["userName"]
    password = data["password"]
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)


def logout_request(request):
    logout(request)
    data = {"userName": ""}
    return JsonResponse(data)


@csrf_exempt
def registration(request):
    data = json.loads(request.body)
    username = data["userName"]
    password = data["password"]
    first_name = data["firstName"]
    last_name = data["lastName"]
    email = data["email"]
    username_exist = False

    try:
        User.objects.get(username=username)
        username_exist = True
    except User.DoesNotExist:
        logger.debug("{} is new user".format(username))

    if not username_exist:
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email,
        )
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
        return JsonResponse(data)
    else:
        data = {"userName": username, "error": "Already Registered"}
        return JsonResponse(data)


def get_cars(request):
    count = CarMake.objects.filter().count()
    if count == 0:
        initiate()
    car_models = CarModel.objects.select_related("car_make")
    cars = []
    for car_model in car_models:
        cars.append(
            {"CarModel": car_model.name, "CarMake": car_model.car_make.name}
        )
    return JsonResponse({"CarModels": cars})


# Update the get_dealerships view to render the list of dealerships
def get_dealerships(request, state="All"):
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/" + state
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


# Create a get_dealer_reviews view to render the reviews of a dealer
def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews_list = get_request(endpoint)

        if reviews_list is not None:
            for review_detail in reviews_list:
                response = analyze_review_sentiments(review_detail["review"])
                review_detail["sentiment"] = response["sentiment"]

            return JsonResponse({"status": 200, "reviews": reviews_list})
        return JsonResponse({"status": 200, "reviews": []})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


# Create a get_dealer_details view to render the dealer details
def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchDealer/{dealer_id}"
        dealer_detail = get_request(endpoint)

        # Flatten array list containers if MongoDB/Express sends it out wrapped
        if isinstance(dealer_detail, list) and len(dealer_detail) > 0:
            dealer_detail = dealer_detail[0]

        return JsonResponse({"status": 200, "dealer": dealer_detail})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})



def add_review(request):
    if not request.user.is_anonymous:
        data = json.loads(request.body)
        try:
            # Capture the returned review from your helper function
            review_data = post_review(data)

            # Return the review data along with a success status
            return JsonResponse(
                {
                    "status": 200,
                    "message": "Review posted successfully",
                    "review": review_data,  # <-- Added this line
                }
            )
        except Exception:
            # It's good practice to log or inspect the actual error if needed
            return JsonResponse(
                {"status": 400, "message": "Error in posting review"}
            )
    else:
        return JsonResponse({"status": 403, "message": "Unauthorized"})
