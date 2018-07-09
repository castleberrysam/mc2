/* File: startup_ARMCM4.S
 * Purpose: startup file for Cortex-M4 devices. Should use with
 *   GCC for ARM Embedded Processors
 * Version: V2.0
 * Date: 16 August 2013
 */
/* Copyright (c) 2011 - 2013 ARM LIMITED

   All rights reserved.
   Redistribution and use in source and binary forms, with or without
   modification, are permitted provided that the following conditions are met:
   - Redistributions of source code must retain the above copyright
     notice, this list of conditions and the following disclaimer.
   - Redistributions in binary form must reproduce the above copyright
     notice, this list of conditions and the following disclaimer in the
     documentation and/or other materials provided with the distribution.
   - Neither the name of ARM nor the names of its contributors may be used
     to endorse or promote products derived from this software without
     specific prior written permission.
   *
   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
   AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
   IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
   ARE DISCLAIMED. IN NO EVENT SHALL COPYRIGHT HOLDERS AND CONTRIBUTORS BE
   LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
   CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
   SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
   INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
   CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
   ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
   POSSIBILITY OF SUCH DAMAGE.
   ---------------------------------------------------------------------------*/
	.syntax	unified
	.arch	armv7e-m

	.section .stack
	.align	3
#ifdef __STACK_SIZE
	.equ	Stack_Size, __STACK_SIZE
#else
	.equ	Stack_Size, 0xc00
#endif
	.globl	__StackTop
	.globl	__StackLimit
__StackLimit:
	.space	Stack_Size
	.size	__StackLimit, . - __StackLimit
__StackTop:
	.size	__StackTop, . - __StackTop

	.section .heap
	.align	3
#ifdef __HEAP_SIZE
	.equ	Heap_Size, __HEAP_SIZE
#else
	.equ	Heap_Size, 0
#endif
	.globl	__HeapBase
	.globl	__HeapLimit
__HeapBase:
	.if	Heap_Size
	.space	Heap_Size
	.endif
	.size	__HeapBase, . - __HeapBase
__HeapLimit:
	.size	__HeapLimit, . - __HeapLimit

	.section .isr_vector
	.align	2
	.globl	__isr_vector
