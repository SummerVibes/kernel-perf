#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BUFFER_NUM 1020
#define BUFFER_SIZE 4*1024

int main() {
        char* buffer;
        printf("Start!\n");
        buffer = (char*) malloc(BUFFER_SIZE*BUFFER_NUM);
        if(!buffer) {
                printf("Alloc failed!\n");
                exit(1);
        }
        for(int i=0;i<BUFFER_NUM;i++) {
                memset(buffer, 0, 1);
        }
        for (unsigned long i = 0; i < BUFFER_NUM*BUFFER_SIZE; i++) {
                if(buffer[i] != 0) {
                        printf("It is not zeroed\n");
                        exit(1);
                }
        }
        printf("Done!\n");
        return 0;
}