# các hàm làm việc với cơ sở dữ liệu sẽ được viết ở đây
def get_all_faces(): #get tất cả các mặt từ csdl lên
    from handle_face.model.models import Face # chỉ import khi hàm thật sự chạy
    return list(Face.objects.all())