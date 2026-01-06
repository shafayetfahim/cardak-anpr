import uuid
from django.db import models


class VehicleAsset(models.Model):
    # We use a UUID so we can link this to SentinelQueue without guessing IDs
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # The raw photography asset
    image = models.ImageField(upload_to='uploads/%Y/%m/%d/')

    # Data extracted by OCR
    license_plate = models.CharField(max_length=20, blank=True, null=True)

    # Data fetched from the Crawler/API
    vin = models.CharField(max_length=17, blank=True, null=True)
    make = models.CharField(max_length=50, blank=True, null=True)
    model = models.CharField(max_length=50, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)

    # Status tracking (The "Sentinel" way)
    STATUS_CHOICES = [
        ('PENDING', 'Pending OCR'),
        ('PROCESSING', 'Crawling Specs'),
        ('COMPLETED', 'Success'),
        ('FAILED', 'Failed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.year} {self.make} {self.model} ({self.license_plate})"