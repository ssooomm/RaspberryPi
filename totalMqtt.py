#pub 과 sub 기능을 모두 가진 mqtt
import time
import paho.mqtt.client as mqtt
import totalCircuit #모든 센서들 입력 모듈 임포트
import birdCamera #새얼굴 인식하고 사진 보내기

flag = False # True이면 "action" 메시지를 수신하였음을 나타냄

#외부로부터 명령 받는 부분
def on_connect(client, userdata, flag, rc):
        client.subscribe("led", qos = 0) 
        #client.subscribe("led2", qos = 0)
        client.subscribe("facerecognition", qos=0)

def on_message(client, userdata, msg) :
        global flag
        command = msg.payload.decode("utf-8") #msg 한글로 잘 읽도록
        if command == "action" :
                print("action msg received..")
                flag = True #"action" 메세지 수신해서 사진찍도록

        else:
                msg = int(msg.payload); #msg 정수로 전환
                print(msg)
                totalCircuit.controlLED(msg) # msg는 0 또는 1


broker_ip = "localhost" # 현재 이 컴퓨터를 브로커로 설정

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_ip, 1883)
client.loop_start()

while(True):
        if flag==True : # "action" 메시지 수신. 사진 촬영
                imageFileName = birdCamera.takePicture() # 카메라 사진 촬영
                print(imageFileName)
                client.publish("image", imageFileName, qos=0) #"image"토픽으로 사진 pub
                flag = False
        print("time...", end=" ")
        print(flag)

        distance = totalCircuit.measureDistance() #초음파 거리에 따른 led점멸
        if(distance<15):
                totalCircuit.controlLED2(1) #무언가 가까이 오면 led 점등
        else:
                totalCircuit.controlLED2(0)
        #client.publish("ultrasonic", distance, qos=0) #"ultrasonic"토픽으로 거리 pub

        #temp = totalCircuit.getTemperature()
        hum = totalCircuit.getHumidity() #습도 센서 값 받아옴
       #client.publish("temp", temp, qos=0)
        client.publish("hum", hum, qos=0) #"hum"토픽으로 습도값 pub

        light = totalCircuit.getMcp() #조도 센서 값 받아옴
        if(light>400): #조도값이 높아지면 
                totalCircuit.controlLED(1) #주위가 어두운 것이므로 led점등
        else:
                totalCircuit.controlLED(0)
        time.sleep(1)

client.loop_stop()
client.disconnect()
