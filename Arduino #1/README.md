# Запуск устройства
1. Подключаем устройство к компьютеру и запускаем программу на python'e.

2. После запуска, если вы хотите перейти в режим установки пароля, то нажмите на кнопку на макетной плате. Горящий желтый светодиод означает, что вы в режиме установки пароля.
После того, как нажали на кнопку, введите пароль комбинацией стуков. Стуки различаются по громкости: стук ногтем или обычный стук.

	![picture](https://sun9-54.userapi.com/impg/aifcsYRmRBXWFx9A6V0YcrNutHB_9edrTcxjAg/NHv9D7LFUEU.jpg?size=202x270&quality=96&sign=22a026b8415cd931bde27bee51408fc6&type=album)

3. После того, как вы ввели пароль, он сохраняется в текстовом файле *password.txt*.

	**G** - это обычный стук.

	**R** - это стук ногтем.

	![password](https://sun9-79.userapi.com/impg/xt_rHKpZYdzdcDBRlF1yr5sekAHNzEoxk_bxOw/nvvRtPG4SVk.jpg?size=345x204&quality=96&sign=60f8252c81230d548b98629dbfc5e9e0&type=album)

4. Если вы не нажали кнопку, то вы будете режиме ввода пароля. После ввода пароль сверяется с тем, что в текстовом файле, и при совпадении загорается зеленый светодиод. В противном же случае красный.
	
	![picture1](https://sun9-10.userapi.com/impg/xnxovtukWA-gn7YY7hznAeUlDDa_mcSa2dAxgw/KFrOcvF6IcU.jpg?size=405x540&quality=95&sign=468aaa41a3fe2f9e3f85efbcf29e3b4f&type=album)
	![picture2](https://sun9-88.userapi.com/impg/K6VeT9rQfhbUzaApfZHuUys0REWV6wTJhzcx9A/Wx3ZL5DGvYA.jpg?size=405x540&quality=95&sign=630fd28cf63fb67f7d6bd60c2caddf9b&type=album)
	
# Как это работает?

При запуске начинается запись звука с микрофона ноутбука. Запись идет только *5 секунд*. За это время нужно ввести пароль, а если вы хотите поменять пароль, то нужно успеть и нажать на кнопку, и ввести пароль.

~~~C++
if(digitalRead(8)==0)
  {
    SetCode=!SetCode;
    digitalWrite(2, LOW);
    digitalWrite(4, LOW);
    digitalWrite(7, SetCode);
  }
  
  if(SetCode==0)
  {
    Serial.println("0"); // непрерывно выводится 0, если кнопку не нажали
    if(Serial.available()){
     signal=Serial.read();
     if(signal=='1')
     {
       digitalWrite(4, HIGH);
     }
     else
     {
       digitalWrite(2, HIGH);
     }
    }

  }
  else
  {
    Serial.println("1"); // непрерывно выводится 1, если кнопку нажали
  }
~~~

В зависимости от того, нажали ли вы кнопку или нет, в буфере будет постоянно выводиться значение, либо 0, либо 1.

#

Происходящее в консоли - это фиксация звука, записываемого с микрофона компьютера. Тут числа в столбике означают громкость звука.

![sound](https://sun9-77.userapi.com/impg/ExpoqJXdOTkO0ykxk-yAs8jkzjzLxKQhYswhPw/PyDtiAF2hiI.jpg?size=185x339&quality=96&sign=2fe8d6530809690e239416eeee5603cd&type=album)

Когда раздается стук, числа возрастают, а потом убывают. Из этой области берется максимальное число.

![knock](https://sun9-29.userapi.com/impg/HTpsmCcilsEG1kQxZe1QzobsC5_VA7x82RWzYQ/wj7xXhFxunc.jpg?size=162x215&quality=96&sign=a63983feaf6f29d031f1b0d51b3111b8&type=album)

Максимальное значение находится, когда фиксируется убывание, а точнее, когда предыдущее значение оказывается больше, чем текущее.

~~~python
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
~~~

Если максимальное значение находится в диапазоне от 22 до 65, то программа определяет звук как стук ногтем и добавляет символ 'R' в строковую переменную ***code***.

Если число выше 65, то звук определяется как обычный стук и добавляет символ 'G' в ***code***.

#

Далее буфер с 0 и 1(0 - режим ввода пароль, 1 - режим смены пароля) очищается, чтобы программа на python'e не считала оттуда другое значение. И т.к. туда всё равно непрерывно выводятся значения, то программа считает именно текущее значение, а не то, которое было до.

В зависимости от считанного значения программа, либо записывает введенный пароль в текстовый файл, либо сверяет его с текстовым файлом.

~~~python
ser.reset_input_buffer() # очищается буфер
if ser.readline().decode("utf-8")[0]=='1': # считывается текущее значение с буфера
   with open("password.txt", 'w') as file:
      file.write(code)
      print(ser.readline().decode("utf-8"))
      file.close()
else:
   with open("password.txt", 'r') as file:
      if file.read()==code:
         ser.write(b'1') # передаёт единицу, означающую, что пароль введен верно.
      else:
         ser.write(b'0') # передаёт ноль, что значит, что пароль неверен.
      file.close()
~~~

#
~~~С++
  if(Serial.available()){
     signal=Serial.read(); // считывает значение, переданное программой на python'e
     if(signal=='1') // если это единица, то зажигается зеленый светодиод
     {
       digitalWrite(4, HIGH);
     }
     else // в противном случае зажигается красный светодиод
     {
       digitalWrite(2, HIGH);
     }
~~~
