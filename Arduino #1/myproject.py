import sounddevice as sd
import numpy as np
import serial
import time

max_volume = 0
prev_val = 0
fall =  False
code = ""

ser = serial.Serial('COM5', 9600)
time.sleep(1)

def print_sound(indata, outdata, frames, time, status):
    volume_norm = np.linalg.norm(indata)*10
    global prev_val
    global max_volume
    global fall
    global code
    if max_volume<volume_norm:
      max_volume=int(volume_norm)
    if volume_norm > 22 and volume_norm > prev_val and fall == False:
      prev_val = volume_norm
    if volume_norm-prev_val<0:
      fall = True
      if prev_val>65:
         print('G')
         code=code+'G'
         prev_val = 0
      elif prev_val>22:
         print('R')
         code=code+'R'
         prev_val = 0
    if fall == True and volume_norm<11:
      fall = False
    print(int(volume_norm))

with sd.Stream(callback=print_sound):
    sd.sleep(5000)

print(max_volume)
print(code)

ser.reset_input_buffer()
if ser.readline().decode("utf-8")[0]=='1':
   with open("password.txt", 'w') as file:
      file.write(code)
      print(ser.readline().decode("utf-8"))
      file.close()
else:
   with open("password.txt", 'r') as file:
      if file.read()==code:
         ser.write(b'1')
      else:
         ser.write(b'0')
      file.close()



