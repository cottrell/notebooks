class LatchNode():
    """ Runs once unless forced """
    def __init__(self, op):
        self.op = op
        self._yesrun = True
    def force(self):
        self._yesrun = True
    def maybe_run(self, force=False):
        status = 'NOOP'
        if force:
            self.force()
        if self._yesrun:
            self._lastresult = self.op()
            self._yesrun = False
            status = 'OP'
        return dict(status=status, res=self._lastresult)

import datetime
l = LatchNode(lambda : datetime.datetime.now())
