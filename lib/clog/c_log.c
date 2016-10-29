#include <stdio.h>
#include <stdarg.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h> 
#include <errno.h>
#include <time.h>
#include "c_log.h"

#define TEST_LOG_PATH "/var/log/c_log_test.log"
#define MSG_LOG_TIMESTR_SIZE 256

static char *msg_log_level_strings[] = {
    "",  /*  NONE */
    "M", /*  EMERGENCY */
    "A", /*  ALERT */
    "C", /*  CRITICAL */
    "E", /*  ERROR */
    "W", /*  WARNING */
    "N", /*  NOTICE */
    "I", /*  INFO */
    "D", /*  DEBUG */
    "T", /*  TRACE */
    ""
};

FILE *log_fp = NULL;
int user_log_levl = MSG_LOG_INFO;

int log_init (char *log_path)
{
    int ret = 0;
    
    if (!log_path) {
        ret = -EINVAL;
        printf ("Arg is NULL! (%s)\n", strerror(-ret));
        goto out;
    }

    log_fp = fopen (log_path, "a+");
    if (!log_fp) {
        ret = -errno;
        printf ("Failed to open LOG_PATH=%s: %s\n", log_path, strerror(-ret));
        goto out;
    }

out:
    return ret;
}

int __log_msg (const char *domain, int levl,
               const char *file, const char *function,
               int line, const char *fmt, ...)
{
    int ret = 0;
    struct timeval tv = {0,};
    struct tm tm = {0,};
    char timestr[MSG_LOG_TIMESTR_SIZE] = {0,};
    char *timefmt = "%Y-%m-%d %H:%M:%S";
    va_list ap;
    size_t utime = 0;
    char *levl_str = NULL;

    if (!domain || !file || !function ||
            !fmt || !log_fp ||
            levl < 0 || line < 0) {
        goto out;
    }

    if (levl > user_log_levl)
        goto out; 

    ret = gettimeofday (&tv, NULL);
    if (ret)
        goto out;
    
    utime = tv.tv_sec;
    if (utime && localtime_r(&utime, &tm) != NULL)
        strftime (timestr, sizeof(timestr), timefmt, &tm);
    else {
        strncpy (timestr, "N/A", sizeof(timestr));
    }
    snprintf (timestr + strlen (timestr), sizeof (timestr) - strlen(timestr),
              ".%06ld", tv.tv_usec);
    fprintf (log_fp, "[%s] %s [%s:%d:%s] %s: ", timestr,
             msg_log_level_strings[levl], file, line,
             function, domain);
    fflush (log_fp);

    va_start (ap, fmt);
    vfprintf (log_fp, fmt, ap);
    va_end (ap);

    fprintf (log_fp, "\n");
    fflush (log_fp);
out:
    return ret;
}

int main (void)
{
    log_init (TEST_LOG_PATH);
    log_msg ("TEST", MSG_LOG_INFO, "hello world %d", 1);
    log_msg ("TEST", MSG_LOG_INFO, "hello world %s %d", "技术为王", 1);

    return 0;
}
