import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import clip_prod

class ProductClipper(APIView):
    def post(self, request):
        # Try normal JSON body first
        url = request.data.get('url')
        
        # If url not found, try parsing from _content (form wrapped JSON)
        if not url and '_content' in request.data:
            try:
                content_list = request.data.getlist('_content')
                if content_list:
                    json_str = content_list[0]
                    data = json.loads(json_str)
                    url = data.get('url')
            except Exception as e:
                return Response({"error": "Invalid JSON in _content"}, status=status.HTTP_400_BAD_REQUEST)

        if not url:
            return Response({"error": "URL not provided"}, status=status.HTTP_400_BAD_REQUEST)

        clip_json = clip_prod(url)
        return Response(clip_json, status=status.HTTP_200_OK)
