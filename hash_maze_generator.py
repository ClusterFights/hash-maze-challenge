import md5
import random
import subprocess
import sys
import os

hashchars = [ c for c in '0123456789abcdef' ]

def randHash():
    global hashchars
    return random.choice(hashchars)

def writeHashishFile(filename, size):
	with open(filename, 'w') as f:
            for i in xrange(0,size):
                f.write(randHash())

def genPassword(hash_length):
	return "".join([ randHash() for i in range(hash_length) ])

def getHashChain(password, size, chain_length,  hash_length, hash_fn):
	chain_hashes = [password]
	for i in range(chain_length-1):
            chain_hashes.append(hash_fn(chain_hashes[-1]).hexdigest())

	chain_positions = []
	for i in range(chain_length):
            collides = True
            while collides:
                start = random.randint(0, size - hash_length)
                collides = False
                for pos in chain_positions:
                    if start >= pos and start <= pos + hash_length:
                        collides = True
                        break
            chain_positions.append(start)

	return zip(chain_hashes, chain_positions)

def insertHashChain(filename, chain):
	with open(filename, 'r+') as f:
            for chash, pos in chain:
                f.seek(pos)
                f.seek(f.tell())
                f.write(chash)

def writeWinFile(filename, password):
	messages = [
		"Cowabunga",
		"Liquid Gold",
		"2 genders of the apocolypse",
		"Cluster Fights Winner",
		"Quizzical Lamprey"
	]
	mesg = random.choice(messages)
	with open(filename, "w") as f:
		f.write(mesg + "\n")
	resp = subprocess.check_output(["zip", "-e", "-P" + password, filename + ".zip", filename])
	print(resp)
	os.remove(filename)

if len(sys.argv) < 4:
	print """
Usage: python hash_maze_generator.py <maze_filename> <win_filename> <chain_length> <file_size_bytes>

ex: python hash_maze_generator.py maze.txt winner.txt 10 $[10*1024*1024]
- 10 megabyte maze files
"""
	exit(1)

filename = sys.argv[1]
winfile = sys.argv[2]
chain_length = int(sys.argv[3])
size = int(sys.argv[4])
hash_length = 32

writeHashishFile(filename, size)
password = genPassword(hash_length)
chain = getHashChain(password, size, chain_length, hash_length, md5.md5)
writeWinFile(winfile, password)
insertHashChain(filename, chain)

print("first hash: " + chain[-1][0])

