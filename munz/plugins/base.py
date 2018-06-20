import asyncio

class MzBase(object):
    def __init__(self, munz):
        self.bokdali = munz

    def proc_msg(self, msg): pass

    @asyncio.coroutine
    def go_msg(self, ch, msg):
        yield from self.bokdali.go_msg(ch, msg)
