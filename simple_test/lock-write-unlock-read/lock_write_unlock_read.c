#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <pthread.h>
#include <stdint.h>

#define LOCK_INIT(x)    pthread_mutex_init (x, 0)
#define LOCK(x)         pthread_mutex_lock (x)
#define TRY_LOCK(x)     pthread_mutex_trylock (x)
#define UNLOCK(x)       pthread_mutex_unlock (x)
#define LOCK_DESTROY(x) pthread_mutex_destroy (x)
typedef pthread_mutex_t gf_lock_t; 

#define MAX_SUBVOLS_COUNT   10

typedef struct {
        gf_lock_t lock;
        uintptr_t xl_up;  
        uint32_t xl_up_cout;
} share_data_t;

void ec_mask_to_char_array (uintptr_t mask, unsigned char *array,
                            int numsubvols)
{
        int i = 0;

        for (i = 0; i < numsubvols; i++)
                array[i] = ((mask >> i) & 1);
}

uintptr_t ec_char_array_to_mask (unsigned char *array, int numsubvols)
{
        int       i    = 0;
        uintptr_t mask = 0;

        for (i = 0; i < numsubvols; i++)
                if (array[i])
                    mask |= (1ULL<<i);

        return mask;
}

void *write_thread (void *data)
{
        int ret = 0;
        int i = 0;
        int count = 0;
        share_data_t *share_data = data; 

        if (!share_data) {
                ret = -EINVAL;
                printf ("arg is invalid!\n");
                goto out;
        }

        while (1) {
                LOCK (&share_data->lock);
                for (i = 0; i < MAX_SUBVOLS_COUNT; i++) {
                        if (count % (i+1)) {
                                share_data->xl_up ^= 1ULL << i;
                        } else {
                                share_data->xl_up |= 1ULL << i;
                        }
                }
                UNLOCK (&share_data->lock);
                count++;
        }
out:
        return NULL;
}

void *read_thread (void *data)
{
        int i = 0;
        int ret = 0;
        share_data_t *share_data = data; 
        unsigned char up_subvols[MAX_SUBVOLS_COUNT] = {0,};

        if (!share_data) {
                ret = -EINVAL;
                printf ("arg is invalid!\n");
                goto out;
        }
        
        while (1) {
                memset (up_subvols, 0, MAX_SUBVOLS_COUNT);
                ec_mask_to_char_array (share_data->xl_up, up_subvols,
                                       MAX_SUBVOLS_COUNT); 

                for (i = 0; i < MAX_SUBVOLS_COUNT; i++) {
                        /*printf ("%d ", up_subvols[i]);*/
                        if (up_subvols[i] < 0 || up_subvols[i] > 1) {
                                printf ("ERROR: %d\n", up_subvols[i]);
                        }
                }
                /*printf ("\n");*/
                /*fflush (stdout);*/
        }

out:
        return NULL;
}

int main (void)
{
        int ret = 0;
        int i = 0;
        pthread_t threads[MAX_SUBVOLS_COUNT];
        share_data_t share_data;

        memset (&share_data, 0, sizeof(share_data_t));
        LOCK_INIT (&share_data.lock);

        for (i = 0; i < MAX_SUBVOLS_COUNT; i++) {
                if (i % 2)
                        ret = pthread_create (&threads[i], NULL, write_thread,
                                              (void*)&share_data);
                else
                        ret = pthread_create (&threads[i], NULL, read_thread,
                                              (void*)&share_data);
                if (ret != 0) {
                        printf ("ERROR: pthread_create() failed:%s\n",
                                strerror(errno));
                        break;
                }
        }

        printf ("Success to create %d threads\n", i);

        for (i = 0; i < MAX_SUBVOLS_COUNT; i++) {
                pthread_join (threads[i], NULL); 
        }

        LOCK_DESTROY (&share_data.lock);

        return ret;
}
