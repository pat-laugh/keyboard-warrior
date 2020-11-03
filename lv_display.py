import time

MAX_SEQ = 70 # based on terminal size

def put_seq_and_go(seq):
	# STATUS: DONE
	assert type(seq) is str and 1 <= len(seq) <= MAX_SEQ
	print(('$ %-'+str(MAX_SEQ)+'s ') % seq, end='', flush=True)
	for i in range(3):
		time.sleep(0.3)
		print('.', end='', flush=True)
	print(' Go!')
