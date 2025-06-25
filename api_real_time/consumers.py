from channels.generic.websocket import AsyncWebsocketConsumer

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
    async def connect(self):
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
        self.connected_devices[device_id]
        await self.send(text_data=f"kết nối với {device_id} thành công")  # Gửi phản hồi về kết nối thành công
    
    async def connect_frontend(self):
        WebSocketConsumer.connected_frontend = self
        self.connected_frontend
        await self.send(text_data="Kết nối với frontend thành công")


    async def disconnect(self, close_code):# close_code: mã lỗi khi ngắt kết nối
       if WebSocketConsumer.connected_frontend == self:
            WebSocketConsumer.connected_frontend = None
            await self.send("Ngắt kết nối với frontend")
            
       for device_id, socket in WebSocketConsumer.connected_devices.items():# tìm xem kết nối nào đã bị ngắt và xoá khỏi dic
            if socket == self:
                WebSocketConsumer.connected_devices[device_id]
                await self.send(text_data="{device_id} ngắt kết nối")
                break
        

    def receive(self, text_data):
        """
        Handle incoming messages from the WebSocket.
        """
        # Process the received message
        self.send(text_data="Message received")  # Echo back the message