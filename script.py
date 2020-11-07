#!/usr/bin/env python3
# /t500/c04

import os, time

from alg_err_perc import err_perc
from alg_lv_success import lv_success

import lv_display, lv_gen

CHARS_PER_WORD = 5

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
			lv_display.put_seq_and_go(seq)
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
		seqs = lv_gen.get_seqs(lv)
		break

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
	lv = min(lv, lv_gen.MAX_LVS)
	return lv

def app(start_lv=None):
	# STATUS: DONE
	if start_lv is None:
		lv = 1
	else:
		assert lv_gen.is_valid_lv(lv)
	
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