__isr_vector:
	.long	__StackTop            /* Top of Stack */
	.long	Reset_Handler         /* Reset Handler */
	.long	NMI_Handler           /* NMI Handler */
	.long	HardFault_Handler     /* Hard Fault Handler */
	.long	MemManage_Handler     /* MPU Fault Handler */
	.long	BusFault_Handler      /* Bus Fault Handler */
	.long	UsageFault_Handler    /* Usage Fault Handler */
	.long	0                     /* Reserved */
	.long	0                     /* Reserved */
	.long	0                     /* Reserved */
	.long	0                     /* Reserved */
	.long	SVC_Handler           /* SVCall Handler */
	.long	DebugMon_Handler      /* Debug Monitor Handler */
	.long	0                     /* Reserved */
	.long	PendSV_Handler        /* PendSV Handler */
	.long	SysTick_Handler       /* SysTick Handler */
        .long   GPIOPortA_Handler     /* GPIO Port A */
        .long   GPIOPortB_Handler     /* GPIO Port B */
        .long   GPIOPortC_Handler     /* GPIO Port C */
        .long   GPIOPortD_Handler     /* GPIO Port D */
        .long   GPIOPortE_Handler     /* GPIO Port E */
        .long   UART0_Handler         /* UART0 Rx and Tx */
        .long   UART1_Handler         /* UART1 Rx and Tx */
        .long   SSI0_Handler          /* SSI0 Rx and Tx */
        .long   I2C0_Handler          /* I2C0 Master and Slave */
        .long   PWM0Fault_Handler     /* PWM 0 Fault */
        .long   PWM0Generator0_Handler/* PWM 0 Generator 0 */
        .long   PWM0Generator1_Handler/* PWM 0 Generator 1 */
        .long   PWM0Generator2_Handler/* PWM 0 Generator 2 */
        .long   Quadrature0_Handler   /* Quadrature Encoder 0 */
        .long   ADC0Seq0_Handler      /* ADC0 Sequence 0 */
        .long   ADC0Seq1_Handler      /* ADC0 Sequence 1 */
        .long   ADC0Seq2_Handler      /* ADC0 Sequence 2 */
        .long   ADC0Seq3_Handler      /* ADC0 Sequence 3 */
        .long   WDT_Handler           /* Watchdog */
        .long   Timer0A_Handler       /* Timer 0 subtimer A */
        .long   Timer0B_Handler       /* Timer 0 subtimer B */
        .long   Timer1A_Handler       /* Timer 1 subtimer A */
        .long   Timer1B_Handler       /* Timer 1 subtimer B */
        .long   Timer2A_Handler       /* Timer 2 subtimer A */
        .long   Timer2B_Handler       /* Timer 2 subtimer B */
        .long   Comp0_Handler         /* Analog Comp 0 */
        .long   Comp1_Handler         /* Analog Comp 1 */
        .long   Comp2_Handler         /* Analog Comp 2 */
        .long   SysCtl_Handler        /* System Control */
        .long   FlashCtl_Handler      /* Flash Control */
        .long   GPIOPortF_Handler     /* GPIO Port F */
        .long   GPIOPortG_Handler     /* GPIO Port G */
        .long   GPIOPortH_Handler     /* GPIO Port H */
        .long   UART2_Handler         /* UART2 Rx and Tx */
        .long   SSI1_Handler          /* SSI1 Rx and Tx */
        .long   Timer3A_Handler       /* Timer 3 subtimer A */
        .long   Timer3B_Handler       /* Timer 3 subtimer B */
        .long   I2C1_Handler          /* I2C1 Master and Slave */
        .long   Quadrature1_Handler   /* Quadrature Encoder 1 */
        .long   CAN0_Handler          /* CAN0 */
        .long   CAN1_Handler          /* CAN1 */
        .long   CAN2_Handler          /* CAN2 */
        .long   Ethernet_Handler      /* Ethernet */
        .long   Hibernate_Handler     /* Hibernate */
        .long   USB0_Handler          /* USB0 */
        .long   PWM0Generator3_Handler/* PWM 0 Generator 3 */
        .long   uDMA_Handler          /* uDMA Software Transfer */
        .long   uDMA_Error            /* uDMA Error */
        .long   ADC1Seq0_Handler      /* ADC1 Sequence 0 */
        .long   ADC1Seq1_Handler      /* ADC1 Sequence 1 */
        .long   ADC1Seq2_Handler      /* ADC1 Sequence 2 */
        .long   ADC1Seq3_Handler      /* ADC1 Sequence 3 */
        .long   I2S0_Handler          /* I2S0 */
        .long   ExtBus_Handler        /* External Bus Interface 0 */
        .long   GPIOPortJ_Handler     /* GPIO Port J */
        .long   GPIOPortK_Handler     /* GPIO Port K */
        .long   GPIOPortL_Handler     /* GPIO Port L */
        .long   SSI2_Handler          /* SSI2 Rx and Tx */
        .long   SSI3_Handler          /* SSI3 Rx and Tx */
        .long   UART3_Handler         /* UART3 Rx and Tx */
        .long   UART4_Handler         /* UART4 Rx and Tx */
        .long   UART5_Handler         /* UART5 Rx and Tx */
        .long   UART6_Handler         /* UART6 Rx and Tx */
        .long   UART7_Handler         /* UART7 Rx and Tx */
        .long   0                     /* Reserved */
        .long   0                     /* Reserved */
        .long   0                     /* Reserved */
        .long   0                     /* Reserved */
        .long   I2C2_Handler          /* I2C2 Master and Slave */
        .long   I2C3_Handler          /* I2C3 Master and Slave */
        .long   Timer4A_Handler       /* Timer 4 subtimer A */
        .long   Timer4B_Handler       /* Timer 4 subtimer B */
        .long   0                     /* Reserved */
        .long   0                     /* Reserved */
        .long   0                     /* Reserved */
        .long   0                     /* Reserved */
        .long   0                     /* Reserved */
        .long   0                     /* Reserved */
        .long   0                     /* Reserved */
        .long   0                     /* Reserved */
        .long   0                     /* Reserved */
        .long   0                     /* Reserved */
        .long   0                     /* Reserved */
        .long   0                     /* Reserved */
        .long   0                     /* Reserved */
        .long   0                     /* Reserved */
        .long   0                     /* Reserved */
        .long   0                     /* Reserved */
        .long   0                     /* Reserved */
        .long   0                     /* Reserved */
        .long   0                     /* Reserved */
        .long   0                     /* Reserved */
        .long   Timer5A_Handler       /* Timer 5 subtimer A */
        .long   Timer5B_Handler       /* Timer 5 subtimer B */
        .long   WideTimer0A_Handler   /* Wide Timer 0 subtimer A */
        .long   WideTimer0B_Handler   /* Wide Timer 0 subtimer B */
        .long   WideTimer1A_Handler   /* Wide Timer 1 subtimer A */
        .long   WideTimer1B_Handler   /* Wide Timer 1 subtimer B */
        .long   WideTimer2A_Handler   /* Wide Timer 2 subtimer A */
        .long   WideTimer2B_Handler   /* Wide Timer 2 subtimer B */
        .long   WideTimer3A_Handler   /* Wide Timer 3 subtimer A */
        .long   WideTimer3B_Handler   /* Wide Timer 3 subtimer B */
        .long   WideTimer4A_Handler   /* Wide Timer 4 subtimer A */
        .long   WideTimer4B_Handler   /* Wide Timer 4 subtimer B */
        .long   WideTimer5A_Handler   /* Wide Timer 5 subtimer A */
        .long   WideTimer5B_Handler   /* Wide Timer 5 subtimer B */
        .long   FPU_Handler           /* FPU */
        .long   PECI0_Handler         /* PECI 0 */
        .long   LPC0_Handler          /* LPC 0 */
        .long   I2C4_Handler          /* I2C4 Master and Slave */
        .long   I2C5_Handler          /* I2C5 Master and Slave */
        .long   GPIOPortM_Handler     /* GPIO Port M */
        .long   GPIOPortN_Handler     /* GPIO Port N */
        .long   Quadrature2_Handler   /* Quadrature Encoder 2 */
        .long   Fan0_Handler          /* Fan 0 */
        .long   0                     /* Reserved */
        .long   GPIOPortP_Handler     /* GPIO Port P (Summary or P0) */
        .long   GPIOPortP1_Handler    /* GPIO Port P1 */
        .long   GPIOPortP2_Handler    /* GPIO Port P2 */
        .long   GPIOPortP3_Handler    /* GPIO Port P3 */
        .long   GPIOPortP4_Handler    /* GPIO Port P4 */
        .long   GPIOPortP5_Handler    /* GPIO Port P5 */
        .long   GPIOPortP6_Handler    /* GPIO Port P6 */
        .long   GPIOPortP7_Handler    /* GPIO Port P7 */
        .long   GPIOPortQ_Handler     /* GPIO Port Q (Summary or Q0) */
        .long   GPIOPortQ1_Handler    /* GPIO Port Q1 */
        .long   GPIOPortQ2_Handler    /* GPIO Port Q2 */
        .long   GPIOPortQ3_Handler    /* GPIO Port Q3 */
        .long   GPIOPortQ4_Handler    /* GPIO Port Q4 */
        .long   GPIOPortQ5_Handler    /* GPIO Port Q5 */
        .long   GPIOPortQ6_Handler    /* GPIO Port Q6 */
        .long   GPIOPortQ7_Handler    /* GPIO Port Q7 */
        .long   GPIOPortR_Handler     /* GPIO Port R */
        .long   GPIOPortS_Handler     /* GPIO Port S */
        .long   PWM1Generator0_Handler/* PWM 1 Generator 0 */
        .long   PWM1Generator1_Handler/* PWM 1 Generator 1 */
        .long   PWM1Generator2_Handler/* PWM 1 Generator 2 */
        .long   PWM1Generator3_Handler/* PWM 1 Generator 3 */
        .long   PWM1Fault_Handler     /* PWM 1 Fault */
	
	.size	__isr_vector, . - __isr_vector

	.text
	.thumb
	.thumb_func
	.align	2
	.globl	Reset_Handler
	.type	Reset_Handler, %function
