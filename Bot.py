
circ_st = []
cros_st = []

def get_cords(table):

	#линии ноликов ушли в стек
	get_line(table , 1) 
	#линии крестиков ушли в стек
	get_line(table , 2)


class Bot:
    next_move = get_cords


def get_line()