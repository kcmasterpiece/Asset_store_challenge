from api.models import Assets
from rest_framework import viewsets
from api.serializers import AssetSerializer


class AssetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows assets to be viewed.
    """
    queryset = Assets.objects.all()
    serializer_class = AssetSerializer

# Create your views here.
