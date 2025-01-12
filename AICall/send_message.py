import serial
import time

# 设置串口通信
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  # 根据实际端口修改

def send_at_command(command, expected_response, timeout=2):
    """
    发送 AT 命令并等待响应
    """
    ser.write((command + '\r\n').encode())  # 发送命令
    time.sleep(timeout)  # 等待模块响应
    response = ser.read_all().decode()  # 读取响应
    print(f"Command: {command}, Response: {response.strip()}")
    return expected_response in response  # 检查响应是否符合预期

def send_sms(phone_number, message):
    """
    发送短信功能
    :param phone_number: 接收短信的目标号码
    :param message: 短信内容
    """
    # 检查模块是否准备好
    if not send_at_command('AT', 'OK'):
        print("GSM 模块未响应，请检查连接")
        return False
    
    ser.write(b'AT+COPS?\r')
    response = ser.read_all().decode()
    print(response)

    # 设置短信文本模式
    if not send_at_command('AT+CMGF=1', 'OK'):
        print("无法设置短信模式")
        return False

    # 设置目标号码并进入文本模式
    ser.write(f'AT+CMGS="{phone_number}"\r\n'.encode())
    time.sleep(1)  # 等待模块进入短信文本模式
    response = ser.read_all().decode()
    if '>' not in response:  # 检查是否进入短信文本输入状态
        print("无法进入短信输入模式，模块返回：", response.strip())
        return False

    # 输入短信内容并发送
    ser.write(message.encode())  # 发送短信内容
    ser.write(b'\x1A')  # 使用 Ctrl+Z (0x1A) 结束短信输入
    time.sleep(3)  # 等待短信发送完成

    # 检查发送状态
    response = ser.read_all().decode()
    if 'OK' in response:
        print(f"短信已成功发送至 {phone_number}")
        return True
    else:
        print("短信发送失败，模块返回：", response.strip())
        return False

if __name__ == '__main__':
    # 目标号码和短信内容
    target_number = "+8618126469416"  # 目标电话号码
    message_content = "shaoye, woxiangnile!"

    # 发送短信
    if send_sms(target_number, message_content):
        print("短信发送完成")
    else:
        print("短信发送失败")
