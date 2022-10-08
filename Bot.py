import random

circ_st = []
cros_st = []

checked = []

for i in range(15):
	checked.append([])
	for j in range(15):
		checked[i].append(False)

def clear_hash():
	for i in range(len(checked)):
		for j in range(len(checked[i])):
			checked[i][j] = False

def find_circ_line():
	global circ_st
	best = []
	weight = -1
	for i in range(len(circ_st)):
		if circ_st[i][3] > weight:
			best = circ_st[i]
			weight = circ_st[i][3]

	return best


def find_cros_line():
	global cros_st
	best = []
	weight = -1
	for i in range(len(cros_st)):
		if cros_st[i][3] > weight:
			best = cros_st[i]
			weight = cros_st[i][3]

	return best

def attac(table , cros):
	if cros[0] == 73:
		for i in range(5):
			if table[cros[1]+i][cros[2]+i] == 0:
				return [cros[1]+i , cros[2]+i]

	elif cros[0] == 15:
		for i in range(5):
			if table[cros[1]+i][cros[2]-i] == 0:
				return [cros[1]+i , cros[2]-i]

	elif cros[0] == 62:
		for i in range(5):
			if table[cros[1]][cros[2]+i] == 0:
				return [cros[1] , cros[2]+i]

	elif cros[0] == 84:
		for i in range(5):
			if table[cros[1]+i][cros[2]] == 0:
				return [cros[1]+i , cros[2]]
	else:
		return None


def deffence(table , circ):
	print("ОБОРОНА СУКААААА!!!")


def find_rand_circ(table):
	circs = []
	for x in range(len(table)):
		for y in range(len(table[x])):
			if table[x][y] == 1:
				circs.append([x,y])

	suc = False
	while not suc:
		place = random.choice(circs)

		for i in ((-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0)):
			if table[place[0]+i[0]][place[1]+i[1]] == 0:
				return [place[0]+i[0] , place[1]+i[1]]


def get_cords(table):
	#линии ноликов ушли в стек
	get_line(table , 1) 
	#линии крестиков ушли в стек
	get_line(table , 2)
	#чистим хэш после всех найденных линий
	clear_hash()

	#находим линии с наибольшими весами
	circ = find_circ_line()
	cros = find_cros_line()

	if cros != [] and circ != []:
		if circ[3] > cros[3]:
			#ломаем линию соперника
			return deffence(table , circ)
		else:
			#строим свою
			return attac(table , cros)
	else:
		#если нет достойных линий для хода, то ходим рядом со случаенным ноликом
		return find_rand_circ(table)


class Bot:
    next_move = get_cords


# 1 |  2  | 3
#---+-----+---
# 8 |self | 4
#---+-----+---
# 7 |  6  | 5

#определение линии: [направленность , Xнач , Yнач , вес]
#например: [73 , 1 , 1 , 7000] - открытая четверка по диагонали снизу вверх

def get_weight(StartF , EndF , Smet):
	#открытые линии
	if StartF and EndF:
		if Smet == 2:
			return 4
		elif Smet == 3:
			return 6
		elif Smet == 4:
			return 100
	#полуоткрытые линии 
	elif StartF and not EndF or not StartF and EndF:
		if Smet == 2:
			return 2
		elif Smet == 3:
			return 3
		elif Smet == 4:
			return 99
	#закрытые линии
	elif not StartF and not EndF:
		if Smet == 2:
			return 2
		elif Smet == 3:
			return 3
		elif Smet == 4:
			return 99		


