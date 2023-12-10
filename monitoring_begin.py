import signal
import sys
import os
from lib.capture import begin_capture, stop_capture

def signal_handler(sig, frame):
    print("Stopping packet sniffer...")
    stop_capture()

def main():
    if len(sys.argv) != 3:
        print("Usage: sudo python3 capture.py <sniffed_log_file> <proc_log_file>")
        sys.exit(1)
    sniff_log = sys.argv[1]
    proc_log = sys.argv[2]
    init(sniff_log, proc_log)

sniff_file = None
proc_file = None

def init(sniff_log, proc_log):
    global sniff_file, proc_file
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    sniff_file = open(sniff_log, 'w')
    proc_file = open(proc_log, 'w')
    print("Starting packet sniffer...")
    print("Process ID is {}".format(os.getpid()))
    if begin_capture(logSniff, logProc):
        sniff_file.close()
        proc_file.close()

def logSniff(text):
    sniff_file.write(str(text))

def logProc(text):
    proc_file.write(str(text))

if __name__ == '__main__':
    main()