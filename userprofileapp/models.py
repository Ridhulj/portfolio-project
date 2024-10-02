
from django.db import models
from django.contrib.auth.models import User

class Portfolio(models.Model):
    # Link each portfolio to a specific user, ensuring one-to-one relationship
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="portfolio")

    # Name field for full name
    full_name = models.CharField(max_length=255)

    # Bio field for personal biography
    bio = models.TextField(blank=True)

    # Skills field for skill sets (can be a comma-separated string)
    skills = models.CharField(max_length=255, help_text="Comma separated skills, e.g., Python, Java, Django")

    # Contact details
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    # Optional field for location
    location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.full_name



class Experience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user (portfolio owner)
    job_title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)  # Optional field for location
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)  # Null/blank for current job

    def __str__(self):
        return f'{self.job_title} at {self.company_name}'


class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user (portfolio owner)
    school_name = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    field_of_study = models.CharField(max_length=255, blank=True)  # Optional field for major/field of study
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)  # Null/blank for ongoing education

    def __str__(self):
        return f'{self.degree} in {self.field_of_study} from {self.school_name}'

class Certification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user (portfolio owner)
    certification_name = models.CharField(max_length=255)
    issuing_organization = models.CharField(max_length=255)
    issue_date = models.DateField()
    expiration_date = models.DateField(null=True, blank=True)  # Some certifications do not expire

    def __str__(self):
        return f'{self.certification_name} by {self.issuing_organization}'




class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link each project to a user
    project_name = models.CharField(max_length=255)
    description = models.TextField()
    image1 = models.ImageField(upload_to='project_images/', verbose_name='Image 1')
    image2 = models.ImageField(upload_to='project_images/', verbose_name='Image 2')
    github_link = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return self.project_name

