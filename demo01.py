from machine import UART
import _thread
import utime
import log

uart = UART(UART.UART2, 115200, 8, 0, 1, 0)
if __name__ == "__main__":
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
print("cnm")