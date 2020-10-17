from django.conf import settings
from django.shortcuts import redirect, reverse

class LoginRequiredMiddleware:

	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		response = self.get_response(request)
		return response

	def process_view(self, request, view_func, *arg, **kwarg):

		current_path = request.path_info

		is_exempt_url = any([current_path == reverse(path) for path in settings.LOGIN_EXEMPT_URLS])

		if not request.user.is_authenticated and not is_exempt_url:
			return redirect(''.join([reverse(settings.LOGIN_URL), '?next=', current_path])) 
		else:
			return None