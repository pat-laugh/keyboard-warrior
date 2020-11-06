import threading

from lv_display import MAX_SEQ

MAX_LVS = 7 # Keep up to date

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
		return [s] * 4
	seqs = []
	if lv in [2, 3]:
		left = ''.join(rlh)
		right = ''.join(rrh)
		if lv == 2:
			for i in range(4):
				_left = get_keys_sequence(left, 2)
				_right = get_keys_sequence(right, 2)
				letters = _left + _right
				seqs.append(''.join(letters[:MAX_SEQ]).strip())
		elif lv == 3:
			for i in range(4):
				letters = get_keys_sequence(left + right, 2)
				seqs.append(''.join(letters[:MAX_SEQ]).strip())
		return seqs
	elif lv == 4:
		left = [rlh[i] + rlu[i] for i in rlf]
		right = [rrh[i] + rru[i] for i in rrf]
		for i in range(4):
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
	for i in range(4):
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

LV_LOCKS = [threading.Lock() for _ in range(MAX_LVS)]
LV_EVENTS_CONSUME = [threading.Event() for _ in range(MAX_LVS)]
LV_EVENTS_GENERATE = [threading.Event() for _ in range(MAX_LVS)]
LV_SEQS = [None] * MAX_LVS
EV_END_APP = threading.Event()

def _gen_lv_thread(lv):
	lv_idx = lv - 1
	ev_consume = LV_EVENTS_CONSUME[lv_idx]
	ev_generate = LV_EVENTS_GENERATE[lv_idx]
	while ev_generate.wait():
		if EV_END_APP.is_set():
			break
		try:
			LV_SEQS[lv_idx] = _get_seqs(lv)
		except Exception:
			continue
		LV_LOCKS[lv_idx].acquire()
		ev_generate.clear()
		ev_consume.set()
		LV_LOCKS[lv_idx].release()
		if EV_END_APP.is_set():
			break

def get_seqs(lv):
	ev_consume = LV_EVENTS_CONSUME[lv - 1]
	ev_consume.wait()
	item = LV_SEQS[lv - 1]
	ev_consume.clear()

	lower = max(1, lv - 1)
	higher = min(MAX_LVS, lv + 1)
	lvs = set([lower, lv, higher])
	for lv in lvs:
		LV_LOCKS[lv - 1].acquire()
		if not LV_EVENTS_CONSUME[lv - 1].is_set():
			LV_EVENTS_GENERATE[lv - 1].set()
		LV_LOCKS[lv - 1].release()
	return item

def end_app():
	EV_END_APP.set()
	for x in LV_EVENTS_CONSUME + LV_EVENTS_GENERATE:
		x.set()

for lv in range(1, MAX_LVS + 1):
	t = threading.Thread(target=_gen_lv_thread, args=[lv])
	t.start()

# prepare lv 1
LV_EVENTS_GENERATE[0].set()