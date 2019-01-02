# Compiler & Linker
CC=arm-none-eabi-gcc
CXX=arm-none-eabi-g++

# List of source files
SOURCES=$(wildcard *.c) $(wildcard *.s) $(wildcard *.S)

# Use newlib-nano. To disable it, specify USE_NANO=
USE_NANO=--specs=nano.specs

# Use semihosting or not
#USE_HOST=--specs=rdimon.specs -lc -lrdimon
USE_HOST=--specs=nosys.specs

# Options for specific architecture
ARCH_FLAGS=-mabi=aapcs -mfloat-abi=soft -mfpu=fpv4-sp-d16 -mthumb -mcpu=cortex-m4

STARTUP_DEFS=-D__STARTUP_CLEAR_BSS -D__START=main -D__NO_SYSTEM_INIT

ALLFLAGS=$(ARCH_FLAGS) $(STARTUP_DEFS) -g -Wl,--no-wchar-size-warning -Wall
CFLAGS=$(ALLFLAGS) --std=c11
CXXFLAGS=$(ALLFLAGS) -fno-exceptions --std=c++11

# Name for the output files
NAME=readrom

# Create map file
MAP=-Wl,-Map=$(NAME).map

# Link for code size
GC=-Wl,--gc-sections

LDSCRIPTS=-L. -T gcc.ld
LFLAGS=$(USE_NANO) $(USE_HOST) $(LDSCRIPTS) $(GC) $(MAP)

$(NAME).axf: $(SOURCES) $(STARTUP)
	$(CC) $^ $(CFLAGS) $(LFLAGS) -o $@

clean: 
	rm -f $(NAME)*.axf *.map *.lst *.o
