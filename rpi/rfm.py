import re
import busio
import board
from digitalio import DigitalInOut

import adafruit_ssd1306
import adafruit_rfm9x

CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
SPI = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(SPI, CS, RESET, 915.0)
rfm9x.tx_power = 23
rfm9x.enable_crc = True

def get_data_from_packet(packet):
    packet = str(packet, 'utf-8')
    packet = packet.split(',')
    
    (temp, pre, hum) = packet

    print(temp)
    print(pre)
    print(hum)
    
    temp = re.match(r'T: ([^"]+) degC', temp).group(1)
    pre = re.match(r' P: ([^"]+) hPa', pre).group(1)
    hum = re.match(r' H: ([^"]+) rH', hum).group(1)
    
    return (temp, pre, hum)

def listen_for_data():
    packet = rfm9x.receive()

    (temp, pre, hum) = (0, 0, 0)
    
    if not packet is None:
       (prev_packet, packet) = (packet, None)
       (temp, pre, hum)= get_data_from_packet(prev_packet)
       
       print(temp)
       print(pre)
       print(hum)
       
       rfm9x.send(bytes("OK", "utf-8"))
       rssi = rfm9x.last_rssi
       print("Signal strength: {0} dB".format(rssi))
    
    return (temp, pre, hum)