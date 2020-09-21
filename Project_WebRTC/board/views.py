from django.shortcuts import render
from django.http import HttpResponse
from .models import Board
from django.utils import timezone
from django.shortcuts import redirect
from django.db import connection
from common.CommonPage import CommonPage, dictfetchall
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json

def index(request):
    return render(request, "index.html")

@login_required(login_url='common:login')
def list(request):
    #페이징에 필요한 정보들
    #나타낼 블록
    cursor = connection.cursor()

    page = int(request.GET.get('page', '1'))  # 페이지
    num = 10
    print("views.list:",page)
    #전체 레코드 개수 구하기
    sql ="select count(*) from board_board"
    cursor.execute(sql)
    totalCount= int(cursor.fetchone()[0])

    commonPage = CommonPage(totalCount, page)
    start = (page-1)*10

    sql = """
            SELECT id, drone, path, filename, ip, date_format(datetime, '%Y-%m-%d %T') as datetime
            FROM board_board
            ORDER BY id DESC
            LIMIT {}, 10
        """.format(start)

    print(sql)

    cursor.execute(sql)
    boards_obj = dictfetchall(cursor)

    context = {'board_list':boards_obj, "commonPage":commonPage, "page":page}

    return render(request, "board/board_list.html", context)


@login_required(login_url='common:login')
def view(request, id, page):

    #page = int(request.GET.get('page', '1'))    # 페이지 유지를 위한 page 값 가져오기
    print("views.view:",page)
    cursor = connection.cursor()

    sql = '''
            SELECT * FROM board_board WHERE id={}
        '''.format(id)

    print(sql)

    cursor.execute(sql)
    boards_obj = dictfetchall(cursor)

    return render(request, "board/board_view.html", {'board':boards_obj[0], 'page':page})

@csrf_exempt
@login_required(login_url='common:login')
def delete(request, id=0):

    cursor = connection.cursor()

    if (request.method == 'POST'):

        data = request.POST.get('myJSON')
        ids = json.loads(data)
        print(ids)
        q = ', '.join(ids)
        print(q)
        sql = '''
                DELETE FROM board_board WHERE id IN ({})
            '''.format(q)

        print(sql)
    else:
        sql = '''
                DELETE FROM board_board WHERE id={}
            '''.format(id)
        print(sql)

    cursor.execute(sql)

    return redirect('board:list')


@login_required(login_url='common:login')
def search(request):
    key = request.GET.get('key', '')
    sel = int(request.GET.get('sel', '1'))
    page = int(request.GET.get('page', '1'))
    print(key)
    print(sel)

    cursor = connection.cursor()
    num = 10

    key = '%' + key + '%'
    print(key)

    # 1. 전체
    # 2. 주소
    # 3. 날짜
    # 4. IP
    # 5. Drone ID
    if sel == 1:
        sql = f"""
            SELECT COUNT(*) FROM board_board
            WHERE drone like '{key}' or filename like '{key}' or
            datetime like '{key}' or ip like '{key}' or
            latitude like '{key}' or longitude like '{key}' or
            address like '{key}'
            """
        print(sql)

        cursor.execute(sql)
        totalCount= int(cursor.fetchone()[0])

        commonPage = CommonPage(totalCount, page)
        start = (page-1)*10

        sql = f"""
            SELECT * FROM board_board
            WHERE drone like '{key}' or filename like '{key}' or
            datetime like '{key}' or ip like '{key}' or
            latitude like '{key}' or longitude like '{key}' or
            address like '{key}'
            """
    elif sel == 2:
        sql = f"""
            SELECT COUNT(*) FROM board_board WHERE address like '{key}'
            """
        print(sql)

        cursor.execute(sql)
        totalCount= int(cursor.fetchone()[0])

        commonPage = CommonPage(totalCount, page)
        start = (page-1)*10

        sql = f"""
            SELECT * FROM board_board WHERE address like '{key}'
            """

    elif sel == 3:
        sql = f"""
            SELECT count(*) FROM board_board WHERE datetime like '{key}'
            """
        print(sql)

        cursor.execute(sql)
        totalCount= int(cursor.fetchone()[0])

        commonPage = CommonPage(totalCount, page)
        start = (page-1)*10

        sql = f"""
            SELECT * FROM board_board WHERE datetime like '{key}'
            """
    elif sel == 4:
        sql = f"""
            SELECT COUNT(*) FROM board_board WHERE ip like '{key}'
            """
        print(sql)

        cursor.execute(sql)
        totalCount= int(cursor.fetchone()[0])

        commonPage = CommonPage(totalCount, page)
        start = (page-1)*10

        sql = f"""
            SELECT * FROM board_board WHERE ip like '{key}'
            """
    elif sel == 5:
        sql = f"""
            SELECT COUNT(*) FROM board_board WHERE drone like '{key}'
            """
        print(sql)

        cursor.execute(sql)
        totalCount= int(cursor.fetchone()[0])

        commonPage = CommonPage(totalCount, page)
        start = (page-1)*10

        sql = f"""
            SELECT * FROM board_board WHERE drone like '{key}'
            """

    cursor.execute(sql)
    boards_obj = dictfetchall(cursor)

    context = {'board_list':boards_obj, "commonPage":commonPage, "page":page, 'key':key, 'sel':sel}

    return render(request, "board/board_list.html", context)




# @login_required(login_url='common:login')
# def search(request):
#     #페이징에 필요한 정보들
#     #나타낼 블록
#     cursor = connection.cursor()

#     page = int(request.GET.get('page', '1'))  # 페이지
#     num = 10

#     sel = int(request.GET.get('sel', '1'))  # 검색 항목 Field

#     # 검색어 얻기
#     strSearch = request.GET.get('key', 'None')  # 검색어

#     # 검색필드 얻기
#     if sel == 1: # 전체
#         strField = "drone"
#     elif sel == 2: # 드론 id
#         strField = "drone"
#     elif sel == 3: # 날짜
#         strField = "drone"
#     elif sel == 4: # 주소
#         strField = "drone"
#     else:
#         strField = "drone"

#     print( "sel : ", sel )

#     #전체 레코드 개수 구하기

#     sql = r"select count(*) from board_board where {} like '%{}%'" .format(strField, strSearch)
#     print( sql )

#     cursor.execute(sql)
#     totalCount= int(cursor.fetchone()[0])

#     commonPage = CommonPage(totalCount, page)
#     start = (page-1)*10

#     sql = """
# SELECT id, drone, path, filename, date_format(datetime, '%Y-%m-%d %T') as datetime, address
#             FROM board_board
#             WHERE {} like '%{}%'
#             ORDER BY id DESC
#             LIMIT {}, 10
#         """.format(strField, strSearch, start)

#     print(sql)

#     cursor.execute(sql)
#     boards_obj = dictfetchall(cursor)

#     context = {'board_list':boards_obj, "commonPage":commonPage, "page":page}

#     return render(request, "board/board_list.html", context)