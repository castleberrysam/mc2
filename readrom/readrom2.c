#include "PLL.h"
#include "UART.h"
#include "tm4c123gh6pm.h"

extern void msleep(int millis);
extern void usleep(int micros);

// D0-1 on PD0-1
// D2-7 on PB2-7
// D8-13 on PE0-5
// D14-15 on PD6-7

// A0-5 on PA2-7
// A6-9 on PC4-7
// A10-11 on PB0-1
// A12-13 on PD2-3
// A14 on PF0
// A15 on PF4

// BUS_ACK on PF1
// BUS_REQ on PF2
// CLK on PF3
void init(void)
{
  PLL_Init(Bus80MHz);
  UART_Init();

  SYSCTL_RCGCGPIO_R |= 0x3f;
  __asm("nop; nop");

  GPIO_PORTA_LOCK_R = GPIO_LOCK_KEY;
  GPIO_PORTB_LOCK_R = GPIO_LOCK_KEY;
  GPIO_PORTC_LOCK_R = GPIO_LOCK_KEY;
  GPIO_PORTD_LOCK_R = GPIO_LOCK_KEY;
  GPIO_PORTE_LOCK_R = GPIO_LOCK_KEY;
  GPIO_PORTF_LOCK_R = GPIO_LOCK_KEY;

  GPIO_PORTA_CR_R = 0xfc;
  GPIO_PORTB_CR_R = 0xff;
  GPIO_PORTC_CR_R = 0xf0;
  GPIO_PORTD_CR_R = 0xff;
  GPIO_PORTE_CR_R = 0xff;
  GPIO_PORTF_CR_R = 0xff;

  GPIO_PORTB_DIR_R &= ~0xfc;
  GPIO_PORTD_DIR_R &= ~0xc3;
  GPIO_PORTE_DIR_R &= ~0x3f;
  GPIO_PORTF_DIR_R &= ~0x02;

  GPIO_PORTA_DIR_R |= 0xfc;
  GPIO_PORTB_DIR_R |= 0x03;
  GPIO_PORTC_DIR_R |= 0xf0;
  GPIO_PORTD_DIR_R |= 0x0c;
  GPIO_PORTF_DIR_R |= 0x1d;

  GPIO_PORTA_AFSEL_R &= ~0xfc;
  GPIO_PORTB_AFSEL_R &= ~0xff;
  GPIO_PORTC_AFSEL_R &= ~0xf0;
  GPIO_PORTD_AFSEL_R &= ~0xcf;
  GPIO_PORTE_AFSEL_R &= ~0x3f;
  GPIO_PORTF_AFSEL_R &= ~0x1f;

  // Set PUR/PDR registers to read 'beef' when D0-15 are floating.
  GPIO_PORTB_PUR_R |= 0xec;
  GPIO_PORTD_PUR_R |= 0x83;
  GPIO_PORTE_PUR_R |= 0x3e;

  // Bus acknowledge is active low, so pull high.
  GPIO_PORTF_PUR_R |= 0x02;

  GPIO_PORTB_PDR_R |= 0x10;
  GPIO_PORTD_PDR_R |= 0x40;
  GPIO_PORTE_PDR_R |= 0x01;

  GPIO_PORTA_DEN_R |= 0xfc;
  GPIO_PORTB_DEN_R |= 0xff;
  GPIO_PORTC_DEN_R |= 0xf0;
  GPIO_PORTD_DEN_R |= 0xcf;
  GPIO_PORTE_DEN_R |= 0x3f;
  GPIO_PORTF_DEN_R |= 0x1f;
}

void set_addr(unsigned short addr)
{
  addr = ~addr;
  *(GPIO_PORTA_DATA_BITS_R+0xfc) = addr << 2;
  *(GPIO_PORTC_DATA_BITS_R+0xf0) = addr >> 2;
  *(GPIO_PORTB_DATA_BITS_R+0x03) = addr >> 10;
  *(GPIO_PORTD_DATA_BITS_R+0x0c) = addr >> 10;
  *(GPIO_PORTF_DATA_BITS_R+0x01) = addr >> 14;
  *(GPIO_PORTF_DATA_BITS_R+0x10) = addr >> 11;
}

void set_bus_req(int val)
{
  *(GPIO_PORTF_DATA_BITS_R+0x04) = val << 2;
}

int get_bus_ack(void)
{
  return !(*(GPIO_PORTF_DATA_BITS_R+0x02) >> 1);
}

void toggle_clk(unsigned cycles)
{
  for(unsigned i=0;i<cycles;++i) {
    *(GPIO_PORTF_DATA_BITS_R+0x08) = 0x08;
    usleep(1);
    *(GPIO_PORTF_DATA_BITS_R+0x08) = 0x00;
    usleep(1);
  }
}

unsigned short get_data(void)
{
  int data = *(GPIO_PORTD_DATA_BITS_R+0x03);
  data |= *(GPIO_PORTB_DATA_BITS_R+0xfc);
  data |= *(GPIO_PORTE_DATA_BITS_R+0x3f) << 8;
  data |= *(GPIO_PORTD_DATA_BITS_R+0xc0) << 8;
  return (unsigned short) data;
}

char to_hex_digit(unsigned value) {
  value &= 15;
  if(value > 9) {value += ('a' - '9' - 1);}
  return '0' + value;
}

void print_hex(unsigned short value) {
  UART_OutChar(to_hex_digit(value >> 12));
  UART_OutChar(to_hex_digit(value >> 8));
  UART_OutChar(to_hex_digit(value >> 4));
  UART_OutChar(to_hex_digit(value));
}

int main(void)
{
  init();
  msleep(3000);

  UART_OutString("Reading ROM data:\n");
  unsigned addr = 0x4000;
  do {
    set_addr(addr);
    set_bus_req(1);
    do {toggle_clk(1);} while(!get_bus_ack());
    
    print_hex(get_data());
    
    set_bus_req(0);
    toggle_clk(2);
  } while(++addr < 0x10000);
  UART_OutString("\nFinished.\n");

  while(1) {}
}
