from django.http import JsonResponse

def status_view(request):
    return JsonResponse({'status': 'ok'}, status=200)
