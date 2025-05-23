from django.urls import path
from .letter_views import *
from .schedule_todo_views import *
from .vista_views import *
from .chat_views import chat_cat_homepage
from .views import *
from .astra_views import *

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', portal_homepage, name='portal_homepage'),
    path('chat-cat/', chat_cat_homepage, name='chat_cat_homepage'),
    path('vista/', vista_homepage, name='vista_homepage'),
    path('create-album/', create_album, name='create_album'),
    path('todo_operations/', todo_operations, name='todo_operations'),
    path('schedule/', cpnet_homepage, name='cpnet_homepage'),  # 修改原路径
    path('create/', letter_create, name='letter_create'),
    path('success/', letter_success, name='letter_success'),
    path('history/', letter_history, name='letter_history'),
    path('history/<int:pk>/', letter_detail, name='letter_detail'),
    path('clear-history/', clear_letter_history, name='clear_letter_history'),
    path('delete/<int:pk>/', letter_delete, name='letter_delete'),
    path('send/<int:pk>/', letter_send, name='letter_send'),
    path('track/<int:pk>/', track_email, name='track_email'),
    path('songline/<int:pk>/comment/', letter_comment, name='letter_comment'),
    path('schedule_operations/', schedule_operations, name='schedule_operations'),
    path('chat/', ai_chat_view, name='ai_chat'),
    path('concern50/', concern50_game, name='concern50-game'),
    path('switch-role/', switch_role, name='switch_role'),
    path('gamejam/', gamejam_home, name='gamejam_home'),
    path('gamejam/concern50/', concern50_game, name='concern50_game'),
    path('astra', astra_home, name='astra_home'),
    path('astra/divination/', astra_divination, name='divination'),
    path('astra/upload_bg/', upload_bg_image, name='upload_bg'),
    path('astra/generate_case/', generate_case, name='generate_case'),
    path('astra/draw_cards/', draw_cards, name='draw_cards'),
    path('astra/get_divination/', get_divination, name='get_divination'),
    path('api/music-list/', music_list),
]