/* Embedded Systems - Exercise 5 */

#include <tinyprintf.h>
#include <stm32f4/rcc.h>
#include <stm32f4/gpio.h>
#include <stm32f4/tim.h>
#include <stm32f4/nvic.h>


//TIM4
#define PSC 1000
#define WAIT_DELAY (APB1_CLK/PSC)
#define DELAY_20 (WAIT_DELAY/100)
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

volatile int test = 0;
enum{m0, m1, m2, m3, m4, m5, m6, d5, d4, d3, d2, d1} state = m0;
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

void handle_TIM4() {
	printf("handle_TIM4 called\n");
	if(test == 2){
		switch(state){
		case m0: 
			turnd_on(10);
			state = m1;
			break;
		case m1:
			turnd_on(11);
			state = m2;
			break;
		case m2:
			turnd_on(12);
			state = m3;
			break;
		case m3:
			turnd_on(13);
			state = m4;
			break;
		case m4:
			turnd_on(14);
			state = m5;
			break;
		case m5:
			turnd_on(15);
			state = m6;
			break;
		case m6:
			turnd_off(10);
			state = d5;
			break;
		case d5:
			turnd_off(11);
			state = d4;
			break;
		case d4:
			turnd_off(12);
			state = d3;
			break;
		case d3:
			turnd_off(13);
			state = d2;
			break;
		case d2:
			turnd_off(14);
			state = d1;
			break;
		case d1:
			turnd_off(15);
			state = m0;
			break;
		}
		test =0;
	}
	test ++;
	

	TIM4_SR &= ~TIM_UIF;
}

void init_TIM4(){

	TIM4_CR1 = 0;
	TIM4_PSC = 1000;
	TIM4_ARR = (APB1_CLK/TIM4_PSC)/2; 
	TIM4_EGR = TIM_UG;
	TIM4_SR = 0;
	TIM4_CR1 = TIM_ARPE;
	TIM4_DIER = TIM_UIE;
}


int main() {
	printf("\nStarting...\n");

	// RCC init
	RCC_AHB1ENR |= RCC_GPIOAEN;
	RCC_AHB1ENR |= RCC_GPIODEN;
	RCC_APB1ENR |= RCC_TIM4EN;

	
	// initialization
	// GPIO init
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

	NVIC_ICER ( TIM4_IRQ>>5 )|=   1<<( TIM4_IRQ  &  0X1f ) ;
	NVIC_IRQ ( TIM4_IRQ )   =   ( uint32_t )handle_TIM4 ;
	
	NVIC_IPR ( TIM4_IRQ )   =   0 ;

	NVIC_ICPR ( TIM4_IRQ>>5 )|=   1<<( TIM4_IRQ  &  0X1f ) ;
	NVIC_ISER ( TIM4_IRQ>>5 )|=   1<<( TIM4_IRQ  &  0X1f ) ;

	init_TIM4();

	ENABLE_IRQS;

	// main loop
	printf("Endless loop!\n");

	TIM4_CR1 = TIM4_CR1 | TIM_CEN;
	
	while(1) {
	}

}



