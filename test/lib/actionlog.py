""" The PyUnit test framework for the actionlog. """

import atexit
import os
import subprocess
import unittest
import pysumo

from io import BytesIO
from pysumo.logger import actionlog
from os.path import isfile
from random import SystemRandom
from shutil import rmtree
from tempfile import mkdtemp
from time import sleep
from threading import Thread

ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'x', 'y', 'z', ' ', '\t', ')', '(', ';', ':', '.']

def corrupt(source, dest, number=200):
    random = SystemRandom()
    sbuf = source.getbuffer()
    length = len(source.getvalue().decode('utf8', errors='replace').split('\n'))
    waitlist = set()
    for i in range(0, number):
        f = '/'.join([dest, '%03d.kif' % i])
        lines = set()
        for j in range(0, random.randint(0, int(length / 1000))):
            line = random.randint(1, length - j)
            lines.add('%dd' % line)
        deletes = ';'.join(lines)
        args = ['sed', deletes]
        popen = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        stdout, _ = popen.communicate(sbuf)
        popen.wait()
        with open(f, 'w+b') as cur:
            cur.write(sbuf)
            cur.flush()
        if random.choice([True, False]):
            count = random.randint(1, 6)
            src = ''.join(random.sample(ALPHABET, count))
            dst = ''.join(random.sample(ALPHABET, count))
            args = ['sed', 'y/%s/%s/' % (src, dst)]
            cur = open(f, 'w+b')
            waitlist.add((subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE), cur, stdout))
        else:
            with open(f, 'w+b') as cur:
                cur.write(stdout)
                cur.flush()
    for proc, cur, content in waitlist:
        stdout, _ = proc.communicate(content)
        proc.wait()
        cur.write(stdout)
        cur.flush()
        cur.close()

