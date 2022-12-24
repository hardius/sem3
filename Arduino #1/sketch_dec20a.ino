char signal;

bool SetCode = false;
void setup() {
  pinMode(2, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(8, INPUT_PULLUP);
  Serial.begin(9600);
}

void loop() {

  if(digitalRead(8)==0)
  {
    SetCode=!SetCode;
    digitalWrite(2, LOW);
    digitalWrite(4, LOW);
    digitalWrite(7, SetCode);
  }
  
  if(SetCode==0)
  {
    Serial.println("0");
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
    Serial.println("1");
  }
  delay(150);
}
