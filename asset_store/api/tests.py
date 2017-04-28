from django.test import TestCase
from api.models import Assets
import json

# Create your tests here.
class DataModelTest(TestCase):
    def test_can_create_asset(self):
        """Tests that an asset can be created"""
        asset = Assets.objects.create(name="Flexidy", asset_type="satellite", asset_class="dove")
        saved_assets = Assets.objects.all()
        self.assertEqual(saved_assets[0].name, asset.name)

class ApiViewsTest(TestCase):
    def test_api_allows_get_by_name_returns_and_correct_properties(self):
         asset = Assets.objects.create(name="Flexidy", asset_type="satellite", asset_class="dove")
         response = self.client.get('/api/assets/' + asset.name)
         self.assertEquals(json.loads(response.content), 
                {"name": "Flexidy",
                 "asset_type": "satellite",
                 "asset_class": "dove"})
