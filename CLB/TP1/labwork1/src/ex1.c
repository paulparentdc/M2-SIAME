/* Embedded Systems - Exercise 1 */

#include <tinyprintf.h>
#include <stm32f4/rcc.h>
#include <stm32f4/gpio.h>



// GPIOD
#define GREEN_LED	12
#define ORANGE_LED	13
#define RED_LED		14
#define BLUE_LED	15

// GPIOA
#define USER_BUT	0

#define EMPTY_ITERATION 10000000000

//Set gpio mode to given mode
void set_gpioMode(int gpio, uint8_t mode){
	GPIOD_MODER = SET_BITS(GPIOD_MODER, gpio*2, 2, mode);
}

//Set gpio to pushpull type
void set_gpioType_pushpull(int gpio){
	GPIOD_OTYPER &= ~(1<<gpio);
}

void turn_on(int gpio){
	GPIOD_BSRR = 1<<gpio;
}

void turn_off(int gpio){
	GPIOD_BSRR = 1<<16+gpio;
}

int main() {
	printf("Starting...\n");
	int i;
	// RCC init
	RCC_AHB1ENR |= RCC_GPIODEN;

	// GPIO init
	for(i=12; i<16; i++){
		set_gpioMode(i, 0b01);
		set_gpioType_pushpull(i);
		turn_off(i);
	}

	enum{GREEN, ORANGE, RED, BLUE} state = RED;
	printf("Endless loop!\n");

	while(1) {
		for(i=0; i<EMPTY_ITERATION; i++);
		switch(state){
			case GREEN : 				
				turn_off(GREEN_LED);
				turn_on(ORANGE_LED);
				printf("Orange\n");
				state = ORANGE;
			break;
			case ORANGE :				
				turn_off(ORANGE_LED);
				turn_on(RED_LED);
				printf("Red\n");
				state = RED;
			break;
			case RED : 
				turn_off(RED_LED);
				turn_on(BLUE_LED);
				printf("Blue\n");
				state = BLUE;
			break;
			case BLUE :				
				turn_off(BLUE_LED);
				turn_on(GREEN_LED);
				printf("Green\n");
				state = GREEN;
			break;
		}
	}

}
