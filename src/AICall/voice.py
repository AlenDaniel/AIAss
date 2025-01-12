import serial
import time
import pyaudio
import wave
import speech_recognition as sr
from gtts import gTTS
import os

# 初始化 GSM 模块
ser = serial.Serial('/dev/ttyUSB0', baudrate=9600, timeout=1)

def send_at_command(command, expected_response="OK", timeout=2):
    """发送 AT 命令并检查响应"""
    ser.write((command + '\r\n').encode())
    time.sleep(timeout)
    response = ser.read_all().decode()
    if expected_response in response:
        print(f"Command: {command} successful.")
    else:
        print(f"Command: {command} failed. Response: {response}")

def answer_call():
    """接听电话"""
    send_at_command('ATA', 'OK')

def end_call():
    """挂断电话"""
    send_at_command('ATH', 'OK')

def record_audio(output_file, duration=10):
    """录制音频"""
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    print("录音中...")
    frames = []

    for _ in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("录音结束")
    stream.stop_stream()
    stream.close()
    p.terminate()

    # 保存录音
    with wave.open(output_file, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

def recognize_speech(audio_file):
    """语音识别"""
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio_data, language='en-US')
        print(f"识别文本: {text}")
        return text
    except sr.UnknownValueError:
        print("无法识别语音")
        return ""
    except sr.RequestError as e:
        print(f"识别服务出错: {e}")
        return ""

def text_to_speech(text, output_file):
    """文字转语音"""
    tts = gTTS(text=text, lang='en')
    tts.save(output_file)
    print(f"生成语音文件: {output_file}")

def play_audio(audio_file):
    """播放音频"""
    os.system(f"aplay {audio_file}")

def monitor_call():
    """监控来电"""
    print("等待来电...")
    while True:
        response = ser.read_all().decode()
        if 'RING' in response:
            print("检测到来电...")
            answer_call()
            process_call()
            break

def process_call():
    """处理通话内容"""
    try:
        # 录制语音
        audio_file = "incoming.wav"
        record_audio(audio_file, duration=10)

        # 语音识别
        recognized_text = recognize_speech(audio_file)

        # 根据识别结果生成回复
        if recognized_text:
            reply_text = f"You said: {recognized_text}. How can I assist you?"
        else:
            reply_text = "Sorry, I didn't catch that. Could you repeat?"

        # 文字转语音
        reply_audio_file = "reply.wav"
        text_to_speech(reply_text, reply_audio_file)

        # 播放语音回复
        play_audio(reply_audio_file)

    finally:
        # 挂断电话
        end_call()
        print("通话结束")

if __name__ == "__main__":
    send_at_command('AT')  # 检查模块是否正常
    send_at_command('AT+CLIP=1')  # 启用来电显示
    monitor_call()
