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

rlf, rrf = [0, 1, 2, 3, 4], [0, 1, 2, 3, 4]
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

def get_seqs(lv):
	# STATUS: DONE
	assert is_valid_lv(lv)
	if lv == 1:
		return [
			'asadsdstdtd t ats a popioioeieinenpeonpn',
			'asadsdstdtd t ats a popioioeieinenpeonpn',
			'asadsdstdtd t ats a popioioeieinenpeonpn',
			'asadsdstdtd t ats a popioioeieinenpeonpn',
		]
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
