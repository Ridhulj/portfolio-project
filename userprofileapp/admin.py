from django.contrib import admin
from .models import Portfolio, Experience, Education, Certification,Project
# Register your models here.
admin.site.register(Portfolio)
admin.site.register(Experience)
admin.site.register(Education)
admin.site.register(Certification)
admin.site.register(Project)