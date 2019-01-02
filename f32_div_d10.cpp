// address 0xbace
// exponent in r3
// mantissa in r6r7
// rXrY has rX as most significant word
void f32_div_d10(uint16_t &r3, uint32_t &r6r7) {
  uint16_t r5;
  
  r3 -= 2; // divide by 4
  r5 = r6;
  
  r6r7 = r5 + (0x6666 * r7);
  r6r7 += r6;
  r6r7 = r6 + (0x6666 * r5);
  r6r5 += r6;
  r6r7 += r5;
  
  while(r6[14] == 0) {
    r6r7 <<= 1;
    r3 -= 1;
  }
}
