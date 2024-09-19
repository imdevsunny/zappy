from django.contrib import admin
from django.urls import path,include
from webapp import views

# app_name='auth'

urlpatterns = [
    path('', views.HomeView.as_view(),name='home'),
    path('testimonials/', views.TestimonialView.as_view(),name='testimonials'),
    path('new-bot/', views.NewBotView.as_view(),name='new_bot'),
    path('project-settings/<id>/', views.ProjectSettingsView.as_view(),name='project_settings'),
    path('chatbot/<pk>/', views.ChatbotView.as_view(),name='chatbot'),
    path('chatbot-response/', views.ChatbotResponseView.as_view(),name='chatbot_response'),
    # path('job/<pk>/', views.DeleteJobView.as_view(),name='delete_job'),
    # path('job-content/<job_id>/', views.JobContentView.as_view(),name='job_content'),
]