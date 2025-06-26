from deepface import DeepFace

# Hàm này sẽ nhận vào một khuôn mặt đã được cắt ra từ ảnh và trả về vector đặc trưng của khuôn mặt đó
def embedding_face(face):
    if face is None:
        raise ValueError("đầu vào khong hợp lệ (file embedd)")
    embedding = DeepFace.represent(face, model_name='Facenet',enforce_detection=False)[0]['embedding']
    return embedding

 # hàm represent là hàm chính để trích xuất vector đặc trưng từ khuôn mặt
    # represent(ảnh đầu vào, model_name='Facenet512',)[0]
    # trả về 1 dictionary các khuôn mặt có trong ảnh nhưng ở đay ta đã cắt 
    #khuôn mặt ra rồi nên chỉ có 1 khuon mặt duy nhất 
    #['embedding'] là lấy vector đặc trưng của khuôn mặt