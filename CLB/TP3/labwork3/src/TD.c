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

//GPIOA
#define ONOFF_BUT     14
#define STARTSTOP_BUT 15

#define PUMP_PIN
#define THERM_PIN

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

void init_sensors(){
	//GPIOA
	GPIOA_MODER = SET_BITS(GPIOA_MODER, THERM_SENS_PIN*2, 2, GPIO_MODER_ANA);
	GPIOA_MODER = SET_BITS(GPIOA_MODER, PRESS_SENS_PIN*2, 2, GPIO_MODER_ANA);
	
	//ADC
	ADC1_SR    = 0;
	ADC1_CR1  = ADC_EOCIE;
	ADC1_CR2  = ADC_T8TRGO;
	ADC1_SQR3 = 1;

	ADC2_SR    = 0;
	ADC2_CR1  = ADC_EOCIE;
	ADC2_CR2  = ADC_T8TRGO;
	ADC2_SQR3 = 2;
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
    if(GPIOA_IDR & (1<<ONOFF_BUT)){
        pushed = 1;
    }
    else{
        pushed = 0;
		return 1;
    }
	return 0;
}

int test_startstop_button(){
    static int pushed = 0;
    if(GPIOA_IDR & (1<<STARTSTOP_BUT)){
        pushed = 1;
    }
    else{
        pushed = 0;
		return 1;
    }
	return 0;
}


void init_TIM3(){
	//GPIOB
	GPIOB_MODER = SET_BITS(GPIOB_MODER, 2*THERM_PIN, 2, GPIOD_MODER_ALT);
	GPIOB_AFRL  = SET_BITS(GPIOB_AFRL, 4*THERM_PIN, 4, 2);
	GPIOB_MODER = SET_BITS(GPIOB_MODER, 2*PUMP_PIN, 2, GPIOB_MODER_ALT);
	GPIOB_AFRL  = SET_BITS(GPIOB_AFRL, 4*PUMP_PIN, 4, 2);

	//TIM3
	TIM3_CCR1 = 0;
	TIM3_PSC  = 8;
	TIM3_ARR  = 60000; //(APB1_CLK/TIM3_PSC)*0.01; 

	TIM3_CCMR1 = TIM_OC1S_OUT | TIM_OC1M_PWM1
			   | TIM_OC2S_OUT | TIM_OC2M_PWM1;
	TIM3_CCER  = TIM_CC1E | TIM_CC2E;
	TIM3_CC1R  = 0;
	TIM3_CC2R  = 0;
	TIM3_CCR1  = TIM_CEN | CIM_ARPE;

	//Dont touch
	TIM3_EGR = TIM_UG;
	TIM3_SR = 0;
	TIM3_CR1 = TIM_ARPE;

	TIM3_CR1 = TIM3_CR1 | TIM_CEN;
}

void start_heater(){
	TIM3_CC1R = TIM3_PERIOD;
}

void stop_heater(){
	TIM3_CC1R = 0
}

void start_pump(){
	TIM3_CC2R = PUMP_POW;
}

void stop_pump(){
	TIM3_CC2R = 0;
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



