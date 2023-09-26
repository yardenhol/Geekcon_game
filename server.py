import socket
import math
def get_direction_vector(accX, accY, accZ):
    # Calculate the magnitude of the acceleration vector
    magnitude = math.sqrt(accX**2 + accY**2 + accZ**2)
    
    # Normalize the accelerometer readings to get the direction vector
    dirX = accX / magnitude
    dirY = accY / magnitude
    dirZ = accZ / magnitude
    
    return dirX, dirY, dirZ


MULTICAST_GROUP = '239.4.4.4'
MULTICAST_PORT = 4444

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to the multicast address and port
sock.bind(('', MULTICAST_PORT))

# Configure the socket to join the multicast group
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(MULTICAST_GROUP) + socket.inet_aton('0.0.0.0'))

while True:
    data, addr = sock.recvfrom(1024)
    #print('Received:', data.decode('utf-8'))
    shift = str(data).index("accX:")
    num = (str)(data)[shift + len ("accAngleX:")] + (str)(data)[shift + len ("accAngleX:")+1]+ (str)(data)[shift + len ("accAngleX:")+2]+(str)(data)[shift + len ("accAngleX:")+3] + (str)(data)[shift + len ("accAngleX:")+4]+ (str)(data)[shift + len ("accAngleX:")+5]+(str)(data)[shift + len ("accAngleX:")+6]+ (str)(data)[shift + len ("accAngleX:")+7]
    #print (num)
    direction_vector = get_direction_vector(str(data).index("angleX:"), str(data).index("angleY:"), str(data).index("angleZ:"))
    print(direction_vector)


