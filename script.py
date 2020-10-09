#!/usr/bin/env python3
# /t500/c04

import os, time

from alg_err_perc import err_perc
from alg_lv_success import lv_success

from c07_draft import get_keys_sequence

DIR_LVS = './levels/' # STATUS: DONE
ALL_LVS = os.listdir(DIR_LVS) # STATUS: DONE
ALL_LVS.sort()
MAX_LVS = len(ALL_LVS) # STATUS: DONE

CHARS_PER_WORD = 5

assert 1 <= MAX_LVS <= 50

def is_valid_lv(lv):
	# STATUS: DONE
	return type(lv) is int and 1 <= lv <= MAX_LVS

class InvalidSeq(Exception):
	pass

def _check_seq(seq, lv_file_name, line_num):
	# STATUS: DONE
	if not 1 <= len(seq) <= 70:
		raise InvalidSeq(
			'filename "%s": line %s: '
			'length must be between 1 and 70' % (
				lv_file_name, line_num + 1
			)
		)		

global_seqs = {}
def _get_seqs(lv):
	# THROWS: InvalidSeq
	# STATUS: DONE
	lv_file_name = os.path.join(DIR_LVS, ALL_LVS[lv - 1])
	with open(lv_file_name) as f:
		s = f.read()
		lines = s.splitlines()
		for i, line in enumerate(lines):
			_check_seq(line, lv_file_name, i)
		global_seqs[lv] = lines

MAX_LVS = 9 # Keep up to date
def get_seqs(lv):
	# THROWS: InvalidSeq
	# STATUS: DONE
	assert is_valid_lv(lv)
	if lv == 1:
		if lv not in global_seqs:
			_get_seqs(lv)
		return global_seqs[lv]
	seqs = []
	if lv in [2, 3]:
		left = 'asdt '
		right = 'neiop'
		if lv == 2:
			for i in range(5):
				_left = get_keys_sequence(left, 2)
				_right = get_keys_sequence(right, 2)
				letters = _left + _right
				seqs.append(''.join(letters[:70]).strip())
		elif lv == 3:
			for i in range(5):
				letters = get_keys_sequence(left + right, 2)
				seqs.append(''.join(letters[:70]).strip())
		return seqs
	elif lv in [4, 5]:
		left = ['aq', 'sw', 'df', 'tgkr', ' ']
		right = ['bnm', 'ehyj', 'i8', 'o9', 'p0']
		if lv == 4:
			for i in range(5):
				_left = get_keys_sequence(left, 2)
				_right = get_keys_sequence(right, 2)
				letters = _left + _right
				seqs.append(''.join(letters[:70]).strip())
		elif lv == 5:
			for i in range(5):
				letters = get_keys_sequence(left + right, 2)
				seqs.append(''.join(letters[:70]).strip())
		return seqs
	elif lv == 6:
		left = ['1qaz', '2wsx', '3fdc', '4rtvkg', ' ']
		right = ['bnm', 'yhje', '8iu', '9ol', '0p']
		for i in range(5):
			letters = get_keys_sequence(left + right, 2)
			seqs.append(''.join(letters[:70]).strip())
		return seqs
	elif lv == 7:
		# Alt. No repeats, no so space.
		left = ['1qaz5', '2wsx6', '3fdc7', '4rtvkg`']
		right = ['bnm,./', 'yhje;', '8iu\'[-', '9ol]=', '0p\\']
		for i in range(5):
			letters = get_keys_sequence(left + right, 2)
			seqs.append(''.join(letters[:70]).strip())
		return seqs
	elif lv == 8:
		# Alt. No repeats, no so space.
		left = ['1qaz5!QAZ%', '2wsx6@WSX^', '3fdc7#FDC&', '4rtvkg`$RTVKG~']
		right = ['bnm,./BNM<>?', 'yhje;HYJE:', '8iu\'[-*IU_{"',
				'9ol]=(OL+}', '0p\\)P|']
		for i in range(5):
			letters = get_keys_sequence(left + right, 2)
			seqs.append(''.join(letters[:70]).strip())
		return seqs
	elif lv == 9:
		left = ['1qaz5!QAZ%', '2wsx6@WSX^', '3fdc7#FDC&', '4rtvkg`$RTVKG~', ' ']
		right = ['bnm,./BNM<>?', 'yhje;HYJE:', '8iu\'[-*IU_{"',
				'9ol]=(OL+}', '0p\\)P|']
		for i in range(5):
			letters = get_keys_sequence(''.join(left + right), 2)
			seqs.append(''.join(letters[:70]).strip())
		return seqs
	assert(False)

def put_seq_and_go(seq):
	# STATUS: DONE
	assert type(seq) is str and 1 <= len(seq) <= 70
	print('$ %-70s ' % seq, end='', flush=True)
	for i in range(3):
		time.sleep(0.3)
		print('.', end='', flush=True)
	print(' Go!')

