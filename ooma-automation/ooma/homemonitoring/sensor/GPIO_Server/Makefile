all: BB-BONE-GP-00A0.dtbo gpioserver

BB-BONE-GP-00A0.dtbo:        BB-BONE-GP.dts
	dtc -O dtb -o BB-BONE-GP-00A0.dtbo -b 0 -@ BB-BONE-GP.dts
                                        
CFLAGS += \
	-W \
	-Wall \
	-D_BSD_SOURCE \
	-Wp,-MMD,$(dir $@).$(notdir $@).d \
	-Wp,-MT,$@ \
	-I. \
	\
	-mtune=cortex-a8 \
	-march=armv7-a \
	-g      
        
gpioserver:	gpioserver.c
	gcc $(CFLAGS) -o bb_gpioserver gpioserver.c -lpthread -g

install:	BB-BONE-GP-00A0.dtbo gpioserver
	cp BB-BONE-GP-00A0.dtbo /lib/firmware
