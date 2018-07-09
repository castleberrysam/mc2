#include "PLL.h"
#include "UART.h"
#include "tm4c123gh6pm.h"

extern void msleep(int millis);
extern void usleep(int micros);

// D0-7 on PB0-7
// A0-5 on PE0-5
// A6-11 on PA2-7
void init(void)
{
  PLL_Init(Bus80MHz);
  UART_Init();
  
  SYSCTL_RCGCGPIO_R |= 0x13;
  __asm("nop; nop");

  GPIO_PORTB_LOCK_R = GPIO_LOCK_KEY;
  GPIO_PORTE_LOCK_R = GPIO_LOCK_KEY;
  GPIO_PORTA_LOCK_R = GPIO_LOCK_KEY;

  GPIO_PORTB_CR_R = 0xff;
  GPIO_PORTE_CR_R = 0x3f;
  GPIO_PORTA_CR_R = 0xfc;

  GPIO_PORTB_DIR_R &= ~0xff;
  GPIO_PORTE_DIR_R |= 0x3f;
  GPIO_PORTA_DIR_R |= 0xfc;

  GPIO_PORTB_AFSEL_R &= ~0xff;
  GPIO_PORTE_AFSEL_R &= ~0x3f;
  GPIO_PORTA_AFSEL_R &= ~0xfc;

  GPIO_PORTB_PDR_R |= 0xff;
  
  GPIO_PORTB_DEN_R |= 0xff;
  GPIO_PORTE_DEN_R |= 0x3f;
  GPIO_PORTA_DEN_R |= 0xfc;
}

void set_addr(int addr)
{
  *(GPIO_PORTE_DATA_BITS_R+0x3f) = addr;
  *(GPIO_PORTA_DATA_BITS_R+0xfc) = addr >> 4;
}

unsigned char get_data(void)
{
  return (unsigned char) GPIO_PORTB_DATA_R;
}

unsigned char to_hex_digit(unsigned char value) {
  if(value > 9) {value += ('a' - '9' - 1);}
  return '0' + value;
}

void print_hex(unsigned char value) {
  UART_OutChar(to_hex_digit(value >> 4));
  UART_OutChar(to_hex_digit(value & 0xf));
}

int main(void)
{
  init();
  msleep(3000);

  UART_OutString("Reading ROM data:\n");
  for(int addr=0;addr<0x1000;++addr) {
    set_addr(addr);
    usleep(1);
    print_hex(get_data());
  }
  UART_OutString("\nFinished.\n");

  while(1) {}
}
