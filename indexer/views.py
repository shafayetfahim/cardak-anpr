import os
from django.shortcuts import render
from .forms import VehicleUploadForm
from .models import VehicleAsset
from sentinel_client.producer import SentinelProducer

def upload_vehicle(request):
    """
    Ingests vehicle images and enqueues tasks for processing.
    """
    success = False
    asset = None

    if request.method == 'POST':
        form = VehicleUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # 1. Save to PostgreSQL
            asset = form.save()

            # 2. Connection Handshake
            try:
                # We connect here so a temporary Redis delay doesn't kill the app
                producer = SentinelProducer(host='redis')
                producer.enqueue_job(asset.id, asset.image.path)
                success = True
            except Exception as e:
                print(f"Queueing Error: {e}")
                # The asset is still in the DB, even if the queue fails

            return render(request, 'indexer/upload.html', {
                'form': VehicleUploadForm(), # Clear the form
                'success': success,
                'asset': asset
            })
    else:
        form = VehicleUploadForm()

    return render(request, 'indexer/upload.html', {'form': form})