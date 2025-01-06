from django.http import JsonResponse
from oscar.apps.catalogue.views import *  # noqa
from oscar.core.loading import get_model

AttributeOption = get_model('catalogue', 'AttributeOption')

def get_attribute_price(request):
    if request.method == 'GET':
        option_id = request.GET.get('option_id')
        try:
            option = AttributeOption.objects.get(id=option_id)
            return JsonResponse({
                'status': 'success',
                'price': float(option.price or 0)
            })
        except AttributeOption.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Option not found'
            })
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})
