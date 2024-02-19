"""ThreadPool based on ThreadPoolExecutor

See:
    https://docs.python.org/3/library/concurrent.futures.html
"""

import concurrent.futures
import uuid
import time
import queue
import threading
from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime

import anfler.util.msg.message as msg
import anfler.util.constants as C
from anfler.util.log.lw import get_logger,level
from anfler.util.helper import get_childs_process, get_childs_process_details, kill_process


_log = get_logger("anfler.mp")
_stat = get_logger("anfler.mp.stat")


class Monitor(threading.Thread):
    __INTERVAL=10
    __TIMEOUT__ = 60
    def __init__(self, interval=__INTERVAL, timeout=__TIMEOUT__, futures=[]):
        self.interval = interval
        self._timeout = timeout
        self._futures = futures

        self.stop_event = threading.Event()
        threading.Thread.__init__(self,name="anfler_monitor")

    def run(self):
        while not self.stop_event.wait(self.interval):
            _log.debug("Executing monitor thread")
            try:
                thds = threading.enumerate()
                num_thds = len(thds)
                _log.debug(f"Active threads = {num_thds}")
                for i, t in enumerate(thds):
                    msg = f"#{i:02d} tid={t.ident} nid={t.native_id} name={t.name}"
                    _log.debug(msg)

                childs = get_childs_process_details()
                num_childs_thds = sum([v["thds_num"] for k, v in childs.items()])
                _log.debug(f"Active childs={len(childs)} num_child_thds={num_childs_thds}")

                childs_with_timeout=0
                for i,child in enumerate(childs.items()):
                    elapsed = time.time() - child[1]["create_time"]
                    if elapsed >= self._timeout:
                        childs_with_timeout += 1
                        _log.warning(f"#{i:02d} pid/ppid={child[1]['pid']}/{child[1]['ppid']} status={child[1]['status']} name={child[1]['name']} elapsed={elapsed:.1f} num_threads={child[1]['thds_num']} threads={child[1]['thds']}")
                    else:
                        _log.debug(f"#{i:02d} pid/ppid={child[1]['pid']}/{child[1]['ppid']} status={child[1]['status']} name={child[1]['name']} elapsed={elapsed:.1f} num_threads={child[1]['thds_num']} threads={child[1]['thds']}")

                futures_with_timeout=0
                for i,f in enumerate(self._futures):
                    elapsed = time.time() - f.t0
                    if elapsed >= self._timeout:
                        futures_with_timeout += 1
                        _log.warning(f"#{i:02d} future={f.id} name={f.name} elapsed={elapsed:.1f} running={f.running()}")
                    else:
                        _log.debug(f"#{i:02d} future={f.id} name={f.name} elapsed={elapsed:.1f} running={f.running()}")

                # if self._interval_counter >= self.interval_count:
                #     self._interval_counter=0
                #     _log.info(f"Active childs={len(childs)} num_child_thds={num_childs_thds} childs_with_timeout={childs_with_timeout}")
                #     _log.info(f"Active futures={len(self._futures)} futures_with_timeout={futures_with_timeout}")

                _log.info(f"Active childs={len(childs)} num_child_thds={num_childs_thds} childs_with_timeout={childs_with_timeout}. "
                          f"Active futures={len(self._futures)} futures_with_timeout={futures_with_timeout}")
            except Exception as e:
                _log.warning(f"Getting some error. Ignoring: {str(e)}",stack_info=False)
        _log.info("Stopping monitor thread")

    def stop(self):
        self.stop_event.set()


def _init_future(*args):
    pass

