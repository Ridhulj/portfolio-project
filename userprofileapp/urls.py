from django.urls import path
from . import views

urlpatterns = [
        path('', views.homepage, name='homepage'),
        path('register/', views.register, name='register'),
        path('login/', views.loginUser, name='login'),
        path('logout/', views.logout_view, name='logout'),
        path('create-portfolio/',views.create_portfolio, name='create_portfolio'),
        path('view-profile/',views.view_portfolio, name='view_portfolio'),
        path('update-portfolio/<int:portfolio_id>/',views.update_portfolio, name='update_portfolio'),
        path('view-portfolio-details/',views.view_details,name='viewdetails'),
        path('create-details/',views.create_details,name='createdetails'),
        path('edit-details/experience/<int:id>/', views.edit_experience, name='edit_experience'),
        path('edit-details/education/<int:id>/', views.edit_education, name='edit_education'),
        path('edit-details/certification/<int:id>/', views.edit_certification, name='edit_certification'),
        path('projects/create/',views.create_project, name='create_project'),
        path('projects/update/<int:project_id>/',views.update_project, name='update_project'),
        path('projects/',views.project_showcase, name='project_showcase'),
        path('projects/delete/<int:project_id>/',views.delete_project, name='delete_project'),
]


