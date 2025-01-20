from django.http import HttpResponse, HttpRequest, JsonResponse, Http404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomLoginForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.views.generic import View
from django.middleware.csrf import get_token
from datetime import date
from .models import CustomUser, Hobby, FriendRequest
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.paginator import Paginator
import json
import requests
import os

def register(request):
    # If the request method is POST, process the submitted form data
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        
        # Check if the form is valid
        if form.is_valid():
            # Save the user to the database
            user = form.save()

            # Save hobbies after the user is created
            hobbies = form.cleaned_data.get('hobbies')
            user.hobbies.set(hobbies)  # Manually set the hobbies (many-to-many field)

            # Display a success message after account creation
            messages.success(request, 'Your account has been created successfully. Please log in.')
            
            # Redirect to the login page
            return redirect('accounts/login/?next=/')  
    else:
        # If the request method is GET, create an empty form
        form = CustomUserCreationForm()

    # Render the registration template with the form
    return render(request, './registration/signup.html', {'form': form})

def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})


def logout_view(request):
    """
    Logs out the user and redirects to the homepage or login page.
    """
    logout(request)  # Logs out the user
    return redirect('accounts/login/?next=/') # Redirect to login page after logout


@login_required
def current_user(request):
    user = request.user
    user_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'date_of_birth': user.date_of_birth.isoformat() if user.date_of_birth else None,
        'hobbies': list(user.hobbies.values("id", "name")),  # Assuming hobbies is a Many-to-Many field
    }
    return JsonResponse(user_data)


@login_required
def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index.html', {})

@login_required
def top_users(request):
    user = request.user  # Current logged-in user
    user_hobbies = user.hobbies.all()
    user_similarity = []
    data = json.loads(request.body)

    min_age = int(data.get("min_age"))
    max_age = int(data.get("max_age"))
    today = date.today()
    other_user_age = 0

    for other_user in CustomUser.objects.all():
            if other_user.date_of_birth is not None and other_user!=user:
                other_user_age = today.year - other_user.date_of_birth.year - ((today.month, today.day) < (other_user.date_of_birth.month, other_user.date_of_birth.day))

                if min_age <= other_user_age and other_user_age <= max_age:
                    common_hobbies = user_hobbies.intersection(other_user.hobbies.all())
                    common_hobby_count = common_hobbies.count()
                    user_similarity.append({
                        'id': other_user.id,
                        'username': other_user.username,
                        'common_hobby_count': common_hobby_count
                    })

    user_similarity.sort(key=lambda x: x['common_hobby_count'], reverse=True)
    page_number = data.get("page",1)

    paginator = Paginator(user_similarity, 10)  
    page_obj = paginator.get_page(page_number)
    
    response_data = {
        "users": list(page_obj.object_list),
        "total_pages": paginator.num_pages,
    }

    return JsonResponse(response_data, safe=False)
