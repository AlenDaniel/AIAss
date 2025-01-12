import serial
import time

# 设置串口通信
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  # 根据实际的串口名称进行修改

def send_at_command(command, expected_response, timeout=2):
    """
    发送 AT 命令，并等待返回响应
    """
    ser.write((command + '\r\n').encode())
    time.sleep(timeout)  # 等待命令响应
    response = ser.read_all().decode()
    if expected_response in response:
        print(f"Command: {command} successful.")
    else:
        print(f"Command: {command} failed. Response: {response}")

def read_sms():
    """
    读取短信
    """
    # 设置短信接收模式
    send_at_command('AT+CSMS=1', 'OK')

    # 启用短信通知
    send_at_command('AT+CNMI=2,2,0,0,0', 'OK')

    while True:
        # 监听接收的短信
        response = ser.read_all().decode()

        if '+CMT' in response:
            # 短信格式：[短信索引],[发送者号码],短信内容
            print("New message received!")
            print(response)  # 打印收到的短信
            time.sleep(1)  # 每秒检查一次

if __name__ == '__main__':
    # 初始化 GSM 模块
    send_at_command('AT', 'OK')  # 确保模块连接成功
    send_at_command('AT+CMGF=1', 'OK')  # 设置短信格式为文本格式

    print("Ready to receive SMS...")
    read_sms()  # 开始接收短信
