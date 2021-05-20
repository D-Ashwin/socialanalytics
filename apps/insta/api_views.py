from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.insta.helpers import update_insta_analytics
from apps.insta.models import InstaStalkUsers
from apps.insta.serializers import InstaStalkUsersSerializer


class DemoApiView(APIView):
    def get(self, request):
        data = {"message": "hello world"}
        return Response(data, status=status.HTTP_200_OK)


class UpdateInsta(APIView):
    def get(self, request):
        update_insta_analytics()
        data = {"message": "hello world"}
        return Response(data, status=status.HTTP_200_OK)


class StalkInstaView(APIView):
    def post(self, request):
        try:
            username = request.data.get('username', None)
            import requests
            import cloudscraper
            from bs4 import BeautifulSoup
            data = {"username":username}

            endpoint = "https://izoomyou.com/en/user/"+username
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}

            scraper = cloudscraper.create_scraper()

            source_data = scraper.get(endpoint).text
            soup = BeautifulSoup(source_data, "html.parser")
            data = soup.find_all('div', class_='profilpicture')
            import time
            print(1)
            time.sleep(5)
            print(3)
            import pdb
            pdb.set_trace()
            # a_class = data[0].find_all('img')
            # print(a_class)
            # url_ = a_class[0].get('href')
            return Response({"image_url": url_}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status':500, 'message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StalkInstaUserListView(APIView):
    serializer_class = InstaStalkUsersSerializer

    def get(self, request):
        stu = InstaStalkUsers.objects.all()
        serializer = self.serializer_class(stu, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)