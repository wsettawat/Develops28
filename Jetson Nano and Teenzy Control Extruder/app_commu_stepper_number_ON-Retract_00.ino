#define LED_1_PIN 6

#define dirPin 2
#define stepPin 3
#define stepsPerRevolution 1600 //360/(1.8/(1/8))

#include <math.h>
String data;

float new_data;
float current_data;
float previous_data;
float reset_data;

float test_data;
float reset_data1 = -10;

float spin_data ;
int estimate_data;

float ahigh = 582;
float alow = 0; 


void setup() {
  Serial.begin(250000); // speed of data between arduino and jetson
  pinMode(LED_1_PIN,OUTPUT);

  //Declare pins as output:
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
}




void reverse()//counterclockwise
{

    spin_data = (current_data)*582 + alow ;


    estimate_data = round(spin_data );

//digitalWrite(LED_1_PIN,HIGH);
//      delay(500);
//      digitalWrite(LED_1_PIN,LOW);
//      delay(500);
//       
//      digitalWrite(LED_1_PIN,HIGH);
//      delay(500);
//      digitalWrite(LED_1_PIN,LOW);
//      delay(500); 
//

      digitalWrite(dirPin, HIGH);//spin counterclockwise
      for (int i =0; i<estimate_data; i++)//spin counterclockwise amount 5 rounds
      {
        // These four line result in 1 steps:
        digitalWrite(stepPin, HIGH);
        delayMicroseconds(500);//0.5ms
        digitalWrite(stepPin,LOW);
        delayMicroseconds(500);
      }
      delay(250);
}




void forward()//clockwise
{

    spin_data = (current_data)*ahigh + alow ;

    estimate_data = round(spin_data );
 //set the spinning direction clockwise: //spin clockwise 1600 stepsPerRevolutiom in 1 round
//      digitalWrite(LED_1_PIN,HIGH);
//      delay(500);
//      digitalWrite(LED_1_PIN,LOW);
      delay(250);
      digitalWrite(dirPin,LOW);// spin clockwise

      //Spin the stepper motor 1 revolution slowly:
      for (int i =0; i<10*stepsPerRevolution; i++)//spin clockwise amount 20 rounds    
      {
        //These four lines result in 1 step:
        digitalWrite(stepPin, HIGH);
        delayMicroseconds(2400);//0.1ms
        digitalWrite(stepPin, LOW);
        delayMicroseconds(2400);//0.1ms

        if(i == estimate_data )
      { 
      break;
      //delay(250);

      }
  
}
}

void sf()//clockwise
{
 // String data = Serial.readStringUntil('\n');

//set the spinning direction clockwise: //spin clockwise 1600 stepsPerRevolutiom in 1 round
//      digitalWrite(LED_1_PIN,HIGH);
//      delay(500);
//      digitalWrite(LED_1_PIN,LOW);
//      delay(500);
      digitalWrite(dirPin,LOW);// spin clockwise

      //Spin the stepper motor 1 revolution slowly:
      for (int i =0; i<1*stepsPerRevolution; i++)//spin clockwise amount 20 rounds    
      {
        //These four lines result in 1 step:
        digitalWrite(stepPin, HIGH);
        delayMicroseconds(1300);//0.1ms
        digitalWrite(stepPin, LOW);
        delayMicroseconds(1300);//0.1ms
      
      
      
      if (data =="OFF")
      {
      break;
      delay(250);
        reverse();
      
      }
  
}
}

void super_f()//clockwise
{
 // String data = Serial.readStringUntil('\n');

//set the spinning direction clockwise: //spin clockwise 1600 stepsPerRevolutiom in 1 round
//      digitalWrite(LED_1_PIN,HIGH);
//      delay(500);
//      digitalWrite(LED_1_PIN,LOW);
//      delay(500);
    current_data = +(current_data);

    spin_data = (current_data)*ahigh + alow ;

    estimate_data = round(spin_data );

    
      digitalWrite(dirPin,LOW);// spin clockwise
      
       previous_data = new_data;
       test_data = new_data + 2.1;

//        String data = Serial.readString();
//
//    //float data = Serial.read() - '0';
//    Serial.print("You sent me: ");    
//    Serial.println(data);
//    new_data  = data.toFloat();
      //Spin the stepper motor 1 revolution slowly:
      for (int i =0; i<estimate_data; i++)//spin clockwise amount 20 rounds    
      {
        //These four lines result in 1 step:
        digitalWrite(stepPin, HIGH);
        delayMicroseconds(2400);//0.1ms   1300ms  foe cube 150
        digitalWrite(stepPin, LOW);
        delayMicroseconds(2400);//0.1ms
      
        // String data = Serial.readString();
//
//      
     //Serial.print("You sent me: ");    
     // Serial.println(data);
     //new_data  = data.toFloat();
      
      
      if (new_data < previous_data)
      {
      break;
      delay(250);
      current_data = -(current_data);
        reverse();
        previous_data = new_data;
        Serial.print("re");
        digitalWrite(LED_1_PIN,HIGH);
       delay(500);
      digitalWrite(LED_1_PIN,LOW);
      delay(500);
      
      }
      else if (current_data < reset_data1)
      {
        break;
        delay(250);
         current_data  = new_data;
         previous_data = new_data;
        
      }
      }

}


void ul_f()
{


      if (current_data < reset_data1)
    {
    current_data  = new_data;
 //   forward();
    previous_data = new_data;
    }
    else if (new_data > previous_data)
    {
     // digitalWrite(LED_1_PIN,HIGH);
     // delay(500);
      //digitalWrite(LED_1_PIN,LOW);
     // delay(500);
      current_data = +(current_data);
      forward();
      previous_data = new_data; 
     
    }
    else if (new_data < previous_data)
    {
      current_data = -(current_data);
      reverse();
      previous_data = new_data; 
    }
}

void loop() {
//    digitalWrite(LED_1_PIN,HIGH);
//    delay(500);
//    digitalWrite(LED_1_PIN,LOW);
//    delay(500);


  
  if (Serial.available() > 0){
    
    String data = Serial.readString();

    //float data = Serial.read() - '0';
    Serial.print("You sent me: ");    
    Serial.println(data);
    new_data  = data.toFloat();
    test_data = new_data + 2.1;
    //Serial.print("You sent me: ");    
    //Serial.println(test_data);
    current_data = new_data - previous_data;

   //super_f();
   ul_f();

//    spin_data = 50*(current_data);
//
//    estimate_data = round(spin_data );
    //Serial.print("You sent me: ");  
   

//    if (current_data < reset_data1)
//    {
//    current_data  = new_data;
// //   forward();
//    previous_data = new_data;
//    }
//    else if (new_data > previous_data)
//    {
//     // digitalWrite(LED_1_PIN,HIGH);
//     // delay(500);
//      //digitalWrite(LED_1_PIN,LOW);
//     // delay(500);
//      current_data = +(current_data);
//      forward();
//      previous_data = new_data; 
//     
//    }
//    else if (new_data < previous_data)
//    {
//      current_data = -(current_data);
//      reverse();
//      previous_data = new_data; 
//    }
    
    

    
                               }
}
