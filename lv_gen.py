import math, string, threading

from lv_display import MAX_SEQ
from c07_draft import get_keys_sequence, get_keys_random, Timeout

MAX_LVS = 7 # Keep up to date
NUM_SEQS = 4
# T(231)
MODES = ['random', 'text', 'doc', 'code']
MODE_RANDOM, MODE_TEXT, MODE_DOC, MODE_CODE = MODES
MODE = MODE_CODE

ROW_HOME = [['a', 's', 'd', 't',   ' '], ['n', 'e', 'i', 'o', 'p']]
ROW_UP = [['q', 'w', 'f', 'rkg', ''], ['bm', 'yhj', '8', '9', '0-=']]
ROW_BOT = [['z', 'x', 'c', 'v',   ''], ['', '', 'u', 'l', '']]
ROW_HOME_ALT = [['',  '',  '',  '',    ''], ['.', ';', '[', ']', '\\']]
ROW_UP_ALT = [['1', '2', '3', '45',  ''], [',/', '67',  '',  '', '']]
ROW_BOT_ALT = [['',  '',  '',  '`',   ''], ['',   '',    '\'', '',  '']]
ROW_HOME_SHIFT = [['A', 'S', 'D', 'T',   ''], ['N',  'E',   'I',  'O', 'P']]
ROW_UP_SHIFT = [['Q', 'W', 'F', 'RKG', ''], ['BM', 'YHJ', '*',  '(', ')_+']]
ROW_BOT_SHIFT = [['Z', 'X', 'C', 'V',   ''], ['',   '',    'U',  'L', '']]
ROW_HOME_ALT_SHIFT = [['',  '',  '',  '',    ''], ['>',  ':',   '{',  '}', '|']]
ROW_UP_ALT_SHIFT = [['!', '@', '#', '$%',  ''], ['<?', '^&',  '',  '', '']]
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

# T(231)
weight_code = {'X': 199, '}': 406, ')': 14422, 'c': 17037, 'J': 88, '└': 7,
'O': 1683, 'Z': 55, 'n': 33012, '%': 2351, '\\': 1001, '7': 186, '?': 152,
'W': 505, 'u': 14618, 'v': 4339, 'ç': 1, 'H': 513, '>': 670, '!': 475,
',': 10698, '–': 2, 'a': 31700, 'à': 3, 'F': 1586, '^': 46, ';': 242,
'=': 11629, 'f': 16572, '/': 1523, 'é': 27, 'R': 1793, '`': 71, '8': 226,
'K': 669, 'r': 35335, '$': 52, '~': 48, '(': 14415, '<': 584, 'B': 733,
'_': 26635, 'y': 7564, '{': 410, 'p': 18129, '5': 466, 'P': 1666, '9': 264,
'G': 828, '\n': 27582, '0': 2511, '|': 120, ']': 3562, 'E': 3715, '-': 2407,
'4': 516, 'A': 2321, 'l': 25363, '.': 12930, 'e': 64153, 'i': 34802, 'C': 1584,
'I': 1904, 'w': 3845, 'b': 6194, '§': 1, ':': 9332, '3': 614, 'x': 4276,
'"': 1032, 'S': 2445, 's': 39246, '[': 3592, 'L': 1506, "'": 15304, ' ': 64766,
't': 45558, '&': 21, 'd': 19795, 'Y': 358, '│': 5, '@': 188, 'N': 2674,
'\t': 41552, 'T': 3292, 'V': 768, 'm': 15269, 'M': 1282, 'Q': 120, 'g': 8303,
'—': 1, '6': 329, '─': 24, '2': 1005, 'h': 7921, '+': 1179, '*': 442, 'U': 805,
'1': 2149, 'D': 1469, 'j': 1897, '├': 5, 'k': 4729, 'o': 29686, '#': 1361,
'q': 1588, 'z': 274}
for key, val in weight_code.items():
	if key in string.ascii_letters or key == '_':
		weight_code[key] = val / 2
code_total = sum(weight_code.values())
for key, val in weight_code.items():
	weight_code[key] = val / code_total

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
		left = [x[i] for x in rl for i in rlf]
		right = [x[i] for x in rr for i in rrf]
		div = 9
		mul = 100
	elif lv == 6:
		# All keys. Alts. Repeats.
		left = [x[i] for x in rl + rla for i in rlf]
		right = [x[i] for x in rr + rra for i in rrf]
		div = 15
		mul = 1000
	elif lv == 7:
		# All keys. Alts. Shifts. Repeats.
		left = [x[i] for x in rl + rla + rls + rlas for i in rlf]
		right = [x[i] for x in rr + rra + rrs + rras for i in rrf]
		div = 15
		mul = 10000
	else:
		assert(False)
	if MODE is MODE_CODE:
		all_letters = []
		for c in set(''.join(left + right)): # get rid of empty string
			all_letters += [c] * math.ceil(weight_code[c] * mul)
	for _ in range(NUM_SEQS):
		if MODE is MODE_CODE:
			letters = get_keys_random(all_letters)
		elif MODE is MODE_RANDOM:
			letters = get_keys_sequence(''.join(left + right), 2)
			# T(112)
			x = ord(letters[0]) % div + 1
			while x < len(letters) - 1:
				letters[x], x = ' ', x + ord(letters[x]) % div + 1
		# T(112)
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
