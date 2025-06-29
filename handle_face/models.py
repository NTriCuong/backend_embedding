from django.db import models

class Face(models.Model):
    image_url = models.CharField(max_length=255) 
    id_user = models.ForeignKey('User', models.DO_NOTHING, db_column='id_user', blank=True, null=True)
    class Meta:
        managed = False # Không quản lý bởi Django, chỉ đọc dữ liệu từ csdl có sẳng và không thay đổi cấu trúc
        db_table = 'Face' # Tên bảng trong cơ sở dữ liệu


class User(models.Model):
    name = models.CharField(max_length=50)
    class Meta:
        managed = False
        db_table = 'User'


