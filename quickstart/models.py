from django.db import models
# from django.contrib.postgres.fields import JSONField
from django.db.models import JSONField
from django.utils.translation import gettext_lazy as _


# Create your models here.

class Order(models.Model):
    id = models.CharField(max_length=10, blank=True, null=False, primary_key=True)
    data = JSONField()
    # metadata_keys = models.TextField(blank=True, null=True)


class MytypeField(models.Field):
    def db_type(self, connection):
        return 'CHAR'


from django.utils.html import format_html_join
from django.utils.html import format_html

class Blog(models.Model):
    name = models.CharField(max_length=100)
    content = models.CharField(max_length=4000, blank=True, null=True)
    tagline = models.TextField()
    taglineqwe = models.TextField()
    FileEntry = models.ForeignKey("FileEntry", on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    use_yn = MytypeField(default='N', max_length=1)
    qwer_yn = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class FileEntry(models.Model):
    origin_name = models.CharField(max_length=100, null=False, blank=False, default='new')
    new_name = models.CharField(max_length=100, null=False, blank=False, default='new')
    file_ext = models.CharField(max_length=10, null=False, blank=False, default='new')
    file_path = models.FileField(upload_to='uploads/')


class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField()
    authors = models.ManyToManyField(Author)
    number_of_comments = models.IntegerField()
    number_of_pingbacks = models.IntegerField()
    rating = models.IntegerField()

    def __str__(self):
        return self.headline




class Dog(models.Model):
    name = models.CharField(max_length=200, null=False)
    data = JSONField()
    content = models.TextField(default=False)

    # file_path = models.TextField(default=False)
    # create_date = models.DateTimeField(auto_now_add=True)
    # upload = models.FileField(upload_to='uploads/')

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        if validated_data:
            return Dog.objects.create(**validated_data)

    class Meta:
        managed = False


class Dog1(models.Model):
    name = models.CharField(max_length=200, null=False)
    data = JSONField()
    content = models.TextField(default=False)

    # file_path = models.TextField(default=False)
    # create_date = models.DateTimeField(auto_now_add=True)
    # upload = models.FileField(upload_to='uploads/')

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        if validated_data:
            return Dog1.objects.create(**validated_data)

    class Meta:
        managed = True


class Dog2(models.Model):
    name = models.CharField(max_length=200, null=False)
    data = JSONField()
    content = models.TextField(default=False, null=True)

    class Meta:
        db_table = 'dog_json'

    # def create(self, validated_data):
    #     """
    #     Create and return a new `Snippet` instance, given the validated data.
    #     """
    #     print('@@@@@@@@@@@', validated_data)
    #     if validated_data:
    #         return Dog2.objects.create(**validated_data)



from quickstart import file_upload_path


class FileModel(models.Model):
    # 실제 디스크에 저장되는 파일 절대 경로
    file_save_name = models.FileField(upload_to=file_upload_path, blank=False, null=False)
    # 파일의 원래 이름
    file_origin_name = models.CharField(max_length=100)
    # 파일 저장 경로
    file_path = models.CharField(max_length=100)
    # 파일 생성일
    create_date = models.DateTimeField(auto_now_add=True)
    # 파일 확장자
    file_ext = models.CharField(max_length=10)
    # 이미지 여부
    is_img = models.BooleanField(default=False)

    class Meta:
        ordering = ['create_date']
        db_table = 'file_box'

    # def __str__(self):
    #     return self.file_origin_name


class Student(models.Model):
    class YearInSchool(models.TextChoices):
        FRESHMAN = 'FR', _('Freshman')
        SOPHOMORE = 'SO', _('Sophomore')
        JUNIOR = 'JR', _('Junior')
        SENIOR = 'SR', _('Senior')
        GRADUATE = 'GR', _('Graduate')

    name = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=False, default="seoul")
    year_in_school = models.CharField(
        max_length=2,
        choices=YearInSchool.choices,
        default=YearInSchool.FRESHMAN,
    )



class Board(models.Model):
    title = models.CharField(max_length=200, null=False)
    content = models.TextField()


class AddFile(models.Model):
    file_ext = models.CharField(max_length=10, null=False)
    file_name = models.CharField(max_length=100, null=False)
    file_path = models.FileField(upload_to='uploads/', null=True, default="qwe.qwe")
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='add_file')


from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

class FlexCategory(models.Model):
    name = models.SlugField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Hero(models.Model):
    name = models.CharField(max_length=100)
    flex_category = GenericRelation(FlexCategory, related_query_name='flex_category')


class Villain(models.Model):
    name = models.CharField(max_length=100)
    flex_category = GenericRelation(FlexCategory, related_query_name='flex_category')


class Teacher(models.Model):
    name = models.CharField(max_length=200, null=False)


class Academy(models.Model):
    name = models.CharField(max_length=200, null=False)


class Subject(models.Model):
    subname = models.CharField(max_length=200, null=False)
    academy = models.ForeignKey(Academy, null=True, on_delete=models.CASCADE, related_name='subjects')


class File(models.Model):
    # 기본 컬럼
    file_path = models.FileField(upload_to='upload/', null=True)
    file_ext = models.CharField(max_length=10, null=False)
    file_url = models.CharField(max_length=100, null=True)

    # 조인을 위해 추가해야 하는 컬럼
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        db_table = 'file'


class BoardTest1(models.Model):
    name = models.CharField(max_length=100, null=True, db_index=True)
    # 연관관계가 될 부분
    file = GenericRelation(File, related_name='file')

    class Meta:
        db_table = 'board_test1'


class Notice(models.Model):
    name = models.CharField(max_length=100, null=True, db_index=True)
    # 연관관계가 될 부분
    file = GenericRelation(File, related_name='notices')

    class Meta:
        db_table = 'notice'

