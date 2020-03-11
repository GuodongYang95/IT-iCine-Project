from django.shortcuts import render
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import RequestContext
import datetime
from django.contrib.auth import authenticate,login as auth_login ,logout 
from icine.forms import SignupForm
from django.contrib.auth import get_user_model


posts = [
	{
		'author': 'Gordon',
		'title': 'Wheathering with you',
		'content': 'It is wroth watching in the cinema',
		'date_posted': 'August 27, 2019'
	},
	{
		'author': 'Gordon',
		'title': 'Wheathering with you',
		'content': 'Good',
		'date_posted': 'August 26, 2019'
	}
]

def index(request):
	context = {
		'posts': posts
	}
	return render(request, 'icine/index.html', context)


def about(request):
    return render(request, 'icine/about.html', {'title': 'About'})

# def home(request):
# 	time = datetime.datetime.now()	
	
# 	return render(request,'icine/index.html',locals())

# def about(request):
	
# 	return render(request,'about.html',locals())


def signup(request):
	path=request.get_full_path()
	if request.method=='POST':
		form=SignupForm(data=request.POST,auto_id="%s")
		if form.is_valid():
			UserModel=get_user_model()
			username = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			user=UserModel.objects.create_user(username=username,email=email,password=password)
			user.save()
			auth_user = authenticate(username=username,password=password)
			auth_login(request,auth_user)
			return redirect("index")
	else:
		form=SignupForm(auto_id="%s")
	return render(request,'icine/signup.html',locals())


def logout_view(request):
	logout(request)
	return redirect('index')