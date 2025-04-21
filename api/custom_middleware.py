from django.utils.deprecation import MiddlewareMixin
import time

class TimeForReqResCycleMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()
    
    def process_response(self, request, response):
        total_time = time.time() - request.start_time
        print(f"---Request took {total_time:.2f} seconds---")
        return response