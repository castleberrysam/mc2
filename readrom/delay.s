	.syntax	unified
	.arch	armv7e-m
	
	.text
	.thumb
	.align	2
	.globl msleep
	.globl usleep

msleep:
	b	2f

0:	sub	r0, #1
	ldr	r1, =10000

1:	nop
	nop
	nop
	nop
	subs	r1, #1
	bne	1b

2:	cmp	r0, #0
	bne 0b

	bx lr

usleep:
	mov	r1, #10
	mul	r0, r1
	b	3f

4:	nop			/* 1 loop = 8 cycles = 100 ns = 0.1 us */
	nop
	nop
	nop
	subs	r0, #1

3:	bne 4b

	bx lr

	.align
	.end
