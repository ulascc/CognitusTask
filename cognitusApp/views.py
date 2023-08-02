from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import DataSerializer
from .models import Data
import requests
from django.http import JsonResponse

class DataView(APIView):

    def get(self,reguest):
        try:
            datas = Data.objects.all()
            serializer = DataSerializer(datas, many=True)

            return Response({
                'data': serializer.data,
                'message': 'Data fetched successfully.'
            }, status=status.HTTP_200_OK)
    
        except Exception as e:
            return Response({
                'data': {},
                'message': 'Something went wrong while fetching data.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
    def post(self,request):
        #import ipdb;ipdb.set_trace()    
        try:
            data = request.data
            serializer = DataSerializer(data=data)
            if not serializer.is_valid():
                return Response({
                    'data' : serializer.errors,
                    'message' : 'something went wrong'
                }, status = status.HTTP_400_BAD_REQUEST)
            
            serializer.save()

            return Response({
                    'data' : serializer.data,
                    'message' : 'data created successfully'
                }, status = status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                    'data' : {},
                    'message' : 'something went wrong'
                }, status = status.HTTP_400_BAD_REQUEST)
        
        
    def patch(self, request):
        data_id = request.data.get('id', None)  
        text = request.data.get('text', None)  
        label = request.data.get('label', None)  

        if data_id is None or (text is None and label is None):
            return Response({"error": "Lütfen güncellenecek verinin id'sini ve en az bir güncellenecek alanı (text veya label) girin."},
                            status=400)

        try:
            data = Data.objects.get(pk=data_id)  

            if text is not None:
                data.text = text  

            if label is not None:
                data.label = label  

            data.save()  

            serializer = DataSerializer(data)  
            return Response(serializer.data, status=200)

        except Data.DoesNotExist:
            return Response({"error": "Belirtilen id'ye sahip veri bulunamadı."}, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request):
        data_id = request.data.get('id', None)  

        if data_id is None:
            return Response({"error": "Lütfen silinecek verinin id'sini girin."}, status=status.HTTP_400_BAD_REQUEST)

        data = get_object_or_404(Data, pk=data_id)  
        data.delete()
        return Response({"message": "Veri başarıyla silindi."}, status=status.HTTP_204_NO_CONTENT)


class TraineView(APIView):
    def get(self, request):

        fastapi_url = 'http://0.0.0.0:8001/fastapi-endpoint'
        response = requests.get(fastapi_url)
        
        response_data = response.json()
        
        return JsonResponse(response_data) 


class PredictView(APIView):
    def post(self, request):
        text_data = request.data.get('text')
        if text_data is None:
            return Response({"error": "Text data not provided"}, status=400)

        
        fastapi_url = "http://0.0.0.0:8001/predict"
        response = requests.get(fastapi_url, params={"text": text_data})

        if response.status_code == 200:
            prediction = response.json().get("prediction")
            return Response({"prediction": prediction}, status=200)
        else:
            return Response({"error": "Error from FastAPI"}, status=500)
            