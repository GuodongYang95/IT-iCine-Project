from django.shortcuts import render



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
