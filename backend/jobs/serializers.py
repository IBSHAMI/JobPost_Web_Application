from rest_framework import serializers
from rest_framework.reverse import reverse
from django.contrib.auth import get_user_model

from .models import Job, SavedJob, AppliedJob
from employee.models import EmployeeProfile


User = get_user_model()

# Create a Serializer class for job create
class JobCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            'pk',
            'title',
            'description',
            'location',
            'type',
            'framework',
            'language',
            'experience',
            'number_of_positions',
            'remote',
            'salary',
            'company',
        ]


# Create a Serializer class for job list
class JobListSerializer(serializers.ModelSerializer):
    company_name = serializers.SerializerMethodField(read_only=True)
    is_saved_job = serializers.SerializerMethodField(read_only=True)


    class Meta:
        model = Job
        fields = [
            'pk',
            'title',
            'type',
            'salary',
            'location',
            'experience',
            'language',
            'date_created',
            'number_of_positions',
            'internal',
            'company_name',
            'is_saved_job',
        ]

    def get_company_name(self, obj):
        if obj.internal:
            return obj.job_company
        company = obj.company
        return company.company_name
    
    def get_is_saved_job(self, obj):
        user = self.context['request'].user
        
        if not user.is_authenticated:
            return False
        
        employee = EmployeeProfile.objects.get(user=user)
        job = obj
        
        if SavedJob.objects.filter(employee=employee, job=job).exists():
            return True
        
        return False
        


# Create a Serializer class for job list for company
class CompanyJobListSerializer(serializers.ModelSerializer):
    number_of_applications = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Job
        fields = [
            'pk',
            'title',
            'type',
            'salary',
            'language',
            'date_created',
            'is_active',
            'number_of_applications',
        ]
    
    def get_number_of_applications(self, obj):
        job = obj 
        number_of_applications = AppliedJob.objects.filter(job=job).count()
        
        return number_of_applications


class JobDetailSerializer(JobCreateSerializer):
    company_data = serializers.SerializerMethodField(read_only=True)
    is_applied = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Job
        fields = [
            'pk',
            'title',
            'description',
            'location',
            'type',
            'language',
            'experience',
            'number_of_positions',
            'date_created',
            'remote',
            'salary',
            'internal',
            'job_link',
            'company_data',
            'is_applied',
        ]

    def get_company_data(self, obj):
        if obj.internal:
            return {
            'company_name': obj.job_company,
            'company_location': None,
            'company_website': None,
            'company_size': None,
            }
        company = obj.company
        return {
            'company_name': company.company_name,
            'company_location': company.company_location,
            'company_website': company.company_website,
            'company_size': company.company_size,
        }
        
    def get_is_applied(self, obj):
        user = self.context['request'].user
        
        if not user.is_authenticated:
            return False
        
        employee = EmployeeProfile.objects.get(user=user)
        job = obj
        
        if AppliedJob.objects.filter(employee=employee, job=job).exists():
            return True
        
        return False


class SavedJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedJob
        fields = [
            'employee', 
            'job',
        ]
        

class SavedJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedJob
        fields = [
            'employee', 
            'job',
        ]


class AppliedJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppliedJob
        fields = [
            'employee', 
            'job',
        ]
        
class ApplicantsJobListSerializer(serializers.ModelSerializer):
    employee_data = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = AppliedJob
        fields = [
            'employee_data',
            'date_applied',
        ]
    
    def get_employee_data(self, obj):
        employee = obj.employee
        employee_data = {
            'pk': employee.pk,
            'first_name': employee.user.first_name,
            'last_name': employee.user.last_name,
            'email': employee.user.email,
            'experience': employee.experience,
            'expected_salary': employee.expected_salary,
            'linkedin_url': employee.linkedin_url,
            'portfolio_url': employee.portfolio_url,
            'about': employee.about,
        }
           
        return employee_data