
# configuration
APP = main
STLINK_ROOT=stlink-1.5.1/build/Release
LOG = stm32f4.log
GDB = gdb
#GDB = gdb
GDB_FLAGS=-command ../scripts/gdbinit

# rules
all:
	cd src; $(MAKE) all

clean:
	rm -f $(LOG)
	cd src; $(MAKE) clean

openocd:
	-rm $(LOG)
	openocd -f scripts/openocd.cfg

debug:
	gdb-multiarch src/$(APP).elf

log:
	tail -f $(LOG)


# exercises
ex%:
	cd src; $(MAKE) ex$*.elf

debug_ex%: ex%
	cd src; $(GDB) $(GDB_FLAGS) ex$*.elf



# build distribution
DIST_FILES = \
	COPYING.md \
	.gdbinit \
	include \
	scripts \
	Makefile
DIST_SRC2 = \
	src/ex8.c \
	src/ex9.c \
	src/ex10.c \
	src/ex11.c
DIST_SRC3 = \
	src/ex12.c \
	src/ex13.c \
	src/ex14.c
DIST_SRC = \
	src/Makefile \
	src/startup.c \
	src/tinyprintf.c \
	$(DIST_SRC3)
DIST_NAME=labwork3

dist:
	if [ -e $(DIST_NAME) ]; then \
		rm -rf $(DIST_NAME); \
	fi
	mkdir $(DIST_NAME)
	cp -R $(DIST_FILES) $(DIST_NAME)
	mkdir $(DIST_NAME)/src
	#cp scripts/Makefile.014 $(DIST_NAME)/Makefile
	for f in $(DIST_SRC); do \
		autofilter.py < $$f > $(DIST_NAME)/$$f; \
	done
	cd $(DIST_NAME); make; make clean
	tar cvfz $(DIST_NAME).tgz $(DIST_NAME)

DATE = $(shell date +"%y%m%d")
assign:
	tar cvfz assign-$(DATE).tgz src/*.c
