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

void handle_TIM4() {
	if(test){
		test = 1;
	}
	else{
		if( (GPIOD_ODR & (1<<GREEN_LED)) == 0 ){
		GPIOD_BSRR = 1<<GREEN_LED;
		}
		else{
			GPIOD_BSRR = 1<<(16+GREEN_LED);
		}
		test = 0;
	}
	printf("handle_TIM4 called\n");

	

	TIM4_SR = 0;
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

	// GPIO init
	GPIOD_MODER  =  SET_BITS ( GPIOD_MODER ,   GREEN_LED*2 ,   2 ,   0b01 ) ;
	GPIOD_OTYPER  =  GPIOD_OTYPER  & ~( 1<<GREEN_LED ) ;
	GPIOD_PUPDR  =  SET_BITS ( GPIOD_PUPDR ,   GREEN_LED*2 ,   2 ,   0b01 ) ;

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

	// main loop
	printf("Endless loop!\n");
	
	while(1) {

	}__asm("nop");

}


