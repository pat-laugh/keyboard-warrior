# /t500/c04

def err_perc(seq, in):
	# STATUS: DONE
	return alg_basic(seq, in)

def _chars_dict(all_chars, str):
	# count the number of each char of all_chars in str
	# STATUS: DONE
	dict = {}
	for c in all_chars:
		dict[c] = 0
	for c in str:
		dict[c] += 1
	return dict

def _alg_basic(seq, in):
	# see /t500/c03/basic
	# STATUS: DONE
	assert type(seq) is str and type(in) is str
	assert len(seq) > 0 and len(in) > 0
	all_chars = set(seq).union(set(in))
	chars_seq = _chars_dict(all_chars, seq)
	chars_in = _chars_dict(all_chars, in)
	tt_diff = 0
	for c in all_chars:
		tt_diff += abs(chars_seq[c] - chars_in[c])
	return min(1, tt_diff / len(seq))

def alg_basic(seq, in):
	# STATUS: DONE
	if type(seq) is str:
		return _alg_basic(seq, in)
	assert type(seq) is list and type(in) is list and len(seq) == len(in)
	err_perc_list = []
	for i in range(len(seq)):
		err_perc_list.append(_alg_basic(seq[i], in[i]))
	return err_perc_list

def alg_complex(seq, in):
	assert False, 'not implemented yet'
