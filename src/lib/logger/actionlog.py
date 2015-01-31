""" The pySUMO action log handler. This module handles undo and redo operations.

This module contains:

- ActionLog: The action log handler.
- LogIO: The action log io interface.

"""

import os
import signal
import subprocess

from atexit import register as atexit
from io import BytesIO
from random import SystemRandom

from lib.logger import CONFIG_PATH

class ActionLog():
    """ The pySUMO action log. The SyntaxController queues a new log entry before every
    operation that makes changes to an Ontology, if the change is successful it OKs the
    entry in the log queue and the entry is written out. Log entries that are not OKed
    time out and are removed from the queue.

    Variables:

    - log_io: The io object for this log.
    - queue: A queue of actions that have not yet successfully completed.
    - actionlog: A list of actions that have completed successfully.
    - redolog: A list of actions that have been undone successfully.
    - current: The current state of the Ontology.

    Methods:

    - queue_log: Create a log entry and append it to the log queue.
    - ok_log_item: Move log entry from log queue to actual log.
    - undo: Undoes the last action.
    - redo: Redoes the last undone action.

    """

    def __init__(self, name, path=None):
        """ Initializes the action log and instantiates variables. """
        self.log_io = LogIO(name, path)
        self.current, self.actionlog, self.redolog = self.log_io.read()
        self.queue = (None, None)
        self._rand = SystemRandom()

    def _rand_lognum(self):
        """ Returns a log entry number that is not already in the queue. """
        lognum = self._rand.getrandbits(32)
        return lognum if lognum not in self.queue else self._rand_lognum()

    def queue_log(self, data):
        """ Create a log entry and queue it for addition to self.actionlog.

        Args:

        - data: the data to be placed in the log

        Returns:

        - int. The log_queue_ok_num

        """
        num = self._rand_lognum()
        self.queue = (num, data)
        return num

    def ok_log_item(self, log_queue_ok_num):
        """ Appends the item in self.queue with log_queue_ok_num to self.actionlog
        and calls self.log_io.append_write_queue on it.

        Args:

        - log_queue_ok_num: the number of the queue item to okay

        Raises:

        - KeyError

        """
        num, entry = self.queue
        if not num == log_queue_ok_num:
            raise KeyError(num)
        if self.current is None:
            self.current = entry
        diff = self.log_io.diff(self.current, entry)
        self.current = self.log_io.redo(self.current, diff)
        self.actionlog.append(diff)
        self.redolog.clear()
        self.log_io.clear('redo')
        self.queue = (None, None)

    def undo(self):
        """ Undoes the last action and appends it to self.redolog. """
        self.log_io.flush_write_queues(None, None)
        try:
            diff = self.actionlog.pop()
        except IndexError:
            return self.current
        self.current = self.log_io.undo(self.current, diff)
        self.redolog.append(diff)
        return self.current

    def redo(self):
        """ Redoes the last undone action, appends it to self.undolog
        and removes it from self.redolog. """
        self.log_io.flush_write_queues(None, None)
        try:
            diff = self.redolog.pop()
        except IndexError:
            return self.current
        self.current = self.log_io.redo(self.current, diff, clean=True)
        self.actionlog.append(diff)
        return self.current

