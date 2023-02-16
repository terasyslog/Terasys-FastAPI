#!/bin/bash

PKGDIR="$(dirname "$RUN")"
PID="./issue.pid"

ACCESS_LOGFILE_PATH="$PKGDIR/gunicorn_log/access.log"
ERROR_LOGFILE_PATH="$PKGDIR/gunicorn_log/error.log"
BIND=0.0.0.0:5000
WORKERS=4
WORKER_CLASS="uvicorn.workers.UvicornWorker"
LOG_FORMAT='%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
CMD="/home/anaconda3/envs/fastapi/bin/gunicorn"
COMMAND="gunicorn --bind $BIND main:app --workers $WORKERS --worker-class $WORKER_CLASS --access-logfile $ACCESS_LOGFILE_PATH --error-logfile $ERROR_LOGFILE_PATH"

echo $COMMAND

User=root

status() {
    echo
    echo "===== Status"

    if [ -f $PID ]
    then
        echo
        echo "Pid file: $( cat $PID ) [$PID]"
        echo
        ps -ef | grep -v grep | grep $( cat $PID )
    else
        echo
        echo "No Pid file"
    fi
}

start() {
    if [ -f $PID ]
    then
        echo
        echo "Already started. PID: [$( cat $PID )]"
    else
        echo "==== Start"
        touch $PID

	source /home/anaconda3/etc/profile.d/conda.sh
	conda activate fastapi

        if nohup $COMMAND >>$ACCESS_LOGFILE_PATH 2>&1 &
        then echo $! >$PID
             echo "Done."
             echo "$(date '+%Y-%m-%d %X'): START" >>$ACCESS_LOGFILE_PATH
        else echo "Error... "
             /bin/rm $PID
        fi
    fi
}

kill_cmd() {
    SIGNAL=""; MSG="Killing "
    while true
    do
        LIST=`ps -ef | grep -v grep | grep $CMD | grep -w $USR | awk '{print $2}'`
        if [ "$LIST" ]
        then
            echo; echo "$MSG $LIST" ; echo
            echo $LIST | xargs kill $SIGNAL
            sleep 2
            SIGNAL="-9" ; MSG="Killing $SIGNAL"
            if [ -f $PID ]
            then
                /bin/rm $PID
            fi
        else
           echo; echo "All killed..." ; echo
           break
        fi
    done
}

stop() {
    echo "==== Stop"

    if [ -f $PID ]
    then
        if kill $( cat $PID )
        then echo "Done."
             echo "$(date '+%Y-%m-%d %X'): STOP" >>$ACCESS_LOGFILE_PATH
        fi
        /bin/rm $PID
        kill_cmd
    else
        echo "No pid file. Already stopped?"
    fi
}

case "$1" in
    'start')
            start ;;
    'stop')
            stop ;;
    'restart')
            stop ; echo "Sleeping..."; sleep 1 ;
            start ;;
    'status')
            status ;;
    *)
            echo
            echo "Usage: $0 { start | stop | restart | status }"
            echo
            exit 1 ;;
esac

exit 0
