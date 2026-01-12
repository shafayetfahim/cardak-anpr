from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .forms import VehicleUploadForm
from .models import VehicleAsset
from sentinel_client.producer import SentinelProducer

@csrf_exempt
def upload_vehicle(request):
    if request.method == 'POST':
        form = VehicleUploadForm(request.POST, request.FILES)
        if form.is_valid():
            asset = form.save()
            try:
                producer = SentinelProducer(host='localhost')
                producer.enqueue_job(asset.id, asset.image.path)
                return JsonResponse({
                    "status": "success",
                    "asset_id": asset.id,
                    "message": "Task enqueued"
                }, status=201)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)
        return JsonResponse({"error": form.errors}, status=400)
    
    return JsonResponse({"error": "Only POST requests allowed"}, status=405)