from django.db import models

# Create your models here.
class Assets(models.Model):
    name = models.CharField(max_length=64, db_index=True, unique=True, null=False)
    asset_type = models.CharField(max_length=20, null=False)
    asset_class = models.CharField(max_length=20, null=False)

class AssetTypeClassRestrictions(models.Model):
    asset_type = models.CharField(max_length=20, null=False)
    asset_class = models.CharField(max_length=20, null=False)
