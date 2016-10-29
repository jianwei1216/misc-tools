#ifndef __C_LOG_H__
#define __C_LOG_H__

typedef enum {
    MSG_LOG_NONE,
    MSG_LOG_EMERG,
    MSG_LOG_ALERT,
    MSG_LOG_CRITICAL,   /*  fatal errors */
    MSG_LOG_ERROR,      /*  major failures (not necessarily fatal) */
    MSG_LOG_WARNING,    /*  info about normal operation */
    MSG_LOG_NOTICE,
    MSG_LOG_INFO,       /*  Normal information */
    MSG_LOG_DEBUG,      /*  internal errors */
    MSG_LOG_TRACE,      /*  full trace of operation */
} msg_log_level_t;

int __log_msg (const char *domain, int levl,
               const char *file, const char *function,
               int line, const char *fmt, ...);

#define log_msg(domain, levl, fmt...) do {                        \
            __log_msg (domain, levl, __FILE__, __FUNCTION__, __LINE__, ##fmt); \
        } while (0)


int log_init (char *log_path);
#endif
