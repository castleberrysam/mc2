// ATMEGA pins PD2-7
#define DB0   2 // addr[0]
#define DB1   3 // addr[1]
#define DB2   4 // addr[2]
#define DB3   5 // addr[3]
#define DB4   6 // addr[4]
#define DB5   7 // addr[5]

// ATMEGA pins PB0-2,4-5
#define DB6   8  // addr[6]
#define DB7   9  // addr[7]
#define P20   10 // addr[8]
#define P21   12 // addr[9]
#define P22   13 // addr[10]

// ATMEGA pins PC0-1
#define RESET A0
#define EA    A1
#define T0    A2

#define DMASK 0xfc
#define BMASK 0x37
#define CMASK 0x07

void setup() {
  // set RESET, T0, EA to output low
  PORTC &= ~CMASK;
  DDRC |= CMASK;

  // observe setup time
  delayMicroseconds(25);

  // configure timer 2 to output a 4MHz signal on pin 11
  TCCR2A = _BV(COM2A0) | _BV(WGM21) | _BV(WGM20);
  TCCR2B = _BV(WGM22) | _BV(CS20);
  OCR2A = 0x01;
  pinMode(11, OUTPUT);

  // start serial and wait for input
  Serial.begin(1000000);
  Serial.flush();
  while(!Serial.available());
  
  // apply 18V to EA
  digitalWrite(EA, HIGH);
  delay(7);

  for(int addr=0;addr<2048;++addr) {
    // output addr on bus
    PORTD = (byte) ((addr << 2) | (PORTD & 0x03));
    PORTB = (byte) ((PORTB & 0xc8) | ((addr & 0x0600) >> 5) | ((addr & 0x01c0) >> 6));
    DDRD |= DMASK;
    DDRB |= BMASK;

    // observe setup time
    delayMicroseconds(25);

    // raise RESET
    digitalWrite(RESET, HIGH);

    // observe hold time
    delayMicroseconds(25);
    
    // switch to inputs
    DDRD &= ~DMASK;
    DDRB &= ~BMASK;
    PORTD &= ~DMASK;
    PORTB &= ~BMASK;

    // raise T0
    digitalWrite(T0, HIGH);

    // observe hold time
    delayMicroseconds(25);

    // read data and send over serial
    unsigned char data = (unsigned char) ((PIND >> 2) | (PINB << 6));
    if(data < 16) {Serial.write('0');}
    Serial.print(data, HEX);

    // lower T0
    digitalWrite(T0, LOW);
    
    // lower RESET
    digitalWrite(RESET, LOW);
  }

  // lower EA
  digitalWrite(EA, LOW);
  delay(4);

  // disable timer 2
  pinMode(11, INPUT);
}

void loop() {}

