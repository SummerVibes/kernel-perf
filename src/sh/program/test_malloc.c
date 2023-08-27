#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// 10 亿次
#define NUM_ITERATIONS 1000000000UL
#define BUFFER_SIZE 4096

int main() {
        long unsigned i;
        char* buffer;
        printf("Start!\n");
        for (i = 0; i < NUM_ITERATIONS; i++) {
                buffer = (char*) malloc(BUFFER_SIZE);
                if (buffer == NULL) {
                        printf("Failed to allocate memory\n");
                        exit(1);
                }
                memset(buffer, i % 256, BUFFER_SIZE);
                free(buffer);
        }
        printf("Done!\n");
        return 0;
}