from api.models import Assets
from rest_framework import serializers


class AssetSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='assets-detail',
        lookup_field='name'
    )
    class Meta:
        model = Assets
        fields = ('id', 'name', 'asset_type', 'asset_class', 'url')

