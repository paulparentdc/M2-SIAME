/* Embedded Systems - Exercise 2 */

#include <tinyprintf.h>
#include <stm32f4/rcc.h>
#include <stm32f4/gpio.h>


// GPIOD
#define GREEN_LED	12
#define ORANGE_LED	13
#define RED_LED		14
#define BLUE_LED	15

// GPIODA
#define USER_BUT	0

//Set gpio mode to given mode
void set_gpiodMode(int gpio, uint8_t mode){
	GPIOD_MODER = SET_BITS(GPIOD_MODER, gpio*2, 2, mode);
}

//Set gpio to pushpull type
void set_gpiodType_pushpull(int gpio){
	GPIOD_OTYPER &= ~(1<<gpio);
}

void turnd_on(int gpio){
	GPIOD_BSRR = 1<<gpio;
}

void turnd_off(int gpio){
	GPIOD_BSRR = 1<<16+gpio;
}

int main() {
	printf("Starting...\n");

	// RCC init
	RCC_AHB1ENR |= RCC_GPIOAEN;
	RCC_AHB1ENR |= RCC_GPIODEN;

	// GPIO init
	set_gpiodMode(GREEN_LED, 0b01);
	set_gpiodType_pushpull(GREEN_LED);
	turnd_off(GREEN_LED);
	
	GPIOA_MODER = SET_BITS(GPIOA_MODER, USER_BUT*2, 2, 0b00);
	
	int but_state = 0;
	printf("Endless loop!\n");
	while(1) {
		if((GPIOA_IDR & (1<<USER_BUT)) != 0){
			but_state = 1;
			turnd_on(GREEN_LED);
		}
		else if(but_state == 1){
			but_state =0;
			turnd_off(GREEN_LED);
		}
		
	}

}
