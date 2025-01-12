import serial
import time
import re
from loguru import logger as log

# 初始化串口
ser = serial.Serial('/dev/ttyUSB0', baudrate=9600, timeout=1)

def send_at_command(command, expected_response, timeout=2):
    ser.write((command + '\r\n').encode())
    time.sleep(timeout)
    response = ser.read_all().decode()
    if expected_response in response:
        log.info(f"命令：{command} 成功")
    else:
        log.info(f"命令：{command} 失败，响应：{response}")

def enable_clip():
    send_at_command('AT+CLIP=1', 'OK')
     # 设置短信接收模式
    send_at_command('AT+CSMS=1', 'OK')
    # 启用短信通知
    send_at_command('AT+CNMI=2,2,0,0,0', 'OK')

def answer_call():
    """
    接听电话并保持通话
    """
    log.info("接听电话...")
    ser.write(b'ATA\r\n')  # 使用 ATA 命令接听电话
    time.sleep(10)  # 等待响应
    
    response = ser.read_all().decode()
    if 'OK' in response:
        log.info("电话已接听，通话保持中...")
        while True:
            # 持续监听电话连接状态
            response = ser.read_all().decode()
            if 'NO CARRIER' in response:  # 检测挂断信号
                log.info("对方已挂断电话，通话结束。")
                break
            time.sleep(1)  # 每秒检查一次状态
    else:
        log.warning("接听电话失败，模块未响应。")


def monitor_incoming_call():
    log.info("等待来电...")
    while True:
        response = ser.read_all().decode(errors='ignore')
        if 'RING' in response and '+CLIP' in response:
            log.info("检测到来电！")
            log.info(response)  # 打印来电信息
            # 提取来电号码
            call_number = response.split('"')[1]
            log.warning(f"来电号码: {call_number}")
            answer_call()  # 尝试接听电话
        if '+CMT' in response:
            # 短信格式：[短信索引],[发送者号码],短信内容
            log.info("收到短信")
            number,mm,next_message = extract_sms_info(response)
            message = read_sms(next_message)
            log.warning(f"短信内容{number}: {message}")  # 打印收到的短信
            time.sleep(0.5)  # 每秒检查一次
        time.sleep(1)
# 提取内容   
def extract_sms_info(sms_string):
    """
    提取短信中的发件人号码、时间戳和十六进制短信内容
    """
    # 正则表达式匹配短信内容
    pattern = r'\+CMT: "([^"]+)",.*?"([^"]+)"\r\n([0-9A-F]+)'
    match = re.search(pattern, sms_string, re.DOTALL)

    if match:
        sender = match.group(1)  # 发件人号码
        timestamp = match.group(2)  # 时间戳
        message_hex = match.group(3)  # 短信十六进制内容
        return sender, timestamp, message_hex
    else:
        print("未能提取短信信息")
        return None, None, None
# 解码消息
def read_sms(response):
    try:
        # 将十六进制字符串转换为字节
        byte_content = bytes.fromhex(response)
        decoded_text = byte_content.decode('utf-16-be', errors='ignore') 
        return decoded_text
        # # 尝试以常见编码解码
        # try:
        #     decoded_text = byte_content.decode('utf-8')
        #     log.info(f"Decoded as UTF-8: {decoded_text}")
        #     return decoded_text
        # except UnicodeDecodeError:
        #     pass
        
        # try:
        #     decoded_text = byte_content.decode('ascii')
        #     log.info(f"Decoded as ASCII: {decoded_text}")
        #     return decoded_text
        # except UnicodeDecodeError:
        #     pass

        # try:
        #     decoded_text = byte_content.decode('utf-16')
        #     log.info(f"Decoded as UTF-16: {decoded_text}")
        #     return decoded_text
        # except UnicodeDecodeError:
        #     pass

        # # GSM 7-bit 解码逻辑（示例）
        # gsm_7bit_mapping = byte_content.decode('latin1')  # 假设直接用 Latin1 解码
        # log.info(f"Decoded as GSM 7-bit (Latin1 mapping): {gsm_7bit_mapping}")
        # return gsm_7bit_mapping
        
    except ValueError:
        log.info("Invalid hex content.")

# if __name__ == '__main__':
def init():
    # 初始化 GSM 模块
    send_at_command('AT', 'OK')  # 确保模块连接成功
    send_at_command('AT+CSQ', 'OK')  # 检查信号强度

    enable_clip()  # 启用来电显示功能
    monitor_incoming_call()  # 开始监听来电
