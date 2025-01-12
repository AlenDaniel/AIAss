import serial
import time

# 初始化串口
ser = serial.Serial('/dev/ttyUSB0', baudrate=9600, timeout=1)

def send_at_command(command, expected_response, timeout=2):
    ser.write((command + '\r\n').encode())
    time.sleep(timeout)
    response = ser.read_all().decode()
    if expected_response in response:
        print(f"命令：{command} 成功")
    else:
        print(f"命令：{command} 失败，响应：{response}")

def enable_clip():
    send_at_command('AT+CLIP=1', 'OK')

def answer_call():
    print("接听电话...")
    ser.write(b'ATH\r\n')  # 接听电话
    time.sleep(5)  # 增加等待时间，确保 GSM 模块能响应
    response = ser.read_all().decode()
    if 'OK' in response:
        print("电话已接听")
    else:
        print("接听电话失败")

def monitor_incoming_call():
    print("等待来电...")
    while True:
        response = ser.read_all().decode()
        print(response)  # 打印所有接收到的串口信息
        if 'RING' in response and '+CLIP' in response:
            print("检测到来电！")
            print(response)  # 打印来电信息
            # 提取来电号码
            call_number = response.split('"')[1]
            print(f"来电号码: {call_number}")
            answer_call()  # 尝试接听电话

        time.sleep(1)

if __name__ == '__main__':
    # 初始化 GSM 模块
    send_at_command('AT', 'OK')  # 确保模块连接成功
    send_at_command('AT+CSQ', 'OK')  # 检查信号强度

    enable_clip()  # 启用来电显示功能
    monitor_incoming_call()  # 开始监听来电
