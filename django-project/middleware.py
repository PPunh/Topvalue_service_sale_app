from django.http import HttpResponse
from django_ratelimit.exceptions import Ratelimited

class CustomRateLimitMeaage:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        if isinstance(exception, Ratelimited):
            return HttpResponse("<h3>You've exceeded the rate limit at 100 requests per minute, \
                                please try again later.</h3>", status=429)
        return None