Reset_Handler:
/*  Firstly it copies data from read only memory to RAM. There are two schemes
 *  to copy. One can copy more than one sections. Another can only copy
 *  one section.  The former scheme needs more instructions and read-only
 *  data to implement than the latter.
 *  Macro __STARTUP_COPY_MULTIPLE is used to choose between two schemes.  */

#ifdef __STARTUP_COPY_MULTIPLE
/*  Multiple sections scheme.
 *
 *  Between symbol address __copy_table_start__ and __copy_table_end__,
 *  there are array of triplets, each of which specify:
 *    offset 0: LMA of start of a section to copy from
 *    offset 4: VMA of start of a section to copy to
 *    offset 8: size of the section to copy. Must be multiply of 4
 *
 *  All addresses must be aligned to 4 bytes boundary.
 */
	ldr	r4, =__copy_table_start__
	ldr	r5, =__copy_table_end__

.L_loop0:
	cmp	r4, r5
	bge	.L_loop0_done
	ldr	r1, [r4]
	ldr	r2, [r4, #4]
	ldr	r3, [r4, #8]

.L_loop0_0:
	subs	r3, #4
	ittt	ge
	ldrge	r0, [r1, r3]
	strge	r0, [r2, r3]
	bge	.L_loop0_0

	adds	r4, #12
	b	.L_loop0

.L_loop0_done:
#else
/*  Single section scheme.
 *
 *  The ranges of copy from/to are specified by following symbols
 *    __etext: LMA of start of the section to copy from. Usually end of text
 *    __data_start__: VMA of start of the section to copy to
 *    __data_end__: VMA of end of the section to copy to
 *
 *  All addresses must be aligned to 4 bytes boundary.
 */
	ldr	r1, =__etext
	ldr	r2, =__data_start__
	ldr	r3, =__data_end__

.L_loop1:
	cmp	r2, r3
	ittt	lt
	ldrlt	r0, [r1], #4
	strlt	r0, [r2], #4
	blt	.L_loop1
#endif /*__STARTUP_COPY_MULTIPLE */

/*  This part of work usually is done in C library startup code. Otherwise,
 *  define this macro to enable it in this startup.
 *
 *  There are two schemes too. One can clear multiple BSS sections. Another
 *  can only clear one section. The former is more size expensive than the
 *  latter.
 *
 *  Define macro __STARTUP_CLEAR_BSS_MULTIPLE to choose the former.
 *  Otherwise efine macro __STARTUP_CLEAR_BSS to choose the later.
 */
#ifdef __STARTUP_CLEAR_BSS_MULTIPLE
/*  Multiple sections scheme.
 *
 *  Between symbol address __copy_table_start__ and __copy_table_end__,
 *  there are array of tuples specifying:
 *    offset 0: Start of a BSS section
 *    offset 4: Size of this BSS section. Must be multiply of 4
 */
	ldr	r3, =__zero_table_start__
	ldr	r4, =__zero_table_end__

.L_loop2:
	cmp	r3, r4
	bge	.L_loop2_done
	ldr	r1, [r3]
	ldr	r2, [r3, #4]
	movs	r0, 0

.L_loop2_0:
	subs	r2, #4
	itt	ge
	strge	r0, [r1, r2]
	bge	.L_loop2_0

	adds	r3, #8
	b	.L_loop2
.L_loop2_done:
#elif defined (__STARTUP_CLEAR_BSS)
/*  Single BSS section scheme.
 *
 *  The BSS section is specified by following symbols
 *    __bss_start__: start of the BSS section.
 *    __bss_end__: end of the BSS section.
 *
 *  Both addresses must be aligned to 4 bytes boundary.
 */
	ldr	r1, =__bss_start__
	ldr	r2, =__bss_end__

	movs	r0, 0
.L_loop3:
	cmp	r1, r2
	itt	lt
	strlt	r0, [r1], #4
	blt	.L_loop3
#endif /* __STARTUP_CLEAR_BSS_MULTIPLE || __STARTUP_CLEAR_BSS */

#ifndef __NO_SYSTEM_INIT
	bl	SystemInit
#endif

#ifndef __START
#define __START _start
#endif
	bl	__START

	.pool
	.size	Reset_Handler, . - Reset_Handler

	.align	1
	.thumb_func
	.globl	Enable_Interrupts
	.type	Enable_Interrupts, %function
Enable_Interrupts:
	cpsie	i
	bx	lr

	.pool
	.size	Enable_Interrupts, . - Enable_Interrupts

	.align	1
	.thumb_func
	.globl	Disable_Interrupts
	.type	Disable_Interrupts, %function
Disable_Interrupts:
	cpsid	i
	bx	lr

	.pool
	.size	Disable_Interrupts, . - Disable_Interrupts
    
	.align	1
	.thumb_func
	.weak	Default_Handler
	.type	Default_Handler, %function
Default_Handler:
	b	.
	.size	Default_Handler, . - Default_Handler

/*    Macro to define default handlers. Default handler
 *    will be weak symbol and just dead loops. They can be
 *    overwritten by other handlers */
	.macro	def_irq_handler	handler_name
	.weak	\handler_name
	.set	\handler_name, Default_Handler
	.endm

	def_irq_handler	NMI_Handler
	def_irq_handler	HardFault_Handler
	def_irq_handler	MemManage_Handler
	def_irq_handler	BusFault_Handler
	def_irq_handler	UsageFault_Handler
	def_irq_handler	SVC_Handler
	def_irq_handler	DebugMon_Handler
	def_irq_handler	PendSV_Handler
	def_irq_handler	SysTick_Handler
	def_irq_handler GPIOPortA_Handler
	def_irq_handler GPIOPortB_Handler
	def_irq_handler GPIOPortC_Handler
	def_irq_handler GPIOPortD_Handler
	def_irq_handler GPIOPortE_Handler
	def_irq_handler UART0_Handler
	def_irq_handler UART1_Handler
	def_irq_handler SSI0_Handler
	def_irq_handler I2C0_Handler
	def_irq_handler PWM0Fault_Handler
	def_irq_handler PWM0Generator0_Handler
	def_irq_handler PWM0Generator1_Handler
	def_irq_handler PWM0Generator2_Handler
	def_irq_handler Quadrature0_Handler
	def_irq_handler ADC0Seq0_Handler
	def_irq_handler ADC0Seq1_Handler
	def_irq_handler ADC0Seq2_Handler
	def_irq_handler ADC0Seq3_Handler
	def_irq_handler WDT_Handler
	def_irq_handler Timer0A_Handler
	def_irq_handler Timer0B_Handler
	def_irq_handler Timer1A_Handler
	def_irq_handler Timer1B_Handler
	def_irq_handler Timer2A_Handler
	def_irq_handler Timer2B_Handler
	def_irq_handler Comp0_Handler
	def_irq_handler Comp1_Handler
	def_irq_handler Comp2_Handler
	def_irq_handler SysCtl_Handler
	def_irq_handler FlashCtl_Handler
	def_irq_handler GPIOPortF_Handler
	def_irq_handler GPIOPortG_Handler
	def_irq_handler GPIOPortH_Handler
	def_irq_handler UART2_Handler
	def_irq_handler SSI1_Handler
	def_irq_handler Timer3A_Handler
	def_irq_handler Timer3B_Handler
	def_irq_handler I2C1_Handler
	def_irq_handler Quadrature1_Handler
	def_irq_handler CAN0_Handler
	def_irq_handler CAN1_Handler
	def_irq_handler CAN2_Handler
	def_irq_handler Ethernet_Handler
	def_irq_handler Hibernate_Handler
	def_irq_handler USB0_Handler
	def_irq_handler PWM0Generator3_Handler
	def_irq_handler uDMA_Handler
	def_irq_handler uDMA_Error
	def_irq_handler ADC1Seq0_Handler
	def_irq_handler ADC1Seq1_Handler
	def_irq_handler ADC1Seq2_Handler
	def_irq_handler ADC1Seq3_Handler
	def_irq_handler I2S0_Handler
	def_irq_handler ExtBus_Handler
	def_irq_handler GPIOPortJ_Handler
	def_irq_handler GPIOPortK_Handler
	def_irq_handler GPIOPortL_Handler
	def_irq_handler SSI2_Handler
	def_irq_handler SSI3_Handler
	def_irq_handler UART3_Handler
	def_irq_handler UART4_Handler
	def_irq_handler UART5_Handler
	def_irq_handler UART6_Handler
	def_irq_handler UART7_Handler
	def_irq_handler I2C2_Handler
	def_irq_handler I2C3_Handler
	def_irq_handler Timer4A_Handler
	def_irq_handler Timer4B_Handler
	def_irq_handler Timer5A_Handler
	def_irq_handler Timer5B_Handler
	def_irq_handler WideTimer0A_Handler
	def_irq_handler WideTimer0B_Handler
	def_irq_handler WideTimer1A_Handler
	def_irq_handler WideTimer1B_Handler
	def_irq_handler WideTimer2A_Handler
	def_irq_handler WideTimer2B_Handler
	def_irq_handler WideTimer3A_Handler
	def_irq_handler WideTimer3B_Handler
	def_irq_handler WideTimer4A_Handler
	def_irq_handler WideTimer4B_Handler
	def_irq_handler WideTimer5A_Handler
	def_irq_handler WideTimer5B_Handler
	def_irq_handler FPU_Handler
	def_irq_handler PECI0_Handler
	def_irq_handler LPC0_Handler
	def_irq_handler I2C4_Handler
	def_irq_handler I2C5_Handler
	def_irq_handler GPIOPortM_Handler
	def_irq_handler GPIOPortN_Handler
	def_irq_handler Quadrature2_Handler
	def_irq_handler Fan0_Handler
	def_irq_handler GPIOPortP_Handler
	def_irq_handler GPIOPortP1_Handler
	def_irq_handler GPIOPortP2_Handler
	def_irq_handler GPIOPortP3_Handler
	def_irq_handler GPIOPortP4_Handler
	def_irq_handler GPIOPortP5_Handler
	def_irq_handler GPIOPortP6_Handler
	def_irq_handler GPIOPortP7_Handler
	def_irq_handler GPIOPortQ_Handler
	def_irq_handler GPIOPortQ1_Handler
	def_irq_handler GPIOPortQ2_Handler
	def_irq_handler GPIOPortQ3_Handler
	def_irq_handler GPIOPortQ4_Handler
	def_irq_handler GPIOPortQ5_Handler
	def_irq_handler GPIOPortQ6_Handler
	def_irq_handler GPIOPortQ7_Handler
	def_irq_handler GPIOPortR_Handler
	def_irq_handler GPIOPortS_Handler
	def_irq_handler PWM1Generator0_Handler
	def_irq_handler PWM1Generator1_Handler
	def_irq_handler PWM1Generator2_Handler
	def_irq_handler PWM1Generator3_Handler
	def_irq_handler PWM1Fault_Handler
	def_irq_handler	DEF_IRQHandler
	
	.end
