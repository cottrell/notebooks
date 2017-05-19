import readchar

def start_repl_typing_capture():
    allowed_nonalpha_chars = {' '}
    print("ctrl-c to quit")
    while True:
        x = readchar.readchar()
        if x == '\x03':
            print('recieved ctrl-c')
            break
        if str.isdigit(x):
            print('number={}'.format(x))
        elif str.isalpha(x) or x in allowed_nonalpha_chars:
            x = x.lower()
            print('letter={}'.format(x))
        else:
            print('skipping={}'.format(x))
