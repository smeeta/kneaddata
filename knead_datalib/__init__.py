import os
import sys
import logging
import tempfile
from math import floor
from functools import partial
from contextlib import contextmanager
from multiprocessing import cpu_count

def divvy_threads(args):
    avail_cpus = args.threads or cpu_count()-1
    n_consumers = len(args.reference_db)
    trim_threads = 1
    align_threads = max(1, floor(avail_cpus/float(n_consumers)))
    return int(trim_threads), int(align_threads)
    

def try_create_dir(d):
    if not os.path.exists(d):
        logging.warning("Directory `%s' doesn't exist. Creating.", d)
        try:
            os.makedirs(d)
        except Exception as e:
            logging.crit("Unable to create directory `%s': %s", d, str(e))
            sys.exit(1)


@contextmanager
def mktempfifo(names=("a",)):
    tmpdir = tempfile.mkdtemp()
    names = map(partial(os.path.join, tmpdir), names)
    map(os.mkfifo, names)
    yield names
    map(os.remove, names)
    os.rmdir(tmpdir)


def process_return(name, retcode, stdout, stderr):
    if retcode:
        log = logging.critical
        log("%s exited with exit status %d", name, retcode)
    else:
        log = logging.debug
    if stdout:
        log("%s stdout:\n%s", name, stdout)
    if stderr:
        log("%s stderr:\n%s", name, stderr)
    if retcode:
        sys.exit(retcode)
