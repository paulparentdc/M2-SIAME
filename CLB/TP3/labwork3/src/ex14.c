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
	set_gpiodMode(8, 0b01);
	set_gpiodType_pushpull(8);
	turnd_off(8);
	set_gpiodMode(9, 0b01);
	set_gpiodType_pushpull(9);
	turnd_off(9);
	set_gpiodMode(10, 0b01);
	set_gpiodType_pushpull(10);
	turnd_off(10);
	set_gpiodMode(11, 0b01);
	set_gpiodType_pushpull(11);
	turnd_off(11);
	set_gpiodMode(12, 0b01);
	set_gpiodType_pushpull(12);
	turnd_off(12);
	set_gpiodMode(13, 0b01);
	set_gpiodType_pushpull(13);
	turnd_off(13);
	set_gpiodMode(14, 0b01);
	set_gpiodType_pushpull(14);
	turnd_off(14);
	set_gpiodMode(15, 0b01);
	set_gpiodType_pushpull(15);
	turnd_off(15);

	int x;

	// main loop
	printf("Endless loop!\n");
	while(1) {
		ADC1_CR2 |= ADC_SWSTART;
		while((ADC1_SR & ADC_EOC) == 0 );
		x = ADC1_DR;

		if( (x > 500)){
			turnd_on(8);
		}
		else{
			turnd_off(8);
		}

		if( (x > 1000)){
			turnd_on(9);
		}
		else{
			turnd_off(9);
		}
		
		if( (x > 1500)){
			turnd_on(10);
		}
		else{
			turnd_off(10);
		}
		
		if( (x > 2000)){
			turnd_on(11);
		}
		else{
			turnd_off(11);
		}
		
		if( (x > 2500)){
			turnd_on(12);
		}
		else{
			turnd_off(12);
		}

		if( (x > 3000)){
			turnd_on(13);
		}
		else{
			turnd_off(13);
		}
		
		if( (x > 3500)){
			turnd_on(14);
		}
		else{
			turnd_off(14);
		}

		if( (x > 4000)){
			turnd_on(15);
		}
		else{
			turnd_off(15);
		}
		
		

		

		




	}

}


