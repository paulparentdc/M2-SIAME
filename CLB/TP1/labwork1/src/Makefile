
# ST-Link configuration
STLINK_ROOT=stlink-1.5.1/build/Release

# sources
PROGRAMS = \
	ex1.elf \
	ex2.elf \
	ex3.elf \
	ex4.elf \
	ex5.elf

OBJECTS = $(SOURCES:.c=.o)

# compiler configuration
ARCH=arm-none-eabi-
CC=$(ARCH)gcc
OBJCOPY=$(ARCH)objcopy
CFLAGS += -g3 -Wall -O2

CFLAGS += \
	-T../scripts/link.ld \
	-mfloat-abi=hard \
	-mlittle-endian \
	-mcpu=cortex-m4 \
	-mfpu=fpv4-sp-d16 \
	-mthumb \
	-I ../include
LDFLAGS = \
	-static \
	-nostdinc -nostdlib \
	-nostartfiles


# rules
all: $(PROGRAMS)

$(APP).elf: $(OBJECTS)
	$(CC) $(CFLAGS) $(OBJECTS) -o $@ $(LDFLAGS)

clean:
	rm -f *.o $(PROGRAMS)

ex1.elf: startup.o ex1.o tinyprintf.o
	$(CC) $(CFLAGS) $^ -o $@ $(LDFLAGS)

ex2.elf: startup.o ex2.o tinyprintf.o
	$(CC) $(CFLAGS) $^ -o $@ $(LDFLAGS)

ex3.elf: startup.o ex3.o tinyprintf.o
	$(CC) $(CFLAGS) $^ -o $@ $(LDFLAGS)

ex4.elf: startup.o ex4.o tinyprintf.o
	$(CC) $(CFLAGS) $^ -o $@ $(LDFLAGS)

ex5.elf: startup.o ex5.o tinyprintf.o
	$(CC) $(CFLAGS) $^ -o $@ $(LDFLAGS)
