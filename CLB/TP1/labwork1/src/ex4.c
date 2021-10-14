/* Embedded Systems - Exercise 1 */

#include <tinyprintf.h>
#include <stm32f4/rcc.h>
#include <stm32f4/gpio.h>
#include <stm32f4/tim.h>

//TIM4
#define PSC 1000
#define WAIT_DELAY (APB1_CLK/PSC)
#define DELAY_50 (WAIT_DELAY/20)
#define DELAY_250 (WAIT_DELAY/4)
#define DELAY_500 (WAIT_DELAY/2)
#define DELAY_1000 (WAIT_DELAY)

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
	GPIOD_BSRR = 1<<16+gpio;
}

void init_TIM4(){
	TIM4_CR1 = 0;
	TIM4_PSC = PSC;
	TIM4_ARR = DELAY_1000;

	//Dont touh
	TIM4_EGR = TIM_UG;
	TIM4_SR = 0;
	TIM4_CR1 = TIM_ARPE;
}

int main() {
	printf("Starting...\n");

	// RCC init
	RCC_AHB1ENR |= RCC_GPIOAEN;
	RCC_AHB1ENR |= RCC_GPIODEN;
	RCC_APB1ENR |= RCC_TIM4EN;

	// GPIO init
	set_gpiodMode(GREEN_LED, 0b01);
	set_gpiodType_pushpull(GREEN_LED);
	turnd_off(GREEN_LED);

	GPIOA_MODER = SET_BITS(GPIOA_MODER, USER_BUT*2, 2, 0b00);
	
	//TIM4 init
	init_TIM4();

	printf("Endless loop!\n");
	enum{F250, F500, F1000} state = F1000;
	int led_state = 0;
	int but_state = 0;
	int last_but = 0;
	while(1) {
		if( (TIM4_SR & TIM_UIF) != 0 ){
			if(led_state){
				led_state = 0;
				turnd_off(GREEN_LED);
			}
			else{
				led_state = 1;
				turnd_on(GREEN_LED);
			}
		}

		if((GPIOA_IDR & (1<<USER_BUT)) != 0){
			but_state = 1;
			last_but = TIM4_CNT;
		}
		else if(but_state == 1){
			int now = TIM4_CNT;
			if(now <= last_but){
				now += DELAY_50;
			}
			if(now-last_but >= DELAY_50){
				but_state = 0;
				switch(state){
					case F250:
						state = F500;
						TIM4_ARR = DELAY_500;
						break;
					case F500:
						state = F1000;
						TIM4_ARR = DELAY_1000;
						break;
					case F1000:
						state = F250;
						TIM4_ARR = DELAY_250;
						break;
				}

			}
			
		}

	}

}
