/* Embedded Systems - Exercise 5 */

#include <tinyprintf.h>
#include <stm32f4/rcc.h>
#include <stm32f4/gpio.h>
#include <stm32f4/nvic.h>
#include <stm32f4/exti.h>
#include <stm32f4/syscfg.h>
#include <stm32f4/tim.h>


// GPIOD
#define GREEN_LED	12
#define ORANGE_LED	13
#define RED_LED		14
#define BLUE_LED	15

// GPIODA
#define USER_BUT	0

//Set gpiod mode to given mode
void set_gpiodMode(int gpio, uint8_t mode){
	GPIOD_MODER = SET_BITS(GPIOD_MODER, gpio*2, 2, mode);
}

//Set gpiod to pushpull type
void set_gpiodType_pushpull(int gpio){
	GPIOD_OTYPER &= ~(1<<gpio);
}

//Turn on gpiod
void turnd_on(int gpio){
	GPIOD_BSRR = 1<<gpio;
}

//Turn off gpiod
void turnd_off(int gpio){
	GPIOD_BSRR = 1<<(16+gpio);
}


int main() {
	printf("\nStarting...\n");

	// RCC init
	RCC_AHB1ENR |= RCC_GPIOAEN;
	RCC_AHB1ENR |= RCC_GPIODEN;
	RCC_APB1ENR |= RCC_TIM4EN;

		// initialization
	// GPIO init
	set_gpiodMode(GREEN_LED, 0b01);
	set_gpiodType_pushpull(GREEN_LED);
	turnd_off(GREEN_LED);

	//init pin button A0
	GPIOA_MODER = SET_BITS(GPIOA_MODER, 0*2, 2, 0b00);
	GPIOA_OTYPER &= ~(1<<0);
	GPIOA_PUPDR =  SET_BITS(GPIOA_PUPDR, 0*2, 2, 0b00);

	// main loop
	printf("Endless loop!\n");
	while(1) {
		if((GPIOA_IDR & (1<<USER_BUT)) != 0){
			turnd_on(GREEN_LED);
		}else{
			turnd_off(GREEN_LED);
		}
	}

}


