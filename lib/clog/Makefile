CC = gcc
CFLAG = -shared -fPIC

libclog.so: c_log.c c_log.h
	$(CC) $(CFLAG) $< -o $@

install:
	cp -f libclog.so /usr/lib64/
	cp -f c_log.h /usr/include/

clean:
	rm -f libclog.so c_log
