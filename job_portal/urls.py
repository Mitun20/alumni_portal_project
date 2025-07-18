from django.urls import path
from .views import *

urlpatterns = [
    # Job Post 
    path('create_job_post/', CreateJobPost.as_view(), name='create_job_post'),
    path('retrieve_job_post/', RetrieveJobPost.as_view(), name='retrieve_job_post'),
    path('retrieve_main_job_post/', MainRetrieveJobPost.as_view(), name='retrieve_main_job_post'),
    path('latest_job_post/', LatestJobPost.as_view(), name='latest_job_post'),
    path('my_job_post/', MyJobPost.as_view(), name='my_job_post'),  
    path('update_job_post/<int:post_id>/', UpdateJobPost.as_view(), name='update_job_post'),
    path('deactivate_job_post/<int:post_id>/', InactivateJobPost.as_view(), name='deactivate_job_post'),
    path('detail_job_post/<int:post_id>/', DetailJobPost.as_view(), name='detail_job_post'),

    # Industry Type
    path('create_industry_type/', CreateIndustryType.as_view(), name='create_industry_type'),
    path('retrieve_industry_type/', RetrieveIndustryType.as_view(), name='retrieve_industry_type'),
    path('update_industry_type/<int:industry_type_id>/', UpdateIndustryType.as_view(), name='update_industry_type'),
    
    # Business
    path('create_business_directory/', CreateBusinessDirectory.as_view(), name='create_business_directory'),
    path('retrieve_business_directory/', RetrieveBusinessDirectory.as_view(), name='retrieve_business_directory'),
    path('my_business_directory/', MyBusinessDirectory.as_view(), name='my_business_directory'),
    path('update_business_directory/<int:directory_id>/', UpdateBusinessDirectory.as_view(), name='update_business_directory'),
    path('delete_business_directory/<int:directory_id>/', CreateBusinessDirectory.as_view(), name='create_business_directory'),
    path('detail_business_directory/<int:directory_id>/', DetailBusinessDirectory.as_view(), name='detail_business_directory'),

    # filter
    path('main_filter_job/', JobPostMainFilterView.as_view(), name='main_filter_job'),
    path('filter_job/', JobPostFilterView.as_view(), name='filter_job'),
    path('filter_business_directory/', BusinessDirectoryFilterView.as_view(), name='filter_business_directory'),

    # commets
    path('create_job_comment/<int:job_id>/', CreateJobComment.as_view(), name='create_job_comment'),  # Create a new comment
    path('retrieve_job_comments/<int:job_id>/', RetrieveJobComments.as_view(), name='retrieve_job_comments'),  # Retrieve comments for a specific job
    path('delete_job_comment/<int:comment_id>/', DeleteJobComment.as_view(), name='delete_job_comment'),  # Delete a specific comment

    # Applications
    path('create_application/<int:job_post_id>/', CreateApplication.as_view(), name='create_application'),
    path('my_job_applications/<int:job_post_id>/', MyJobApplication.as_view(), name='my_job_applications'),
    path('detail_view_application/<int:application_id>/', DetailViewApplication.as_view(), name='detail_view_application'),
]
