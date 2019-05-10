#CC=clang++
#CFLAGS=-stdlib=libc++ -std=c++11 -g -Wall -Werror -Wextra -I.

# with gcc, need to explictly link to stdc++
#CC=gcc
#CFLAGS=-std=c++11 -g -Wall -Werror -Wextra -I. -lstdc++

CC=g++
CFLAGS=-std=c++11 -g -Wall -Werror -Wextra -I.

SRC=main.cpp
SOLUTION=solution.h
OUT=Debug/a.out

$(OUT): $(SRC) $(SOLUTION)
	$(CC) -o $@ $< $(CFLAGS)

#depend: .depend
#
#.depend: $(SRC)
#	rm -f ./.depend
#	$(CC) $(CFLAGS) -MM $^ -MF  ./.depend;
#
#include .depend

run:$(OUT)
	$(OUT)

.PHONY: clean
clean:
	rm -rf $(OUT) $(OUT).dSYM
