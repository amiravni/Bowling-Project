
unsigned long time1 = 0;
unsigned long time2 = 0;
double sensorGapInM = 0.1; 


void setup() {                
  // initialize the digital pin as an output.
  pinMode(13,OUTPUT);
   attachInterrupt(0, intfunc1, FALLING);
   attachInterrupt(1, intfunc2, FALLING);
    Serial.begin(9600);
}

void loop() {

  if (time1>0 && time2>0 && time2>time1 )
  {
    double velocity = 3.6 * ( sensorGapInM ) /  (((double)time2 - (double)time1) / 1000.0);
    Serial.println(velocity);
    time1=0;
    time2=0;
  }
  
}

void changeState(int pin) {
  if (digitalRead(pin))
      digitalWrite(pin,LOW);
  else
      digitalWrite(pin,HIGH);
  
}

void intfunc1() {
  time1 = millis();
  changeState(13); 
}

void intfunc2() {
  time2 = millis();
  changeState(13);
}


