import wiotp.sdk.device
import time
import random
myConfig = { 
    "identity": {
        "orgId": "glif1g",
        "typeId": "sarahdevice",
        "deviceId":"060801"
    },
    "auth": {
        "token": "06082001"
    }
}
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import playsound
 
authenticator = IAMAuthenticator('PjC0bvAGJ1nFseEZGlUNUfZjO9ntqUkrYdFwS065OWVa')
text_to_speech = TextToSpeechV1(
    authenticator=authenticator
)
 
text_to_speech.set_service_url('https://api.eu-gb.text-to-speech.watson.cloud.ibm.com/instances/761a99f7-59be-443f-9106-ddce29442f5f')
 
 
def myCommandCallback(cmd):
    print("Message received from IBM IoT Platform: %s" % cmd.data['command'])
    m=cmd.data['command']
 
client = wiotp.sdk.device.DeviceClient(config=myConfig, logHandlers=None)
client.connect()
 
while True:
    fooditems={"i1":{"item":"chicken biriyani","price":100},"i2":{"item":"chicken noodles","price":120},"i3":{"item":"chicken friedrice","price":130},
                 "i4":{"item":"veg biriyani","price":100},"i5":{"item":"veg noodles","price":110},"i6":{"item":"egg biriyani","price":125}}
    myData={'fooditems':fooditems}
    client.publishEvent(eventId="status", msgFormat="json", data=myData, qos=0, onPublish=None)
#sending the data to IBM IoT platform which will store the menu card in the cloudant
    print("Published data Successfully: %s", myData)
    client.commandCallback = myCommandCallback
    time.sleep(2)
    break
client.disconnect()
 
def myCommandCallback(cmd):
#receiving the data from the IBM IoT platform which will be recieving the order placed from the MIT App
print("Food order received from IBM IoT Platform: %s" % cmd.data['order_qty'])
with open('order.mp3', 'wb') as audio_file:
#voice command of the order placed
    audio_file.write(
        text_to_speech.synthesize(
            cmd.data['order_qty'],
            voice='en-US_AllisonV3Voice',
            accept='audio/mp3'        
        ).get_result().content)
    playsound.playsound('order.mp3')
 
client = wiotp.sdk.device.DeviceClient(config=myConfig, logHandlers=None)
client.connect()
while True:
client.commandCallback = myCommandCallback
time.sleep(2)
client.disconnect()
 
