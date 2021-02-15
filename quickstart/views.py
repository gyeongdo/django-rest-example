import pandas as pd
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import *
from django.db.models import F, Func
from quickstart.exceldownload import ExcelRenderer
from quickstart.models import *
from rest_framework.response import Response


class OrderView(generics.ListCreateAPIView):
    """
    Order조회
    ---
    raw 쿼리 조회 시
    """
    serializer_class = OrderSerializer

    def get_queryset(self):
        return

    def get(self, request, pk):
        # orders = Order.objects.raw("select * "
        #                            "from quickstart_order a  "
        #                            "WHERE id = %s", str(pk))

        orders = Order.objects.raw("select "
                                   "distinct a.id "
                                   ",a.group_id "
                                   ",a.group_nm "
                                   ",a.data_id "
                                   ",a.data_nm "
                                   ",a.standard_date "
                                   "from tblist_stdr a, ( "
                                   "select ( "
                                   "select "
                                   "id "
                                   "from tblist_stdr "
                                   "where data_id = a.data_id "
                                   "and group_id = a.group_id "
                                   "order by standard_date desc , reg_date desc "
                                   "limit 1 "
                                   ") id from tblist_stdr a "
                                   ")b where a.id = b.id ")

        serializer = self.get_serializer(orders, many=True).data
        return Response(serializer)


class DogColumn(generics.ListCreateAPIView):
    """
    Dog조회
    ---
    Dog 컬럼만 조회
    """

    serializer_class = DogColumnSerializer

    def get_queryset(self):
        queryset = Dog.objects.all()
        return queryset

    def get(self, request):
        queryset = Dog.objects.filter(data__0__has_keys=['주소'])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class OrderDynamicView(APIView):
    def get(self, request, pk):
        orders = Order.objects.raw("select * from ("
                                   "select a.id"
                                   "     , jsonb_object_keys(a.data -> 'table') as metadata_keys "
                                   "from quickstart_order a  "
                                   ") a WHERE a.id = %s", str(pk))

        serializer = OrderSerializer(orders, many=True).data
        return Response(serializer)


class JsonKeys(Func):
    function = 'jsonb_object_keys'


class OrderViews(APIView):
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True).data
        return Response(serializer)


class OrderCustomViews(APIView):
    def get(self, request):
        # 컬럼 검색어
        columnParams = request.query_params.get("data", None)

        if columnParams is not None:
            columnParams = columnParams.split(',')

        print(columnParams)  # phonenumber

        # value값으로 가져오기
        # orders = Order.objects.filter(data__tablename=columnParams)

        # 전체 가져오기
        # orders = Order.objects.annotate(metadata_keys=JsonKeys("data")).distinct("id")

        # ㅇㅇ 모든 값을 알 때
        # orders = Order.objects.filter(data__table__contained_by={"qty": 6, "product": "Beer"})

        # https://docs.djangoproject.com/en/3.0/ref/contrib/postgres/fields/
        # has_key 테이블안에 json에서 키 값으로 결과 찾고 && 테이블의 컬럼으로 필터
        # orders = Order.objects.filter(data__table__has_any_keys=columnParams)
        # orders = orders.filter(data__tablename='covid product')

        # 필터 추가 1
        # orders = orders.filter(id="8")

        # 필터 추가 2
        # orders = Order.objects.filter(data__table__values__contains='Samsung hospital')

        # 테이블안의 테이블에서 value값으로 찾기 ???
        # orders = Order.objects.filter(data__table__values__contains='Samsung hospital')

        # keys
        filterKey = 'data__breed'
        filterValue = 'collie'
        orders = Order.objects.filter(data__breed='collie')

        serializer = OrderSerializer(orders, many=True).data
        return Response(serializer)

        # orders = Order.objects.all()
        # serializer = OrderSerializer(orders, many=True).data


class ExcelViews(APIView):
    def get(self, request):
        read_file = pd.read_csv(
            '/quickstart/file/hospital.csv',
            sep=',', encoding='euc-kr')
        read_file.to_excel(
            'C:/Users/openmateon/Downloads/dev-example/djangoRestApi/postgresql-example/quickstart/file/sample4.xlsx',
            index=None, header=True)


class DogViews(APIView):
    def get(self, request):
        dogs = Dog.objects.filter(data__0__has_keys=['size'])

        # orders = Order.objects.filter(data__table__has_any_keys=columnParams)

        serializer = DogSerializer(dogs, many=True).data
        return Response(serializer)


