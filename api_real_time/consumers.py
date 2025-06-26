from channels.generic.websocket import AsyncWebsocketConsumer
import json
import base64
from io import BytesIO
from PIL import Image
from backend_embedding.ultils import get_all_faces
from handle_face.services.crop import crop_face
from handle_face.services.embedd import embedding_face
from handle_face.services.equa import compare_embeddings
import cv2

#      self.scope = {
    #     'type': 'websocket',
    #     'path': '/ws/face/',
    #     'query_string': b'device',   # đây chính là phần ta cần!
    #     'headers': [...],
    #     ... }

class WebSocketConsumer(AsyncWebsocketConsumer):#kế thừa từ AsyncWebsocketConsumer để sử dụng WebSocket trong Django Channels
    #dự án sẻ có 2 kết nối từ device và từ frontend
    connected_devices = {} # device_id : <WebSocketConsumer>
    connected_frontend = None
    async def connect(self): #khi người dùng kết nối thì sẻ chạy hàm connect
        await self.accept() # chấp nhận kết nối
        query_string = self.scope['query_string'].decode()
        if "device" in query_string:
            await self.connect_device(query_string)
        elif "frontend" in query_string:
            await self.connect_frontend()
        else:
            await self.close()

    async def connect_device(self, query):
        device_id = query.split("device=")[-1]  # cắt Lấy ID sau dấu =
        WebSocketConsumer.connected_devices[device_id] = self # Lưu kết nối vào dictionary
        await self.send(text_data=f"kết nối với {device_id} thành công")  # Gửi phản hồi về kết nối thành công
    
    async def connect_frontend(self):
        WebSocketConsumer.connected_frontend = self
        await self.send(text_data="Kết nối với frontend thành công")

#khi người dùng ngắt kêts nối (ngắt kết nối trước) sẻ chạy vào hàm desconnect
    async def disconnect(self, close_code):# close_code: mã lỗi khi ngắt kết nối
       if WebSocketConsumer.connected_frontend == self:
            WebSocketConsumer.connected_frontend = None
            
       for device_id, socket in WebSocketConsumer.connected_devices.items():# tìm xem kết nối nào đã bị ngắt và xoá khỏi dic
            if socket == self:
                del WebSocketConsumer.connected_devices[device_id]
                break
#async def receive(self, text_data=None, bytes_data=None):
    # Hàm này sẽ được gọi khi có dữ liệu gửi đến từ client
    async def receive(self, data):
      #xử lý dữ liệu
      #giải mã data nhận được từ device
        data_device = json.loads(data) # data là JSON chứa thông tin về ảnh device_id và image_base
        device_id = data_device.get("device_id")
        device_img = data_device.get("image_base")
        # Giải mã ảnh
        try:
            image_bytes = base64.b64decode(device_img)
            image = Image.open(BytesIO(image_bytes)) #khôi phục hiện trạng của ảnh gốc .jpg 
        
        #xử lý nhận diện 
            # get db
            data_DB = get_all_faces()
            data_embedding_db = [] # list các vector khuôn mặt trích xuât từ db
            for face in data_DB:
                detected_face = crop_face(face.image_url)['image'] # cắt khuôn mặt từ ảnh
                data_embedding_db.append(embedding_face(detected_face[0]))
            
            #xử lý khuôn mặt từ ảnh vừa nhận được từ device
            warning = ''
            detected_faces = crop_face(image) # cắt khuôn mặt từ ảnh
            for face in detected_faces:
                face_embedding = embedding_face(face['image'])
                for face_db in data_embedding_db:
                    #toạ độ
                    x1 = face['boder_box']['x1']
                    y1 = face['boder_box']['y1']
                    x2 = face['boder_box']['x2']
                    y2 = face['boder_box']['y2']
                    if compare_embeddings(face_embedding, face_db):#nhận diện thành công
                        #vẽ border trên ảnh gốc nhận được từ device
                        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        warning = ''
                        break
                    else:
                        #nếu không nhận diện được thì vẽ border màu đỏ
                        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
                        warning = 'cảnh báo có người lạ'

            
            # Encode ảnh từ numpy array sang base64 string
            _, buffer = cv2.imencode('.jpg', image)
            image_base64 = base64.b64encode(buffer).decode()
            
            result = {
                "device_id": device_id,
                "image": image_base64,
                "warning": warning
            }
            # Gửi kết quả cho frontend

            await WebSocketConsumer.connected_frontend.send(
                text_data=json.dumps(result)
            )
        except Exception as e:
            await WebSocketConsumer.connected_frontend.send(
                text_data=json.dumps({"error": str("Lỗi xử lý ảnh: " + str(e))})
            )