#двигаем буфер из 5 клеток по возможной линии
def start_search(table , obj , x , y):

	line_st = []

	contObj = 0
	if obj == 1:
		contObj = 2
	elif obj == 2:
		contObj = 1

	Smet = 0
	#открытость краев
	StartF , EndF = True , True


	#x+i стартовая точка под 7-3
	for i in range(-4,1):
		#проверка на то, что буффер будет внутри поля
		if x+i < 0 or x+i+4 >= len(table[0]) or y+i < 0 or y+i+4 >= len(table[0]):
			continue

		#проверка на открытость линии
		if x+i-1 < 0 or y+i-1 < 0 or table[x+i-1][y+i-1] == contObj:
			StartF = False
		if x+i+5 >= len(table[0]) or y+i+5 >= len(table[0]) or table[x+i+5][y+i+5] == contObj:
			EndF = False

		#проход по буферу
		for j in range(5):

			if table[x+i+j][y+i+j] == obj:
				Smet += 1
			elif table[x+i+j][y+i+j] == contObj:
				Smet = 0
				break

		#если оказалось что линия прегодна, заносим ее в стек с учетом веса
		if Smet >= 2:
			line_st.append([73 , x+i , y+i , get_weight(StartF , EndF , Smet)])

		StartF , EndF = True , True
		Smet = 0


	#x-i стартовая точка под 1-5
	for i in range(4,-1,-1):
		#проверка на то, что буффер будет внутри поля
		if x-i < 0 or x-i+4 >=len(table[0]) or y+i >= len(table[0]) or y+i-4 < 0:
			continue

		#проверка на открытость линии
		if x-i-1 < 0 or y+i+1 >= len(table[0]) or table[x-i-1][y+i+1] == contObj:
			StartF = False
		if x-i+5 >= len(table[0]) or y+i-5 < 0 or table[x-i+5][y+i-5]:
			EndF = False

		#проход по буфферу
		for j in range(5):

			if table[x-i+j][y+i-j] == obj:
				Smet += 1
			elif table[x-i+j][y+i-j] == contObj:
				Smet = 0
				break
		#если оказалось что линия прегодна, то занисим в стек
		if Smet >= 2:
			line_st.append([15 , x-i , y+i , get_weight(StartF , EndF , Smet)])

		StartF , EndF = True , True
		Smet = 0


	#y-i стартовая точка под 6-2
	for i in range(4,-1,-1):
		#проверка на то, что буффер внутри поля
		if y-i < 0 or y-i+4 >= len(table[0]):
			continue

		#проверка на открытость линии
		if y-i-1 < 0 or table[x][y-i-1] == contObj:
			StartF = False
		if y-i+5 >= len(table[0]) or table[x][y-i+5] == contObj:
			EndF = False

		#проход по буфферу
		for j in range(5):

			if table[x][y-i+j] == obj:
				Smet += 1
			elif table[x][y-i+j] == contObj:
				Smet = 0
				break

		#если оказалось прегодна, то добавляем ее в стек
		if Smet >= 2:
			line_st.append([62 , x , y-i , get_weight(StartF , EndF , Smet)])

		StartF , EndF = True , True
		Smet = 0


	#x-i стартовая точка под 8-4
	for i in range(4,-1,-1):
		#проверка на то, что буффер внутри поля
		if x-i < 0 or x-i+4 >= len(table[0]):
			continue

		#проверка на открытость линии
		if x-i-1 < 0 or table[x-i-1][y] == contObj:
			StartF = False
		if x-i+5 >= len(table[0]) or table[x-i+5][y] == contObj:
			EndF = False

		#проход по буфферу
		for j in range(5):

			if table[x-i+j][y] == obj:
				Smet += 1
			elif table[x-i+j][y] == contObj:
				Smet = 0
				break

		#если линия оказалась пригодна, то добавляем
		if Smet >= 2:
			line_st.append([84 , x-i , y , get_weight(StartF , EndF , Smet)])

		StartF , EndF = True , True
		Smet = 0

	return line_st


def get_line(table , obj):
	global circ_st , checked

	if obj == 1:
		#проходка по клеткам с ноликами кроме уже проверенных
		for x in range(len(table)):
			for y in range(len(table[x])):
				if table[x][y] == obj and not checked[x][y]:
					#поиск по соседям клетки
					circ_st = start_search(table , obj , x , y)
					checked[x][y] = True

	elif obj == 2:
		#проходка по клеткам с крестиками кроме проверенных 
		#(хэш таблица одна и та же тк крестики и нолики не могут находиться в одной клетке)
		for x in range(len(table)):
			for y in range(len(table[i])):
				if table[x][y] == obj and not checked[x][y]:
					#поиск по соседям клетки
					cros_st = start_search(table , obj , x , y)
					checked[x][y] = True
