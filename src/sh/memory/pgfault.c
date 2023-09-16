#include <fcntl.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <unistd.h>

int nr_threads = 1;
int iterations = 1;
unsigned long memory = 1;
unsigned long bytes_per_thread = 1;
int real = 0;

unsigned long page_size = 4096;
//unsigned long page_size = 4096*512;

void *alloc_mem(void *arg) {
  int nr_pages, iter = 0;
  char *tmp, *start;

  while (iter < iterations) {
    tmp = malloc(bytes_per_thread);
    if (!tmp) {
      printf("Malloc failed");
      exit(EXIT_FAILURE);
    }

    start = tmp;
    nr_pages = bytes_per_thread / page_size;
    while (nr_pages--) {
      *start = 'A';
      start += page_size;
      if(real) {
	int clock = 10000; 
	while(clock-- > 0)
	  continue;
	//usleep(2);
	//if(nr_pages%512==0){
	//  usleep(10);
	//}
      }
    }
    free(tmp);
    iter++;
  }
  return NULL;
}

int main(int argc, char *argv[]) {
  int i, c, pid, ret;
  pthread_t *pthread;

  while ((c = getopt(argc, argv, "m:t:i:r")) != -1) {
    switch (c) {
    case 'm':
      memory = atoi(optarg);
      break;
    case 't':
      nr_threads = atoi(optarg);
      break;
    case 'i':
      iterations = atoi(optarg);
      break;
    case 'r':
      real = 1;
      break;
    default:
      printf("Usage: %s [-m memoryGB] [-t nr_threads] [-i iterations]\n",
             argv[0]);
      exit(EXIT_FAILURE);
    }
  }

  pthread = (pthread_t *)malloc(sizeof(pthread_t) * nr_threads);
  if (!pthread) {
    printf("Error while allocating pthreads\n");
    exit(EXIT_FAILURE);
  }
  bytes_per_thread = (memory * 1024 * 1024 * 1024) / nr_threads;
  printf("Running with the following configuration...\n");
  printf("Memory: \t\t%ldGB\n", memory);
  printf("Threads: \t\t%d\n", nr_threads);
  printf("Iterations: \t\t%d\n", iterations);
  printf("PageSize: \t\t%lu\n", page_size);
  printf("Bytes Per Thread: \t%ld\n", bytes_per_thread);

  for (i = 0; i < nr_threads; i++)
    pthread_create(&pthread[i], NULL, alloc_mem, NULL);

  for (i = 0; i < nr_threads; i++)
    pthread_join(pthread[i], NULL);
  printf("Exiting successfully.\n");
  return 0;
}