@login_required
def update_hobbies(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse the JSON request body
            print("Received data:", data)

            hobbies = data.get("hobbies")
            if hobbies is None:
                return JsonResponse({"error": "Hobbies field is required."}, status=400)

            user = request.user
            if not user.is_authenticated:
                return JsonResponse({"error": "Authentication required."}, status=401)

            # Clear current hobbies and add new ones
            user.hobbies.clear()

            for hobby_data in hobbies:
                hobby_name = hobby_data.get("name")
                if hobby_name:
                    hobby, created = Hobby.objects.get_or_create(name=hobby_name)  # Create or get hobby from DB
                    user.hobbies.add(hobby)  # Add hobby to user

            # Check and delete hobbies that are no longer used by any user
            all_hobbies = Hobby.objects.all()
            for hobby in all_hobbies:
                if not hobby.users.exists():  # If no users are associated with this hobby
                    hobby.delete()  # Delete the hobby

            return JsonResponse({"message": "Hobbies updated successfully."}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON."}, status=400)

        except Exception as e:
            print("Error:", e)
            return JsonResponse({"error": "An error occurred while updating hobbies."}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)
@login_required
def add_single_hobby(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse the JSON request body
            hobby_id = data.get("hobby_id")  # Expecting a single hobby ID

            if hobby_id is None:
                return JsonResponse({"error": "Hobby ID is required."}, status=400)

            user = request.user
            if not user.is_authenticated:
                return JsonResponse({"error": "Authentication required."}, status=401)

            # Add the hobby to the user's hobbies
            try:
                hobby = Hobby.objects.get(id=hobby_id)
                user.hobbies.add(hobby)  # Add hobby to user
            except Hobby.DoesNotExist:
                return JsonResponse({"error": "Hobby not found."}, status=404)

            return JsonResponse({"message": "Hobby added successfully."}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON."}, status=400)

        except Exception as e:
            print("Error:", e)
            return JsonResponse({"error": "An error occurred while adding the hobby."}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)

@login_required
def update_profile(request):
    if request.method == "POST":
        # Assuming you are sending JSON data
        data = json.loads(request.body)
        user = request.user  # Get the logged-in user
        
        # Update user data
        user.first_name = data.get("first_name", user.first_name)
        user.last_name = data.get("last_name", user.last_name)
        user.email = data.get("email", user.email)
        user.date_of_birth = data.get("date_of_birth", user.date_of_birth)
        user.save()  # Save the updated user

        return JsonResponse({"message": "Profile updated successfully"})
    return JsonResponse({"message": "Invalid request"}, status=400)

@login_required
def change_password(request):
    if request.method == 'POST':
        # Get the current and new passwords from the request body
        try:
            data = json.loads(request.body)
            current_password = data.get('current_password')
            new_password = data.get('new_password')

            if not current_password or not new_password:
                return JsonResponse({'message': 'Missing required fields'}, status=400)
            
            # Authenticate the user
            user = request.user
            if not user.check_password(current_password):
                return JsonResponse({'message': 'Current password is incorrect'}, status=400)
            
            # Update the password
            user.set_password(new_password)
            user.save()

            # Re-authenticate the user
            update_session_auth_hash(request, user)
            
            return JsonResponse({'message': 'Password changed successfully'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON'}, status=400)
        
@login_required
def send_friend_request(request):
    if request.method == "POST":
        data = json.loads(request.body)
        to_user_id = data.get("to_user_id")
        try:
            to_user = CustomUser.objects.get(id=to_user_id)
            if FriendRequest.objects.filter(from_user=request.user, to_user=to_user).exists():
                return JsonResponse({"message": "Friend request already sent."}, status=400)
            FriendRequest.objects.create(from_user=request.user, to_user=to_user)
            return JsonResponse({"message": "Friend request sent."}, status=200)
        except CustomUser.DoesNotExist:
            return JsonResponse({"message": "User does not exist."}, status=404)
    return JsonResponse({"message": "Invalid request method."}, status=405)

@login_required
def handle_friend_request(request):
    if request.method == "POST":
        data = json.loads(request.body)
        request_id = data.get("request_id")
        action = data.get("action")  # "accept" or "reject"
        try:
            friend_request = FriendRequest.objects.get(id=request_id, to_user=request.user)
            if action == "accept":
                request.user.friends.add(friend_request.from_user)  # Assuming a friends ManyToManyField
                friend_request.from_user.friends.add(request.user)
                friend_request.delete()
                return JsonResponse({"message": "Friend request accepted."}, status=200)
            elif action == "reject":
                friend_request.delete()
                return JsonResponse({"message": "Friend request rejected."}, status=200)
            else:
                return JsonResponse({"message": "Invalid action."}, status=400)
        except FriendRequest.DoesNotExist:
            return JsonResponse({"message": "Friend request does not exist."}, status=404)
    return JsonResponse({"message": "Invalid request method."}, status=405)

@login_required
def get_friend_requests(request):
    if request.method == "GET":
        friend_requests = FriendRequest.objects.filter(to_user=request.user, status="pending")
        requests_data = [
            {
                "id": fr.id,
                "from_user": {
                    "id": fr.from_user.id,
                    "username": fr.from_user.username,
                },
            }
            for fr in friend_requests
        ]
        return JsonResponse(requests_data, safe=False)
    return JsonResponse({"error": "Invalid request method"}, status=400)

@login_required
def send_friend_request(request):
    if request.method == "POST":
        data = json.loads(request.body)
        to_user_id = data.get("to_user_id")
        if not to_user_id:
            return JsonResponse({"error": "to_user_id is required"}, status=400)
        
        try:
            to_user = CustomUser.objects.get(id=to_user_id)
            if FriendRequest.objects.filter(from_user=request.user, to_user=to_user).exists():
                return JsonResponse({"error": "Friend request already sent"}, status=400)
            
            FriendRequest.objects.create(from_user=request.user, to_user=to_user)
            return JsonResponse({"message": "Friend request sent successfully"}, status=201)
        except CustomUser.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
    return JsonResponse({"error": "Invalid request method"}, status=405)

@login_required
def accept_friend_request(request):
    if request.method == "POST":
        data = json.loads(request.body)
        request_id = data.get("request_id")
        if not request_id:
            return JsonResponse({"error": "request_id is required"}, status=400)
        
        try:
            friend_request = FriendRequest.objects.get(id=request_id, to_user=request.user)
            request.user.friends.add(friend_request.from_user)
            friend_request.from_user.friends.add(request.user)
            friend_request.delete()
            return JsonResponse({"message": "Friend request accepted"}, status=200)
        except FriendRequest.DoesNotExist:
            return JsonResponse({"error": "Friend request not found"}, status=404)
    return JsonResponse({"error": "Invalid request method"}, status=405)

@login_required
def get_friends(request):
    # Get the logged-in user
    user = request.user
    # Fetch the friends related to the user
    friends = user.friends.all()
    # Create a list of dictionaries to return in the response
    friend_list = [{"username": friend.username, "email": friend.email} for friend in friends]
    return JsonResponse(friend_list, safe=False)

@login_required
def get_all_hobbies(request):
    if request.method == "GET":
        hobbies = Hobby.objects.all().values('id','name')  # Adjust to match your model
        return JsonResponse(list(hobbies), safe=False)


class HobbiesSPA(View):
    def get(self, request, *args, **kwargs):
        # Path to the Vue app's index.html
        index_file_path = os.path.join(
            os.path.dirname(__file__), 
            'static/api/spa/index.html'  # Adjust path to the Vue build's index.html
        )
        try:
            with open(index_file_path, 'r', encoding='utf-8') as f:
                return HttpResponse(f.read(), content_type='text/html')
        except FileNotFoundError:
            return HttpResponse(
                "Vue app build not found. Run `npm run build` in the frontend folder.", 
                status=500
            )
    
def main_spa(request):
    # Redirect to the Vue app
    return render(request, 'index.html')
