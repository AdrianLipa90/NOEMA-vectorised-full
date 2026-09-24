CC = gcc
CFLAGS = -O2 -march=native -pthread -Wall -Wextra
LDLIBS = -lm

TARGET = kuramoto_substrate
SRC = $(TARGET).c

.PHONY: all clean help

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) -o $@ $< $(LDLIBS)

clean:
	rm -f $(TARGET)

help:
	@echo "Usage:"
	@echo "  make          build $(TARGET)"
	@echo "  make clean    remove binary"
	@echo "  ./$(TARGET) --help  show options"
