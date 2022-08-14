def say_hello_to(name):
    print("Hello %s!" % name)



import cython
@cython.boundscheck(False)
@cython.wraparound(False)
def file_count(filename, chunk_size):
    fin = open(filename, 'rb')
    cdef int count = 0
    x = 'asdf'
    while x:
        x = fin.read1(chunk_size)
        count += 1
    return count


from libc.stdio cimport *

cdef extern from "stdio.h":
    FILE *fopen(const char *, const char *)
    int fclose(FILE *)
    ssize_t getline(char **, size_t *, FILE *)

def read_file_slow(filename):
    f = open(filename, "rb")
    while True:
        line = f.readline()
        if not line: break

        #yield line

    f.close()

    return []

def read_file(filename, chunk_size):
    filename_byte_string = filename.encode("UTF-8")
    cdef char* fname = filename_byte_string

    cdef FILE* cfile
    cfile = fopen(fname, "rb")
    if cfile == NULL:
        raise FileNotFoundError(2, "No such file or directory: '%s'" % filename)

    cdef char * line = NULL
    cdef size_t l = chunk_size
    cdef ssize_t read
    cdef int count = 0

    while True:
        read = getline(&line, &l, cfile)
        print(count, line)
        if count > 3:
            break
        count += 1
        if read == -1: break

    fclose(cfile)

    return count
