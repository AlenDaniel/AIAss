import serial
import time

def dial_number(phone_number):
    # 初始化串口
    ser = serial.Serial('/dev/ttyUSB0', baudrate=9600, timeout=1)
    
    # 检查模块是否正常
    ser.write(b'AT\r')
    time.sleep(1)
    response = ser.read(64).decode()
    print(response)
    if "OK" not in response:
        print("GSM 模块未响应")
        ser.close()
        return
    # 查看sim卡状态
    ser.write(b'AT+CPIN?\r')
    time.sleep(1)
    response = ser.read(64).decode()
    print(response)
    
    # 检查 SIM 卡状态
    ser.write(b'AT+CSMINS?\r')
    time.sleep(1)
    response = ser.read(64).decode()
    print("SIM 检测状态:", response)
    if "+CSMINS: 0,1" in response:
        print("SIM 卡正常插入")
    elif "+CSMINS: 0,0" in response:
        print("SIM 卡未插入或接触不良")
    else:
        print("无法检测 SIM 卡状态")
    
    # 检查 SIM 卡状态
    ser.write(b'AT+CREG?\r')
    time.sleep(1)
    response = ser.read(64).decode()
    print(response)
    if "+CREG: 0,1" not in response and "+CREG: 0,5" not in response:
        print("SIM 卡未注册到网络")
        ser.close()
        return

    # 检查信号强度
    ser.write(b'AT+CSQ\r')
    time.sleep(1)
    response = ser.read(64).decode()
    print(response)
    if "CSQ" in response:
        signal_strength = int(response.split(":")[1].split(",")[0].strip())
        if signal_strength < 10:
            print("信号过弱")
            ser.close()
            return
    
    # 设置为语音模式
    ser.write(b'AT+FCLASS=1\r')
    time.sleep(1)
    response = ser.read(64).decode()
    print(response)
    if "OK" not in response:
        print("无法设置语音模式")
        ser.close()
        return

    # 拨打电话
    command = f'ATD{phone_number};\r\n'.encode()
    ser.write(command)
    time.sleep(1)
    response = ser.read(64).decode()
    print(response)
    if "OK" in response:
        print("正在拨号...")
    elif "ERROR" in response:
        print("拨号失败，可能是号码格式错误或模块未就绪")
        ser.close()
        return
    
    # 延迟一段时间模拟通话过程
    time.sleep(20)

    # 挂断电话
    ser.write(b'ATH\r')
    time.sleep(1)
    print("挂断电话")
    ser.close()

# 拨打目标号码
dial_number("18126469416")
