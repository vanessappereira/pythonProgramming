# Import views
# Import required modules
from django.contrib import admin
from django.urls import path, include

# Import views from the current directory
from app import views

# Define URL patterns for this Django application
urlpatterns = [
    # Include the admin site's URLs
    path('admin/', admin.site.urls),

    # Define a URL pattern for the response view
    path('', include('app.urls')),
]