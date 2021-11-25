/* Embedded Systems - Exercise 5 */

#include <tinyprintf.h>
#include <stm32f4/rcc.h>
#include <stm32f4/gpio.h>
#include <stm32f4/tim.h>
#include <stm32f4/nvic.h>
#include <stm32f4/exti.h>
#include <stm32f4/syscfg.h>


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

int but_state = 0;
int last_but  = 0;
int led_state = 0;

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
	TIM4_ARR = DELAY_500;

	//Dont touch
	TIM4_EGR = TIM_UG;
	TIM4_SR = 0;
	TIM4_CR1 = TIM_ARPE;

	ENABLE_IRQS;

	TIM4_CR1 = TIM4_CR1 | TIM_CEN;
}

void handle_B1(){
    if((GPIOA_IDR & (1<<USER_BUT)) != 0){
			but_state = 1;
		}
		else if(but_state == 1){
			but_state =0;
			if(led_state == 1){
				turnd_off(GREEN_LED);
				led_state = 0;
			}
			else{
				turnd_on(GREEN_LED);
				led_state = 1;
			}
		}

}


void init_interrupt(){
    DISABLE_IRQS ;// c o n f i g u r e  
    EXTISETBITS (SYSCFG_CR1, 0, 4, 0);
    // 0 = GPIOA0
    EXTI_RTSR |=  1<<0 ;
    EXTI_FTSR |=  1<<0 ;
    EXTI_IMR  |=  1<<0 ;
    EXTI_IPR  |=  1<<0 ;

    NVIC_ICER( EXTI0IRQ>>5 ) |=   1<<( EXTI0_IRQ & 0X1f) ;
    NVIC_IRQ( EXTI0IRQ )      =   (uint32_t) handle_B1;
    NVIC_IPR( EXTI0IRQ )      =   0 ;
    NVIC_ICPR( EXTI0IRQ>>5 ) |=  1<<( EXTI0_IRQ & 0X1f );
    NVIC_ISER( EXTI0IRQ>>5 ) |=  1<<( EXTI0_IRQ & 0X1f );
    ENABLE_IRQS ;
}

int main() {
	printf("\nStarting...\n");

	// RCC init
	RCC_AHB1ENR |= RCC_GPIOAEN;
	RCC_AHB1ENR |= RCC_GPIODEN;
	RCC_APB1ENR |= RCC_TIM4EN;

	// GPIO init
	set_gpiodMode(GREEN_LED, 0b01);
	set_gpiodType_pushpull(GREEN_LED);
	turnd_on(GREEN_LED);
	
	//TIM4 init
	init_TIM4();
    init_interrupt();


	// main loop
	printf("Endless loop!\n");
	
	while(1) {
	}

}