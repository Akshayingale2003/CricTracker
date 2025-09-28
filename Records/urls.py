from django.urls import path 
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   path('index' , views.index,name="index"),
   path('' , views.dashboard  , name="dashboard"),
   path('register' , views.register , name="register"),
   path('profile',views.profile , name='profile'),
   path('change_password',views.change_password , name='change_password'),
   path('Logout' , views.Logout , name="Logout"),
   path('add_player',views.add_player , name="add_player"),
   path('add_team', views.add_team, name="add_team"),
   path('my_teams',views.my_teams, name = "my_teams"),
   path('my_players',views.my_players,name="my_players"),
   path('edit_team/<int:id>' , views.edit_team , name="edit_team"),
   path('edit_player/<int:id>', views.edit_player , name ="edit_player"),
   path('delete_team/<int:id>', views.delete_team , name="delete_team"),
   path('delete_player/<int:id>', views.delete_player , name = 'delete_player'),
   path('my_dashboard', views.my_dashboard , name='my_dashboard'),
   path('add_performance', views.add_performance , name='add_performance'),
   path('add_batting_performance/<int:id>',views.add_batting_performance , name='add_batting_performance'),
   path('add_balling_performance/<int:id>',views.add_balling_performance , name='add_balling_performance'),
   path('add_fielding_performance/<int:id>',views.add_fielding_performance , name='add_fielding_performance'),
   path('add_wicketkeeping_performance/<int:id>',views.add_wicketkeeping_performance , name='add_wicketkeeping_performance'),
   path('view_performance',views.view_performance, name='view_performance'),
   path('player_batting_performance/<int:id>',views.player_batting_performance,name='player_batting_performance'),
   path('player_balling_performance/<int:id>',views.player_balling_performance,name='player_balling_performance'),
   path('player_fielding_performance/<int:id>',views.player_fielding_performance,name='player_fielding_performance'),
   path('player_wicketkeeping_performance/<int:id>',views.player_wicketkeeping_performance,name='player_wicketkeeping_performance'),
   path('player_stats/<int:id>',views.player_stats,name='player_stats')
 

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


