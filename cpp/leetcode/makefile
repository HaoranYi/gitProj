CC=clang++
CFLAGS=-stdlib=libc++ -std=c++11 -g -Wall -Werror -Wextra -I.

# with gcc, need to explictly link to stdc++
#CC=gcc
#CFLAGS=-std=c++11 -g -Wall -Werror -Wextra -I. -lstdc++

#CC=g++
#CFLAGS=-std=c++11 -g -Wall -Werror -Wextra -I.

SRC=main.cpp
OUT=Debug/a.out

$(OUT): $(SRC) solution.h 
	$(CC) -o $@ $< $(CFLAGS)

run:$(OUT)
	$(OUT)

.PHONY: clean
clean:
	rm -rf $(OUT) $(OUT).dSYM
