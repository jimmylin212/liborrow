from django.shortcuts import render_to_response, redirect
from mainsite.modules.cronjob_related import CronJobRelated

def home(request):
	return render_to_response('home.html')

def rss_update(request, school_name):
	cronjob_related = CronJobRelated()
	cronjob_related.rss_update(school_name)

	return render_to_response('dummy_cronjob_page.html')
