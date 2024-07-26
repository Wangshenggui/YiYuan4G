from machine import UART
import _thread
import utime
import log
import paho.mqtt.client as mqtt

broker_address = "8.137.81.229"
broker_port = 8000

uart = UART(UART.UART2, 115200, 8, 0, 1, 0)
if __name__ == "__main__":
    client = mqtt.Client()
    client.connect(broker_address, broker_port)
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
        utime.sleep_ms(1000)
       