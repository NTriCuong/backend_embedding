# from django.apps import apps


def get_all_faces():
    from handle_face.models import Face
    return list(Face.objects.all())

