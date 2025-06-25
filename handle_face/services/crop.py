import cv2
from .detect import detect_face 

def crop_face(image_path):
    boxes = detect_face(image_path)  # ← detect_face xử lý cả đường dẫn hoặc ảnh
    faces = []  # danh sách các khuôn mặt đã cắt

    # Gán biến image tương ứng
    if isinstance(image_path, str):
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Không thể đọc ảnh từ đường dẫn (file crop)")
    else:
        image = image_path  # ← ảnh truyền trực tiếp từ webcam

    # Cắt các khuôn mặt dựa vào toạ độ
    for box in boxes:
        x1, y1, x2, y2 = map(int, box)
        face_image = image[y1:y2, x1:x2]
        faces.append(face_image)

    return faces
