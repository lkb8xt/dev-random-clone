# Since /dev/random is the closest thing to "true" randomness on a computer, and basically all other PRNGS use it, I thought I would have some fun
# and use a live stream of recent wiki changes to emulate entropy and use as the input to a hash chain (similar to what dev/urandom does with /dev/random/'s
# entropy pool).
#  
# I use the current epoc time, concatenated with a random num from /dev/urandom, as my initial seed, and then use each subsequent
# hash as the new seed. 