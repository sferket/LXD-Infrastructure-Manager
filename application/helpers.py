import math

def convert_size(size_bytes):
    if not isinstance( size_bytes, ( int, long ) ) :
        try:
            size_bytes = int(size_bytes)
        except ValueError:
            size_bytes = 0   
     
    if (size_bytes == 0):
        return '0B'
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes/p, 2)
    return '%s %s' % (s, size_name[i])