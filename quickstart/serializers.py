from rest_framework import serializers
from .models import *

'''class OrderSerializer(serializers.ModelSerializer):

    meta_field = serializers.SerializerMethodField('add_meta_keys')

    # read_only_fields = ("user", "id", "created", "updated")

    def add_meta_keys(self, foo):
        return foo.metadata_keys

    class Meta:
        model = Order
        fields = ['id', 'data']
        # fields = ['meta_field']
        # fields = ['data']
'''


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'data']


class DogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dog2
        fields = ['id','data', 'name']
        # fields = ['meta_field']
        # fields = ['data']


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'
        # fields = ['meta_field']
        # fields = ['data']


class DogColumnSerializer(serializers.ModelSerializer):
    qwname = serializers.SerializerMethodField(read_only=True)

    def get_qwname(self, obj):

        dicc = obj.data[0]
        distlist = [dicc]
        print(type(distlist[0]))
        # print(obj["name"])
        return obj.name + '123'

    class Meta:
        model = Dog
        fields = ['id', 'name', 'qwname']


from rest_framework import serializers
from quickstart.models import FileModel


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileModel
        fields = '__all__'

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        if validated_data:
            return FileModel.objects.create(**validated_data)


class AddFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddFile
        fields = ['file_ext','file_name','board']


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'title', 'add_file']


class BoardJoinSerializer(serializers.ModelSerializer):
    add_file = AddFileSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'add_file']


class StudentSerializer(serializers.ModelSerializer):
    year_in_school = serializers.CharField(source='get_year_in_school_display')

    class Meta:
        model = Student
        fields = '__all__'




class AddSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class AcademySerializer(serializers.ModelSerializer):
    # subjects = AddSubjectSerializer(read_only=True, many=True)

    class Meta:
        model = Academy
        fields = ['id', 'name', 'subjects']


class SubjectSerializer(serializers.ModelSerializer):
    # academy = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = '__all__'

    # def get_academy(self, obj):
    #     print("obj :: ", obj.__dict__)
    #     return obj.__dict__


class BoardTest1Serializer(serializers.ModelSerializer):

    class Meta:
        model = BoardTest1
        fields = '__all__'


class NoticeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notice
        fields = '__all__'