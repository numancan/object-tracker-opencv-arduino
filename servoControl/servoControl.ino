#include <Servo.h>

Servo servo;
byte servoDegree=90;

void setup() 
{

  Serial.begin(9600);
  servo.attach(9);
  
  // Servoyu başlangıç pozisyonuna getiriyoruz
  servo.write(servoDegree);

}

void loop() {

 if(Serial.available())
  {
    switch(Serial.read())
    {
      case '0' : 
        servoDegree-=2;
        if(servoDegree<0)
        {
          servoDegree=0;
        }
        break;

      case '1' : 
        servoDegree+=2;
        if(servoDegree>180)
        {
          servoDegree=180;
        }
        break;
    }
  }

  servo.write(servoDegree);
  delay(1);
}
