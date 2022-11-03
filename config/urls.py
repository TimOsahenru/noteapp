"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from app import views
# from app.views import NoteList
from app.views import LoginUser, RegisterPage
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', NoteList.as_view(), name='notes'),
    path('', views.all_notes, name='notes'),
    path('create/', views.create_note, name='create'),
    path('edit-note/<str:pk>/', views.edit_note, name='edit-note'),
    path('delete-note/<str:pk>/', views.delete_note, name='delete-note'),

    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('signup/', RegisterPage.as_view(), name='signup'),
    path('profile/<str:pk>/', views.creator_profile, name='profile'),
    path('profile-update/', views.creator_profile_update, name='profile-update'),
    path('like/<str:pk>/', views.like_note, name='like'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
