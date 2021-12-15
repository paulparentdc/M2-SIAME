/* Embedded Systems - Exercise 5 */

#include <tinyprintf.h>
#include <stm32f4/rcc.h>
#include <stm32f4/gpio.h>
#include <stm32f4/nvic.h>
#include <stm32f4/exti.h>
#include <stm32f4/syscfg.h>
#include <stm32f4/tim.h>


// GPIOD
#define ONOFF_LED     12
#define STARTSTOP_LED 13
#define ONOFF_BUT     14
#define STARTSTOP_BUT 15

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

void init_ui(){
    //Leds
    GPIOD_MODER  = SET_BITS(GPIOD_MODER, 2*ONOFF_LED, GPIO_MODER_OUT);
    GPIOD_OTYPER -= 1 >> ONOFF_LED;
    GPIOD_BSRR   = (1 << (16 + ONOFF_LED));

    GPIOD_MODER  = SET_BITS(GPIOD_MODER, 2*STARTSTOP_LED, GPIO_MODER_OUT);
    GPIOD_OTYPER -= 1 >> STARTSTOP_LED;
    GPIOD_BSRR   = (1 << (16 + STARTSTOP_LED));

    //Buttons
    GPIOA_MODER = SET_BITS(GPIOA_MODER, 2*ONOFF_BUT, 2, GPIOD_MODER_IN);
    GPIOA_PUPDR = SET_BITS(GPIOA_PUPDR, 2*ONOFF_BUT, 2, GPIOD_PUPDR_PU);

    GPIOA_MODER = SET_BITS(GPIOA_MODER, 2*STARTSTOP_BUT, 2, GPIOD_MODER_IN);
    GPIOA_PUPDR = SET_BITS(GPIOA_PUPDR, 2*STARTSTOP_BUT, 2, GPIOD_PUPDR_PU);
}

void set_onoff_led(int s){
    if( s ){
        GPIOD_BSRR = 1 << ONOFF_LED;
    }
    else{
        GPIOD_BSRR = 1 << (16+ONOFF_LED);
    }
}

void set_startstop_led(int s){
    if( s ){
        GPIOD_BSRR = 1 << STARTSTOP_LED;
    }
    else{
        GPIOD_BSRR = 1 << (16+STARTSTOP_LED);
    }
}

int test_onoff_button(){
    static int pushed = 0;
    if(GPIOA_ODR & (1<<ONOFF_BUT)){
        return 1;
    }
    else{
        return 0;
    }
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


