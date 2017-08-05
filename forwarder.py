import serial, time, requests
import smtplib
import datetime


DELAY = 15

arduino = serial.Serial('COM3', 9600, timeout=2.0)
i=0

def get_value(arduino, value):
    #tim = datetime.datetime.now().time()
    text = "[" + value + "]\n"
    bytes = text.encode("latin-1")
    print("Writing " + text)
    arduino.write(bytes)
    while True:
        bytes = arduino.readline() 
        text = bytes.decode("utf-8").strip()
        if text != "?":
            text = text.replace("[","")
            text = text.replace("]","")
            text = text.replace(value,"")
            text = text.replace("=","")
            return float(text)
 
def post_to_stream(stream,
                   userid, ti, 
                   lat, lon, 
                   temp):
    url = "http://drdelozier.pythonanywhere.com/stream/store/"
    payload = {
        'userid': str(userid),
        #'city': str(city),
        #'state': str(state),
        #'ti': str(tim),
        'lat': str(lat),
        'lon': str(lon),
        'temp': str(temp),
        #'color': str(color),
        #'light': str(light),
        #'outdoors': str(outdoors),
    }
    response = requests.get(url + stream, params=payload)
    print(response.status_code)
    print(response.url)
    print(response.text)

time.sleep(3)
clock = time.time()
while True:
   temp = get_value(arduino,"TEMP")
   if temp > 10:
       i = i + 1
   color = get_value(arduino,"color")
   if i>4 :
       s = smtplib.SMTP('smtp.gmail.com', 587)

       s.starttls()

       s.login('*****************@gmail.com','***********')

       message = "Take care of me !!."

       s.sendmail("******************@gmail.com","*********@gmail.com",message)

       i=0

   print(temp)

   post_to_stream("datam", "amuthava", datetime.datetime.now().time(), 
                   41, -81, temp)
   
   while time.time() < clock + DELAY:
       time.sleep(0.5)
   clock = clock + DELAY 