class RestrictedThreadPoolExecutor(ThreadPoolExecutor):
    __INTERVAL=10
    __INTERVAL_COUNT = 3
    __TIMEOUT__=60
    __WAIT_TIMEOUT_SECS__=None
    def __init__(self, max_workers=3, preffix="anfler", wait_timeout_sec=__WAIT_TIMEOUT_SECS__, monitor_timeout_sec=__TIMEOUT__ , monitor_interval_sec=__INTERVAL, monitor_interval_count=__INTERVAL_COUNT, child_process_names=[]):
        self.task_max = max_workers
        self._preffix = preffix
        self._child_process_names = child_process_names
        self.__WAIT_TIMEOUT_SECS__ = wait_timeout_sec
        super().__init__(max_workers=max_workers,thread_name_prefix=preffix,initializer=_init_future())

        self._futures = []
        self._monitor=None
        self.__launchMonitor(monitor_interval_sec, monitor_timeout_sec)
        # @TBD
        # self._done_jobs = queue.SimpleQueue()
        self._future_with_timeout=False
        _log.info(f"Pool started with max_workers={max_workers} monitor_interval={monitor_interval_sec} monitor_timeout_sec={monitor_timeout_sec}")

    def __launchMonitor(self, monitor_interval_sec=__INTERVAL, monitor_timeout_sec=__TIMEOUT__):
        _log.info(f"Starting monitor thread.")
        self._monitor = Monitor(interval=monitor_interval_sec, timeout=monitor_timeout_sec, futures=self._futures)
        self._monitor.start()



    def __get_threads_info(self, threads=None):
        thds=[]
        if threads == None:
            thds=self._threads
        else:
            thds=[threads]
        return [{t.name: {"tid": t._ident, "nid": t._native_id}} for t in thds]

    def __task_done(self, future):
        """Task done callback, see https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Future.add_done_callback
        Log to _stat logger
        """
        future.t1 = time.time()
        _log.debug(f"Future done id={future.id} name={future.name} t0={future.t0} t1={future.t1}. {future}")
        dt=datetime.now().strftime("%Y%m%d%H%M%S")
        _stat.info(f"{dt},{future.id},{future.name},{future.t0},{future.t1},{future._state},{str(future._exception).rstrip()}")


    def _printthds(self):
        for t in self._threads:
            print(t.name, t.ident, t.native_id)

    def     submit(self, fn, /, *args, **kwargs):
        """Submit a new task (See ThreadPoolExecutor.submit)
        Add the following field to the future:
        - name: function name (fn)
        - id: uuid4()
        - t0: current time
        - t1: to be filled by __task_done()

        :param fn: function name
        :param args: function args
        :param kwargs: function kwargs
        :return: task id (uuid)
        """
        name = fn.__name__
        if fn.__name__ == "execute_class_method":
            name=f"{fn.__name__}_{kwargs.get('string_func','')}"
        id=str(uuid.uuid4())
        t0=time.time()
        future = super().submit(fn, *args, **kwargs)
        future.name=name
        future.t0=t0
        future.t1=0
        future.id= id
        future.add_done_callback(self.__task_done)
        self._futures.append(future)
        _log.debug(f"qsize={self._work_queue.qsize()} future={future.id},{future.name}. {future}")
        return id


    def __kill_child(self,childs):
        for p in childs:
            try:
                _log.debug(f"Killing pid={p.pid} name={p.name()} status={p.status()}")
                # Seems that the following doesn't work properly
                # p.kill()
                kill_process(p.pid)
            except Exception as e:
                _log.warning(f"Got some error getting childs, ignoring. {str(e)}")

    def kill_childs(self, process=[]):
        """Kill child processes if futures are running after reach timeout

        :param process: list of process names to kill
        :return: None
        """
        _log.warning(f"Running futures={len(self._futures)}")
        for f in self._futures:
            _log.debug(f"Future id={f.id} running={f.running()}")
        if len(process) == 0:
            childs = get_childs_process(process)
        else:
            childs = get_childs_process(self._child_process_names)
        try:
            _log.info(f"Found {len(childs)} child process")
            for i, child in enumerate(childs):
                thds = [t.id for t in child.threads()]
                elapsed = time.time() - child.create_time()
                _log.warning(f"Child process #{i:02d} {child.name()} pid={child.pid} status={child.status()} threads={len(thds)} elapsed={elapsed:.1f}")
            self.__kill_child(childs)
            # Avoid defunct
            childs = get_childs_process(process)
            self.__kill_child(childs)
            for i, child in enumerate(childs):
                thds = [t.id for t in child.threads()]
                elapsed = time.time() - child.create_time()
                _log.warning(f"Remaining child process #{i:02d} {child.name()} threads={len(thds)} elapsed={elapsed:.1f}")
        except:
            pass
        if len(self._futures) == 0:
            self._future_with_timeout = False


    def shutdown(self, wait=True):
        super().shutdown(wait)
        self._monitor.stop()
        #self._cleanup()
        self.kill_childs()
        _log.info("Shutdown done")


    def isFull(self):
        """Check if internal queue size is less than max configured tasks"""
        return self._work_queue.qsize() >= self.task_max

    def getSize(self):
        """Get internal queue size (concurrent._work_queue.qsize() and number of threads (fitered by preffix)

        :returns array [self._work_queue.qsize(),len(thds)]
        """
        thds = [t for t in threading.enumerate() if t.name.startswith(self._preffix)]
        return [self._work_queue.qsize(),len(thds)]

    def pending_jobs(self):
        """Check if there are pending jobs (futures still running)
        :return: Number of running futures
        """
        if len(self._futures) > 0:
            count=0
            for f in self._futures:
                if f.running(): count+= 1
            return count
            #[count+=1 if f.running() for f in self._futures]
        else:
            return 0


    def wait(self, timeout=__WAIT_TIMEOUT_SECS__):
        """Return result from task. If futures reach timeout mark "_future_with_timeout" (see

        :param timeout: Wait for task (see https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.wait)
        :return: Array of BASIC_MESSAGE
                [{
                id: future.id
                header.fn : future.name
                status: constants.ERRORS_CDDE.OK | constants.ERRORS_CDDE.GENERIC_ERROR1
                errors: error if defined
                payload: future.result()
                }]

        """
        results=[]

        try:
            for future in concurrent.futures.as_completed(self._futures, timeout=timeout):
                _log.debug(f"Future back {future.id, future.name}. {future}")
                response = msg.get_basic_message(header={"fn":future.name})
                try:
                    response = msg.update_message(response, id=future.id, status=C.ERRORS_CDDE.OK, payload=future.result())
                except Exception as e:
                    _log.warning(f"Future {future.id, future.name} end with exception. {str(e)}",exc_info=True)
                    response = msg.update_message(response, id=future.id, status=C.ERRORS_CDDE.GENERIC_ERROR1,errors=[str(future.exception())])
                results.append(response)
                self._futures.remove(future)
        except concurrent.futures.TimeoutError as te:
            _log.warning(f"Futures count={len(self._futures)} reach timeout, qsize={self.getSize()}. {str(te)}", exc_info=False)
            self._future_with_timeout = True
        except Exception as e:
            _log.warning(f"Error waiting", exc_info=True)
        return results
