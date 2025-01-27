# -*- coding: utf-8 -*-
import os

from .directory import Directory, NotInteresting
from .file import NotAllowed
from .util import escape


class Tree(object):
    def __init__(self, path, destpath, options=None, log=None):
        assert os.path.isdir(path)
        self.path = path
        self.destpath = destpath
        self.options = {'quality': 8, 'gain': False, 'delete': False,
                        'maxrate': None, 'maxbits': None, 'lossycheck': True,
                        'hardlink': False, 'reflink': False,
                        'outside': False, 'inside': False}
        if options:
            self.options.update(options)
        self.log = log

    def allowed(self, root, dirname):
        path = os.path.join(root, dirname)
        if not os.path.islink(path):
            return True

        dest = os.path.join(root, os.readlink(path))
        outside = os.path.relpath(dest, self.path).startswith(os.path.pardir + os.path.sep)
        if outside and self.options['outside']:
            return True
        elif not outside and self.options['inside']:
            return True
        else:
            return False

    def commands(self):
        commands = []
        wanted = []
        num = 0
        if self.log:
            print("Walking source directory...", file=self.log)
        for root, dirs, files in os.walk(self.path, followlinks=True):
            for dirname in [dirname for dirname in dirs if not self.allowed(root, dirname)]:
                dirs.remove(dirname)
            num += 1
            if not num % 200:
                self.progress(num)
            relpath = os.path.relpath(root, self.path)
            if relpath != '.':
                destpath = os.path.join(self.destpath, relpath)
            else:
                destpath = self.destpath
            try:
                d = Directory(root, destpath, self.options, _files=files)
                c = d.commands()
                if c:
                    commands.append(c)
                if self.options['delete']:
                    wanted.extend(d.wanted())
            except NotInteresting:
                pass
            except NotAllowed as e:
                commands.append(['echo %s' % escape('%s: %s' % (root, str(e)))])

        if self.options['delete']:
            if self.log:
                print("Walking destination directory...", file=self.log)
            c = list(self.delete(wanted))
            if c:
                commands.append(c)
        return commands

    def delete(self, wanted):
        wanted = frozenset(wanted)
        num = 0
        for root, dirs, files in os.walk(self.destpath, topdown=False, followlinks=False):
            num += 1
            if not num % 2000:
                self.progress(num)
            for d in dirs:
                d = os.path.normpath(os.path.join(root, d))
                if d not in wanted:
                    yield 'rmdir %s' % escape(d)
            for f in files:
                f = os.path.normpath(os.path.join(root, f))
                if f not in wanted:
                    yield 'rm %s' % escape(f)

    def progress(self, num):
        if self.log:
            print("%s directories processed..." % num, file=self.log)
