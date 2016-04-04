# coding: utf-8
"""一个简单的线程池实现
usage:
    from threadpool import ThreadPool

    class WorkPool(ThreadPool):
        def __init__(self, threads):
            # implement it

        def work(self, job):
            # implement it

        def run(self):
            # implement
"""
import Queue
import logging
import threading


class ThreadPool(object):
    """Handler with a fixed size pool of threads which process some tasks."""

    def __init__(self, threads=10, delay=None, daemon=False):
        self.queue = Queue.Queue()
        self.threads = threads
        self.daemon = daemon
        self.delay = delay

    def workerThread(self):
        """ Loop around getting arguments from the shared queue,
        and process them.
        """
        while True:
            try:
                args = self.queue.get()
                self.serve(args)
            except Exception as err:
                logging.exception(err)

    def work(self, num):
        """Process any operations in here."""
        raise NotImplementedError()

    def start(self):
        """Start a fixed number of worker threads and call the run method."""
        for i in range(self.threads):
            try:
                t = threading.Thread(target=self.serveThread)
                t.setDaemon(self.daemon)
                t.start()
            except Exception as x:
                logging.exception(x)

        self.run()

    def run(self):
        """Actually running part and put arguments into a queue"""
        raise NotImplementedError()
