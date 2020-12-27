# /t500/c04

import difflib

def err_perc(seq, in_str):
	# THROWS: KeyboardInterrupt
	# STATUS: DONE
	# alg = alg_basic

	# T(204)
	alg = alg_complex

	if type(seq) is str:
		assert(type(in_str) is str)
		return alg(seq, in_str)
	assert type(seq) is list and type(in_str) is list and len(seq) == len(in_str)
	return [alg(seq[i], in_str[i]) for i in range(len(seq))]

def _chars_dict(all_chars, str):
	# count the number of each char of all_chars in str
	# STATUS: DONE
	dict = {}
	for c in all_chars:
		dict[c] = 0
	for c in str:
		dict[c] += 1
	return dict

def alg_basic(seq, in_str):
	# see /t500/c03/basic
	# STATUS: DONE
	assert type(seq) is str and type(in_str) is str
	assert len(seq) > 0 and len(in_str) > 0
	all_chars = set(seq).union(set(in_str))
	chars_seq = _chars_dict(all_chars, seq)
	chars_in = _chars_dict(all_chars, in_str)
	tt_diff = 0
	for c in all_chars:
		tt_diff += abs(chars_seq[c] - chars_in[c])
	return min(1, tt_diff / len(seq))

def alg_complex(seq, in_str):
	# T(204)
	sm = difflib.SequenceMatcher(None, in_str, seq)
	return min(1, abs(1 - sm.ratio()))
