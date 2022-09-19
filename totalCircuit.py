import time
#GPIO제어 위한
import RPi.GPIO as GPIO
#온습도센서 위한
from adafruit_htu21d import HTU21D 
import busio
#조도센서 위한
import Adafruit_MCP3008

#BCM모드로 작동
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#센서들의 GPIO핀 번호 변수에 초기화
#led 센서
led = 6 
led2 = 5
#초음파 센서
trig = 20
echo = 16
#온습도 센서
sda = 2 
scl = 3 
i2c = busio.I2C(scl, sda)
sensor = HTU21D(i2c) # HTU21D 장치를 제어하는 객체 리턴
#조도센서
mcp = Adafruit_MCP3008.MCP3008(clk=11, cs=8, miso=9, mosi=10)

#led
GPIO.setup(led, GPIO.OUT) 
GPIO.setup(led2, GPIO.OUT)

#초음파
GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)
GPIO.output(trig, False)

# led 번호의 핀에 onOff(0/1) 값 출력하는 함수
def controlLED(onOff): 
        GPIO.output(led, onOff)
def controlLED2(onOff): 
        GPIO.output(led2, onOff)

# HTU21D 장치로부터 습도 값 읽기
def getHumidity() :
        return float(sensor.relative_humidity) 

#초음파 센서로부터 거리 측정
def measureDistance():
        global trig, echo
        GPIO.output(trig, True) # 신호 1 발생
        time.sleep(0.00001)
        GPIO.output(trig, False) # 신호 0 발생
        while(GPIO.input(echo) == 0):
                pass
        pulse_start = time.time()
        while(GPIO.input(echo) == 1):
                pass
        pulse_end = time.time() # 신호 0. 초음파 수신 완료를 알림

        pulse_duration = pulse_end - pulse_start
        return 340*100/2*pulse_duration

#조로센서로부터 조도값 리턴
def getMcp():
        return mcp.read_adc(0)
