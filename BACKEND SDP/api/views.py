from django.shortcuts import render
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .models import User, PasswordResetToken
from rest_framework.response import Response
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.decorators import api_view, throttle_classes
from .serializers import (
    UserSerializer, Notification, AcademicYear, YearsSerializer, 
    NotificationsSerializer, CourseSerializer, Course, ProgrammeSerializer, 
    Programme, MissingMarksComplaint, MissingMarksComplaintSerializer, 
    RegistrationComplaint, RegistrationComplaintSerializer
)
import random
from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from rest_framework.throttling import AnonRateThrottle


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims to the token payload
        token['role'] = user.role
        token['email'] = user.email
        token['student_number'] = user.student_number
        token['registration_number'] = user.registration_number
        token['programme'] = user.programme
        token['has_profile'] = user.has_profile

        return token
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

@api_view(["POST"])
def sign_up(request):
    try:
        if request.method == "POST":
            # Validate email domain
            if "students.mak.ac.ug" not in request.data["email"] and "cit.mak.ac.ug" not in request.data["email"]:
                return Response({"error": "Invalid email domain. Must be students.mak.ac.ug or cit.mak.ac.ug"}, 
                             status=status.HTTP_400_BAD_REQUEST)

            # Hash the password
            request.data["password"] = make_password(request.data["password"])

            # Set role based on email domain
            if "students.mak.ac.ug" in request.data["email"]:
                request.data["role"] = "student"
            elif "cit.mak.ac.ug" in request.data["email"]:
                request.data["role"] = "lecturer"

            # Check if user already exists
            try:
                user = User.objects.get(email=request.data["email"])
                return Response({"error": "User with this email already exists"}, 
                             status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                pass

            # Create new user
            converted = UserSerializer(data=request.data)
            if converted.is_valid():
                new_user = converted.save()
                return Response({
                    "message": "Account created successfully. Please login.",
                    "user": converted.data
                }, status=status.HTTP_201_CREATED)
            else:
                return Response(converted.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def login(request):
    if request.method == "POST":
        try:
            email = request.data.get("email")
            password = request.data.get("password")
            
            if not email or not password:
                return Response({"error": "Email and password are required"}, 
                             status=status.HTTP_400_BAD_REQUEST)

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error": "Invalid email or password"}, 
                             status=status.HTTP_401_UNAUTHORIZED)

            if not user.check_password(password):
                return Response({"error": "Invalid email or password"}, 
                             status=status.HTTP_401_UNAUTHORIZED)

            # Generate tokens
            access_token = AccessToken.for_user(user)
            refresh_token = RefreshToken.for_user(user)

            try:
                user_programme = int(user.programme.id) if user.programme else None
            except:
                user_programme = None

            return Response({
                "access": str(access_token),
                "refresh": str(refresh_token),
                "user": {
                    "email": user.email,
                    "student_number": user.student_number,
                    "registration_number": user.registration_number,
                    "programme": user_programme,
                    "role": user.role,
                    "user_id": user.id,
                    "has_profile": "true" if user.has_profile else "false",
                }
            })
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def verify_otp(request):
    if request.method == "POST":
        try:
            OTP = request.data["OTP"]
            user = User.objects.get(OTP = OTP)
            user.save()
            access_token = AccessToken.for_user(user)
            refresh_token = RefreshToken.for_user(user)
            try:
                user_programme = int(user.programme.id)
            except:
                user_programme = None    
            return Response({"access": str(access_token), "refresh": str(refresh_token), "user": {
                "email": user.email,
                "student_number": user.student_number,
                "registration_number": user.registration_number,
                "programme": user_programme,
                "role": user.role,
                "user_id": user.id,
                "has_profile": "true" if user.has_profile else "false",
            }})
        except:
            return Response(status = status.HTTP_403_FORBIDDEN)
        
@api_view(['PATCH'])
def update_profile(request, pk):
    try:
        user = User.objects.get(id =pk)
    except:
        user = None

    if user is not None:
        converted = UserSerializer(user, data=request.data, partial = True)

        if converted.is_valid():
            converted.save()

            user.has_profile = True
            user.save()
            return Response(converted.data, status=status.HTTP_202_ACCEPTED)
        
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
            

    else:      
        return Response(status= status.HTTP_404_NOT_FOUND)     

@api_view(['GET', 'POST'])
def courses(request, pk):
    courses = Course.objects.filter(lecturer = pk)
    converted = CourseSerializer(courses, many = True)
    
    if request.method == "POST":
        converted = CourseSerializer(data = request.data)

        if converted.is_valid():
            converted.save()
            return Response(converted.data, status= status.HTTP_201_CREATED)
        
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response(converted.data)  

@api_view(['GET'])
def all_courses(request, pk):
    courses = Course.objects.filter(programme = pk)
    converted = CourseSerializer(courses, many = True)
    return Response(converted.data)  
  
@api_view(['GET', 'POST'])
def programmes(request):

    programmes = Programme.objects.all()
    converted = ProgrammeSerializer(programmes, many = True)
    
    if request.method == "POST":
        converted = ProgrammeSerializer(data = request.data)

        if converted.is_valid():
            converted.save()
            return Response(converted.data, status= status.HTTP_201_CREATED)
        
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response(converted.data)    

@api_view(['GET'])
def student_statistics(request, pk):
    reg_complaints_all = RegistrationComplaint.objects.filter(student=pk).count()
    reg_complaints_pending = RegistrationComplaint.objects.filter(student=pk, status="pending").count()
    marks_complaints_all = MissingMarksComplaint.objects.filter(student=pk).count()
    marks_complaints_pending = MissingMarksComplaint.objects.filter(student=pk, status="pending").count()

    response = {
        "total": marks_complaints_all + reg_complaints_all,
        "pending": marks_complaints_pending + reg_complaints_pending
    }

    return Response(response)



@api_view(['GET', 'POST'])
def notifications(request, pk):
    try:
        user = User.objects.get(id = pk)
    except:
        user = None

    if user is not None:

        if request.method == "POST":
            converted = NotificationsSerializer(data=request.data)

            if converted.is_valid():

                converted.save()

                return Response(converted.data, status=status.HTTP_201_CREATED)

            else:
                return Response(status=status.HTTP_201_CREATED)    
            

        notifications = Notification.objects.filter(reciever = pk)
        converted = NotificationsSerializer(notifications, many = True)
        return Response(converted.data)
    
    else:
        return Response(status = status.HTTP_403_FORBIDDEN)
    

@api_view(['GET'])
def view_notifications(request, pk):
    try:
        user = User.objects.get(id = pk)
    except:
        user = None

    if user is not None:
        notifications = Notification.objects.filter(reciever = pk)

        for notification in notifications:
            notification.is_viewed = True
            notification.save()

        return Response(status=status.HTTP_202_ACCEPTED)
    
    else:
        return Response(status = status.HTTP_403_FORBIDDEN)

    
@api_view(['GET', 'POST'])
def academic_years(request):
    if request.method == "POST":
        # Validate that the title is in the format YYYY/YYYY
        title = request.data.get('title', '')
        if not title or not '/' in title:
            return Response({"error": "Academic year must be in format YYYY/YYYY"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            start_year, end_year = title.split('/')
            if not (start_year.isdigit() and end_year.isdigit() and len(start_year) == 4 and len(end_year) == 4):
                raise ValueError
            if int(end_year) != int(start_year) + 1:
                return Response({"error": "End year must be start year + 1"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({"error": "Academic year must be in format YYYY/YYYY"}, status=status.HTTP_400_BAD_REQUEST)

        converted = YearsSerializer(data=request.data)
        if converted.is_valid():
            converted.save()
            return Response(converted.data, status=status.HTTP_201_CREATED)
        else:
            return Response(converted.errors, status=status.HTTP_400_BAD_REQUEST)

    academic_years = AcademicYear.objects.all().order_by('-created')
    converted = YearsSerializer(academic_years, many=True)
    return Response(converted.data)

@api_view(['GET', 'POST'])
def missing_marks(request, pk):

    if request.method == "POST":
        converted = MissingMarksComplaintSerializer(data = request.data)

        if converted.is_valid():
            student = User.objects.get(id = request.data["student"])
            course = Course.objects.get(id = request.data["course"])
            lecturer = User.objects.get(id = course.lecturer.id)
            
            Notification.objects.create(
                severity = "warning",
                body = f"You have a new complaint on {course.name} from {student.email}",
                reciever = lecturer
            )
            converted.save()
            return Response(converted.data, status = status.HTTP_201_CREATED)
        
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)

    complaints = MissingMarksComplaint.objects.filter(student = pk)
    converted = MissingMarksComplaintSerializer(complaints, many = True)
    return Response(converted.data)

@api_view(['GET', 'POST'])
def registration_issues(request, pk):

    if request.method == "POST":
        converted = RegistrationComplaintSerializer(data = request.data)

        if converted.is_valid():
            student = User.objects.get(id = request.data["student"])
            registrar = User.objects.get(role = "registrar")
            Notification.objects.create(
                severity = "warning",
                body = f"You have a new complaint titled ({(request.data["subject"])}) from {student.email}",
                reciever = registrar
            )            
            converted.save()
            return Response(converted.data, status = status.HTTP_201_CREATED)
        
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)

    complaints = RegistrationComplaint.objects.filter(student = pk)
    converted = RegistrationComplaintSerializer(complaints, many = True)
    return Response(converted.data)


@api_view(['GET'])
def sent_complaints(request, pk):
    reg_complaints_all = RegistrationComplaint.objects.filter(student=pk)
    marks_complaints_all = MissingMarksComplaint.objects.filter(student=pk)

    all_complaints = []

    converted_missing = MissingMarksComplaintSerializer(marks_complaints_all, many=True)
    converted_reg = RegistrationComplaintSerializer(reg_complaints_all, many=True)
    
    for complaint in converted_missing.data:
        complaint["type"] = "missing marks complaint"
        all_complaints.append(complaint)

    for complaint in converted_reg.data:
        complaint["type"] = "registration issues"
        all_complaints.append(complaint)

    return Response(all_complaints)


@api_view(['GET'])
def reg_complaints(request, pk):
    reg_complaints = RegistrationComplaint.objects.filter(student__programme = pk)
    
    for complaint in reg_complaints:
        complaint.seen = True
        complaint.save()

    converted = RegistrationComplaintSerializer(reg_complaints, many = True)

    return Response(converted.data)

@api_view(['PATCH'])
def update_reg_complaint(request, pk):
    try:
        complaint = RegistrationComplaint.objects.get(id = pk)
    except:
        complaint = None

    if complaint is not None:
        
        Notification.objects.create(
            reciever = complaint.student,
            severity = "success" if request.data["status"] == "resolved" else "info",
            body = "The registrar has addressed a complaint you made, please get to know more about this from the complaints page"
        )
        complaint.status = request.data["status"]
        complaint.save()
        
        return Response(status= status.HTTP_202_ACCEPTED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST) 
         
@api_view(['PATCH'])
def update_marks_complaint(request, pk):
    try:
        complaint = MissingMarksComplaint.objects.get(id = pk)
    except:
        complaint = None

    if complaint is not None:
        
        Notification.objects.create(
            reciever = complaint.student,
            severity = "success" if request.data["status"] == "resolved" else "info",
            body = f"The lecturer ({complaint.course.lecturer.email}) has addressed a complaint you made about missing marks for a courseunit  ({complaint.course.name}) that you covered in {complaint.year_of_study}, please get to know more about this from the complaints page"
        )
        complaint.status = request.data["status"]
        complaint.save()
        
        return Response(status= status.HTTP_202_ACCEPTED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)      

@api_view(['GET'])
def marks_complaints(request, pk):
    complaints = MissingMarksComplaint.objects.filter(course = pk)
    
    for complaint in complaints:
        complaint.seen = True
        complaint.save()

    converted = MissingMarksComplaintSerializer(complaints, many = True)

    return Response(converted.data)      

class PasswordResetThrottle(AnonRateThrottle):
    rate = '3/hour'  # Allow 3 requests per hour

@api_view(['POST'])
@throttle_classes([PasswordResetThrottle])
def forgot_password(request):
    email = request.data.get('email')
    if not email:
        return Response({'error': 'Email is required'}, status=400)

    # Check if a reset request was made recently
    cache_key = f'password_reset_{email}'
    if cache.get(cache_key):
        return Response({
            'error': 'A password reset request was already sent. Please check your email or try again later.'
        }, status=429)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        # Don't reveal if the email exists or not for security
        return Response({
            'message': 'If an account exists with this email, you will receive password reset instructions.'
        })

    # Generate a random token
    token = get_random_string(length=32)
    
    # Store the token in the database with an expiration time (24 hours)
    PasswordResetToken.objects.create(
        user=user,
        token=token,
        expires_at=timezone.now() + timedelta(hours=24)
    )

    # Set cache to prevent multiple requests
    cache.set(cache_key, True, 3600)  # Cache for 1 hour

    # Send the reset email
    reset_url = f"{settings.FRONTEND_URL}/reset-password/{token}"
    try:
        send_mail(
            'Password Reset Request - WBCMS',
            f'Hello,\n\n'
            f'You have requested to reset your password for the Web-based Complaint Monitoring System (WBCMS).\n\n'
            f'Click the following link to reset your password: {reset_url}\n\n'
            f'This link will expire in 24 hours.\n\n'
            f'If you did not request a password reset, please ignore this email and ensure your account is secure.\n\n'
            f'Best regards,\nWBCMS Team',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
    except Exception as e:
        # Log the error but don't expose it to the user
        print(f"Failed to send password reset email: {str(e)}")
        return Response({
            'error': 'Failed to send reset email. Please try again later.'
        }, status=500)

    return Response({
        'message': 'If an account exists with this email, you will receive password reset instructions.'
    })

@api_view(['POST'])
def reset_password(request, token):
    password = request.data.get('password')
    if not password:
        return Response({'error': 'Password is required'}, status=400)

    try:
        # Validate password strength
        validate_password(password)
    except ValidationError as e:
        return Response({
            'error': 'Password validation failed',
            'details': list(e.messages)
        }, status=400)

    try:
        reset_token = PasswordResetToken.objects.get(
            token=token,
            expires_at__gt=timezone.now(),
            used=False
        )
    except PasswordResetToken.DoesNotExist:
        return Response({
            'error': 'Invalid or expired reset token. Please request a new password reset.'
        }, status=400)

    # Update the user's password
    user = reset_token.user
    try:
        user.set_password(password)
        user.save()
    except Exception as e:
        return Response({
            'error': 'Failed to update password. Please try again.'
        }, status=500)

    # Mark the token as used and delete other unused tokens
    reset_token.used = True
    reset_token.save()
    PasswordResetToken.objects.filter(user=user, used=False).delete()

    # Clear any existing sessions for this user
    user.auth_token_set.all().delete()

    return Response({
        'message': 'Password has been reset successfully. You can now login with your new password.'
    })

@api_view(['GET'])
def lecturers(request):
    lecturers = User.objects.filter(role='lecturer')
    converted = UserSerializer(lecturers, many=True)
    return Response(converted.data)
