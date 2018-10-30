#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time
import hashlib
import sseclient

WIKI_STREAM_URL = 'https://stream.wikimedia.org/v2/stream/recentchange'

# Since /dev/random is the closest thing to "true" randomness on a computer, and basically all other PRNGS use it, I thought I would have some fun
# and use a live stream of recent wiki changes to emulate entropy and use as the input to a hash chain (similar to what dev/urandom does with /dev/random/'s
# entropy pool).
#  
# I use the current epoc time, concatenated with a random num from /dev/urandom, as my initial seed, and then use each subsequent
# hash as the new seed. 

def generate_hash(seed, entropy):
    input = seed + entropy.encode('utf-8')
    return hashlib.sha256(input).digest()

def generate_initial_seed():
    #current global time
    curr_time = str(time.time())

    #get a random number from /dev/urandom
    rand = os.urandom(10)
    return curr_time + rand

def generate_entropy():
    seed = generate_initial_seed()
    for event in sseclient.SSEClient(WIKI_STREAM_URL):
            if event.event == 'message':
                entropy = event.data
                hash = generate_hash(seed, entropy) 
                write_raw_bytes(hash)
                seed = str(hash)


# prints raw binary to std out, to emulate $ cat /dev/random/. 
def write_raw_bytes(hx):
    os.write(1, hx)

def main():
    try:
        generate_entropy()
    except KeyboardInterrupt:
        sys.exit()

if __name__ == '__main__':
    main()