from django.test import TestCase
from api.models import Assets, AssetTypeClassRestrictions
import json

# Create your tests here.
class DataModelTest(TestCase):
    def test_can_create_asset(self):
        """Tests that an asset can be created"""
        asset = Assets.objects.create(name="Flexidy", asset_type="satellite", asset_class="dove")
        saved_assets = Assets.objects.all()
        self.assertEqual(saved_assets[0].name, asset.name)
    
    def test_asset_types_limited_to_available_types(self):
        asset = Assets.objects.create(name="Flexidy", asset_type="rock", asset_class="dove")
        


class ApiViewsTest(TestCase):
    def setUp(self): 
        self.test_data = {"name": "Flexidy",
                "asset_type": "satellite",
                "asset_class": "dove"}
        self.asset = Assets.objects.create(name=self.test_data["name"],
                asset_type=self.test_data["asset_type"], 
                asset_class=self.test_data["asset_class"])

    def test_api_lists_all_assets(self):
        response = self.client.get('/api/assets/')
        self.assertEquals(len(json.loads(response.content)['results']), 1)
         
    def test_api_allows_get_by_name_and_returns_correct_properties(self):
        response = self.client.get('/api/assets/' + self.test_data["name"] + '/')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.content)['name'],
                self.test_data['name'] )
        self.assertEquals(json.loads(response.content)['asset_type'],
                self.test_data['asset_type'] )
        self.assertEquals(json.loads(response.content)['asset_class'],
                self.test_data['asset_class'] )

    def test_api_allows_creation_of_assets(self):
        new_asset = {"name": "Roxana",
                "asset_type": "satellite",
                "asset_class": "dove"}
        post_response = self.client.post('/api/assets/',new_asset)
        self.assertEquals(post_response.status_code, 201)

    def test_api_requires_name_class_type_on_create(self):
        new_asset = {"name": "Roxana",
                "asset_class": "dove"}
        post_response = self.client.post('/api/assets/',new_asset)
        self.assertEquals(post_response.status_code, 400)

        new_asset = {"name": "Roxana",
                "asset_type":"satellite"}
        post_response = self.client.post('/api/assets/',new_asset)
        self.assertEquals(post_response.status_code, 400)
        
        new_asset = {"asset_class": "dove",
                "asset_type":"satellite"}
        post_response = self.client.post('/api/assets/',new_asset)
        self.assertEquals(post_response.status_code, 400)
        
    def test_api_enforces_asset_name_uniqueness(self):
        existing_asset = Assets.objects.all()[0]
        new_asset =  {"name": existing_asset.name,
                "asset_type": existing_asset.asset_type,
                "asset_class": existing_asset.asset_class}
        post_response = self.client.post('/api/assets/',new_asset)
        self.assertEquals(post_response.status_code, 400)

    def test_api_prevents_names_shorter_than_allowed(self):
        new_asset =  {"name": "aaa",
                "asset_type": "satellite",
                "asset_class": "dove"}
        post_response = self.client.post('/api/assets/',new_asset)
        self.assertEquals(post_response.status_code, 400)

    
    def test_api_prevents_names_longer_than_allowed(self):
        new_asset =  {"name": "a"*65,
                "asset_type": "satellite",
                "asset_class": "dove"}
        post_response = self.client.post('/api/assets/',new_asset)
        self.assertEquals(post_response.status_code, 400)

    def test_api_prevents_disallowed_characters_in_name(self):
        disallowed_chars = '!"#$%&\'()*+,./:;<=>?@[\]^`{|}~'
        for c in disallowed_chars:
            new_asset = {"name": "Roxana"+c,
                    "asset_type": "satellite",
                    "asset_class": "dove"}
            post_response = self.client.post('/api/assets/',new_asset)
            self.assertEquals(post_response.status_code, 400)

    def test_api_prevents_names_beginning_with_dash_or_underscore(self):
        chars = '-_'
        for c in chars:
            new_asset = {"name": c+"Roxana",
                    "asset_type": "satellite",
                    "asset_class": "dove"}
            post_response = self.client.post('/api/assets/',new_asset)
            self.assertEquals(post_response.status_code, 400)

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


    def test_api_limits_asset_types_to_available_types(self):
        asset_types = [a['asset_type'] for a in AssetTypeClassRestrictions.objects.values('asset_type').distinct()]
        for t in asset_types:
            classes = [a['asset_class'] for a in AssetTypeClassRestrictions.objects.values('asset_class').filter(asset_type=t)]
            for c in classes:
                new_asset = {"name": "Roxana_"+t+c,
                    "asset_type": t,
                    "asset_class": c}
                post_response = self.client.post('/api/assets/',new_asset)
                self.assertEquals(post_response.status_code, 201)
                
                fail_asset = {"name": "Roxana_"+t+c+'fail',
                    "asset_type": t+'fail',
                    "asset_class": c}
                post_response = self.client.post('/api/assets/', fail_asset)
                self.assertEquals(post_response.status_code, 400)

    def test_api_limits_asset_class_to_available_classes_for_type(self):
        asset_types = [a['asset_type'] for a in AssetTypeClassRestrictions.objects.values('asset_type').distinct()]
        for t in asset_types:
            classes = [a['asset_class'] for a in AssetTypeClassRestrictions.objects.values('asset_class').filter(asset_type=t)]
            for c in classes:
                new_asset = {"name": "Roxana_"+t+c,
                    "asset_type": t,
                    "asset_class": c}
                post_response = self.client.post('/api/assets/',new_asset)
                self.assertEquals(post_response.status_code, 201)
                
                fail_asset = {"name": "Roxana_"+t+c+'fail',
                    "asset_type": t,
                    "asset_class": c+'fail'}
                post_response = self.client.post('/api/assets/', fail_asset)
                self.assertEquals(post_response.status_code, 400)


