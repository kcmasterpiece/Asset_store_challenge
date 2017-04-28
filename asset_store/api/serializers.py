from api.models import Assets
from rest_framework import serializers


class AssetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Assets
        fields = ('name', 'asset_type', 'asset_class')

