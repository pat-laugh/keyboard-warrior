from itertools import permutations
import random, threading, time

def _get_pairs(keys, i):
	pairs = []
	while i + 1 < len(keys):
		j = i + 1
		while j < len(keys):
			pairs.append([keys[i], keys[j]])
			j += 1
		i += 1
	return pairs


def _get_combs(keys, i, len_combinations):
	if len_combinations == 1:
		return keys
	if len_combinations == 2:
		return _get_pairs(keys, i)
	combs = []
	while i + (len_combinations - 1) < len(keys):
		c = keys[i]
		items = _get_combs(keys, i + 1, len_combinations - 1)
		for l in items:
			l.insert(0, c)
		combs += items
		i += 1
	return combs


def _get_permutations(keys, len_combinations):
	if type(keys) is not set:
		keys = set(keys)
	keys = list(keys)
	keys.sort()
	return _get_combs(keys, 0, len_combinations)


def _get_keys_sequence(keys, len_combinations, ret, lock):
	l = _get_permutations(keys, len_combinations)
	for x in l:
		random.shuffle(x)
	while True:
		random.shuffle(l)
		seq = l[0][:]
		i, swap_i = 1, 1
		while i < len(l):
			c = l[i]
			if seq[-1] != c[0]:
				seq += c
				i += 1
				swap_i = i
				continue
			swap_i += 1
			if swap_i == len(l):
				break
			l[i], l[swap_i] = l[swap_i], l[i]
		else:
			break
	try:
		lock.acquire()
		ret[0] = seq
	finally:
		lock.release()


def _check_thread(ret, lock):
	try:
		lock.acquire()
		return ret[0]
	finally:
		lock.release()
	

def get_keys_sequence(keys, len_combinations, timeout=None, tries=None):
	assert(0 < len_combinations <= len(keys))
	if timeout is None:
		timeout, tries = len(keys), 3
	else:
		assert(tries > 0 and timeout > 0)
	counter = 0
	while counter < tries:
		ret, lock = [None], threading.Lock()
		t = threading.Thread(target=_get_keys_sequence,
			args=(keys, len_combinations, ret, lock))
		t.daemon = True
		t1 = time.time()
		t.start()
		time.sleep(0.1)
		while time.time() - t1 < (timeout / tries):
			if _check_thread(ret, lock) is not None:
				return ret[0]
			time.sleep(0.1)
		if _check_thread(ret, lock) is not None:
			return ret[0]
		counter += 1
	raise Exception('Could not get keys: timeout')

