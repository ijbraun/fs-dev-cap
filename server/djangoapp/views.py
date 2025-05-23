# Uncomment the required imports before adding the code

from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .populate import initiate
from .models import CarMake, CarModel
from .restapis import get_request, analyze_review_sentiments, post_review

# Get an instance of a logger
logger = logging.getLogger(__name__)


@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)


def logout_request(request):
    print("request received")
    logout(request)
    data = {"username": ""}
    return JsonResponse(data)


@csrf_exempt
def registration(request):

    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    username_exist = False

    try:
        # Check if user already exists
        User.objects.get(username=username)
        username_exist = True
    except Exception:
        # If not, simply log this is a new user
        logger.debug("{} is new user".format(username))

    # If it is a new user
    if not username_exist:
        # Create user in auth_user table
        user = User.objects.create_user(username=username,
                                        first_name=first_name,
                                        last_name=last_name,
                                        password=password,
                                        email=email)
        # Login the user and redirect to list page
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
        return JsonResponse(data)
    else:
        data = {"userName": username, "error": "Already Registered"}
        return JsonResponse(data)


def get_cars(request):
    count = CarMake.objects.filter().count()
    print(count)
    if (count == 0):
        initiate()
    car_models = CarModel.objects.select_related('make')
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name,
                     "CarMake": car_model.make.name})
    return JsonResponse({"CarModels": cars})


def get_dealerships(request, state="All"):
    if (state == "All"):
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/" + state
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_reviews(request, dealer_id):
    if (dealer_id):
        dealer_reviews = get_request("/fetchReviews/dealer/" + str(dealer_id))

        for review_detail in dealer_reviews:
            sentimentResponse = analyze_review_sentiments(
                review_detail['review'])
            review_detail['sentiment'] = sentimentResponse['sentiment']

        return JsonResponse({"status": 200, "reviews": dealer_reviews})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


def get_dealer_details(request, dealer_id):
    if (dealer_id):
        dealer = get_request("/fetchDealer/" + str(dealer_id))
        return JsonResponse({"status": 200, "dealer": dealer})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


def add_review(request):
    if (request.user.is_anonymous is False):
        data = json.loads(request.body)
        try:
            response = post_review(data)
            print(response)
            return JsonResponse({"status": 200})
        except Exception:
            return JsonResponse({"status": 401,
                                 "message": "Error in posting review"})
    else:
        return JsonResponse({"status": 403, "message": "Unauthorized"})
