#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <sys/stat.h> 
#include <fcntl.h>
#include <errno.h>


#define LOG_PATH "/var/log/digioceanfs/test-a.log"
#define MAX_WRITE_COUNT  30  /* indicate one file 30MB*/
#define MAX_FILES_COUNT   150000 /* all files count */
#define MAX_THREADS_COUNT 100    /* all handle threads count */
#define MAX_TEST_LOOP_TIMES 1000 /* all loop count */

char *buf = NULL;
int *my_fd = NULL;
int my_index = -1;
int log_fd = -1;
unsigned long num = MAX_FILES_COUNT;

pthread_mutex_t lock;

void *thread_proc(void *arg)
{
    ssize_t ret = 0;
    int tmp_fd = -1;
    int i = 0; 
    ssize_t offset = 0;
    char logbuf[1024] = {0,};

    while(1) {
        pthread_mutex_lock(&lock);
        if (my_index < 0) {
            pthread_mutex_unlock(&lock);
            goto sleep;
        }
        tmp_fd = my_fd[my_index];
        my_index++;
        if (my_index >= num) {
            my_index = -2;
        }
        pthread_mutex_unlock(&lock);

        for (i = 0; i < MAX_WRITE_COUNT; i++) {
            ret = pwrite (tmp_fd, buf, offset, 0);
            if (-1 == ret) {
                memset (logbuf, '\0', 1024);
                sprintf (logbuf, "Failed to write tmp_fd=%d:%s\n",
                         tmp_fd, strerror(errno));
                write (log_fd, logbuf, strlen(logbuf));
		break;
            }
            offset += 1024 * 1024;
        }

	if (-1 != ret) {
            printf("write %d success\n", tmp_fd);
	}
		
        close(tmp_fd);

        pthread_mutex_lock(&lock);
        if (my_index == -2) {
            my_index = -1;
        }
        pthread_mutex_unlock(&lock);
        continue;      
sleep:
        sleep (1);
    }

    return NULL;
}

int main()
{
    unsigned long i = 0;
    char file[1024];
    int j;
    char logbuf[1024] = {0,};
    pthread_t tid[100];

    /*init log*/
    log_fd = open (LOG_PATH, O_RDWR|O_CREAT|O_APPEND);
    if (-1 == log_fd) {
        printf("Failed to create LOG_PATH=%s: %s\n", LOG_PATH, strerror(errno));
        return -1;
    }

    pthread_mutex_init (&lock, NULL);

    for(j=0;j<MAX_THREADS_COUNT;j++) {
        if (pthread_create(&tid[j], NULL, thread_proc, NULL)) {
            memset (logbuf, '\0', 1024);
            sprintf (logbuf, "%s:thread-%d\n",
                     "Failed to create thread failed!", i);
            write (log_fd, logbuf, strlen(logbuf));
        }

        pthread_detach(tid[j]);
    }

    buf = (char *)malloc(1024*1024);
    if (NULL == buf) {
        printf("malloc failed\n");
        return -1;
    }

    memset (buf, 1, 1024*1024);

    my_fd = (int *)calloc(num, sizeof(int));
    if (NULL == my_fd) {
        memset (logbuf, '\0', 1024);
        sprintf (logbuf, "Failed to calloc myfd:%s\n", strerror(errno));
        write (log_fd, logbuf, strlen(logbuf));
        return -1;
    }

    for (j=0;j<MAX_TEST_LOOP_TIMES;j++) {
        memset (logbuf, '\0', 1024);
        sprintf (logbuf, "=====DI-%d-LUN=========\n", j);
        write (log_fd, logbuf, strlen(logbuf));

        pthread_mutex_lock(&lock);
        if (my_index != -1) {
            pthread_mutex_unlock(&lock);
            goto wait;
        }

        for(i=0; i<num; i++) {
            memset(file, 0, sizeof(file));
            sprintf(file, "%s%lu", "/cluster2/test/", i);

            my_fd[i] = open (file, O_RDWR|O_CREAT);
            if (-1 == my_fd[i]) {
                memset (logbuf, '\0', 1024);
                sprintf (logbuf, "Failed to open my_fd:%s\n",
                         strerror(errno));
                write (log_fd, logbuf, strlen(logbuf));
                return -1;
            }
            printf("%lu\n", i);
        }
        my_index = 0;
        pthread_mutex_unlock(&lock);

        continue;
wait:
        j--;
        sleep(1);
    }

    for(;;){
        sleep(100);
    }

    if (my_fd)
        free (my_fd);
    return 0;
}
