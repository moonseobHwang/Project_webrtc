import math
class CommonPage:
    def __init__(self, totalCont=1, curPage=1, pagesize=10 ):
        self.curPage = curPage
        self.totalCount = totalCont
        self.totalPage = math.ceil(self.totalCount/pagesize) #ceil 특정값보다 더큰 정숙값 4.5 이면 5페이지이다
        self.start_index = (curPage-1) // 10 * 10 +1
        self.end_index = self.start_index + 10

        if self.end_index >= self.totalPage:
            self.end_index = self.totalPage+1

        if curPage > 1:
            self.isPrev = True
            self.previous_page_number=curPage-1
        else:
            self.isPrev = False
            self.previous_page_number=1

        if curPage == self.totalPage:
            self.isNext = False
            self.next_page_number=curPage
        else:
            self.isNext = True
            self.next_page_number=curPage+1

        self.page_range = range(self.start_index, self.end_index)


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