class BlogViews(APIView):
    def get(self, request):
        blogs = Blog.objects.all()

        # orders = Order.objects.filter(data__table__has_any_keys=columnParams)

        serializer = BlogSerializer(blogs, many=True).data
        return Response(serializer)


class DogExcelViews(APIView):
    renderer_classes = [ExcelRenderer]

    def get(self, request):
        dogs = Dog.objects.filter(data__0__has_keys=['address'])
        serializer = DogSerializer(dogs, many=True).data

        header_list = []
        rows_list = []

        for key in dogs.values('data')[0].values():
            header_list = list(key[0].keys())

        for item in dogs.values('data'):
            rows_list = item['data']

        data = {
            'header': header_list,
            'rows': rows_list
        }

        headers = {}
        headers['Content-Disposition'] = 'attachment; filename=excel.xlsx'
        return Response(data=data, headers=headers)


import csv
from django.http import HttpResponse, HttpResponseRedirect


def export_users_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'

    writer = csv.writer(response)
    writer.writerow(['Username', 'First name', 'Last name', 'Email address'])

    # dogs = Dog.objects.all().values_list('username', 'first_name', 'last_name', 'email')
    dogs = [{'Username', 'First name', 'Last name', 'Email address'},
            {'Username1', 'First name1', 'Last name1', 'Email address1'}]
    for user in dogs:
        writer.writerow(user)

    return response


import xlwt


def export_users_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Username', 'First name', 'Last name', 'Email address', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    # rows = User.objects.all().values_list('username', 'first_name', 'last_name', 'email')
    rows = [{'Username', 'First name', 'Last name', 'Email address'},
            {'Username', 'First name', 'Last name', 'Email address'},
            {'Username', 'First name', 'Last name', 'Email address'}]

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


from django.http import HttpResponse, JsonResponse
import json


class ConvertCsvJson(APIView):
    def get(self, request):
        with open('quickstart/file/sevenHundred.csv') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        with open('quickstart/file/test.json', 'w') as f:
            json.dump(rows, f)

        with open('quickstart/file/test.json') as f:
            json_result = json.load(f)

        data = json_result
        result = {
            'name': 'asd',
            'data': data,
            'content': 'zxc'
        }

        serializer = DogSerializer(data=result)
        if serializer.is_valid():
            serializer.save()
        else:
            print('not valid')

        return JsonResponse(json_result[:5], json_dumps_params={'ensure_ascii': True}, safe=False)


class DogSelct(APIView):

    def get(self, request):

        ket_foo = "병상수"
        key_str = '"' + ket_foo + '"'
        value_str = "'499'"

        limit_str = str(5)
        # (off + 1) ~ limit + off
        offset_str = str(0)

        queryset = Dog2.objects.raw(
            "with t_unnested as ("
            "    select id, "
            "           jsonb_array_elements(data) as data"
            "      from dog_json"
            "      where id = '1'"
            "      limit " + limit_str + " offset " + offset_str + ""
            ")"
            "select id"
            "	 , (select count(*) from"
            "		 	(select jsonb_array_elements(data)"
            "		 	  from dog_json "
            "		 	 where id = 1"
            "	 	     ) name1"
            " 	    ) as name "
            "	 , jsonb_agg (data) as data "
            "  from t_unnested "
            " where id = '1'"
            " group by id, name"
        )

        serializer = DogSerializer(queryset, many=True)
        return Response(serializer.data)

'''
        queryset = Dog2.objects.raw(
                "with t_unnested as ( "
                "    select id, "
                "           jsonb_array_elements(data) as data "
                "      from dog_json "
                "      where id = '1' "
                "      limit 5 offset 5 "
                "     "
                ")"
                "select id, jsonb_agg (data) as data "
                "  from t_unnested "
                "where id = '1' "
                "group by id "
        )
        
                        
        queryset = Dog2.objects.raw(
            "select id, a as data "
            "from ( "
            "    select jsonb_array_elements(data) a "
            "          ,id "
            "      from dog_json "
            "     where id = 1 "
            ") t "
            "where t.a->> " + key_str + " = " + value_str
        )
'''

from rest_framework.parsers import MultiPartParser, FormParser
from quickstart import file_upload_path
import os
from quickstart.utils import is_image
from django.http.request import QueryDict
from rest_framework import status


