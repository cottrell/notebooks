import cloudpickle
def some_function(a, b=1):
    """ things """
    return a, b

if __name__ == '__main__':
    print(cloudpickle.dumps(some_function))
