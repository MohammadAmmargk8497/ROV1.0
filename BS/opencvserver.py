import cv2
import socket
import pickle
import sys
# Check if IP address is provided as command-line argument
if len(sys.argv) < 2:
    print("Error: LAN IP address not provided.")
    sys.exit(1)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_ip = sys.argv[1]
server_port = 6666
s.bind((server_ip, server_port))

while True:
    x = s.recvfrom(1000000)
    client_ip = x[1][0]
    data = x[0]
    data = pickle.loads(data)
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)
    cv2.imshow("Img Server", img)

    if cv2.waitKey(5) & 0xFF == 27:
        break

cv2.destroyAllWindows()
