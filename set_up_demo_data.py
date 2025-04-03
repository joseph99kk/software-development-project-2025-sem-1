# issues/management/commands/setup_demo_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from issues.models import Department, Category, Issue, Activity

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates initial demo data for the application'

    def handle(self, *args, **options):
        # Create admin user if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            self.stdout.write(self.style.SUCCESS('Admin user created successfully'))
        else:
            admin_user = User.objects.get(username='admin')
        
        # Create departments
        departments = [
            {'name': 'Computer Science', 'description': 'Department of Computer Science and Software Engineering'},
            {'name': 'Mathematics', 'description': 'Department of Mathematics and Statistics'},
            {'name': 'Physics', 'description': 'Department of Physics and Astronomy'},
            {'name': 'Humanities', 'description': 'Department of Humanities and Social Sciences'},
            {'name': 'Administration', 'description': 'Administrative Department'},
        ]
        
        created_departments = []
        for dept_data in departments:
            dept, created = Department.objects.get_or_create(
                name=dept_data['name'],
                defaults={'description': dept_data['description']}
            )
            created_departments.append(dept)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Department "{dept.name}" created'))
            else:
                self.stdout.write(self.style.WARNING(f'Department "{dept.name}" already exists'))
        
        # Create categories
        categories = [
            {'name': 'Grading', 'color': 'blue'},
            {'name': 'Registration', 'color': 'green'},
            {'name': 'Scheduling', 'color': 'purple'},
            {'name': 'Technical', 'color': 'yellow'},
            {'name': 'Materials', 'color': 'red'},
        ]
        
        created_categories = []
        for cat_data in categories:
            cat, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'color': cat_data['color']}
            )
            created_categories.append(cat)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Category "{cat.name}" created'))
            else:
                self.stdout.write(self.style.WARNING(f'Category "{cat.name}" already exists'))
        
        self.stdout.write(self.style.SUCCESS('Demo data setup completed successfully'))