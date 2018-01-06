from subprocess import Popen, PIPE
import re


def disk_space(warning_size = 2000000000):
    ps = Popen("dir", shell=True, stdout=PIPE, stderr=PIPE)
    outline = (line.split() for line in ps.stdout)

    free_bytes = warning_size

    for line in outline:
        if len(line)>4 and line[3] == b"bytes" and line[4] == b"free":
            free_bytes = int(line[2].replace(b",",b""))

    if free_bytes<warning_size:
        print("Warning only",free_bytes,"bytes left")


disk_space(20000000000)