class FileView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, req, *args, **kwargs):

        # 요청된 데이터를 꺼냄( QueryDict)
        new_data = req.data.dict()

        # 요청된 파일 객체
        file_name = req.data['file_name']

        # 저장될 파일의 풀path를 생성
        print('file_name.name : ', file_name.name)
        new_file_full_name = file_upload_path(file_name.name)
        print('new_file_full_name : ', new_file_full_name)
        # 새롭게 생성된 파일의 경로
        file_path = '\\'.join(new_file_full_name.split('\\')[0:-1])

        # 파일 확장자
        file_ext = os.path.splitext(file_name.name)[1]

        # QueryDict에 새로운 데이터 추가( DB와 매핑을 위해서)
        new_data['file_ext'] = file_ext
        new_data['is_img'] = is_image(file_ext)
        new_data['file_path'] = file_path
        new_data['file_origin_name'] = req.data['file_name'].name
        new_data['file_save_name'] = req.data['file_name']

        print(new_data)

        new_query_dict = QueryDict('', mutable=True)
        new_query_dict.update(new_data)

        file_serializer = FileSerializer(data=new_query_dict)
        if file_serializer.is_valid():

            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            file_serializer.save()
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!2")

            print(file_serializer.data)

            return Response(status=status.HTTP_201_CREATED)
        else:

            print(__name__, file_serializer.errors)
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from wsgiref.util import FileWrapper


class FileDownloadView(generics.ListAPIView):

    def get(self, request, id, format=None):
        try:
            queryset = FileEntry.objects.get(id=id)
            file_handle = queryset.upload.path
            document = open(file_handle, 'rb')
            response = HttpResponse(FileWrapper(document), content_type='application/msword')
            response['Content-Disposition'] = 'attachment; filename="%s"' % queryset.upload.name
            return response
        except FileEntry.DoesNotExist as ex:
            print(ex)
            pass

        return Response(status.HTTP_404_NOT_FOUND)


# 시퀄라이저로 컬럼을 추가하는 방법 1
class BoardView(APIView):
    def get(self, request):
        baords = Board.objects.all()
        serializer = BoardJoinSerializer(baords, many=True).data
        return Response(serializer)


# 시퀄라이저로 컬럼을 추가하는 방법 1
class StudentView(generics.ListCreateAPIView):
    serializer_class = StudentSerializer

    def get_queryset(self):
        return

    def get(self, request):
        students = Student.objects.all()
        students = students.values('year_in_school')
        print(type(students))
        serializer = StudentSerializer(students, many=True).data
        return Response(serializer)


def get_enum_Field_display(klass, field):
    f = klass._meta.get_field(field)
    return dict(f.flatchoices)


class StudentEnumList(generics.ListAPIView):

    def get(self, request):
        result = get_enum_Field_display(Student, "year_in_school")
        return Response(result)


'''
class AcademyView(generics.ListCreateAPIView):
    serializer_class = AcademySerializer

    def get_queryset(self):
        return

    def get(self, request):
        queryset = Academy.objects.all()
        
        # academy를 조회하는데
        # academy를 조회하고 그 
        # 결과값을 IN 조건으로 subject를 조회함
        
        queryset = queryset.prefetch_related('academy_id')
        serializer = AcademySerializer(queryset, many=True).data
        return Response(serializer)
'''


class AcademyView(generics.ListCreateAPIView):
    serializer_class = AcademySerializer

    def get_queryset(self):
        queryset = Academy.objects.all()
        return queryset

    def get(self, request):
        queryset = self.get_queryset()
        queryset = queryset.prefetch_related('subjects')
        queryset = AcademySerializer(queryset, many=True).data
        return Response(queryset)


class SubjectView(generics.ListCreateAPIView):
    serializer_class = SubjectSerializer

    def get_queryset(self):
        return

    def get(self, request):
        queryset = Subject.objects.all()

        # academy를 조회하는데
        # academy를 조회하고 그
        # 결과값을 IN 조건으로 subject를 조회함

        queryset = queryset.select_related('academy')
        # queryset = Subject.objects.filter(academy=3)
        serializer = SubjectSerializer(queryset, many=True).data
        return Response(serializer)


class BoardTest1View(generics.ListCreateAPIView):
    serializer_class = BoardTest1Serializer

    def get_queryset(self):
        return

    def get(self, request):
        file = File.objects.all
        queryset = BoardTest1.objects.filter()

        serializer = BoardTest1Serializer(queryset, many=True).data
        return Response(serializer)


class NoticeView(generics.ListCreateAPIView):
    serializer_class = NoticeSerializer

    def get_queryset(self):
        return

    def get(self, request):
        queryset = Notice.objects.all()
        serializer = NoticeSerializer(queryset, many=True).data
        return Response(serializer)
