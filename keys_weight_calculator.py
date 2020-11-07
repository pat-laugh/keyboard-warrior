import sys

from lv_gen import rl, rla, rls, rlas, rr, rra, rrs, rras

USAGE = '''\
script files

Put line-separate absolute file names in "files", possibly using something like:
    find . -name '*.py' -exec echo `pwd`/{} \; >files
'''
if len(sys.argv) != 2:
	sys.exit(USAGE)

weights = {}
for ll in [rl, rla, rls, rlas, rr, rra, rrs, rras]:
	for l in ll:
		for s in l:
			for c in s:
				weights[c] = 0

files_name = sys.argv[1]
with open(files_name) as files:
	f_names = files.read().splitlines()
for f_name in f_names:
	with open(f_name) as f:
		s = f.read()
	for c in s:
		try:
			weights[c] += 1
		except KeyError:
			weights[c] = 1

print(weights)
