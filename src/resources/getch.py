class _Getch:
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            try:
                self.impl = _GetchMacCarbon()
            except (AttributeError, ImportError):
                self.impl = _GetchUnix()

    def __call__(self): return self.impl()

class _GetchUnix:
    def __init_(self):
        import tty, sys, termios

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

class _GetchMacCarbon:
    def __init__(self):
        import Carbon
        if Carbon.Evt.EventAvail(0x0008)[0]==0:
            return ''
        else:
            (what, msg, where, mod) = Carbon.Evt.GetNextEvent(0x0008)[1]
            return chr(msg & 0x000000FF)

if __name__ == '__main__':
    print ('Press a key')
    inkey = _Getch()
    import sys
    #for i in range(sys.maxsize):
    #    k = inkey()
    #    if k < '':break
    print ('you pressed ', inkey())
