from django.test import TestCase
from api.models import Assets

# Create your tests here.
class DataModelTest(TestCase):
    def test_can_create_asset(self):
        """Tests that an asset can be created"""
        asset = Assets.objects.create(name="Flexidy", asset_type="satellite", asset_class="dove")
        saved_assets = Assets.objects.all()
        self.assertEqual(saved_assets[0].name, asset.name)

