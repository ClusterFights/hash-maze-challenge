import os
import md5
import sys

def find_hash(filename, hash):
  hash_length = len(hash)
  filesize = os.path.getsize(filename)
  with open(filename, "r") as f:
    for i in xrange(filesize):
      f.seek(i)
      substring = f.read(hash_length)
      md5hash = md5.md5(substring).hexdigest()
      if md5hash == hash:
        return substring

      if i % 100000 == 0:
        print("reached index %d" % i)


def find_password(filename, current_hash):
  while True:
    print("searching for %s" % current_hash);
    new_hash = find_hash(filename, current_hash)

    # if we cant find the hash, we assume this is the password
    if new_hash is None: return current_hash

    current_hash = new_hash

print(find_password(sys.argv[1], sys.argv[2]))
