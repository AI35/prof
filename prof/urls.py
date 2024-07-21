from django.urls import path
from .views import base, userslist, profile, signin, signup, Logout, change_password, activate, PassResetComplete, change_username, PassReset, PassResetDone, PassResetConfirm
from .views import settings as SETTINGS
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', base, name='base'),
    path('profile/<str:username>/', profile, name='profile'),
    path('profile/', profile, name='profile'),
    path('login/', signin, name='login'),
    path('logout/', Logout, name='logout'),
    path('signup/', signup, name='signup'),
    path('settings/', SETTINGS, name='settings'),
    path('change_password/', change_password, name='change_password'),
    path('change_username/', change_username, name='change_username'),
    path('activate/<uidb64>/<token>/',
        activate, name='activate'),
    path('password_reset/', PassReset.as_view(), name='password_reset'),               # password_reset/ -> change (password_reset/done/) when change this url
    path('password_reset/done/', PassResetDone.as_view(), name='password_reset_done'), # password_reset/done/ -> when change (password_reset/) make this url same and add (done/)
    path('reset/<uidb64>/<token>/',
        PassResetConfirm.as_view(), name='password_reset_confirm'), # reset/ -> change (reset/done/) when change this url
    path('reset/done/', PassResetComplete.as_view(), name='password_reset_complete'),  # reset/done/ -> when change (reset/) make this url same and add (done/)
    path('userslist/', userslist, name='userslist'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
