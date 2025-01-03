from django.contrib import admin
from django.urls import path
from Main import views as m_views
from bus import views as b_views
from employee import views as e_views
from django.conf import settings
from django.conf.urls.static import static
from train import views as t_views
from air import views as a_views
from launch import views as l_views
from prof import views as p_views
from payment import views as h_views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', m_views.home, name='Home'),
    path('Main/', m_views.main, name='Main'),
    path('about/', m_views.about_us, name='about_us'),
    path('contact_us/', m_views.contact_us, name='contact_us'),
    path('submit-contact-form/',m_views.submit_contact_form, name='submit_contact_form'),
    path('terms/', m_views.terms, name='terms'),
    path('Sign_Up/', m_views.signup_view, name='Sign_Up'),
    path('Log_In/', m_views.login_view, name='Log_In'),
    path('employee/signup/',e_views. employee_signup_view, name='employee_signup'),
    path('employee/login/', e_views. employee_login_view, name='employee_login'),
    path('employee_dashboard/', e_views.employee_dashboard, name='employee_dashboard'),
    path('bus_routes/', e_views.bus_routes, name='bus_routes'),
    path('create_bus_routes/',e_views.create_bus_routes, name='create_bus_routes'),
    path('update_bus_route/<int:route_id>/', e_views.update_bus_route, name='update_bus_route'),
    path('delete-bus-route/<int:route_id>/', e_views.delete_bus_route, name='delete_bus_route'),
    path('forgot-password/', m_views.forget_password, name='forgot_password'),
    path('reset-password/<int:user_id>/<str:token>/', m_views.reset_password, name='reset_password'),
    path('Bus_Home/', b_views.bus_home, name='Bus_Home'),
    path('book/<int:route_id>/', b_views.book_ticket, name='book_ticket'),
    path('booking_history/', b_views.booking_history, name='booking_history'),
    path('reserve/', b_views.reserve_seat, name='reserve_seat'),
    path('ticket_confirmation/<int:booking_id>/', b_views.ticket_confirmation, name='ticket_confirmation'),
    path('cancel_ticket/<int:booking_id>/',b_views.cancel_ticket, name='cancel_ticket'),
    path('search_bus/', b_views.search_bus, name='search_bus'),
    path('search_train/', t_views.search_train, name='search_train'),
    path('search_air/', a_views.search_air, name='search_air'),
    path('search_launch/', l_views.search_launch, name='search_launch'),
    path('cancel_train_ticket/<int:booking_id>/',t_views.cancel_train_ticket, name='cancel_train_ticket'),
    path('train/payment/<int:booking_id>/',t_views.train_payment_page, name='train_payment_page'),
    path('cancel_air_ticket/<int:booking_id>/',a_views.cancel_air_ticket, name='cancel_air_ticket'),
    path('air/payment/<int:booking_id>/',a_views.air_payment_page, name='air_payment_page'),
    path('cancel_launch_ticket/<int:booking_id>/', l_views.cancel_launch_ticket,name='cancel_launch_ticket'),
    path('launch/payment/<int:booking_id>/', l_views.launch_payment_page, name='launch_payment_page'),
    path('train_home/', t_views.train_home, name='Train_Home'),
    path('air_home/', a_views.air_home, name='Air_Home'),
    path('launch_home/', l_views.launch_home, name='Launch_Home'),
    path('train_routes/', e_views.train_routes, name='train_routes'),
    path('create_train_routes/', e_views.create_train_routes, name='create_train_routes'),
    path('update_train_route/<int:route_id>/', e_views.update_train_route, name='update_train_route'),
    path('delete-train-route/<int:route_id>/', e_views.delete_train_route, name='delete_train_route'),
    path('air_routes/', e_views.air_routes, name='air_routes'),
    path('create_air_routes/', e_views.create_air_routes, name='create_air_routes'),
    path('update_air_route/<int:route_id>/', e_views.update_air_route, name='update_air_route'),
    path('delete-air-route/<int:route_id>/', e_views.delete_air_route, name='delete_air_route'),
    path('launch_routes/', e_views.launch_routes, name='launch_routes'),
    path('create_launch_routes/', e_views.create_launch_routes, name='create_launch_routes'),
    path('update_launch_route/<int:route_id>/', e_views.update_launch_route, name='update_launch_route'),
    path('delete-launch-route/<int:route_id>/', e_views.delete_launch_route, name='delete_launch_route'),
    path('get_seat_info/<int:route_id>/<str:seat_class>/', t_views.get_seat_info, name='get_seat_info'),
    path('book_train_ticket/<int:route_id>/',t_views.book_train_ticket, name='book_train_ticket'),
    path('get_seat_info_air/<int:route_id>/<str:seat_class>/', a_views.get_seat_info_air, name='get_seat_info_air'),
    path('book_air_ticket/<int:route_id>/',a_views.book_air_ticket, name='book_air_ticket'),
    path('get_seat_info_launch/<int:route_id>/<str:seat_class>/', l_views.get_seat_info_launch, name='get_seat_info_launch'),
    path('book_launch_ticket/<int:route_id>/',l_views.book_launch_ticket, name='book_launch_ticket'),
    path('pay/<int:booking_id>/', b_views.payment_page, name='payment'),
    path('pay_card/<int:booking_id>/',b_views.pay_card, name='pay_card'),
    path('pay_bkash/<int:booking_id>/',h_views.pay_bkash, name='pay_bkash'),
    path('bkash_payment_process/<int:booking_id>/',h_views.bkash_payment_process,name='bkash_payment_process'),
    path('pay_rocket/<int:booking_id>/',h_views.pay_rocket, name='pay_rocket'),
    path('rocket_payment_process/<int:booking_id>/',h_views.rocket_payment_process, name='rocket_payment_process'),
    path('process_card_payment/<int:booking_id>/', b_views.process_card_payment, name='process_card_payment'),
    path('profile_management/', p_views.profile_management, name='Profile_Management'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_change.html'), name='password_change'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
    path('user/profile/', p_views.user_profile, name='user_profile'),  # For user_profile.html
    path('profile/edit/', p_views.edit_profile, name='edit_profile'),  # For edit_profile.html
    path('share-experience/',p_views.share_experience, name='share_experience'),
    path('user-forum/', p_views.user_forum, name='user_forum'),
    path('add-reaction/<int:experience_id>/<str:reaction_type>/', p_views.add_reaction, name='add_reaction'),
    path('add-comment/<int:experience_id>/', p_views.add_comment, name='add_comment'),
    path('delete-experience/<int:experience_id>/', p_views.delete_experience, name='delete_experience'),
    path('delete-account/', p_views.delete_account, name='delete_account'),
    path('account-deleted/', p_views.account_deleted_confirmation, name='account_deleted_confirmation'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

