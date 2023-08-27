all: vm-pgfault

vm-pgfault: pgfault.c
	gcc -o pgfault pgfault.c -lpthread

clean:
	@rm -f pgfault
