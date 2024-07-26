
# #运行本例程，需要通过串口线连接开发板的 MAIN 口和PC，在PC上通过串口工具
# #打开 MAIN 口，并向该端口发送数据，即可看到 PC 发送过来的消息。

# import _thread
# import utime
# import log
# from machine import UART


#  #* 参数1：端口
#  #       注：EC100YCN平台与EC600SCN平台，UARTn作用如下
#  #      UART0 - DEBUG PORT
#  #      UART1 – BT PORT
#  #      UART2 – MAIN PORT
#  #     UART3 – USB CDC PORT
#  #* 参数2：波特率
#  #* 参数3：data bits  （5~8）
#  # * 参数4：Parity  （0：NONE  1：EVEN  2：ODD）
#  #* 参数5：stop bits （1~2）
#  #* 参数6：flow control （0: FC_NONE  1：FC_HW）


# # 设置日志输出级别
# log.basicConfig(level=log.INFO)
# uart_log = log.getLogger("UART")

# class Example_uart(object):
#     def __init__(self, no=UART.UART2, bate=115200, data_bits=8, parity=0, stop_bits=1, flow_control=0):
#         self.uart = UART(no, bate, data_bits, parity, stop_bits, flow_control)
#         self.uart.set_callback(self.callback)


#     def callback(self, para):
#         uart_log.info("call para:{}".format(para))
#         if(0 == para[0]):
#             self.uartRead(para[2])


#     def uartWrite(self, msg):
#         uart_log.info("write msg:{}".format(msg))
#         self.uart.write(msg)

#     def uartRead(self, len):
#         msg = self.uart.read(len)
#         utf8_msg = msg.decode()
#         uart_log.info("UartRead msg: {}".format(utf8_msg))
#         return utf8_msg

#     def uartWrite_test(self):
#         while True :
#             a = self.uartRead(8)
#             utime.sleep_ms(1000)
#             if a :
#                 print("你收到的数据：",a)


# if __name__ == "__main__":
#     uart_test = Example_uart()
#     uart_test.uartWrite_test()

# # 运行结果示例

from machine import UART
import _thread
import usocket
import utime
import log
import checkNet

# Create a socket object
sock = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM, usocket.IPPROTO_TCP)  # usocket.socket(IPv6 地址,socket流,TCP协议类型)

def Tcp_Client(address, port):
    global TCP_Handle
    global Tx2tcp
    global uart2_data
    
    print('socket object created.')
    
    # Connect to the TCP server
    sock.connect((address, port))
    print('tcp link established: %s, %s' % (address, port))
    TCP_Handle = 1
    
    while True:
        try:
            # Send the data
            sock.send(Tx2tcp.encode())
            print('<-- send data:')
            print(Tx2tcp.encode())
            Tx2tcp=None
            # time.sleep(0.5)
            # print('--> recv data:')
            # data = sock.recv(1024)
            # print(data.encode())
            break
        except:
            # Connection ends until the data is fully received
            print('tcp disconnected.')
            #sock.close()
            break

def Tcp_Init():
    stage, state = checkNet.wait_network_connected(30)
    if stage == 3 and state == 1: # Network connection is normal
        print('[Network connection successful.]')
        Tcp_Client('120.253.239.161', 8002) # Start the client
    else:
        print('Network connection failed, stage={}, state={}'.format(stage, state))
        

uart = UART(UART.UART2, 115200, 8, 0, 1, 0)
if __name__ == "__main__":
    # 只保留GGA和RMC信息
    uart.write("$PAIR062,3,0*3D\r\n$PAIR062,2,0*3C\r\n$PAIR062,5,0*3B\r\n$PAIR062,1,0*3F\r\n")
    print("$PAIR062,3,0*3D\r\n$PAIR062,2,0*3C\r\n$PAIR062,5,0*3B\r\n$PAIR062,1,0*3F\r\n")

    Tcp_Init()

    sock.send("GET /RTCM33_GRCEpro HTTP/1.0\r\nUser-Agent: NTRIP GNSSInternetRadio/1.4.10\r\nAccept: */*\r\nConnection: close\r\nAuthorization: Basic Y2VkcjIxNTEzOmZ5eDY5NzQ2\r\n\r\n")

    while True:
        msgLen = uart.any()
        if msgLen:
            msg = uart.read(msgLen)
            utf8_msg = msg.decode()
            print(utf8_msg)
            uart.write('rev msg and send back: ')
            uart.write(utf8_msg)
        else:
            print("wjs")

        sock.send("$GNGGA,054704.00,2623.00740643,N,10636.51117030,E,1,08,1.9,1218.1202,M,-29.1518,M,,*65\r\n")
        
        # Receive data
        data = sock.recv(1200)  # Buffer size is 1024 bytes
        if data:
            utf8_data = data.decode()
            print('--> received data:')
            print(utf8_data)
            uart.write(utf8_data)
            # Process received data here
        else:
            # If no data, break the loop
            print('No data received. Closing connection.')
            break

        utime.sleep_ms(1000)





















       