from django.shortcuts import render
from icine.models import Category
from icine.models import Page
from icine.forms import CategoryForm
from django.shortcuts import redirect
from icine.forms import PageForm
from django.urls import reverse
from icine.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from icine.bing_search import run_query
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User 
from icine.models import UserProfile
from django.http import HttpResponse

class IndexView(View):
    def get(self,request):
        # Query the database for a list of ALL categories currently stored.
        # Order the categories by the number of likes in descending order.
        # Retrieve the top 5 only -- or all if less than 5.
        # Place the list in our context_dict dictionary (with our boldmessage)
        # that will be passed to the template engine.

        category_list = Category.objects.order_by('-likes')[:5]
        page_list = Page.objects.order_by('-views')[:5]

        context_dict = {}
        context_dict['pages'] = page_list
        context_dict['categories'] = category_list
        visitor_cookie_handler(request)
        response = render(request, 'icine/index.html', context=context_dict)
        # Return response back to the user, updating any cookies that need changed.
        return response

class AboutView(View):    
    def get(self,request):
        context_dict = {}
        visitor_cookie_handler(request)
        context_dict['visits'] = request.session['visits']
        return render(request, 'icine/about.html', context=context_dict)

# def index(request):
# 	context = {
# 		'posts': posts
# 	}
# 	return render(request, 'icine/index.html', context)

def show_category(request, category_name_slug):
        context_dict = {}

        try:
            category = Category.objects.get(slug=category_name_slug)
            pages = Page.objects.filter(category=category).order_by('-views')

            context_dict['pages'] = pages
            context_dict['category'] = category

        except Category.DoesNotExist:
            context_dict['category'] = None
            context_dict['pages'] = None
        return render(request, 'icine/category.html', context_dict)
# class ShowCategoryView(View):
#     def show_category(self, category_name_slug):
#         context_dict = {}

#         try:
#             category = Category.objects.get(slug=category_name_slug)
#             pages = Page.objects.filter(category=category).order_by('-views')

#             context_dict['pages'] = pages
#             context_dict['category'] = category

#         except Category.DoesNotExist:
#             context_dict['category'] = None
#             context_dict['pages'] = None
    
#     def get(self,request,category_name_slug):
#         context_dict = self.create_context_dict(category_name_slug)
#         return render(request, 'icine/category.html', context_dict)
#         # Start new search functionality code.
    
    # # @method_decorator(login_required)
    # # def POST(self,request,category_name_slug):  
    #     context_dict = self.create_context_dict(category_name_slug)
    #     query = request.POST['query'].strip()

    #     if query:
    #         context_dict['result_list'] = run_query(query)
    #         context_dict['query'] = query
    #     # End new search functionality code.
    #     return render(request, 'icine/category.html', context_dict)

def visitor_cookie_handler(request):
# Get the number of visits to the site.
# We use the COOKIES.get() function to obtain the visits cookie.
# If the cookie exists, the value returned is casted to an integer. # If the cookie doesn't exist, then the default value of 1 is used. 
    visits = int(get_server_side_cookie(request, 'visits', '1')) 
    last_visit_cookie = get_server_side_cookie(request,
                                                'last_visit',
                                                str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                         '%Y-%m-%d %H:%M:%S')

    # If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
    # Update the last visit cookie now that we have updated the count 
        request.session['last_visit'] = str(datetime.now())
    else:
    # Set the last visit cookie 
        request.session['last_visit'] = last_visit_cookie
        # Update/set the visits cookie
    request.session['visits'] = visits

# A helper method
def get_server_side_cookie(request, cookie, default_val=None): 
    val = request.session.get(cookie)
    if not val:
        val = default_val 
    return val

class GoToView(View):
    def get(self,request):
        page_id = request.GET.get('page_id')
        try:
            selected_page = Page.objects.get(id=page_id)
        except Page.DoesNotExist:
            return redirect(reverse('icine:index'))
        selected_page.views = selected_page.views + 1
        selected_page.save()
            
        return redirect(selected_page.url)


class RegisterProfileView(View):
    @method_decorator(login_required)
    def get(self,request): 
        form = UserProfileForm()
        context_dict = {'form': form}
        return render(request, 'icine/profile_registration.html', context_dict)

    @method_decorator(login_required)
    def post(self, request):
        form = UserProfileForm(request.POST, request.FILES)

        if form.is_valid():
            user_profile = form.save(commit=False) 
            user_profile.user = request.user 
            user_profile.save()

            return redirect(reverse('icine:index')) 
        else:
            print(form.errors)

        context_dict = {'form': form}
        return render(request, 'icine/profile_registration.html', context_dict)
            
class ProfileView(View):
    def get_user_details(self,username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist: 
            return None

        user_profile = UserProfile.objects.get_or_create(user=user)[0] 
        form = UserProfileForm({'website': user_profile.website,
                                'picture': user_profile.picture})
        return (user, user_profile, form)

    @method_decorator(login_required) 
    def get(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('icine:index'))
      
        context_dict = {'user_profile': user_profile, 
                        'selected_user': user,
                        'form': form}
        return render(request, 'icine/profile.html', context_dict)
    
    @method_decorator(login_required)
    def post(self,request,username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('icine:index'))

        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            form.save(commit=True)
            return redirect('icine:profile', user.username)
        else: 
            print(form.errors)
        
        context_dict = {'user_profile': user_profile, 
                        'selected_user': user,
                        'form': form}
        return render(request, 'icine/profile.html', context_dict)

class ListProfilesView(View):
    @method_decorator(login_required) 
    def get(self, request):
        profiles = UserProfile.objects.all()
        return render(request, 'icine/list_profiles.html',{'userprofile_list': profiles})

class LikeCategoryView(View): 
    @method_decorator(login_required) 
    def get(self, request):
        category_id = request.GET['category_id'] 
        try:
            category = Category.objects.get(id=int(category_id)) 
        except Category.DoesNotExist:
            return HttpResponse(-1) 
        except ValueError:
            return HttpResponse(-1) 
        
        category.likes = category.likes + 1
        category.save()
        
        return HttpResponse(category.likes)

def get_category_list(max_results=0, starts_with=''): 
    category_list = []
    
    if starts_with:
        category_list = Category.objects.filter(name__istartswith=starts_with)
    if max_results > 0:
        if len(category_list) > max_results:
            category_list = category_list[:max_results] 
    return category_list

class CategorySuggestionView(View): 
    def get(self, request):
        if 'suggestion' in request.GET:
            suggestion = request.GET['suggestion']
        else:
            suggestion = ''

        category_list = get_category_list(max_results=8, starts_with=suggestion)
        
        if len(category_list) == 0:
            category_list = Category.objects.order_by('-likes')
        
        return render(request, 'icine/categories.html',{'categories': category_list})