class actionLogTestCase(unittest.TestCase):
    def setUp(self):
        self.tmpdir = mkdtemp()
        self.al = actionlog.ActionLog('test', path=self.tmpdir)
        atexit.unregister(self.al.log_io.flush_write_queues)

    def tearDown(self):
        self.al.log_io.flush_write_queues()
        rmtree(self.tmpdir)

    def add_and_ok(self, data):
        num = self.al.queue_log(data)
        self.al.ok_log_item(num)
        assert self.al.queue == (None, None)
        assert self.al.current.getvalue() == data.getvalue()

    def test0Init(self):
        num = self.al.queue_log(SUMO)
        assert isinstance(num, int)
        qnum, diff = self.al.queue
        assert num == qnum
        assert diff is SUMO

    def test1OKQueue(self):
        self.add_and_ok(SUMO)
        self.assertEqual(self.al.current.getvalue(), SUMO.getvalue())
        assert len(self.al.actionlog) == 1
        assert isinstance(self.al.actionlog.pop(), BytesIO)

    def test2AddAction(self):
        randomize.join()
        self.add_and_ok(SUMO)
        while not isfile('/'.join([CORRUPTDIR, '003.kif'])):
            sleep(1)
        with open('/'.join([CORRUPTDIR, '000.kif']), 'r+b') as kif:
            new = BytesIO(kif.read())
        self.add_and_ok(new)
        diff = self.al.actionlog[1].getvalue().decode('utf8')
        self.assertNotEqual(diff, '')
        diff0 = self.al.actionlog[0].getvalue().decode('utf8')
        self.assertNotEqual(diff, diff0)
        self.assertEqual(len(self.al.actionlog), 2)
        self.al.log_io.flush_write_queues()
        self.assertEqual(os.listdir(self.tmpdir), ['test'])
        self.assertEqual(sorted(os.listdir('/'.join([self.tmpdir, 'test']))), sorted(['current', 'redo', 'undo']))
        self.assertEqual(sorted(os.listdir('/'.join([self.tmpdir, 'test', 'undo']))), sorted(['000', '001']))
        with open('/'.join([self.tmpdir, 'test', 'undo', '001'])) as patchfile:
            patch = patchfile.read()
            self.assertNotEqual(patch, '')
            self.assertEqual(patch, diff)

    def test3Undo(self):
        self.add_and_ok(SUMO)
        with open('/'.join([CORRUPTDIR, '000.kif']), 'r+b') as kif:
            new = BytesIO(kif.read())
        self.add_and_ok(new)
        undoed = self.al.undo().getvalue()
        self.assertEqual(undoed.decode('utf8', errors='replace'), SUMO.getvalue().decode('utf8', errors='replace'))
        self.assertEqual(undoed, SUMO.getvalue())
        self.al.log_io.flush_write_queues()
        self.assertEqual(sorted(os.listdir('/'.join([self.tmpdir, 'test', 'undo']))), sorted(['000']))
        self.assertEqual(sorted(os.listdir('/'.join([self.tmpdir, 'test', 'redo']))), sorted(['000']))

    def test4Redo(self):
        self.add_and_ok(SUMO)
        with open('/'.join([CORRUPTDIR, '000.kif']), 'r+b') as kif:
            new = BytesIO(kif.read())
        self.add_and_ok(new)
        self.al.undo()
        self.assertEqual(self.al.redo().getvalue(), new.getvalue())
        self.al.log_io.flush_write_queues()
        self.assertEqual(sorted(os.listdir('/'.join([self.tmpdir, 'test', 'undo']))), sorted(['000', '001']))
        self.assertEqual(sorted(os.listdir('/'.join([self.tmpdir, 'test', 'redo']))), [])

    def test5SizeFlush(self):
        self.add_and_ok(SUMO)
        for kif in os.listdir(CORRUPTDIR)[:9]:
            with open('/'.join([CORRUPTDIR, kif]), 'r+b') as mkif:
                new = BytesIO(mkif.read())
            self.add_and_ok(new)
        self.assertEqual(len(self.al.actionlog), 10)
        assert self.al.log_io.uwrite_queue == [], 'uwrite_queue is %s, but should be []' % self.al.log_io.uwrite_queue
        assert sorted(os.listdir('/'.join([self.tmpdir, 'test', 'undo']))) == sorted(['%03d' % x for x in range(0, 10)]), 'undo contains %s, but should contain %s' % (sorted(os.listdir('/'.join([self.tmpdir, 'test', 'undo']))), sorted(['%03d' % x for x in range(0, 10)]))

    def test6QueueOverwrite(self):
        self.add_and_ok(SUMO)
        for kif in os.listdir(CORRUPTDIR)[:2]:
            with open('/'.join([CORRUPTDIR, kif]), 'r+b') as mkif:
                new = BytesIO(mkif.read())
            num = self.al.queue_log(new)
        qnum, diff = self.al.queue
        self.assertEqual(num, qnum)
        self.assertEqual(diff, new)
        self.al.ok_log_item(num)
        self.assertEqual(len(self.al.actionlog), 2)
        self.al.log_io.flush_write_queues()
        self.assertEqual(os.listdir(self.tmpdir), ['test'])
        self.assertEqual(sorted(os.listdir('/'.join([self.tmpdir, 'test']))), sorted(['current', 'redo', 'undo']))
        self.assertEqual(sorted(os.listdir('/'.join([self.tmpdir, 'test', 'undo']))), sorted(['000', '001']))

    def test7ExcessiveUndo(self):
        self.add_and_ok(SUMO)
        for kif in os.listdir(CORRUPTDIR)[:6]:
            with open('/'.join([CORRUPTDIR, kif]), 'r+b') as mkif:
                new = BytesIO(mkif.read())
            self.add_and_ok(new)
        for i in range(0, 10):
            self.al.undo()
        self.assertEqual(self.al.redo().getvalue(), SUMO.getvalue())

    def test8ExcessiveRedo(self):
        self.add_and_ok(SUMO)
        for kif in os.listdir(CORRUPTDIR)[:9]:
            with open('/'.join([CORRUPTDIR, kif]), 'r+b') as mkif:
                new = BytesIO(mkif.read())
            self.add_and_ok(new)
        self.assertEqual(self.al.redo().getvalue(), new.getvalue())

    def test9HammerTime(self):
        self.add_and_ok(SUMO)
        for kif in os.listdir(CORRUPTDIR)[:50]:
            with open('/'.join([CORRUPTDIR, kif]), 'r+b') as mkif:
                new = BytesIO(mkif.read())
            self.add_and_ok(new)
        undoes = sorted(os.listdir('/'.join([self.tmpdir, 'test', 'undo'])))
        redoes = sorted(os.listdir('/'.join([self.tmpdir, 'test', 'redo'])))
        curr = self.al.current
        for i in range(0, 20):
            self.al.undo()
            self.al.redo()
        self.assertEqual(sorted(os.listdir('/'.join([self.tmpdir, 'test', 'redo']))), redoes)
        assert sorted(os.listdir('/'.join([self.tmpdir, 'test', 'undo']))) == undoes, 'undo is %s, but should be %s' % (sorted(os.listdir('/'.join([self.tmpdir, 'test', 'undo']))), undoes)
        self.assertEqual(self.al.current.getvalue(), curr.getvalue())
        for i in range(0, 17):
            self.al.undo()
        for i in range(0, 13):
            self.al.redo()
        self.al.undo()
        self.al.redo()
        self.assertEqual(sorted(os.listdir('/'.join([self.tmpdir, 'test', 'redo']))), sorted(['%03d' % x for x in range(0, 4)]))
        for kif in os.listdir(CORRUPTDIR)[50:]:
            with open('/'.join([CORRUPTDIR, kif]), 'r+b') as mkif:
                new = BytesIO(mkif.read())
            self.add_and_ok(new)
        self.assertEqual(self.al.current.getvalue(), new.getvalue())
        assert sorted(os.listdir('/'.join([self.tmpdir, 'test', 'undo']))) == sorted(['%03d' % x for x in range(0, 110)]), 'undo is %s, but should be %s' % (sorted(os.listdir('/'.join([self.tmpdir, 'test', 'undo']))), sorted(['%03d' % x for x in range(0, 110)]))
        self.assertEqual(sorted(os.listdir('/'.join([self.tmpdir, 'test', 'redo']))), [])

    def test10FalseOk(self):
        num = self.al.queue_log(SUMO)
        self.assertRaises(KeyError, self.al.ok_log_item, num + 1)

    def test11ReadLogPath(self):
        self.add_and_ok(SUMO)
        self.al.log_io.flush_write_queues()
        current = self.al.current.getvalue()
        del self.al
        self.al = actionlog.ActionLog('test', path=self.tmpdir)
        atexit.unregister(self.al.log_io.flush_write_queues)
        self.assertEqual(self.al.current.getvalue(), current)


actionLogSuit = unittest.makeSuite(actionLogTestCase, 'test')
CORRUPTDIR = mkdtemp()
atexit.register(rmtree, CORRUPTDIR)
with open('src/pysumo/data/Merge.kif', 'r+b') as kif:
    SUMO = BytesIO(kif.read())
randomize = Thread(target=corrupt, name='kif-randomizer', args=(SUMO, CORRUPTDIR))
randomize.start()

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(actionLogSuit)
