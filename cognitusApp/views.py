from datetime import timezone
import time
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import DataSerializer, TrainingLogSerializer
from .models import Data, TrainingLog
import requests
from django.http import JsonResponse
from django.utils import timezone

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
        fastapi_url = 'http://0.0.0.0:8001/traine/'
        try:
            response = requests.get(fastapi_url)
            response_data = response.json()
            task_id = response_data.get('task_id')

            # Bekleme süresi
            wait_time = 0.01

            # Bekleme süresi boyunca uyumak
            time.sleep(wait_time)

            # FastAPI'den sonuç al
            fastapi_result_url = f'http://0.0.0.0:8001/traine_result/{task_id}/'
            try:
                response = requests.get(fastapi_result_url)
                result_data = response.json()
                message = result_data.get('message')
                if message == "Model trained and saved.":
                    status = 'completed'
                    end_time = timezone.now()
                elif message == "Task is still pending. Check back later.":
                    status = 'running'
                    end_time = None
                else:
                    status = 'error'
                    end_time = None
            except Exception as e:
                status = 'error'
                end_time = None

            # Yeni bir TrainingLog kaydı oluştur ve veritabanına kaydet
            log = TrainingLog.objects.create(status=status, end_time=end_time)

            # TrainingLog nesnesini serialize et
            serialized_data = {
                'task_id': task_id,
                'start_time': log.start_time,
                'end_time': log.end_time,
                'status': log.status,
            }
            
            return Response(serialized_data)
        except Exception as e:
            return Response({'error': str(e)}, status=500)



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
            