/**
 *	Torpy - grid-follower wheeling and box delivering bot.
 *	Copyright (C) 2021  Université de Toulouse <casse@irit.fr>
 *
 *	This program is free software: you can redistribute it and/or modify
 *	it under the terms of the GNU General Public License as published by
 *	the Free Software Foundation, either version 3 of the License, or
 *	(at your option) any later version.
 *
 *	This program is distributed in the hope that it will be useful,
 *	but WITHOUT ANY WARRANTY; without even the implied warranty of
 *	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *	GNU General Public License for more details.
 */
#ifndef STM32F4_TIM_H
#define STM32F4_TIM_H

#include "io.h"

// bases
#define TIM2_BASE	0x40000000
#define TIM3_BASE	0x40000400
#define TIM4_BASE	0x40000800
#define TIM5_BASE	0x40000C00
#define TIM6_BASE	0x40001000
#define TIM7_BASE	0x40001400
#define TIM12_BASE	0x40001800
#define TIM13_BASE	0x40001C00
#define TIM14_BASE	0x40002000

#define TIM1_BASE	0x40010000
#define TIM8_BASE	0x40010400
#define TIM9_BASE	0x40014000
#define TIM10_BASE	0x40014400
#define TIM11_BASE	0x40014800

// registers
#define TIM_IOREG(n, o)	_IOREG(TIM##n##_BASE, o)
#define TIM_CR1(n)		TIM_IOREG(n, 0x00)
#define TIM_CR2(n)		TIM_IOREG(n, 0x04)
#define TIM_SMCR(n)		TIM_IOREG(n, 0x08)
#define TIM_DIER(n)		TIM_IOREG(n, 0x0C)
#define TIM_SR(n)		TIM_IOREG(n, 0x10)
#define TIM_EGR(n)		TIM_IOREG(n, 0x14)
#define TIM_CCMR1(n)	TIM_IOREG(n, 0x18)
#define TIM_CCMR2(n)	TIM_IOREG(n, 0x1C)
#define TIM_CCER(n)		TIM_IOREG(n, 0x20)
#define TIM_CNT(n)		TIM_IOREG(n, 0x24)
#define TIM_PSC(n)		TIM_IOREG(n, 0x28)
#define TIM_ARR(n)		TIM_IOREG(n, 0x2C)
#define TIM_CCR1(n)		TIM_IOREG(n, 0x34)
#define TIM_CCR2(n)		TIM_IOREG(n, 0x38)
#define TIM_CCR3(n)		TIM_IOREG(n, 0x3C)
#define TIM_CCR4(n)		TIM_IOREG(n, 0x40)
#define TIM_DCR(n)		TIM_IOREG(n, 0x48)
#define TIM_DMAR(n)		TIM_IOREG(n, 0x4C)
#define TIM_OR(n)		TIM_IOREG(n, 0x50)
#define TIM_CCRx(n, m)	TIM_IOREG(n, 0x34 + (m -1)*4)

// TIM_CR1
#define TIM_ARPE		(1 << 7)
#define TIM_CMS_MODE0	(0b00 << 5)
#define TIM_DIR_DOWN	(1 << 4)
#define TIM_OPM			(1 << 3)
#define TIM_CEN			(1 << 0)

// TIM_SR
#define TIM_UIF		(1 << 0)
#define TIM_TIF		(1 << 6)

// TIM_EGR
#define TIM_CC1G	(1 << 1)
#define TIM_CC2G	(1 << 2)
#define TIM_CC3G	(1 << 3)
#define TIM_CC4G	(1 << 4)
#define TIM_UG		(1 << 0)

