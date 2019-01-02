#include <stdint.h>

uint16_t ram[0x4000];
const uint16_t rom[0xc000];

uint16_t rd(uint16_t addr)
{
  return (addr < 0x4000) ? ram[addr] : rom[addr-0x4000];
}

void wr(uint16_t addr, uint16_t val)
{
  if(addr < 0x4000) {ram[addr] = val;}
}

uint16_t sp = 0;
#define psh(val) wr(--sp, val)
#define pop(var) (var = rd(sp++);)

#define r0 r[0]
#define r1 r[1]
#define r2 r[2]
#define r3 r[3]
#define r4 r[4]
#define r5 r[5]
#define r6 r[6]
#define r7 r[7]

// address 0xa082
void sub_a082(uint16_t *r)
{
  uint16_t test_var;
  
  psh(r2);
  psh(r5);
  psh(r4);
  psh(r7);
  psh(r6);
  
  do {
    psh(r3);
    r6 = rd(r0++);

    if((r6 & 0xf000) != 0) {
      if((r6 & 0x0200) == 0) {r3 = r2;}

      r7 = (r6 & 0x01ff) - 0x20 + r3;
      r3 = r6 >> 8;
      if(r3 < 0xc0) {
        r6 = rd(r7);
        r7 = rd(r7+1);
      }

      sub_a0ce();
    } else {
      r3 = (r6 >> 8) | (r6 << 8);
      if((r6 & 0x0100) != 0) {
        pop(r7); // r3 from start of loop
        pop(r6); // r6 from entry
        psh(r6);
        psh(r7);

        psh(r5);

        if((r3 & 0x0002) != 0) {r6 = r7;}

        r5 = (r3 >> 8) & 0xf;
        r7 = r3 >> 8;
        if(r7 < 0xc0) {
          r7 &= 0xfff0;
          r3 |= r7;
          
          mem_rd16();
          psh(r7);
          
          mem_rd16();
          
          pop(r6);
          pop(r5);
          sub_a0ce();
        } else {
          r7 = r4;
          mem_wr16();

          pop(r7);
          mem_wr16();

          r5 = r7;
        }
      } else {
        r7 = (r6 >> 4) & 0xf;
        if(r7 != 0) {
          r7 = r0;
          r0 += 2;
          r3 |= r6 & 0xff;

          r6 = rd(r7);
          r7 = rd(r7+1);

          sub_a0ce();
        } else {
          xchg32();
          sub_a0c0();
          xchg32();
        }
      }
    }

    r6 = r3 & 0x0c;
    pop(r3);
  } while(r6 == 0);

  if(r6 <= 4) {
    pop(r6);
    pop(r7);
    pop(r2);
    pop(r2);
    pop(r2);

    if(r4 == 0) {
      asm("\tcmpri r5, 0\n");
      asm("\trbit r1, r1(N)\n");
    }

    return;
  }

  xchg32();
  test_var = r4 & 0x0004;
  pop(r2);
  pop(r2);
  pop(r4);
  pop(r5);
  pop(r2);
  
  if(test_var == 0) {
    i32_setcc();
    return;
  }

  psh(r5);
  r5 = rd(r0);
  wr(r2-1, r5);
  r0 += 1;
  pop(r5);

  psh_034567();
  f32_base10();
  f32_width();

  r0 = rd(r2-1);
  psh(r4);
  r4 = (r0 >> 8) - r4;
  if(((int16_t) r4) < 0) {
    pop(r4);
    math_fuzz();
  } else {
    math_clear();
    pop(r4);
    math_fmt_f32();
  }

  pop(r7);
  pop(r6);
  pop(r5);
  pop(r4);
  pop(r3);
  pop(r0);
}
