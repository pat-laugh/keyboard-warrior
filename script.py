#!/usr/bin/env python3
# /t500/c04

import os, time

DIR_LVS = './levels/'
ALL_LVS = os.listdir(DIR_LVS)
MAX_LVS = len(ALL_LVS)

assert 1 <= MAX_LVS <= 50

# configs
NEXT_LV_PERCENTAGE = 95
NEXT_LV_SPEED = 150
NEXT_LV_SPEED_INC = 6

def is_valid_lv(lv):
	# STATUS: DONE
	return type(lv) is int and 1 <= lv <= MAX_LVS

seqs = {}
def _get_seqs(lv):
	# STATUS: DONE
	lv_file_name = os.path.join(DIR_LVS, ALL_LVS[lv - 1])
	with open(lv_file_name) as f:
		s = f.read()
		seqs[lv] = s.splitlines()

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
	assert type(seq) is str and 1 <= len(seq) <= 70
	print('$ %-70s ' % seq, end='')
	for i in range(3):
		time.sleep(0.1)
		print('.', end='')
	print(' Go!')

def run_seq(seq):
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
	tt_time, tt_seq, tt_in, tt_err_perc = [], [], [], []
	for seq in seqs:
		# TODO: Handle Ctrl+D and Ctrl+C
		s_in, tt = run_seq(seq)
		tt_time.append(tt)
		tt_seq.append(seq)
		tt_in.append(s_in)
	# TODO: each perc calculated in separate threads, weighted average
	err_perc = error_percentage(seq, s_in)



def app(start_lv=None):
	if start_lv is None:
		lv = 1
	else:
		assert is_valid_lv(lv)
	
	while True:
		run_lv(lv)
	

if __name__ == '__main__':
	app()
