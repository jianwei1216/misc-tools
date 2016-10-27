CC = gcc
C_FLAGS = -g -O0 -Wall
LD_FLAGS = -lpthread

test: lock_write_unlock_read.c
	$(CC) $(C_FLAGS) $(LD_FLAGS) $< -o $@

clean:
	rm -f test