// CCMR1
#define TIM_OC2CE		(1 << 15)
#define TIM_OC2M_FROZEN	(0b000 << 12)
#define TIM_OC2M_SET	(0b001 << 12)
#define TIM_OC2M_CLR	(0b010 << 12)
#define TIM_OC2M_TOGGLE	(0b011 << 12)
#define TIM_OC2M_PWM1	(0b110 << 12)
#define TIM_OC2M_PWM2	(0b111 << 12)
#define TIM_OC2PE		(1 << 11)
#define TIM_OC2FE		(1 << 10)
#define TIM_CCS2S_OUT	(0b00 << 8)
#define TIM_OC1CE		(1 << 7)
#define TIM_OC1M_FROZEN	(0b000 << 4)
#define TIM_OC1M_SET	(0b001 << 4)
#define TIM_OC1M_CLR	(0b010 << 4)
#define TIM_OC1M_TOGGLE	(0b011 << 4)
#define TIM_OC1M_PWM1	(0b110 << 4)
#define TIM_OC1M_PWM2	(0b111 << 4)
#define TIM_OC1PE		(1 << 3)
#define TIM_OC1FE		(1 << 2)
#define TIM_CCS1S_OUT	(0b00 << 0)

// CCMR2
#define TIM_OC4CE		(1 << 15)
#define TIM_OC4M_FROZEN	(0b000 << 12)
#define TIM_OC4M_SET	(0b001 << 12)
#define TIM_OC4M_CLR	(0b010 << 12)
#define TIM_OC4M_TOGGLE	(0b011 << 12)
#define TIM_OC4M_PWM1	(0b110 << 12)
#define TIM_OC4M_PWM2	(0b111 << 12)
#define TIM_OC4PE		(1 << 11)
#define TIM_OC4FE		(1 << 10)
#define TIM_CCS4S_OUT	(0b00 << 8)
#define TIM_OC3CE		(1 << 7)
#define TIM_OC3M_FROZEN	(0b000 << 4)
#define TIM_OC3M_SET	(0b001 << 4)
#define TIM_OC3M_CLR	(0b010 << 4)
#define TIM_OC3M_TOGGLE	(0b011 << 4)
#define TIM_OC3M_PWM1	(0b110 << 4)
#define TIM_OC3M_PWM2	(0b111 << 4)
#define TIM_OC3PE		(1 << 3)
#define TIM_OC3RE		(1 << 2)
#define TIM_CCS3S_OUT	(0b00 << 0)

// CCER
#define TIM_CCxNP(n)	(1 << (4*(n-1) + 3))
#define TIM_CCxP(n)		(1 << (4*(n-1) + 1))
#define TIM_CCxE(n)		(1 << (4*(n-1) + 0))

// TIM_DIER
#define TIM_UIE			(1 << 0)


// TIM4
#define TIM4_CR1		TIM_IOREG(4, 0x00)
#define TIM4_CR2		TIM_IOREG(4, 0x04)
#define TIM4_SMCR		TIM_IOREG(4, 0x08)
#define TIM4_DIER		TIM_IOREG(4, 0x0C)
#define TIM4_SR			TIM_IOREG(4, 0x10)
#define TIM4_EGR		TIM_IOREG(4, 0x14)
#define TIM4_CCMR1		TIM_IOREG(4, 0x18)
#define TIM4_CCMR2		TIM_IOREG(4, 0x1C)
#define TIM4_CCER		TIM_IOREG(4, 0x20)
#define TIM4_CNT		TIM_IOREG(4, 0x24)
#define TIM4_PSC		TIM_IOREG(4, 0x28)
#define TIM4_ARR		TIM_IOREG(4, 0x2C)
#define TIM4_CCR1		TIM_IOREG(4, 0x34)
#define TIM4_CCR2		TIM_IOREG(4, 0x38)
#define TIM4_CCR3		TIM_IOREG(4, 0x3C)
#define TIM4_CCR4		TIM_IOREG(4, 0x40)
#define TIM4_DCR		TIM_IOREG(4, 0x48)
#define TIM4_DMAR		TIM_IOREG(4, 0x4C)
#define TIM4_OR			TIM_IOREG(4, 0x50)

// interrupts
#define TIM2_IRQ		28
#define TIM3_IRQ		29
#define TIM4_IRQ		30
#define TIM5_IRQ		50
#define TIM7_IRQ		55

#endif	// STM32F4_TIM_H
