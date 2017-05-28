import readchar

def char_generator_from_repl():
    while True:
        x = readchar.readchar()
        yield x

class CharProcessor():
    """
    store full history in memory for now.
    """
    def __init__(self):
        self._chars = list()
        self._numbers = list()
    def start_repl(self):
        self.char_loop(char_generator_from_repl())
    def char_loop(self, char_generator):
        allowed_nonalpha_chars = {' '}
        print("ctrl-c to quit")
        for x in char_generator:
            if x == '\x03':
                print('recieved ctrl-c')
                break
            if str.isdigit(x):
                print('number={}'.format(x))
                self.put_number((len(self._chars), x))
            elif str.isalpha(x) or x in allowed_nonalpha_chars:
                x = x.lower()
                print('letter={}'.format(x))
                self.put_char(x)
            else:
                print('skipping={}'.format(x))
                continue
    def put_char(self, x):
        self._chars.append(x)
    def put_number(self, x):
        self._numbers.append(x)

cp = CharProcessor()

# def start_repl_typing_capture():
#     allowed_nonalpha_chars = {' '}
#     print("ctrl-c to quit")
#     while True:
#         x = readchar.readchar()
#         if x == '\x03':
#             print('recieved ctrl-c')
#             break
#         if str.isdigit(x):
#             print('number={}'.format(x))
#         elif str.isalpha(x) or x in allowed_nonalpha_chars:
#             x = x.lower()
#             print('letter={}'.format(x))
#         else:
#             print('skipping={}'.format(x))
