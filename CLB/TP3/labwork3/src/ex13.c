/* Embedded Systems - Exercise 5 */

#include <tinyprintf.h>
#include <stm32f4/rcc.h>
#include <stm32f4/gpio.h>
#include <stm32f4/nvic.h>
#include <stm32f4/exti.h>
#include <stm32f4/syscfg.h>
#include <stm32f4/tim.h>
#include <stm32f4/adc.h>


// GPIOD
#define GREEN_LED	12
#define ORANGE_LED	13
#define RED_LED		14
#define BLUE_LED	15

// GPIODA
#define USER_BUT	0

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


void init_ADC(){
	GPIOA_MODER = SET_BITS (GPIOA_MODER, 3*2 , 2, 0b11);
	GPIOA_PUPDR = SET_BITS (GPIOA_PUPDR, 3*2 , 2, 0b01);
	ADC1_SQR3   = 3;
	ADC1_CR1    = 0;
	ADC1_CR2    = ADC_ADON;
}


int main() {
	printf("\nStarting...\n");

	// RCC init
	RCC_AHB1ENR |= RCC_GPIOAEN;
	RCC_AHB1ENR |= RCC_GPIODEN;
	RCC_APB1ENR |= RCC_TIM4EN;
	RCC_APB2ENR |= RCC_ADC1EN;

	// initialization
	init_ADC();

	set_gpiodMode(GREEN_LED, 0b01);
	set_gpiodType_pushpull(GREEN_LED);
	turnd_off(GREEN_LED);

	// main loop
	printf("Endless loop!\n");
	while(1) {
	}

}


