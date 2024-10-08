from django.urls import path
from . import views
urlpatterns = [

    path('', views.home, name=""),

    path('register',views.register, name="register"),

    path('my-login',views.my_login, name="my-login"),

    path('user-logout',views.user_logout, name="user-logout"),

    ############ CRUD ############

    # read
    path('dashboard',views.dashboard, name="dashboard"),

    # create
    path('create-record', views.create_record, name="create-record"),

    # update
    path('update-record/<int:pk>', views.update_record,name="update-record"),

    #view a single record
    path('record/<int:pk>', views.singular_record, name="record"),

    #delete a record
    path('delete-record/<int:pk>', views.delete_record, name="delete-record"),

    #cats
    path('cats',views.cats, name="cats"),

    #game data page
    path('game-data', views.game_data, name="game-data"),
]