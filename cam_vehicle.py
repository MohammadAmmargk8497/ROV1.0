import cv2
import socket
import pickle


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1000000)

server_ip = "169.254.88.156"
server_port = 6666

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

while cap.isOpened():
    ret, img = cap.read()
    ret, buffer = cv2.imencode(".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), 30])
    x_as_bytes = pickle.dumps(buffer)
    s.sendto((x_as_bytes), (server_ip, server_port))

cv2.destroyAllWindows()
cap.release()
