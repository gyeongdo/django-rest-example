from django.urls import path
from . import views

app_name="quickstart"

urlpatterns = [
    path('', views.OrderViews.as_view()),
    path('<int:pk>', views.OrderView.as_view()),
    path('custom', views.OrderCustomViews.as_view()),
    path('dog', views.DogViews.as_view()),
    path('blog', views.BlogViews.as_view()),
    path('coversionExcel', views.ExcelViews.as_view()),
    path('dogExcelDownload', views.DogExcelViews.as_view()),

    path('dogExcelDownload1', views.export_users_xls, name='export_users_xls'),
    path('dogCsvlDownload1', views.export_users_csv, name='export_users_csv'),

    path('dogCsvToJson', views.ConvertCsvJson.as_view()),
    path('dogSelect', views.DogSelct.as_view()),

    path('dogColumn', views.DogColumn.as_view(), name='list'),

    path('fileupload', views.FileView.as_view(), name="file-upload"),

    # path('fileudownload', views.FileDownloadView.as_view(), name="file-download")
    path('download/<int:id>/', views.FileDownloadView.as_view()),

    path('board', views.BoardView.as_view()),

    path('student', views.StudentView.as_view()),

    path('studentEnumList', views.StudentEnumList.as_view()),

    path('academy', views.AcademyView.as_view()),

    path('subject', views.SubjectView.as_view()),

    path('boardtest1', views.BoardTest1View.as_view()),

    path('notice', views.NoticeView.as_view()),

]
