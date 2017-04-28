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
    def setUp(self): 
        self.test_data = {"name": "Flexidy",
                "asset_type": "satellite",
                "asset_class": "dove"}
        self.asset = Assets.objects.create(name=self.test_data["name"],
                asset_type=self.test_data["asset_type"], 
                asset_class=self.test_data["asset_class"])

    def test_api_allows_get_by_name_returns_and_correct_properties(self):
        response = self.client.get('/api/assets/' + self.test_data["name"] + '/')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.content)['name'],
                self.test_data['name'] )
        self.assertEquals(json.loads(response.content)['asset_type'],
                self.test_data['asset_type'] )
        self.assertEquals(json.loads(response.content)['asset_class'],
                self.test_data['asset_class'] )

    def test_api_prevents_deletion_of_assets(self):
        
        delete_response = self.client.delete('/api/assets/' + self.test_data["name"] + '/')
        get_response = self.client.get('/api/assets/' + self.test_data["name"] + '/')
        self.assertEquals(delete_response.status_code, 405)
        self.assertEquals(get_response.status_code, 200)
        self.assertEquals(json.loads(get_response.content)['name'],
                self.test_data['name'] )
        self.assertEquals(json.loads(get_response.content)['asset_type'],
                self.test_data['asset_type'] )
        self.assertEquals(json.loads(get_response.content)['asset_class'],
                self.test_data['asset_class'] )
