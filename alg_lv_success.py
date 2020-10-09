# /t500/c04

# configs
NEXT_LV_PERC = 0.95
NEXT_LV_PERC_INC = 0.005
NEXT_LV_PERC_MAX = 1
NEXT_LV_WPM = 24
NEXT_LV_WPM_INC = 2
NEXT_LV_WPM_MAX = 50

SAME_LV_PERC = 0.95
SAME_LV_PERC_INC = 0
SAME_LV_PERC_MAX = 1
SAME_LV_WPM = 20
SAME_LV_WPM_INC = 1
SAME_LV_WPM_MAX = 30

def lv_success(weighted_correct_perc, wpm, lv):
	return alg_simple(weighted_correct_perc, wpm, lv)

def alg_simple(correct_perc, wpm, lv):
	req_perc = min(NEXT_LV_PERC_MAX, NEXT_LV_PERC + lv * NEXT_LV_PERC_INC)
	req_speed = min(NEXT_LV_WPM_MAX, NEXT_LV_WPM + lv * NEXT_LV_WPM_INC)
	if correct_perc >= req_perc and wpm >= req_speed:
		return 1
	
	req_perc = min(SAME_LV_PERC_MAX, SAME_LV_PERC + lv * SAME_LV_PERC_INC)
	req_speed = min(SAME_LV_WPM_MAX, SAME_LV_WPM + lv * SAME_LV_WPM_INC)
	if correct_perc >= req_perc and wpm >= req_speed:
		return 0
	
	return -1
