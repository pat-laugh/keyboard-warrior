import threading

from lv_display import MAX_SEQ
from c07_draft import get_keys_sequence, Timeout

MAX_LVS = 7 # Keep up to date
NUM_SEQS = 4

ROW_HOME = [['a', 's', 'd', 't',   ' '], ['n', 'e', 'i', 'o', 'p']]
ROW_UP = [['q', 'w', 'f', 'rkg', ''], ['bm', 'yhj', '8', '9', '0']]
ROW_BOT = [['z', 'x', 'c', 'v',   ''], ['', '', 'u', 'l', '']]
ROW_HOME_ALT = [['',  '',  '',  '',    ''], ['.', ';', '[', ']', '\\']]
ROW_UP_ALT = [['1', '2', '3', '45',  ''], [',/', '67',  '-',  '=', '']]
ROW_BOT_ALT = [['',  '',  '',  '`',   ''], ['',   '',    '\'', '',  '']]
ROW_HOME_SHIFT = [['A', 'S', 'D', 'T',   ''], ['N',  'E',   'I',  'O', 'P']]
ROW_UP_SHIFT = [['Q', 'W', 'F', 'RKG', ''], ['BM', 'YHJ', '*',  '(', ')']]
ROW_BOT_SHIFT = [['Z', 'X', 'C', 'V',   ''], ['',   '',    'U',  'L', '']]
ROW_HOME_ALT_SHIFT = [['',  '',  '',  '',    ''], ['>',  ':',   '{',  '}', '|']]
ROW_UP_ALT_SHIFT = [['!', '@', '#', '$%',  ''], ['<?', '^&',  '_',  '+', '']]
ROW_BOT_ALT_SHIFT = [['',  '',  '',  '~',   ''], ['',   '',    '"',  '',  '']]

rlf, rrf = [4, 3, 2, 1, 0], [0, 1, 2, 3, 4]
rlh, rlu, rlb = [x[0] for x in [ROW_HOME, ROW_UP, ROW_BOT]]
rrh, rru, rrb = [x[1] for x in [ROW_HOME, ROW_UP, ROW_BOT]]
rl = [rlh, rlu, rlb]
rr = [rrh, rru, rrb]
rla = [x[0] for x in [ROW_HOME_ALT, ROW_UP_ALT, ROW_BOT_ALT]]
rra = [x[1] for x in [ROW_HOME_ALT, ROW_UP_ALT, ROW_BOT_ALT]]
rls = [x[0] for x in [ROW_HOME_SHIFT, ROW_UP_SHIFT, ROW_BOT_SHIFT]]
rrs = [x[1] for x in [ROW_HOME_SHIFT, ROW_UP_SHIFT, ROW_BOT_SHIFT]]
rlas = [x[0] for x in [ROW_HOME_ALT_SHIFT, ROW_UP_ALT_SHIFT, ROW_BOT_ALT_SHIFT]]
rras = [x[1] for x in [ROW_HOME_ALT_SHIFT, ROW_UP_ALT_SHIFT, ROW_BOT_ALT_SHIFT]]

def is_valid_lv(lv):
	# STATUS: DONE
	return type(lv) is int and 1 <= lv <= MAX_LVS

def gen_lv_1():
	s = []
	for i in range(2):
		if i == 0:
			r = rlh
			f4, f3, f2, f1, f0 = rlf
		else:
			r = rrh
			f4, f3, f2, f1, f0 = rrf
		s += [
			r[f0], r[f1], r[f0], r[f2],
			r[f1], r[f2], r[f1], r[f3],
			r[f2], r[f3], r[f2], r[f4],
			r[f3], r[f4],
			r[f0], r[f3],
			r[f1], r[f4],
			r[f0], r[f4],
		]
	return ''.join(s)

