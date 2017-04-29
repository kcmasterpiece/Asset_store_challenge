from api.models import Assets, AssetTypeClassRestrictions
from rest_framework import serializers
import re

class AssetSerializer(serializers.HyperlinkedModelSerializer):

    def validate_name(self, value):
        valid_chars = re.compile('^[a-zA-Z0-9][a-zA-Z0-9\-_]{3,63}$')
        if valid_chars.match(value) is None:
            raise serializers.ValidationError('This field may only contain alphanumeric characters, dashes, and underscores. It may not start with dashes or underscores and must be between 4 and 64 characters long')
        return value
    
    def validate_asset_type(self, value):
        a_ts = [a['asset_type'] for a in AssetTypeClassRestrictions.objects.values('asset_type').distinct()]
        if value not in a_ts:
            raise serializers.ValidationError('asset_type must be one of the following: {vals}'.format(vals=a_ts))
        return value

    def validate(self, data):
        a_ts = {}
        for a in AssetTypeClassRestrictions.objects.values('asset_type','asset_class').distinct():
            if a['asset_type'] not in a_ts:
                a_ts[a['asset_type']]=[a['asset_class']]
            else: 
                a_ts[a['asset_type']].append(a['asset_class'])
        if data['asset_class'] not in a_ts[data['asset_type']]:
            raise serializers.ValidationError('asset_type {type} only allows the following asset_classes: {vals}'.format(
                vals=a_ts[data['asset_type']],type=[data['asset_type']]))
        return data 

    def create(self, validated_data):
        return Assets.objects.create(**validated_data)

    url = serializers.HyperlinkedIdentityField(
        view_name='assets-detail',
        lookup_field='name'
    )
    class Meta:
        model = Assets
        fields = ('id', 'name', 'asset_type', 'asset_class', 'url')



