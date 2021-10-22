#include <SPI.h>
#include <Servo.h> 

Servo servo1; //axe central
Servo servo2; //axe gauche
Servo servo3; //axe droite

void setup() {
    //Initialize serial and wait for port to open:
    Serial.begin(9600); 
    while (!Serial) {
        ; // Attend que le port soit connecté
    }
    servo1.attach(4);
    servo2.attach(3);
    servo3.attach(5);
    servo1.write(0);
    servo2.write(0);
    servo3.write(0);
}

void print_letter_using_servo_motors(String my_string){
    if (my_string == "A" )   {servo1.write(90); servo2.write(0); servo3.write(179);delay(1000);}
    else if (my_string == "B" )   {servo1.write(45); servo2.write(0); servo3.write(179);delay(1000);}
    else if (my_string == "C" )   {servo1.write(0); servo2.write(0); servo3.write(179);delay(1000);}
    else if (my_string == "D" )   {servo1.write(135); servo2.write(179); servo3.write(0);delay(1000);}
    else if (my_string == "E" )   {servo1.write(90); servo2.write(179); servo3.write(0);delay(1000);}
    else if (my_string == "F" )   {servo1.write(45); servo2.write(179); servo3.write(0);delay(1000);}
    else if (my_string == "G" )   {servo1.write(0); servo2.write(179); servo3.write(0);delay(1000);}
    else if (my_string == "H" )   {servo1.write(135); servo2.write(0); servo3.write(179);delay(1000);}
    else if (my_string == "I" )   {servo1.write(90); servo2.write(0); servo3.write(0);delay(1000);}
    else if (my_string == "J" )   {servo1.write(90); servo2.write(0); servo3.write(0);delay(1000);}
    else if (my_string == "K" )   {servo1.write(45); servo2.write(0); servo3.write(0);delay(1000);}
    else if (my_string == "L" )   {servo1.write(0); servo2.write(0); servo3.write(0);delay(1000);}
    else if (my_string == "M" )   {servo1.write(135); servo2.write(0); servo3.write(0);delay(1000);}
    else if (my_string == "N" )   {servo1.write(90); servo2.write(179); servo3.write(179);delay(1000);}
    else if (my_string == "O" )   {servo1.write(45); servo2.write(179); servo3.write(179);delay(1000);}
    else if (my_string == "P" )   {servo1.write(0); servo2.write(179); servo3.write(179);delay(1000);}
    else if (my_string == "Q" )   {servo1.write(135); servo2.write(179); servo3.write(179);delay(1000);}
    else if (my_string == "R" )   {servo1.write(90); servo2.write(90); servo3.write(179);delay(1000);}
    else if (my_string == "S" )   {servo1.write(45); servo2.write(90); servo3.write(179);delay(1000);}
    else if (my_string == "T" )   {servo1.write(0); servo2.write(90); servo3.write(179);delay(1000);}
    else if (my_string == "U" )   {servo1.write(135); servo2.write(179); servo3.write(90);delay(1000);}
    else if (my_string == "V" )   {servo1.write(90); servo2.write(179); servo3.write(90);delay(1000);}
    else if (my_string == "W" )   {servo1.write(45); servo2.write(179); servo3.write(90);delay(1000);}
    else if (my_string == "X" )   {servo1.write(0); servo2.write(179); servo3.write(90);delay(1000);}
    else if (my_string == "Y" )   {servo1.write(135); servo2.write(90); servo3.write(179);delay(1000);}
    else if (my_string == "Z" )   {servo1.write(90); servo2.write(0); servo3.write(90);delay(1000);}
    else if (my_string == "&" )   {servo1.write(45); servo2.write(0); servo3.write(90);delay(1000);}
    else if (my_string == "1" )   {servo1.write(0); servo2.write(0); servo3.write(90);delay(1000);}
    else if (my_string == "2" )   {servo1.write(135); servo2.write(90); servo3.write(0);delay(1000);}
    else if (my_string == "3" )   {servo1.write(90); servo2.write(90); servo3.write(0);delay(1000);}
    else if (my_string == "4" )   {servo1.write(45); servo2.write(90); servo3.write(0);delay(1000);}
    else if (my_string == "5" )   {servo1.write(0); servo2.write(90); servo3.write(0);delay(1000);}
    else if (my_string == "6" )   {servo1.write(135); servo2.write(0); servo3.write(90);delay(1000);}
    else if (my_string == "7" )   {servo1.write(90); servo2.write(90); servo3.write(90);delay(1000);}
    else if (my_string == "8" )   {servo1.write(45); servo2.write(90); servo3.write(90);delay(1000);}
    else if (my_string == "9" )   {servo1.write(0); servo2.write(90); servo3.write(90);delay(1000);}
    else if (my_string == "10" )   {servo1.write(135); servo2.write(90); servo3.write(90);delay(1000);}
    else {Serial.println("Ce string n'est pas pris en compte dans le code Chappe: " & my_string);}
}


void loop() {
    String secret_sentence = "bonjourtoutlemonde";
    for (int i=0; i <= secret_sentence.length(); i++){
        String my_string;
        my_string = secret_sentence[i];
        Serial.println(my_string);
        print_letter_using_servo_motors(my_string);
    }
}


