from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.forms import modelformset_factory
from .forms import PortfolioForm, ExperienceForm, EducationForm, CertificationForm,ProjectForm
from .models import Portfolio, Experience, Education, Certification,Project






def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['password1']

        # Check if username or email already exists
        if password==cpassword:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken.')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already in use.')
                return redirect('register')
            else:
                user = User.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password
                )
                user.save()
            return redirect('login')
        else:
            messages.info(request,'This password does not match')
            return redirect('register')

    return render(request, 'register.html')


def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('view_portfolio')  # Replace with your admin page URL
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')

    return render(request, 'login.html')

def logout_view(request):
    auth.logout(request)  # Log out the user
    return redirect('login')  # Redirect to login page after logout

# Homepage View
def homepage(request):
    return render(request, 'homepage.html')

def create_portfolio(request):
    # Prevent a user from creating multiple portfolios
    if Portfolio.objects.filter(user=request.user).exists():
        return redirect('view_portfolio')  # Redirect to their existing portfolio view

    if request.method == 'POST':
        form = PortfolioForm(request.POST)
        if form.is_valid():
            portfolio = form.save(commit=False)
            portfolio.user = request.user  # Associate the portfolio with the logged-in user
            portfolio.save()
            return redirect('view_portfolio')  # Redirect to the portfolio view
    else:
        form = PortfolioForm()

    return render(request, 'createportfolio.html', {'form': form})


def update_portfolio(request, portfolio_id):
    # Retrieve the portfolio, but only if it belongs to the current user
    portfolio = get_object_or_404(Portfolio, id=portfolio_id, user=request.user)

    if request.method == 'POST':
        form = PortfolioForm(request.POST, files=request.FILES, instance=portfolio)
        if form.is_valid():
            form.save()  # Save the updated portfolio
            return redirect('view_portfolio')  # Redirect to the portfolio view after saving
    else:
        form = PortfolioForm(instance=portfolio)

    return render(request, 'updateportfolio.html', {'form': form})

def view_portfolio(request):
    # Retrieve the current user's portfolio
    try:
        portfolio = Portfolio.objects.get(user=request.user)
    except Portfolio.DoesNotExist:
        portfolio = None  # Handle case where the user doesn't have a portfolio yet

    return render(request, 'viewportfolio.html', {'portfolio': portfolio})




def create_details(request):
    # Create formsets for Experience, Education, and Certification models
    ExperienceFormSet = modelformset_factory(Experience, form=ExperienceForm, extra=1)
    EducationFormSet = modelformset_factory(Education, form=EducationForm, extra=1)
    CertificationFormSet = modelformset_factory(Certification, form=CertificationForm, extra=1)

    if request.method == 'POST':
        # Initialize formsets with POST data (form submission)
        experience_formset = ExperienceFormSet(request.POST, queryset=Experience.objects.filter(user=request.user))
        education_formset = EducationFormSet(request.POST, queryset=Education.objects.filter(user=request.user))
        certification_formset = CertificationFormSet(request.POST, queryset=Certification.objects.filter(user=request.user))

        # Validate all formsets
        if experience_formset.is_valid() and education_formset.is_valid() and certification_formset.is_valid():
            # Save Experience formset
            experiences = experience_formset.save(commit=False)
            for experience in experiences:
                experience.user = request.user  # Assign the user
                experience.save()  # Now save each instance

            # Save Education formset
            educations = education_formset.save(commit=False)
            for education in educations:
                education.user = request.user  # Assign the user
                education.save()  # Save each instance

            # Save Certification formset
            certifications = certification_formset.save(commit=False)
            for certification in certifications:
                certification.user = request.user  # Assign the user
                certification.save()  # Save each instance

            return redirect('viewdetails')  # Redirect to success page after saving

    else:
        # Display formsets with any existing data
        experience_formset = ExperienceFormSet(queryset=Experience.objects.filter(user=request.user))
        education_formset = EducationFormSet(queryset=Education.objects.filter(user=request.user))
        certification_formset = CertificationFormSet(queryset=Certification.objects.filter(user=request.user))

    # Pass formsets to the template
    context = {
        'experience_formset': experience_formset,
        'education_formset': education_formset,
        'certification_formset': certification_formset,
    }
    return render(request, 'create_details.html', context)


def view_details(request):
    experiences = Experience.objects.filter(user=request.user)
    education = Education.objects.filter(user=request.user)
    certifications = Certification.objects.filter(user=request.user)

    context = {
        'experiences': experiences,
        'education': education,
        'certifications': certifications,

    }

    return render(request, 'view_details.html', context)



def edit_experience(request, id):
    experience = get_object_or_404(Experience, id=id)
    if request.method == "POST":
        form = ExperienceForm(request.POST, instance=experience)
        if form.is_valid():
            form.save()
            return redirect('viewdetails')  # Redirect after saving
    else:
        form = ExperienceForm(instance=experience)
    return render(request, 'edit_details.html', {'experience_form': form})

def edit_education(request, id):
    education = get_object_or_404(Education, id=id)
    if request.method == "POST":
        form = EducationForm(request.POST, instance=education)
        if form.is_valid():
            form.save()
            return redirect('viewdetails')  # Redirect after saving
    else:
        form = EducationForm(instance=education)
    return render(request, 'edit_details.html', {'education_form': form})

def edit_certification(request, id):
    certification = get_object_or_404(Certification, id=id)
    if request.method == "POST":
        form = CertificationForm(request.POST, instance=certification)
        if form.is_valid():
            form.save()
            return redirect('viewdetails')  # Redirect after saving
    else:
        form = CertificationForm(instance=certification)
    return render(request, 'edit_details.html', {'certification_form': form})


def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)  # Include FILES for image uploads
        if form.is_valid():
            project = form.save(commit=False)  # Don't save yet, we need to set the user
            project.user = request.user  # Assign the current logged-in user
            project.save()  # Save the project with the user assigned
            return redirect('project_showcase')  # Redirect to the project showcase page
    else:
        form = ProjectForm()

    return render(request, 'create_project.html', {'form': form})


def update_project(request, project_id):
    project = get_object_or_404(Project, id=project_id,
                                user=request.user)  # Ensure the project belongs to the current user
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_showcase')
    else:
        form = ProjectForm(instance=project)

    return render(request, 'update_project.html', {'form': form})



def project_showcase(request):
    projects = Project.objects.filter(user=request.user)  # Show only projects belonging to the logged-in user
    return render(request, 'project_showcase.html', {'projects': projects})


def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        project.delete()
        return redirect('project_showcase')  # Redirect to your project list or showcase page

    return render(request, 'confirm_delete.html', {'project': project})
