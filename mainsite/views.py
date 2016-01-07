from django.template.context_processors import csrf
from django.shortcuts import render_to_response, redirect
from mainsite.modules.cronjob_related import CronJobRelated
from mainsite.modules.book_related import BookRelated

def home(request):
	passed_dict = {}
	passed_dict.update(csrf(request))
	book_related = BookRelated()

	if request.method == 'POST' and request.POST.get('form_action') == 'trace':
		trace_book_info = request.POST.get('trace_book_info')
		if trace_book_info[0].isalpha():
			isbn = book_related.add_new_book_by_record(trace_book_info)
		elif trace_book_info.isdigit():
			isbn = input_value

		book_related.add_trace_book(isbn)
		
	elif request.method == 'POST' and request.POST.get('form_action') == 'update':
		book_related.update_book_status()

	trace_books = book_related.get_trace_books()
	passed_dict['trace_books'] = trace_books
	return render_to_response('home.html', passed_dict)

def remove(request, isbn):
	book_related = BookRelated()
	book_related.remove_trace_book(isbn)
	return redirect('/')

def rss_update(request, school_name):
	cronjob_related = CronJobRelated()
	cronjob_related.rss_update(school_name)

	return render_to_response('dummy_cronjob_page.html')
