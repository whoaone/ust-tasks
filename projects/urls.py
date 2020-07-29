from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('employee/', views.employeePage, name="employee"),
    path('', views.managementPage, name="management"),

    path('create_project/', views.createProject, name="create_project"),
    path('update_project/<str:pk>', views.updateProject, name="update_project"),
    path('delete_project/<str:pk>', views.deleteProject, name="delete_project"),
    
    path('create_task/', views.createTask, name="create_task"),
    path('update_task/<str:pk>', views.updateTask, name="update_task"),
    path('update_employee_task/<str:pk>', views.updateEmployeeTask, name="update_employee_task"),



    path('daily_log/', views.dailyLog, name="daily_log"),
    path('generate_report/', views.reportPage, name="generate_report"),

    path('all_projects/', views.allProjectsPage, name="all_projects"),
    path('all_tasks/', views.allTasksPage, name="all_tasks"),



    # path('update_task/<str:pk>', views.updateTask, name="update_task"),
    # path('delete_task/<str:pk>', views.deleteTask, name="delete_task"),
    # path('', views.home, name="home"),
    # path('user/', views.userPage, name="user-page"),
    # path('products/', views.products, name='products'),
    # path('customer/<str:pk_test>/', views.customer, name="customer"),
    # path('create_order/<str:pk>/', views.createOrder, name="create_order"),
    # path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    # path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),
]