class StopApp(Exception):
	pass

class StopLevel(Exception):
	pass

def confirm_stop(msg, exc):
	# THROWS: exc
	# STATUS: DONE
	while True:
		try:
			print('')
			yn = input('Stop %s? [y/N] ' % msg)
			if yn.lower() == 'y':
				raise exc()
			elif yn.lower() == 'n' or yn == '':
				break
		except (KeyboardInterrupt, EOFError):
			pass

def confirm_stop_app():
	# THROWS: StopApp
	confirm_stop('app', StopApp)
	
def confirm_stop_level():
	# THROWS: StopLevel
	confirm_stop('level', StopLevel)
	
def run_seq(seq):
	# THROWS: StopApp
	# STATUS: DONE
	while True:
		try:
			put_seq_and_go(seq)
			t_start = time.time()
			s_in = input('> ')
			t_end = time.time()
			tt = t_end - t_start
			return s_in, tt
		except (KeyboardInterrupt, EOFError):
			confirm_stop_level()

def get_list_lens_tt_chars(list_str):
	# STATUS: DONE
	list_lens = [len(x) for x in list_str]
	tt_chars = sum(list_lens)
	return list_lens, tt_chars

def get_err_perc_weighted(list_seq, list_err_perc):
	# STATUS: DONE
	seq_lens, tt_chars = get_list_lens_tt_chars(list_seq)
	weighted_perc = 0
	for i, seq_len in enumerate(seq_lens):
		weighted_perc += seq_len / tt_chars * list_err_perc[i]
	return weighted_perc

def get_printable_stats(stats):
	# STATUS: DONE
	# returns weighthed success rate (opposite of err perc) and typing speed
	list_time, list_seq, list_in, list_err_perc = stats
	err_perc_weighted = get_err_perc_weighted(list_seq, list_err_perc)
	in_lens, tt_chars = get_list_lens_tt_chars(list_in)
	secs = sum(list_time)
	mins = secs / 60
	if mins == 0:
		wpm = 0
	else:
		wpm = tt_chars / mins / CHARS_PER_WORD
	return secs, 1 - err_perc_weighted, wpm

def print_stats(stats):
	# STATUS: DONE
	secs, perc, wpm = get_printable_stats(stats)
	print('Time:%2d:%02d:%02d -- Correct %%: %3d%% -- Words/min: %3d' % (
		secs / 3600, (secs / 60) % 60, secs % 60, perc * 100, wpm))
	return secs, perc, wpm

def run_lv(lv):
	# STATUS: DONE
	# THROWS: StopApp
	while True:
		try:
			seqs = get_seqs(lv)
			break
		except InvalidSeq as e:
			print('Error: could not load level.')
			print(e.args[0])
			try:
				input('Change the file and press Enter to continue')
			except (KeyboardInterrupt, EOFError):
				confirm_stop_app()

	lv_stats = [[], [], [], []]
	lv_time, lv_seq, lv_in, lv_err_perc = lv_stats
	lv_inc = 0
	for seq in seqs:
		try:
			seq_in, seq_time = run_seq(seq)
			lv_time.append(seq_time)
			lv_seq.append(seq)
			lv_in.append(seq_in)
		except StopLevel:
			lv_inc = None
			break

	print('Level done. Now calculating stats...')
	while True:
		try:
			lv_err_perc += err_perc(lv_seq, lv_in)
			break
		except KeyboardInterrupt:
			confirm_stop_app()
	
	print('Level stats:')
	secs, perc, wpm = print_stats(lv_stats)

	if lv_inc is not None:
		lv_inc = lv_success(perc, wpm, lv)

	return lv_inc, lv_stats

def inc_lv(lv, lv_inc):
	# STATUS: DONE
	lv += lv_inc
	lv = max(lv, 1)
	lv = min(lv, MAX_LVS)
	return lv

def app(start_lv=None):
	# STATUS: DONE
	if start_lv is None:
		lv = 1
	else:
		assert is_valid_lv(lv)
	
	tt_stats = [[], [], [], []]
	tt_time, tt_seq, tt_in, tt_err_perc = tt_stats
	try:
		while True:
			try:
				input('Next level: %s. Press Enter to continue.' % lv)
			except (KeyboardInterrupt, EOFError):
				confirm_stop_app()
			lv_inc, lv_stats = run_lv(lv)
			for i in range(len(lv_stats)):
				tt_stats[i] += lv_stats[i]
			if lv_inc is None:
				confirm_stop_app()
				continue
			lv = inc_lv(lv, lv_inc)
	except (KeyboardInterrupt, StopApp):
		pass
	
	print('Total stats:')
	print_stats(tt_stats)

if __name__ == '__main__':
	app()
