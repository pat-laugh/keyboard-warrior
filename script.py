#!/usr/bin/env python3
# /t500/c04

import os, time

DIR_LVS = './levels/' # STATUS: DONE
ALL_LVS = os.listdir(DIR_LVS) # STATUS: DONE
MAX_LVS = len(ALL_LVS) # STATUS: DONE

assert 1 <= MAX_LVS <= 50

# configs
NEXT_LV_PERCENTAGE = 95
NEXT_LV_SPEED = 150
NEXT_LV_SPEED_INC = 6

def is_valid_lv(lv):
	# STATUS: DONE
	return type(lv) is int and 1 <= lv <= MAX_LVS

class InvalidSeq(Exception):
	pass

def _check_seq(seq, lv, line_num):
	if not 1 <= len(seq) <= 70:
		raise InvalidSeq(
			'level %s: line %s: '
			'length must be between 1 amd 70' % (
				lv, line_num + 1
			)
		)		

seqs = {}
def _get_seqs(lv):
	# THROWS: InvalidSeq
	# STATUS: TODO
	lv_file_name = os.path.join(DIR_LVS, ALL_LVS[lv - 1])
	with open(lv_file_name) as f:
		s = f.read()
		lines = s.splitlines()
		for i, line in enumerate(lines):
			_check_seq(line, lv, i)
		seqs[lv] = lines

def get_seqs(lv):
	# STATUS: DONE
	assert is_valid_lv(lv)
	if lv not in seqs:
		_get_seqs(lv)
	return seqs[lv]

def error_percentage():
	pass

def alg_lv_success_simple(err_perc, typing_speed, lv):
	req_perc, req_speed = 95, (150 + lv * 6)
	if err_perc >= req_perc and typing_speed >= req_speed:
		return 1
	
	req_perc, req_speed = 90, (150 + lv * 3)
	if err_perc >= req_perc and typing_speed >= req_speed:
		return 0
	
	return -1

def lv_success(err_perc, typing_speed, lv):
	return alg_lv_success_simple(err_perc, typing_speed, lv)

def put_seq_and_go(seq):
	# STATUS: DONE
	assert type(seq) is str and 1 <= len(seq) <= 70
	print('$ %-70s ' % seq, end='')
	for i in range(3):
		time.sleep(0.1)
		print('.', end='')
	print(' Go!')

def run_seq(seq):
	# THROWS: EOFError
	# STATUS: DONE
	put_seq_and_go(seq)
	t_start = time.time()
	s_in = input('> ')
	t_end = time.time()
	tt = t_end - t_start
	return s_in, tt

def run_lv(lv):
	# STATUS: TODO
	print(f'Running level {lv}')
	seqs = get_seqs(lv)
	lv_time, lv_seq, lv_in, lv_err_perc = [], [], [], []
	for seq in seqs:
		# TODO: Handle Ctrl+D and Ctrl+C
		try:
			seq_in, seq_time = run_seq(seq)
			lv_time.append(seq_time)
			lv_seq.append(seq)
			lv_in.append(seq_in)
		except (KeyboardInterrupt, EOFError):
	# TODO: each perc calculated in separate threads, weighted average
	err_perc = error_percentage(seq, seq_in)



def app(start_lv=None):
	# STATUS: TODO
	if start_lv is None:
		lv = 1
	else:
		assert is_valid_lv(lv)
	
	tt_time, tt_seq, tt_in, tt_err_perc = [], [], [], []
	tt_stats = [tt_time, tt_seq, tt_in, tt_err_per]
	while True:
			lv_stats = run_lv(lv)
			for i in range(len(lv_stats)):
				tt_stats[i] += lv_stats[i]

if __name__ == '__main__':
	app()
