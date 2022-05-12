import socket
import subprocess
import time

from redis import Redis
from rq import Queue, Worker

from magna.config import REDIS_HOST, REDIS_PASS, RQ_GENERAL, CONDA_PATH


def rq_start_worker():
    """Start a pre-configured RQ worker that will listen on two queues:
        - The "general" queue.
        - The "host" queue.
    """
    host_name = socket.gethostname()
    worker_name = f'{host_name}-{int(time.time())}'
    with Redis(host=REDIS_HOST, password=REDIS_PASS) as conn:
        q_host = Queue(host_name, connection=conn, default_timeout='60d')
        q_general = Queue(RQ_GENERAL, connection=conn, default_timeout='60d')
        worker = Worker([q_host, q_general], connection=conn, name=worker_name)
        worker.work()


def rq_run_conda(env: str, cmd: str):
    """Run a shell command in a conda environment.

    Args:
        env: The name of the conda environment to use.
        cmd: The command to run.
    """
    cmd = f'. {CONDA_PATH} && conda activate {env} && {cmd}'
    proc = subprocess.run(cmd, shell=True, capture_output=True,
                          encoding='utf-8', check=True, executable='/bin/bash')
    if proc.returncode != 0:
        raise Exception(f'{cmd} failed with code {proc.returncode}')
    return


def rq_enqueue_conda(queue: str, env: str, cmd: str):
    """Enqueue a shell command in a conda environment.

    Args:
        queue: The name of the queue to use.
        env: The name of the conda environment to use.
        cmd: The command to run.
    """
    with Redis(host=REDIS_HOST, password=REDIS_PASS) as conn:
        q_host = Queue(queue, connection=conn, default_timeout='60d')
        q_host.enqueue(rq_run_conda, args=(env, cmd,))


def rq_delete_queue(queue: str):
    """Delete a queue and all jobs contained in it.

    Args:
        queue: The name of the queue to delete.
    """
    with Redis(host=REDIS_HOST, password=REDIS_PASS) as conn:
        q = Queue(queue, connection=conn)
        q.delete(delete_jobs=True)
