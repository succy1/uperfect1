from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegisterForm
from .quiz import *
from django.contrib.auth.decorators import login_required
from .models import Profile, SkincareGoal, SkinCondition, SkinType
from django.apps import apps
from django.contrib import messages

# Create your views here.
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get('username')
            # messages.success(request, f"Tài khoản của bạn đã được tạo!")
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def skin_quiz(request):
    return render(request, 'skin-quiz.html', {'questions': SKIN_QUIZ})

@login_required
def profile(request):
    profile = get_object_or_404(Profile, user=request.user)

    UserProduct = apps.get_model('product', 'UserProduct')
    Review = apps.get_model('product', 'Review')

    user_products = UserProduct.objects.filter(user=request.user).select_related('product')
    user_reviews = Review.objects.filter(user=request.user).select_related('product')

    grouped_user_products = {}
    for user_product in user_products:
        product_type = user_product.product.product_type.name
        if product_type not in grouped_user_products:
            grouped_user_products[product_type] = []
        grouped_user_products[product_type].append(user_product)

    context = {
        'profile': profile,
        'user_products': grouped_user_products,
        'user_reviews': user_reviews,
    }
    return render(request, 'profile.html', context)

@login_required
def onboarding(request):
    if request.method == 'POST':
        step = request.POST.get('step')
        
        if step == 'goals':
            selected_goals = request.POST.getlist('goals')
            request.session['selected_goals'] = selected_goals
            return redirect('onboarding')  # This will now redirect to the 'profile' step
        
        elif step == 'profile':
            gender = request.POST.get('gender')
            skin_types = request.POST.getlist('skin_types')
            skin_conditions = request.POST.getlist('skin_conditions')
            
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.gender = gender
            profile.skin_types.set(SkinType.objects.filter(id__in=skin_types))
            profile.skin_conditions.set(SkinCondition.objects.filter(id__in=skin_conditions))
            profile.skincare_goals.set(SkincareGoal.objects.filter(id__in=request.session.get('selected_goals', [])))
            profile.save()
            
            messages.success(request, 'Profile created successfully!')
            return redirect('profile_completed')
    
    else:
        # Check if goals have been selected
        if 'selected_goals' in request.session:
            step = 'profile'
        else:
            step = 'goals'
    
    context = {
        'step': step,
        'skincare_goals': SkincareGoal.objects.all(),
        'skin_types': SkinType.objects.all(),
        'skin_conditions': SkinCondition.objects.all(),
    }
    return render(request, 'onboarding.html', context)