class LogIO():
    """ The IO interface for the pySUMO action log. This class provides a storage
    backend for the Action Log. Entries in the write queue are written to disk
    after a timeout, or when the write queue reaches a maximum size.

    Variables:

    - default_path: The default log path.
    - timeout: The time period after which if no new packets have entered the queue, the queue is flushed.
    - max_size: The maximum number of actions in the write queue after which when another packet enters the queue, the queue is flushed.
    - max_diffs: When the number of stored diffs exceeds max_diffs, old diffs will be deleted.
    - path: The log path (defaults to default_path).
    - name: The name of the Ontology.
    - current: The path to the current state of the Ontology.
    - uwrite_queue: The queue in which undo actions are stored before being written to disk.
    - rwrite_queue: The queue in which redo actions are stored before being written to disk.

    Methods:

    - diff: Creates a diff between 2 Files
    - read: Instantiates an Action Log with the data in the stored log at path.
    - flush_write_queues: Appends all entries in the write queue to the log file.
    - clear: Clears a queue in memory and on disk.
    - pop: Removes the last entry from a queue.
    - undo: Appends an entry to the redo write queue.
    - redo: Appends an entry to the undo write queue.

    """

    default_path = '/'.join([CONFIG_PATH, 'actionlog'])
    timeout = 10
    max_size = 10
    max_diffs = 100

    def __init__(self, name, path=default_path):
        """ Initializes the IO interface for an action log. """
        self.path = path if path is not None else self.default_path
        self.name = name
        try:
            for sub in ['undo', 'redo']:
                os.makedirs('/'.join([self.path, self.name, sub]), exist_ok=True)
        except PermissionError:
            self.path = self.default_path
            for sub in ['undo', 'redo']:
                os.makedirs('/'.join([self.default_path, self.name, sub]), exist_ok=True)
        self.current = '/'.join([self.path, self.name, 'current'])
        self.uwrite_queue = []
        self.rwrite_queue = []
        atexit(self.flush_write_queues)

    def diff(self, current, new):
        """ Returns a diff between current and new. """
        args = ['diff', '-u', self.current, '-']
        with open(self.current, 'w+b') as cur:
            cur.write(current.getbuffer())
            cur.flush()
        popen = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        stdout, _ = popen.communicate(new.getbuffer())
        return BytesIO(stdout)

    def _patch(self, current, diff, reverse=False):
        """ Returns current after diff has been applied to it. """
        args = ['patch', '-u', '-N', self.current]
        if reverse:
            args.append('-R')
        with open(self.current, 'w+b') as cur:
            cur.write(current.getbuffer())
            cur.flush()
        popen = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL)
        popen.communicate(diff.getbuffer())
        with open(self.current, 'r+b') as cur:
            return BytesIO(cur.read())

    def read(self):
        """ Reads the log at self.path into log. """
        cur = None
        undoes = list()
        redoes = list()
        files = list()
        cwd = os.getcwd()
        try:
            with open(self.current, 'r+b') as c:
                cur = BytesIO(c.read())
            os.chdir('/'.join([self.path, self.name, 'undo']))
            files = os.listdir()
            files.sort()
            for undo in files:
                with open(undo, 'r+b') as u:
                    undoes.append(BytesIO(u.read()))
            os.chdir('/'.join([self.path, self.name, 'redo']))
            files = os.listdir()
            files.sort()
            for redo in files:
                with open(redo, 'r+b') as r:
                    undoes.append(BytesIO(r.read()))
        except FileNotFoundError:
            pass
        os.chdir(cwd)
        return cur, undoes, redoes

    def flush_write_queues(self, _=None, __=None):
        """ Flush self.rwrite_queue and self.uwrite_queue to disk. """
        signal.alarm(0)
        cwd = os.getcwd()
        ucopy = self.uwrite_queue.copy()
        self.uwrite_queue.clear()
        rcopy = self.rwrite_queue.copy()
        self.rwrite_queue.clear()
        self._flush_write_queue(ucopy, 'undo')
        self._flush_write_queue(rcopy, 'redo')
        os.chdir(cwd)

    def _flush_write_queue(self, queue, name):
        """ Flushes queue to disk. """
        os.chdir('/'.join([self.path, self.name, name]))
        files = os.listdir()
        files = self._refactor(files) if len(files) > self.max_diffs else sorted(files)
        i = len(files)
        for entry in queue:
            with open('%03d' % i, 'w+b') as ent:
                ent.write(entry.getbuffer())
                ent.flush()
            i += 1

    def _refactor(self, files):
        """ Removes excess entries in queue and reorganizes it. """
        files.sort(reverse=True)
        while len(files) > self.max_diffs:
            os.remove(files.pop())
        files.sort()
        new_names = sorted(['%03d' % x for x in range(0, 100)], reverse=True)
        for f in files:
            os.rename(f, new_names.pop())
        return sorted(os.listdir())

    def clear(self, queue):
        """ Clears queue both in memory and on disk. """
        self.rwrite_queue.clear()
        cwd = os.getcwd()
        os.chdir('/'.join([self.path, self.name, queue]))
        for f in os.listdir():
            os.remove(f)
        os.chdir(cwd)


    def pop(self, queue):
        """ Removes the last entry in queue. """
        cwd = os.getcwd()
        os.chdir('/'.join([self.path, self.name, queue]))
        files = os.listdir()
        files.sort()
        os.remove(files.pop())
        os.chdir(cwd)

    def undo(self, current, entry):
        """ Append entry to self.rwrite_queue. """
        self.rwrite_queue.append(entry)
        self.pop('undo')
        if len(self.rwrite_queue) < self.max_size:
            signal.signal(signal.SIGALRM, self.flush_write_queues)
            signal.alarm(self.timeout)
        else:
            self.flush_write_queues()
        return self._patch(current, entry, reverse=True)

    def redo(self, current, entry, clean=False):
        """ Append entry to self.uwrite_queue.
        If clean is True, pop an object from the redo queue. """
        self.uwrite_queue.append(entry)
        if clean:
            self.pop('redo')
        if len(self.uwrite_queue) < self.max_size:
            signal.signal(signal.SIGALRM, self.flush_write_queues)
            signal.alarm(self.timeout)
        else:
            self.flush_write_queues(None, None)
        return self._patch(current, entry)
