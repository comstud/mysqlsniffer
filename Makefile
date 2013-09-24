CC=gcc
CFLAGS=-g
LDFLAGS=-lpcap

all: mysqlsniffer

OBJS=src/mysqlsniffer.o src/packet_handlers.o src/misc.o

mysqlsniffer: ${OBJS}
	$(CC) $(CFLAGS) -o mysqlsniffer $(OBJS) $(LDFLAGS)

clean:
	rm -f ${OBJS} mysqlsniffer
