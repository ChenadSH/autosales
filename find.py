#coding:utf-8  
import binascii
import math
import serial
import asyncio
import websockets

localws = ''
from time import sleep  
ser = serial.Serial('/dev/ttyUSB0', 115200,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=0.5)
ser.flushInput()
#ser = serial.Serial('serial0', 115200, timeout=0.5)   
def recv(serial):
    data = ''
    while True:
        sleep(0.2)
        # data =serial.read()
        data=serial.read_all() # more complete
        #data = serial.readline()
        # data = serial.readlines()
        #sleep(0.5)
        if data == '' and data == b'':    
            continue  
        else:
            break  
    return data

# 向服务器端发送认证后的消息
async def send_msg(websocket):
    #ser.write([0xBB,0x00,0x27,0x00,0x03,0x22,0x27,0x10,0x83,0x7E])
    while True:
        ser.flushOutput()
        ser.write([0xBB,0x00,0x22,0x00,0x00,0x22,0x7E])
        data =recv(ser)
        if data not in [b'',b'\xbb\x01\xff\x00\x01\x15\x16\x7E',b'\xbb\x01\xff\x00\x01\x15\x16~']:
            readData = data.hex()
            readArr = []
            if len(data)>=20:
                for b in data.split(b'\xbb'):
                    if len(b)>=13:
                        # delete duplicate
                        canInsert = 1
                        for v in readArr:
                            if v['epc'] == b[7:-4].hex():
                                canInsert = 0
                        if canInsert == 1:
                            readArr.append({'epc':b[7:-4].hex()})#,'crc':b[-4:-2].hex(),'rssi':b[5:6].hex()
                print(readArr)
                await websocket.send(str(readArr))
        else:
            # print(data)
            await websocket.send('[]')

# 客户端主逻辑
async def main_logic():
    async with websockets.connect('ws://localhost:5000') as websocket:
        await send_msg(websocket)

asyncio.get_event_loop().run_until_complete(main_logic())









# #coding:utf-8  
# import binascii
# import math
# import serial
# from time import sleep  
# ser = serial.Serial('/dev/ttyUSB0', 115200,
#                     parity=serial.PARITY_NONE,
#                     stopbits=serial.STOPBITS_ONE,
#                     bytesize=serial.EIGHTBITS,
#                     timeout=0.5)
# ser.flushInput()
# #ser = serial.Serial('serial0', 115200, timeout=0.5)   
# def recv(serial):
#     data = ''
#     while True:    
#         #data =serial.read()
#         serial.flushOutput()
#         #data=serial.read_all()
#         data = serial.readline()
#         #data = serial.readlines()
#         #sleep(0.1)
#         if data == '' and data == b'':    
#             continue  
#         else:
#             break  
        
#     return data
# while True:
#     #ser.write("\xBB\x00\x03\x00\x01\x00\x04\x7E".encode("utf-16"))
#     #ser.write(b"\xBB\x00\x03\x00\x01\x00\x04\x7E")
#     #write data
#     #ser.write([0xBB,0x00,0x49,0x00,0x0D,0x00,0x00,0xFF,0xFF,0x03,0x00,0x00,0x00,0x02,0x12,0x34,0x56,0x78,0x6D,0x7E])
#     #read data
#     #ser.write([0xBB,0x00,0x39,0x00,0x09,0x00,0x00,0xFF,0xFF,0x03,0x00,0x00,0x00,0x02,0x45,0x7E])
#     # multi search
#     #ser.write(b"\xBB\x00\x27\x00\x03\x22\x27\x10\x83\x7E")
#     #single search
#     ser.write([0xBB,0x00,0x22,0x00,0x00,0x22,0x7E])
#     #ser.write(b"\xBB\x00\x39\x00\x09\x00\x00\x00\x00\x01\x00\x00\x00\x08\x4B\x7E\r\n")#read epc
#     #ser.write(b"\xBB\x00\x0D\x00\x00\x0D\x7E")
#     #ser.write(b"\xBB\x00\x39\x00\x09\x00\x00\x00\x00\x02\x00\x00\x00\x06\x4a\x7E")#read tid    
#     data =recv(ser)

#     #print(data)
#     if data not in [b'',b'\xbb\x01\xff\x00\x01\x15\x16\x7E']:
#         readData = data.hex()
#         readArr = []
#         if len(data)>=20:
#             for b in data.split(b'\xbb'):
#                 if len(b)>=13:
#                     readArr.append({'epc':b[7:-4].hex(),'crc':b[-4:-2].hex(),'rssi':b[5:6].hex()})
#             #for i in range(math.ceil(len(data)/20)):
#                 #readArr.append({'epc':readData[i*40+16:(i+1)*40-8],'crc':readData[i*40+32:(i+1)*40 -4],'rssi':readData[i*40+10:(i+1)*40 -28]})
#             print(readArr)
#         else:
#             print(data)
#         # 删除换行和回车
#         #data = str(data).replace('\n', '').replace('\r', '').replace('\t', '')
#         # print(data.decode("gbk"))
#         # data.decode("utf-8","ignore")
#         #print(data.split(b'\xbb'))

#         #print(data.hex())
#         #print(binascii.b2a_hex(data))