def _get_seqs(lv):
	# STATUS: DONE
	assert is_valid_lv(lv)
	if lv == 1:
		s = gen_lv_1()
		return [s] * NUM_SEQS
	seqs = []
	if lv in [2, 3]:
		left = ''.join(rlh)
		right = ''.join(rrh)
		if lv == 2:
			for _ in range(NUM_SEQS):
				_left = get_keys_sequence(left, 2)
				_right = get_keys_sequence(right, 2)
				letters = _left + _right
				seqs.append(''.join(letters[:MAX_SEQ]).strip())
		elif lv == 3:
			for _ in range(NUM_SEQS):
				letters = get_keys_sequence(left + right, 2)
				seqs.append(''.join(letters[:MAX_SEQ]).strip())
		return seqs
	elif lv == 4:
		left = [rlh[i] + rlu[i] for i in rlf]
		right = [rrh[i] + rru[i] for i in rrf]
		for _ in range(NUM_SEQS):
			letters = get_keys_sequence(left + right, 2)
			seqs.append(''.join(letters[:MAX_SEQ]).strip())
		return seqs
	elif lv == 5:
		# All keys. Repeats.
		left = [''.join([x[i] for x in rl]) for i in rlf]
		right = [''.join([x[i] for x in rr]) for i in rrf]
	elif lv == 6:
		# All keys. Alts. Repeats.
		left = [''.join([x[i] for x in rl + rla]) for i in rlf]
		right = [''.join([x[i] for x in rr + rra]) for i in rrf]
	elif lv == 7:
		# All keys. Alts. Shifts. Repeats.
		left = [''.join([x[i] for x in rl + rla + rls + rlas]) for i in rlf]
		right = [''.join([x[i] for x in rr + rra + rrs + rras]) for i in rrf]
	else:
		assert(False)
	for _ in range(NUM_SEQS):
		letters = get_keys_sequence(''.join(left + right), 2)
		# T(112)
		div = 9 if lv <= 5 else 15
		x = ord(letters[0]) % div + 1
		while x < len(letters) - 1:
			letters[x], x = ' ', x + ord(letters[x]) % div + 1
		x = 0
		while x < len(letters) - 1:
			if letters[x] == letters[x+1] == ' ':
				del letters[x]
			else:
				x += 1
		seqs.append(''.join(letters[:MAX_SEQ]).strip())
	return seqs

LV_LOCKS, LV_EV_CON, LV_EV_GEN, LV_THREADS, LV_SEQS = [], [], [], [], []
EV_END_APP = threading.Event()

def _gen_lv_thread(lv):
	lv_idx = lv - 1
	ev_con, ev_gen = LV_EV_CON[lv_idx], LV_EV_GEN[lv_idx]
	while ev_gen.wait():
		if EV_END_APP.is_set():
			break
		try:
			LV_SEQS[lv_idx] = _get_seqs(lv)
		except Timeout:
			continue
		LV_LOCKS[lv_idx].acquire()
		ev_gen.clear()
		ev_con.set()
		LV_LOCKS[lv_idx].release()
		if EV_END_APP.is_set():
			break

def _check_gen_lv_items(lv):
	lv_idx = lv - 1
	LV_EV_CON.append(threading.Event())
	ev_gen = threading.Event()
	LV_EV_GEN.append(ev_gen)
	LV_LOCKS.append(threading.Lock())
	LV_SEQS.append(None)
	t = threading.Thread(target=_gen_lv_thread, args=[lv])
	LV_THREADS.append(t)
	ev_gen.set()
	t.start()

def get_seqs(lv):
	ev_con = LV_EV_CON[lv - 1]
	ev_con.wait()
	item = LV_SEQS[lv - 1]
	ev_con.clear()

	lower = max(1, lv - 1)
	higher = min(MAX_LVS, lv + 1)
	lvs = set([lower, lv, higher])
	for lv in lvs:
		if len(LV_THREADS) < lv:
			_check_gen_lv_items(lv)
			continue
		LV_LOCKS[lv - 1].acquire()
		if not LV_EV_CON[lv - 1].is_set():
			LV_EV_GEN[lv - 1].set()
		LV_LOCKS[lv - 1].release()
	return item

def _kill_threads():
	threading.main_thread().join()
	EV_END_APP.set()
	for x in LV_EV_CON + LV_EV_GEN:
		x.set()

threading.Thread(target=_kill_threads, daemon=True).start()

# prepare lv 1
_check_gen_lv_items(1)
