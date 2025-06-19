from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import clip_prod


# Create your views here.
class ProductClipper(APIView):
    def post(self, request):
        url = request.data['url']
        clip_json = clip_prod(url)
        return Response(f"{clip_json}", status=status.HTTP_200_OK)