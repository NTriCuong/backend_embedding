import cv2
from .detect import detect_face 
#cắt khuôn mặt từ khung hình
def crop_face(image_path):
    boxes = detect_face(image_path)  # danh sasch các toạ độ khuôn mặt được phát hiện là 1 list
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
        faces.append({
            'image': face_image,
            'boder_box': {
                'x1': x1,
                'y1': y1,
                'x2': x2,
                'y2': y2
            },
            })

    return faces #arr dictionary
