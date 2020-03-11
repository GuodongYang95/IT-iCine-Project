from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from icine.models import Category,Page
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from icine.bing_search import run_query

class IndexView(View):
    def get(self,request):
        # Query the database for a list of ALL categories currently stored.
        # Order the categories by the number of likes in descending order.
        # Retrieve the top 5 only -- or all if less than 5.
        # Place the list in our context_dict dictionary (with our boldmessage)
        # that will be passed to the template engine.

        category_list = Category.objects.order_by('-likes')[:5]
        # page_list = Page.objects.order_by('-views')[:5]

        context_dict = {}
        # context_dict['pages'] = page_list
        context_dict['categories'] = category_list
        # Return a rendered response to send to the client.
        # We make use of the shortcut function to make our lives easier.
        # Note that the first parameter is the template we wish to use.
        # # Call the helper function to handle the cookies
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


# def about(request):
#     return render(request, 'icine/about.html', {'title': 'About'})
class ShowCategoryView(View):
    def show_category(self, category_name_slug):
        context_dict = {}

        try:
            category = Category.objects.get(slug=category_name_slug)
            pages = Page.objects.filter(category=category).order_by('-views')

            context_dict['pages'] = pages
            context_dict['category'] = category

        except Category.DoesNotExist:
            context_dict['category'] = None
            context_dict['pages'] = None

    def get(self,request,category_name_slug):
        context_dict = self.create_context_dict(category_name_slug)
        return render(request, 'icine/category.html', context_dict)
        # Start new search functionality code.
    
    @method_decorator(login_required)
    def POST(self,request,category_name_slug):  
        context_dict = self.create_context_dict(category_name_slug)
        query = request.POST['query'].strip()

        if query:
            context_dict['result_list'] = run_query(query)
            context_dict['query'] = query
        # End new search functionality code.
        return render(request, 'icine/category.html', context_dict)

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
