from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from django.utils import timezone
from django.db import connection
import os

from board.models import Board

# 폼태그 이용해서 테이터 보낼 때 {%csrf_token%}
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
import base64

def front(request):
    return render(request, "frontpage.html")

def index(request):
    return render(request, "index.html")

@csrf_exempt    # csrf_token 에러 제거
def save(request):
    if (request.method == 'POST'):
        drone_id = request.POST.get('drone_id')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        address = request.POST.get('address')

        if address == None or latitude == None or longitude == None:    # 잘못된 데이터 DB insertion 제외
            return HttpResponse("fail")
        else:
            img = request.POST.get('img')
            img = img.replace('data:image/png;base64,', '')
            img = img.replace(' ', '+')
            d = base64.b64decode(img)   # base64 디코딩 작업

            today = datetime.now().strftime('%Y%m%d')
            now = datetime.now().strftime('%H%M%S')
            path = f'upload/{today}/{drone_id}'
            filename = f'{today}{now}.png'

            if not os.path.exists(path):
                os.makedirs(path)

            file = open(os.path.join(path, filename), mode="wb")
            file.write(d)
            file.close()

            cursor =  connection.cursor()

            sql = f"""
                    INSERT INTO board_board (drone, path, filename, datetime, ip, latitude, longitude, address)
                    VALUES ('{drone_id}', '{path}', '{filename}', '{datetime.now()}', '{request.META['REMOTE_ADDR']}', '{latitude}', '{longitude}', '{address}')
                """
            print(sql)
            cursor.execute(sql)


        # 폴더 만들고 /upload/2020/09/14/20200914_1234.png
        # DB 저장할 내용
        # 드론식별값, 이미지 path, 이미지명, 저장된 날짜시간분초, 상대방 IP,
        # GPS 좌표값(클라이언트 좌표값, 브라우저에서 좌표를 알아낼 수 있다.)
        # 주소(클라이언트로부터 받아온)도 저장하는 걸로
        # 리스트, 상세보기 화면-삭제 기능추가
        # optional : 로그인/로그아웃

        # print(img)
        # print(address)
        # print(longitude)
        # print(latitude)
        # print(drone_id)
    return HttpResponse("receive")


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from common.forms import UserForm


def signup(request):
    """
    계정생성
    """
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/board/list')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})