from multiprocessing import cpu_count

# socket path
bind = 'unix:/home/workspace/fastApiServer/gunicorn.sock'

# worker options
workers = cpu_count() + 1
worker_class = 'uvicorn.workers.UvicornWorker'

# Logging Option
loglevel = 'debug'
accesslog = '/home/workspace/fastApiServer/gunicorn_log/access_log'
errorlog = '/home/workspace/fastApiServer/gunicorn_log/error_log'
