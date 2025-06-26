import os
from ultralytics import YOLO

def get_model_yolo():
    current_dir = os.path.dirname(os.path.abspath(__file__))  # Thư mục của detect.py
    model_path = os.path.join(current_dir, '..', 'inference', 'best.pt')
    model_path = os.path.abspath(model_path)  # Chuyển thành đường dẫn tuyệt đối
    return YOLO(model_path)

# hàm phát hiện khuôn mặt trong khung hình
def detect_face(image_path):
    model_yolo= get_model_yolo()  # Lấy mô hình YOLO
    results = []
    if isinstance(image_path, str):
        results = model_yolo(image_path, show=True)
    # Nếu là ảnh webcam (numpy array)
    else:
        results = model_yolo(source=image_path, show=True)
    boxes = results[0].boxes.xyxy.cpu().numpy()# lấy tọa độ của các khuôn mặt được phát hiện
    
    if boxes.size == 0:  # Kiểm tra nếu không có khuôn mặt nào được phát hiện
        return []  # Trả về danh sách rỗng nếu không có khuôn mặt nào được phát hiện
    
    # Chuyển đổi tọa độ từ numpy array sang list
    return boxes.tolist() # Trả về danh sách các tọa độ khuôn mặt


