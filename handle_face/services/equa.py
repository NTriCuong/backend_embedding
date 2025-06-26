from typing import Final
import numpy as np

THRESHOLD: Final = 0.95

def cosine_similarity(vec1, vec2):
    if np.linalg.norm(vec1) == 0 or np.linalg.norm(vec2) == 0:
        # Tránh chia cho 0 tránh lỗi 
        return 0
     # Chuẩn hoá 2 vector
    vec1_norm = vec1 / np.linalg.norm(vec1)
    vec2_norm = vec2 / np.linalg.norm(vec2)
    # Tính cosine similarity
    return np.dot(vec1_norm, vec2_norm)

#so sansh 2 khuon mặt
def compare_embeddings(vec1, vec2):
    # chuyển các vector đặc trưng trả về từ hàm embedd thành numpy array
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    similarity =cosine_similarity(vec1, vec2)
    return similarity >=  THRESHOLD # Giá trị gần 1 => giống, gần 0 => khác