import serial
import time
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
        # response = ser.read_all()
        # try:
        #     response = response.decode('utf-8')
        # except UnicodeDecodeError:
        #     response = response.decode('latin1')  # 或使用 `errors='ignore'`
        
        if 'RING' in response and '+CLIP' in response:
            log.info("检测到来电！")
            log.info(response)  # 打印来电信息
            # 提取来电号码
            call_number = response.split('"')[1]
            log.warning(f"来电号码: {call_number}")
            answer_call()  # 尝试接听电话

        time.sleep(1)

# if __name__ == '__main__':
def init():
    # 初始化 GSM 模块
    send_at_command('AT', 'OK')  # 确保模块连接成功
    send_at_command('AT+CSQ', 'OK')  # 检查信号强度

    enable_clip()  # 启用来电显示功能
    monitor_incoming_call()  # 开始监听来电
