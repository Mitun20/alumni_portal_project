# views.py
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import *
from account.models import *
from .serializers import *
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Count
from account.permissions import *
from rest_framework.pagination import PageNumberPagination
from media_portal.models import PostCategory, Post
class CreateJobPost(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        # Retrieve the industry and role objects
        industry = Industry.objects.get(id=request.data.get('industry'))
        role = Role.objects.get(id=request.data.get('role'))

        # Create the job_post object
        job_post = JobPost(
            posted_by=request.user,
            job_title=request.data.get('job_title'),
            industry=industry,
            experience_level_from=request.data.get('experience_level_from'),
            experience_level_to=request.data.get('experience_level_to'),
            location=request.data.get('location'),
            contact_email=request.data.get('contact_email'),
            contact_link=request.data.get('contact_link'),
            role=role,
            salary_package=request.data.get('salary_package'),
            dead_line=request.data.get('dead_line'),
            job_description=request.data.get('job_description'),
            file=request.FILES.get('file'),
            post_type=request.data.get('post_type')
        )
        
        # Save the job_post object first
        job_post.save()

        # Now, create an activity log
        try:
            activity = ActivityPoints.objects.get(name="Job Post")
        except ActivityPoints.DoesNotExist:
            return Response("Activity not found.")

        # Log the user activity
        UserActivity.objects.create(
            user=request.user,
            activity=activity,
            details=f"{job_post.job_title} Posted"
        )

        # Create the Post object after job_post is saved
        Post.objects.create(
            title=job_post.job_title,
            job_post=job_post,
            published=True,
            posted_by=job_post.posted_by,
            post_category=PostCategory.objects.get(name='Job'),
        )
        
        # Set the skills for the job_post
        job_post.skills.set(request.data.getlist('skills'))

        # Return success response
        return Response({"message": "Job post created successfully"}, status=status.HTTP_201_CREATED)
class RetrieveJobPost(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        job_posts = JobPost.objects.filter(is_active=True).order_by('-id')
        
        # Apply pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Set the number of items per page
        paginated_job_posts = paginator.paginate_queryset(job_posts, request)

        # Manually create a list of job post data
        job_posts_data = []
        for job in paginated_job_posts:
            job_posts_data.append({
                'id': job.id,
                'posted_by': job.posted_by.username,  # Assuming User has a username field
                'job_title': job.job_title,
                'industry': job.industry.title,  # Adjust based on your Industry model
                'experience_level_from': job.experience_level_from,
                'experience_level_to': job.experience_level_to,
                'location': job.location,
                'contact_email': job.contact_email,
                'contact_link': job.contact_link,
                'role': job.role.role,  # Adjust based on your Role model
                'skills': [skill.skill for skill in job.skills.all()],  # List of skill names
                'salary_package': job.salary_package,
                'dead_line': job.dead_line,
                'job_description': job.job_description,
                'file': request.build_absolute_uri(job.file.url) if job.file else None,
                'post_type': job.post_type,
                'posted_on': job.posted_on,
                'is_active': job.is_active,
            })

        return paginator.get_paginated_response(job_posts_data)

class LatestJobPost(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        job_posts = JobPost.objects.filter(is_active=True).order_by('-id')
        
        # Apply pagination
        paginator = PageNumberPagination()
        paginator.page_size = 5  # Set the number of items per page
        paginated_job_posts = paginator.paginate_queryset(job_posts, request)

        # Manually create a list of job post data
        job_posts_data = []
        for job in paginated_job_posts:
            job_posts_data.append({
                'id': job.id,
                'posted_by': job.posted_by.username,  # Assuming User has a username field
                'job_title': job.job_title,
                'industry': job.industry.title,  # Adjust based on your Industry model
                'experience_level_from': job.experience_level_from,
                'experience_level_to': job.experience_level_to,
                'location': job.location,
                'contact_email': job.contact_email,
                'contact_link': job.contact_link,
                'role': job.role.role,  # Adjust based on your Role model
                'skills': [skill.skill for skill in job.skills.all()],  # List of skill names
                'salary_package': job.salary_package,
                'dead_line': job.dead_line,
                'job_description': job.job_description,
                'file': request.build_absolute_uri(job.file.url) if job.file else None,
                'post_type': job.post_type,
                'posted_on': job.posted_on,
                'is_active': job.is_active,
            })

        return paginator.get_paginated_response(job_posts_data)
    
class MainRetrieveJobPost(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        job_posts = JobPost.objects.annotate(application_count=Count('application')).order_by('-id')
        
        # Apply pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Set the number of items per page
        paginated_job_posts = paginator.paginate_queryset(job_posts, request)

        # Manually create a list of job post data
        job_posts_data = []
        for job in paginated_job_posts:
            job_posts_data.append({
                'id': job.id,
                'posted_by': job.posted_by.username,  # Assuming User has a username field
                'job_title': job.job_title,
                'industry': job.industry.title,  # Adjust based on your Industry model
                'experience_level_from': job.experience_level_from,
                'experience_level_to': job.experience_level_to,
                'location': job.location,
                'contact_email': job.contact_email,
                'contact_link': job.contact_link,
                'role': job.role.role,  # Adjust based on your Role model
                'skills': [skill.skill for skill in job.skills.all()],  # List of skill names
                'salary_package': job.salary_package,
                'dead_line': job.dead_line,
                'job_description': job.job_description,
                'file': request.build_absolute_uri(job.file.url) if job.file else None,
                'post_type': job.post_type,
                'posted_on': job.posted_on,
                'is_active': job.is_active,
                'application_count': job.application_count,
            })

        return paginator.get_paginated_response(job_posts_data)
    
class MyJobPost(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            job_posts = JobPost.objects.filter(posted_by=request.user).annotate(application_count=Count('application')).order_by('-id')

            # Apply pagination
            paginator = PageNumberPagination()
            paginator.page_size = 10  # Set the number of items per page
            paginated_job_posts = paginator.paginate_queryset(job_posts, request)

            job_posts_data = []
            for job in paginated_job_posts:
                job_posts_data.append({
                    'id': job.id,
                    'posted_by': job.posted_by.username,  # Assuming User has a username field
                    'job_title': job.job_title,
                    'industry': job.industry.title,  # Adjust based on your Industry model
                    'experience_level_from': job.experience_level_from,
                    'experience_level_to': job.experience_level_to,
                    'location': job.location,
                    'contact_email': job.contact_email,
                    'contact_link': job.contact_link,
                    'role': job.role.role,  # Adjust based on your Role model
                    'skills': [skill.skill for skill in job.skills.all()],  # List of skill names
                    'salary_package': job.salary_package,
                    'dead_line': job.dead_line,
                    'job_description': job.job_description,
                    'file': request.build_absolute_uri(job.file.url) if job.file else None,
                    'post_type': job.post_type,
                    'posted_on': job.posted_on,
                    'is_active': job.is_active,
                    'application_count': job.application_count,
                })

            return paginator.get_paginated_response(job_posts_data)
        except JobPost.DoesNotExist:
            return Response({"message": "Job post not found"}, status=status.HTTP_404_NOT_FOUND)
                        
class UpdateJobPost(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        try:
            job_post = JobPost.objects.get(id=post_id)
            serializer = JobPostSerializer(job_post, context={'request': request})  # Pass the request context
            return Response(serializer.data, status=status.HTTP_200_OK)
        except JobPost.DoesNotExist:
            return Response({"message": "Job post not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, post_id):
        try:
            job_post = JobPost.objects.get(id=post_id)
        except JobPost.DoesNotExist:
            return Response({"message": "Job post not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Assuming you want to check for permissions
        # if job_post.posted_by != request.user:
        #     return Response({"message": "You do not have permission to Edit this comment."}, status=status.HTTP_403_FORBIDDEN)

        serializer = JobPostUpdateSerializer(job_post, data=request.data)
        
        if serializer.is_valid():
            # Handle file upload if it exists
            if 'file' in request.FILES:
                job_post.file = request.FILES['file']
                
            serializer.save()  # This will call the update method in the serializer
            return Response({"message": "Job post updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InactivateJobPost(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, post_id):
        if post_id is None:
            return Response({"message": "Post ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            job_post = JobPost.objects.get(id=post_id)
            job_post.is_active = request.data.get('is_active', False)
            job_post.save()
            return Response({"message": "Job post status updated successfully"}, status=status.HTTP_200_OK)
        except JobPost.DoesNotExist:
            return Response({"message": "Job post not found"}, status=status.HTTP_404_NOT_FOUND)
        
class DetailJobPost(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        try:
            job = JobPost.objects.get(id=post_id)
        
        # Manually create a list of job post data
           
            job_posts_data={
                    'id': job.id,
                    'posted_by': job.posted_by.username,  # Assuming User has a username field
                    'job_title': job.job_title,
                    'industry': job.industry.title,  # Adjust based on your Industry model
                    'experience_level_from': job.experience_level_from,
                    'experience_level_to': job.experience_level_to,
                    'location': job.location,
                    'contact_email': job.contact_email,
                    'contact_link': job.contact_link,
                    'role': job.role.role,  # Adjust based on your Role model
                    'skills': [skill.skill for skill in job.skills.all()],  # List of skill names
                    'salary_package': job.salary_package,
                    'dead_line': job.dead_line,
                    'job_description': job.job_description,
                    'file': request.build_absolute_uri(job.file.url) if job.file else None,
                    'posted_on': job.posted_on,
                    'post_type': job.post_type,
                    'is_active': job.is_active,
                }

            return Response(job_posts_data, status=status.HTTP_200_OK)
        except JobPost.DoesNotExist:
            return Response({"message": "Job post not found"}, status=status.HTTP_404_NOT_FOUND)

# manage Industry type
class CreateIndustryType(APIView):
    permission_classes = [IsAuthenticated, IsAlumniManagerOrAdministrator]

    def post(self, request):
        industry_type = Industry_Type(
            type_name=request.data['type_name'],
            description=request.data.get('description', '')
        )
        industry_type.save()
        return Response({"message": "Industry Type created successfully"}, status=status.HTTP_201_CREATED)

class RetrieveIndustryType(APIView):
    def get(self, request):
        industry_types = Industry_Type.objects.all()

        # Apply pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Set the number of items per page
        paginated_industry_types = paginator.paginate_queryset(industry_types, request)

        data = [
            {
                "id": industry_type.id,
                "type_name": industry_type.type_name,
                "description": industry_type.description
            }
            for industry_type in paginated_industry_types
        ]
        return paginator.get_paginated_response(data)

class UpdateIndustryType(APIView):
    permission_classes = [IsAuthenticated, IsAlumniManagerOrAdministrator]

    def get(self, request, industry_type_id):
        try:
            industry_type = Industry_Type.objects.get(id=industry_type_id)
            data = {
                "type_name": industry_type.type_name,
                "description": industry_type.description
            }
            return Response(data, status=status.HTTP_200_OK)
        except Industry_Type.DoesNotExist:
            return Response({"message": "Industry Type not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, industry_type_id):
        try:
            industry_type = Industry_Type.objects.get(id=industry_type_id)
        except Industry_Type.DoesNotExist:
            return Response({"message": "Industry Type not found"}, status=status.HTTP_404_NOT_FOUND)

        industry_type.type_name = request.data.get("type_name", industry_type.type_name)
        industry_type.description = request.data.get("description", industry_type.description)
        industry_type.save()

        return Response({"message": "Industry Type updated successfully"}, status=status.HTTP_200_OK)
    
# manage Business Directory
class CreateBusinessDirectory(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        business_directory = BusinessDirectory(
            business_name=request.data.get('business_name'),
            description=request.data.get('description'),
            website=request.data.get('website'),
            industry_type_id=request.data.get('industry_type'),
            location=request.data.get('location'),
            contact_email=request.data.get('contact_email'),
            contact_number=request.data.get('contact_number'),
            country_code_id=request.data.get('country_code'),
            are_you_part_of_management=request.data.get('are_you_part_of_management', True),
            logo=request.FILES.get('logo'),
            listed_by=request.user
        )
        try:
            activity = ActivityPoints.objects.get(name="Business Directory")
        except ActivityPoints.DoesNotExist:
            return Response("Activity not found.")
        UserActivity.objects.create(
            user=request.user,
            activity=activity,
            details=f"{business_directory.business_name} Posted"
        )
        business_directory.save()
        return Response({"message": "Business directory entry created successfully"}, status=status.HTTP_201_CREATED)

    def delete(self,request,directory_id):
        business = BusinessDirectory.objects.get(id=directory_id)
        business.delete()
        return Response({"message": "Business directory deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class RetrieveBusinessDirectory(APIView):
    permission_classes = [IsAuthenticated]

    
    def get(self, request):
        try:
            business_directories = BusinessDirectory.objects.all()

            # Apply pagination
            paginator = PageNumberPagination()
            paginator.page_size = 10  # Set the number of items per page
            paginated_business_directories = paginator.paginate_queryset(business_directories, request)

            data = []
            for business in paginated_business_directories:
                data.append({
                    "id": business.id,
                    "business_name": business.business_name,
                    # "description": business.description,
                    "website": business.website,
                    "industry_type": business.industry_type.type_name,  # or business.industry_type.name if you want the name
                    "location": business.location,
                    # "contact_email": business.contact_email,
                    # "contact_number": business.contact_number,
                    # "country_code": business.country_code.id,  # or business.country_code.name if you want the name
                    # "are_you_part_of_management": business.are_you_part_of_management,
                    "logo": request.build_absolute_uri(business.logo.url) if business.logo else None,
                    "listed_on": business.listed_on,
                    # "listed_by": business.listed_by.id,  # or business.listed_by.username if you want the username
                })

            return paginator.get_paginated_response(data)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MyBusinessDirectory(APIView):
    def get(self, request):
        try:
            business_directories = BusinessDirectory.objects.filter(listed_by=request.user).order_by('-id')

            # Apply pagination
            paginator = PageNumberPagination()
            paginator.page_size = 10  # Set the number of items per page
            paginated_business_directories = paginator.paginate_queryset(business_directories, request)

            data = []
            for business in paginated_business_directories:
                data.append({
                    "id": business.id,
                    "business_name": business.business_name,
                    # "description": business.description,
                    "website": business.website,
                    "industry_type": business.industry_type.type_name, 
                    "location": business.location,
                    # "contact_email": business.contact_email,
                    # "contact_number": business.contact_number,
                    # "country_code": business.country_code.country_code,  
                    # "are_you_part_of_management": business.are_you_part_of_management,
                    "logo": request.build_absolute_uri(business.logo.url) if business.logo else None,
                    "listed_on": business.listed_on,
                    # "listed_by": business.listed_by.id,  # or business.listed_by.username if you want the username
                })
            return paginator.get_paginated_response(data)

        except BusinessDirectory.DoesNotExist:
            return Response({"message": "Business directory not found"}, status=status.HTTP_404_NOT_FOUND)
        
class UpdateBusinessDirectory(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, directory_id):
        try:
            business = BusinessDirectory.objects.get(id=directory_id)
            # for business in business_directories:
            data={
                "id": business.id,
                "business_name": business.business_name,
                "description": business.description,
                "website": business.website,
                "industry_type": business.industry_type.type_name,
                "industry_type_detail":{
                    "id": business.industry_type.id,
                    "type_name": business.industry_type.type_name,
                    "description": business.industry_type.description,
                },
                "location": business.location,
                "contact_email": business.contact_email,
                "contact_number": business.contact_number,
                "country_code": business.country_code.country_name,
                "country_detail":{
                    "id": business.country_code.id,
                    "country_name": business.country_code.country_name,
                    "country_code": business.country_code.country_code,
                },
                "are_you_part_of_management": business.are_you_part_of_management,
                "logo": request.build_absolute_uri(business.logo.url) if business.logo else None,
                "listed_on": business.listed_on,
                "listed_by_id": business.listed_by.id if business.listed_by else None,
                "listed_by": f"{business.listed_by.first_name} {business.listed_by.last_name}" if hasattr(business.listed_by, 'first_name') and hasattr(business.listed_by, 'last_name') else business.listed_by.username,
            }
            return Response(data, status=status.HTTP_200_OK)
        
        except BusinessDirectory.DoesNotExist:
            return Response({"message": "Business directory not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, directory_id):
        try:
            business_directory = BusinessDirectory.objects.get(id=directory_id)
        except BusinessDirectory.DoesNotExist:
            return Response({"message": "Business directory not found"}, status=status.HTTP_404_NOT_FOUND)
        if request.data.get('industry_type'):
            try:
                industry_type = Industry_Type.objects.get(id=request.data['industry_type'])
                
            except Industry_Type.DoesNotExist:
                return Response({"message": "Industry type not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if request.data.get('country_code'):
            try:
                country_code = Country.objects.get(id=request.data['country_code'])
            except Country.DoesNotExist:
                return Response({"message": "Country code not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Update fields
        business_directory.business_name = request.data.get('business_name', business_directory.business_name)
        business_directory.description = request.data.get('description', business_directory.description)
        business_directory.website = request.data.get('website', business_directory.website)
        business_directory.industry_type = industry_type if industry_type else business_directory.industry_type
        business_directory.location = request.data.get('location', business_directory.location)
        business_directory.contact_email = request.data.get('contact_email', business_directory.contact_email)
        business_directory.contact_number = request.data.get('contact_number', business_directory.contact_number)
        business_directory.country_code = country_code if country_code else business_directory.country_code
        business_directory.are_you_part_of_management = request.data.get('are_you_part_of_management', business_directory.are_you_part_of_management)

        # Handle logo upload
        if request.FILES.get('logo'):
            business_directory.logo = request.FILES.get('logo')

        business_directory.save()
        return Response({"message": "Business directory entry updated successfully"}, status=status.HTTP_200_OK)
# class UpdateBusinessDirectory(APIView):
#     # permission_classes = [IsAuthenticated]

#     def get(self, request, directory_id):
#         try:
#             business = BusinessDirectory.objects.get(id=directory_id)
#             serializer = BusinessDirectorySerializer(business)
#             data = serializer.data

#             # Convert logo to absolute URI
#             if business.logo:
#                 data['logo'] = request.build_absolute_uri(business.logo.url)

#             return Response(data, status=status.HTTP_200_OK)
        
#         except BusinessDirectory.DoesNotExist:
#             return Response({"message": "Business directory not found"}, status=status.HTTP_404_NOT_FOUND)


#     def post(self, request, directory_id):
#         try:
#             business_directory = BusinessDirectory.objects.get(id=directory_id)
#         except BusinessDirectory.DoesNotExist:
#             return Response({"message": "Business directory not found"}, status=status.HTTP_404_NOT_FOUND)

#         serializer = BusinessDirectorySerializer(business_directory, data=request.data, partial=True)
        
#         if serializer.is_valid():
#             # Handle logo upload separately if included in request.FILES
#             if request.FILES.get('logo'):
#                 serializer.validated_data['logo'] = request.FILES['logo']
            
#             serializer.save()
#             return Response({"message": "Business directory entry updated successfully"}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DetailBusinessDirectory(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, directory_id):
        try:
            business_directory = BusinessDirectory.objects.get(id=directory_id)
            data = {
                "business_name": business_directory.business_name,
                "description": business_directory.description,
                "website": business_directory.website,
                "industry_type": business_directory.industry_type.type_name,  # or business_directory.industry_type.name
                "location": business_directory.location,
                "contact_email": business_directory.contact_email,
                "contact_number": business_directory.contact_number,
                "country_code": business_directory.country_code.country_name,  # or business_directory.country_code.name
                "logo": request.build_absolute_uri(business_directory.logo.url) if business_directory.logo else None,
                "listed_on": business_directory.listed_on,
                "listed_by": business_directory.listed_by.username,  # or business_directory.listed_by.username
            }
            return Response(data, status=status.HTTP_200_OK)
        except BusinessDirectory.DoesNotExist:
            return Response({"message": "Business directory not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# filter job post

class JobPostMainFilterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Extract data from the JSON body
        job_title = request.data.get('job_title', None)
        industry_id = request.data.get('industry', None)  # Assuming you're passing the industry ID
        location = request.data.get('location', None)
        role_id = request.data.get('role', None)  # Assuming you're passing the role ID
        post_type = request.data.get('post_type', None)
        search = request.data.get('search', None)

        # Create a dictionary for the filter arguments
        filters = Q()
        if search:
            filters &= Q(job_title__icontains=search) | Q(location__icontains=search)
        if job_title:
            filters &= Q(job_title__icontains=job_title)
        if industry_id:
            filters &= Q(industry_id=industry_id)
        if location:
            filters &= Q(location__icontains=location)
        if role_id:
            filters &= Q(role_id=role_id)
        if post_type:
            filters &= Q(post_type__icontains=post_type)

        # Apply the filters in a single query
        queryset = JobPost.objects.filter(filters).annotate(application_count=Count('application')).order_by('-id')

        # Apply pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Set the number of items per page
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        # Prepare the response data without serializers
        data = []
        for job in paginated_queryset:
            data.append({
                'id': job.id,
                'posted_by': job.posted_by.username, 
                'job_title': job.job_title,
                'industry': job.industry.title, 
                'location': job.location,
                'role': job.role.role,  # Adjust based on your Role model
                'skills': [skill.skill for skill in job.skills.all()],  # List of skill names
                'salary_package': job.salary_package,
                'dead_line': job.dead_line,
                'job_description': job.job_description,
                'file': request.build_absolute_uri(job.file.url) if job.file else None,
                'post_type': job.post_type,
                'posted_on': job.posted_on,
                'is_active': job.is_active,
                'application_count': job.application_count,
            })

        return paginator.get_paginated_response(data)
    
class JobPostFilterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Extract data from the JSON body
        job_title = request.data.get('job_title', None)
        industry_id = request.data.get('industry', None)  # Assuming you're passing the industry ID
        location = request.data.get('location', None)
        role_id = request.data.get('role', None)  # Assuming you're passing the role ID
        post_type = request.data.get('post_type', None)

        # Create a dictionary for the filter arguments
        filters = Q(is_active=True)
        if job_title:
            filters &= Q(job_title__icontains=job_title)
        if industry_id:
            filters &= Q(industry_id=industry_id)
        if location:
            filters &= Q(location__icontains=location)
        if role_id:
            filters &= Q(role_id=role_id)
        if post_type:
            filters &= Q(post_type__icontains=post_type)

        # Apply the filters in a single query
        queryset = JobPost.objects.filter(filters).annotate(application_count=Count('application')).order_by('-id')

        # Apply pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Set the number of items per page
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        # Prepare the response data without serializers
        data = []
        for job in paginated_queryset:
            data.append({
                'id': job.id,
                'posted_by': job.posted_by.username, 
                'job_title': job.job_title,
                'industry': job.industry.title, 
                'location': job.location,
                'role': job.role.role,  # Adjust based on your Role model
                'skills': [skill.skill for skill in job.skills.all()],  # List of skill names
                'salary_package': job.salary_package,
                'dead_line': job.dead_line,
                'job_description': job.job_description,
                'file': request.build_absolute_uri(job.file.url) if job.file else None,
                'post_type': job.post_type,
                'posted_on': job.posted_on,
                'is_active': job.is_active,
                'application_count': job.application_count,
            })

        return paginator.get_paginated_response(data)

# filter Business directory

class BusinessDirectoryFilterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Extract data from the JSON body
        business_name = request.data.get('business_name', None)
        industry_id = request.data.get('industry', None)  # Assuming you're passing the industry ID
        location = request.data.get('location', None)

        # Create a dictionary for the filter arguments
        filters = Q()
        if business_name:
            filters &= Q(business_name__icontains=business_name)
        if industry_id:
            filters &= Q(industry_type_id=industry_id)
        if location:
            filters &= Q(location__icontains=location)

        # Apply the filters in a single query
        queryset = BusinessDirectory.objects.filter(filters).order_by('-id')

        # Apply pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Set the number of items per page
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        # Prepare the response data
        data = []
        for business in paginated_queryset:
            data.append({
                "id": business.id,
                "business_name": business.business_name,
                # "description": business.description,
                "website": business.website,
                "industry_type": business.industry_type.type_name,  # or business.industry_type.name if you want the name
                "location": business.location,
                # "contact_email": business.contact_email,
                # "contact_number": business.contact_number,
                # "country_code": business.country_code.id,  # or business.country_code.name if you want the name
                # "are_you_part_of_management": business.are_you_part_of_management,
                "logo": request.build_absolute_uri(business.logo.url) if business.logo else None,
                "listed_on": business.listed_on,
                # "listed_by": business.listed_by.id,  # or business.listed_by.username if you want the username
            })

        return paginator.get_paginated_response(data)

# manage comments
class CreateJobComment(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, job_id):
        job = get_object_or_404(JobPost, id=job_id)
        comment_text = request.data.get('comment')
        
        if not comment_text:
            return Response({"error": "Comment text is required."}, status=status.HTTP_400_BAD_REQUEST)

        comment = JobComment(
            job=job,
            comment_by=request.user,
            comment=comment_text
        )
        comment.save()
        return Response({"message": "Comment created successfully"}, status=status.HTTP_201_CREATED)

class RetrieveJobComments(APIView):
    def get(self, request, job_id):
        comments = JobComment.objects.filter(job_id=job_id).order_by('-id')
        data = [
            {
                "comment_id": comment.id,
                "comment_by": comment.comment_by.username,
                "comment": comment.comment,
            }
            for comment in comments
        ]
        return Response(data, status=status.HTTP_200_OK)

class DeleteJobComment(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, comment_id):
        comment = get_object_or_404(JobComment, id=comment_id)

        # Check if the comment was made by the requesting user
        if comment.comment_by != request.user:
            return Response({"message": "You do not have permission to delete this comment."}, status=status.HTTP_403_FORBIDDEN)

        comment.delete()
        return Response({"message": "Comment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

# Applications

class CreateApplication(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request,job_post_id):
        job_post = JobPost.objects.get(id=job_post_id)
        
        application = Application(
            job_post=job_post,
            full_name=request.data.get('full_name'),
            email=request.data.get('email'),
            mobile_number=request.data.get('mobile_number'),
            current_industry_id=request.data.get('current_industry'),
            current_role_id=request.data.get('current_role'),
            total_years_of_experience=request.data.get('total_years_of_experience'),
            notes_to_recruiter=request.data.get('notes_to_recruiter'),
            resume=request.FILES.get('resume')
        )
        try:
            activity = ActivityPoints.objects.get(name="Business Directory")
        except ActivityPoints.DoesNotExist:
            return Response("Activity not found.")
        UserActivity.objects.create(
            user=request.user,
            activity=activity,
            details=f"Applied for {application.job_post.job_title}"
        )
        application.save()
        application.skills.set(request.data.getlist('skills'))  # Assuming skills is a list of IDs

        # Send email to the job post's posted user
        self.send_email_notification(job_post.posted_by.email, application)

        return Response({"message": "Application submitted successfully"}, status=status.HTTP_201_CREATED)

    def send_email_notification(self, recipient_email, application):
        subject = f"New Application for {application.job_post.job_title}"
        message = f"""
        Hello,

        You have received a new application for the job '{application.job_post.job_title}'.

        Applicant Name: {application.full_name}
        Email: {application.email}
        Mobile Number: {application.mobile_number}
        Current Role: {application.current_role.role}
        Total Years of Experience: {application.total_years_of_experience}
        Notes to Recruiter: {application.notes_to_recruiter}

        Best regards,
        Your Job Portal
        """

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,  # Ensure you have DEFAULT_FROM_EMAIL set in your settings
            [recipient_email],
            fail_silently=False,
        )

# class RetrieveApplication(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
        
#         applications = Application.objects.all()
        
#         applications_data = []
#         for application in applications:
#             applications_data.append({
#                 'id': application.id,
#                 'full_name': application.full_name,
#                 'email': application.email,
#                 # 'mobile_number': application.mobile_number,
#                 # 'current_industry': application.current_industry.title,  # Adjust based on your Industry model
#                 'current_role': application.current_role.title,  # Adjust based on your Role model
#                 'total_years_of_experience': application.total_years_of_experience,
#                 # 'skills': [skill.skill for skill in application.skills.all()],  # List of skill names
#                 # 'applied_on': application.applied_on,
#                 'resume': request.build_absolute_uri(application.resume.url) if application.resume else None,
#                 # 'notes_to_recruiter': application.notes_to_recruiter,
#             })

#         return Response(applications_data, status=status.HTTP_200_OK)

class MyJobApplication(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, job_post_id):
        # Get the job posts created by the authenticated user
        job_post = JobPost.objects.get(id=job_post_id)

        # Get applications for those job posts
        applications = Application.objects.filter(job_post=job_post).order_by('-id')

        # Apply pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Set the number of items per page
        paginated_applications = paginator.paginate_queryset(applications, request)

        applications_data = []
        for application in paginated_applications:
            applications_data.append({
                'id': application.id,
                'full_name': application.full_name,
                'email': application.email,
                'current_role': application.current_role.role,  # Adjust based on your Role model
                'total_years_of_experience': application.total_years_of_experience,
                'resume': request.build_absolute_uri(application.resume.url) if application.resume else None,
            })

        return paginator.get_paginated_response(applications_data)

class DetailViewApplication(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request,application_id):
        
        application = Application.objects.get(id=application_id)

        
        applications_data={
                'id': application.id,
                'job_id':application.job_post.id,
                'job_name': application.job_post.job_title,
                'full_name': application.full_name,
                'email': application.email,
                'mobile_number': application.mobile_number,
                'current_industry': application.current_industry.title,  # Adjust based on your Industry model
                'current_role': application.current_role.role,  # Adjust based on your Role model
                'total_years_of_experience': application.total_years_of_experience,
                'skills': [skill.skill for skill in application.skills.all()],  # List of skill names
                'applied_on': application.applied_on,
                'resume': request.build_absolute_uri(application.resume.url) if application.resume else None,
                'notes_to_recruiter': application.notes_to_recruiter,
        }

        return Response(applications_data, status=status.HTTP_200_OK)