from django.http import StreamingHttpResponse
import cv2
from handle_face.services.equa import compare_embeddings
from handle_face.services.crop import crop_face
from handle_face.services.embedd import embedding_face
from backend_embedding.ultils import get_all_faces

def gen_frames():
    # B1: Load cơ sở dữ liệu vector khuôn mặt
    data = get_all_faces()
    data_embedding = []
    for face in data:
        detected_face = crop_face(face.image_url)
        data_embedding.append(embedding_face(detected_face[0]))

    face_test = crop_face('/Users/nguyentricuong/Desktop/media_faces/quynhnhu/1.JPG')
    embedd = embedding_face(face_test[0])

    for i in range(len(data_embedding)):
        if compare_embeddings(embedd, data_embedding[i]):
            print(str(i)+": 🟢")
        else:
            print(str(i)+": 🔴")
    # # B2: Mở webcam
    # cap = cv2.VideoCapture(1)
    # if not cap.isOpened():
    #     print("Không thể mở webcam")
    #     return

    # # B3: Xử lý từng frame
    # while True:
    #     ret, frame = cap.read()
    #     if not ret:
    #         break

    #     # Cắt mặt
    #     detected_faces = crop_face(frame)
    #     for face in detected_faces:
    #         face_embedding = embedding_face(face)
    #         recognized = False
    #         for db_embedding in data_embedding:
    #             if compare_embeddings(face_embedding, db_embedding):
    #                 recognized = True
    #                 break

    #         if recognized:
    #             print("🟢")
    #         else:
    #             print("🔴")

    #         cv2.putText(frame,'khung cam',(10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    #     # B4: Encode ảnh và gửi cho browser
    #     _, buffer = cv2.imencode('.jpg', frame)
    #     frame_bytes = buffer.tobytes()
    #     yield (b'--frame\r\n'
    #            b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    # cap.release()

def run_camera(request):
    return StreamingHttpResponse(gen_frames(), content_type='multipart/x-mixed-replace; boundary=frame')
