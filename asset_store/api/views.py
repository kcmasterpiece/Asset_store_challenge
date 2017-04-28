from api.models import Assets
from rest_framework import viewsets, mixins
from api.serializers import AssetSerializer


class AssetViewSet(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    """
    API endpoint that allows assets to be viewed.
    """
    queryset = Assets.objects.all().order_by('id')
    serializer_class = AssetSerializer
    lookup_field = 'name'

# Create your views here.
