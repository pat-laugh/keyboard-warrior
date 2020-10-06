# /t500/c04

# configs
NEXT_LV_PERC = 0.99
NEXT_LV_WPM = 30
NEXT_LV_WPM_INC = 1

SAME_LV_PERC = 0.95
SAME_LV_WPM = 20
SAME_LV_WPM_INC = 1

def lv_success(weighted_correct_perc, wpm, lv):
	return alg_simple(weighted_correct_perc, wpm, lv)

def alg_simple(correct_perc, wpm, lv):
	req_perc = NEXT_LV_PERC
	req_speed = NEXT_LV_WPM + lv * NEXT_LV_WPM_INC
	if correct_perc >= req_perc and wpm >= req_speed:
		return 1
	
	req_perc = SAME_LV_PERC
	req_speed = SAME_LV_WPM + lv * SAME_LV_WPM_INC
	if correct_perc >= req_perc and wpm >= req_speed:
		return 0
	
	return -1
