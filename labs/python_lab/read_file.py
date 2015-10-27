# This is an example of reading file lazy and with arbitary delimiter

def readbydelimiter(filename, chunk=1024, delimiter='\r'):
    segments = []
    with open(filename, 'r') as f:
        buf      = f.read(chunk)
        segments = buf.split(delimiter)
        while True:
            if len(segments) > 1:
                yield segments[0]
                segments.pop(0)
            else:
                buf = f.read(chunk)
                if buf:
                    s = buf.split(delimiter)
                    segments[-1] += s[0]
                    segments.extend(s[1:])
                else:
                    yield segments[0]
                    break;

