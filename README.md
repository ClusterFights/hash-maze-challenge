# hash-maze-challengeA new ClusterFight challenge!

Challenge
---------

You are given an encrypted zip file. That zip file contains another
encrypted zip file, which contains another zip file, and it\'s encrypted
zip files all the way down.

The passwords for these zip files are all MD5 sum hexdigest strings.

You are provided with an large text file and a starter MD5 hash. Search
the text file for a 32-character substring that MD5 hashes to the
starter hash, use it to decrypt the zip file. The substring will be an
MD5 sum string itself. Reverse that hash using the text file as well.
Repeat this until you reach the last zip file containing a text file.
When you get it, shout out the value of the zip file.

For a 5-hash long challenge, the passwords would be:

`starter_hash   == md5(md5(md5(md5(md5(final_password)))))`\
`zip 1 password == md5(md5(md5(md5(final_password))))`\
`zip 2 password == md5(md5(md5(final_password)))`\
`zip 3 password == md5(md5(final_password))`\
`zip 4 password == md5(final_password)`\
`zip 5 password == final_password`

!!! NOTE !!! \-- sample code currently does not have nested zip files,
that needs to be fixed.

### In short {#in_short}

1.  Be given starter MD5 sum string
2.  Search text file for substring where md5(substring) == md5hash
3.  Unzip current zip file
4.  Repeat from 2

A trivial-solution is provided in python. You may use it during the
competition, IF YOU WANT TO LOSE. It\'s horribly unoptimized!

### Generating a Sample Dataset {#generating_a_sample_dataset}

make a maze with 10 hash links that is 1,000,000 bytes large.

` pi@node0:~/pi_challenge $ python hash_maze_generator.py maze.txt winner.txt 10 $[1024*1024]`\
` updating: winner.txt (stored 0%)`\
` `\
` first hash: 47c386878ad4c69b403a70d7001a5daa`

### Testing With the Trivial Solution {#testing_with_the_trivial_solution}

Run the solver script:

` pi@node0:~/pi_challenge $ time python 01_trivial_solver.py maze.txt 47c386878ad4c69b403a70d7001a5daa`\
` searching for 47c386878ad4c69b403a70d7001a5daa`\
` reached index 0...`\
` reached index 600000`\
` searching for f9a0ea9e2c06cadb12a8ded01e378234`\
` reached index 0...`\
` reached index 200000`\
` searching for 86bb5c8d68a3b4b04aa2ffe3116dd076`\
` reached index 0...`\
` reached index 600000`\
` searching for d8800caaa74076365914ad9cdf1de205`\
` reached index 0...`\
` reached index 600000`\
` searching for 38f25a41bfb6fe091e37e76995dadd1e`\
` reached index 0...`\
` reached index 800000`\
` searching for fceced6d39980661e36fa9c959a810d2`\
` reached index 0...`\
` reached index 200000`\
` searching for 6c4ee9a8d4f8842ccb325ac45a0701eb`\
` reached index 0...`\
` reached index 400000`\
` searching for 65a2e3e0aae321883cae714558fa71ff`\
` reached index 0...`\
` reached index 800000`\
` searching for 774a52fdd8735520f244516522112e79`\
` reached index 0...`\
` reached index 700000`\
` searching for b25248d7144badadbcda318434948353`\
` reached index 0...`\
` reached index 1000000`\
` b25248d7144badadbcda318434948353`\
` `\
` real    1m32.294s`\
` user    1m28.231s`\
` sys     0m4.041s`

Use unzip to unzip it:

` pi@node0:~/pi_challenge $ unzip -e -Pb25248d7144badadbcda318434948353 winner.txt.zip`\
` Archive:  winner.txt.zip`\
`  extracting: winner.txt              `\
` pi@node0:~/pi_challenge $ cat winner.txt`\
` Liquid Gold`

Trivial Solution (python) {#trivial_solution_python}
-------------------------

The trivial solution presented here pulls 32 bytes from the text file,
checks if they MD5sum to the given hash, and if it does not, moves the
file pointer back 31 bytes and repeats. This algorithm is wrapped in an
infinite loop that exits when we can\'t reverse a hash.

`import os`\
`import md5`\
`import sys`\
` `\
`def find_hash(filename, hash):`\
`  hash_length = len(hash)`\
`  filesize = os.path.getsize(filename)`\
`  with open(filename, "r") as f:`\
`    for i in xrange(filesize):`\
`      f.seek(i)`\
`      substring = f.read(hash_length)`\
`      md5hash = md5.md5(substring).hexdigest()`\
`      if md5hash == hash:`\
`        return substring`\
`       `\
`      if i % 100000 == 0:`\
`        print("reached index %d" % i)`\
`   `\
`def find_password(filename, current_hash):`\
`  while True:`\
`    print("searching for %s" % current_hash);`\
`    new_hash = find_hash(filename, current_hash)`\
`     `\
`    # if we cant find the hash, we assume this is the password`\
`    if new_hash is None: return current_hash`\
`     `\
`    current_hash = new_hash`\
` `\
`print(find_password(sys.argv[1], sys.argv[2]))`

Files
-----

[01\_trivial\_solution.py](https://gist.github.com/tetsuharu/082ad4c000fd484e251a3fba574aeedd/raw/6d6d4a8191d451b282710607857e013a8e4d65be/01_trivial_solution.py)
[hash\_maze\_generator.py](https://gist.github.com/tetsuharu/082ad4c000fd484e251a3fba574aeedd/raw/6d6d4a8191d451b282710607857e013a8e4d65be/hash_maze_generator.py)
