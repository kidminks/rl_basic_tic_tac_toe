import copy
import pickle
import random

class States:
	table = {}
	alpha = 0.2

	def __init__(self):
		return
	def check_win(self, key):
		for i in range(3):
			if key[i*3]==key[i*3+1] and key[i*3+1]==key[i*3+2] and key[i*3]!='.':
				return True
			if key[i]==key[i+3] and key[i+3]==key[i+6] and key[i]!='.':
				return True
		if key[0]==key[4] and key[4]==key[8] and key[0]!='.':
			return True
		if key[2]==key[4] and key[4]==key[6] and key[2]!='.':
			return True
		return False
	
	def get_prob(self, current, chance):
		if self.check_win(current):
			if(chance==0):
				return 1
			else:
				return 0
		return 0.5
	
	def store_table(self):
		with open("table.txt", "wb") as table:
			pickle.dump(self.table, table)

	def retrive_table(self):
		with open("table.txt", "rb") as table:
			self.table = pickle.load(table)
    
	def create_states(self, current, val, chance):
		result = self.get_prob(current,chance)
		self.table["".join(current)] = result
		print current
		if result==0.5:
			temp = copy.deepcopy( current )
			for i,v in enumerate(current):
				if(v=='.'):
					temp[i] = val 
					if chance==0:
						t_val = 'X'
						t_chance = 1
					else:
						t_val = 'O'
						t_chance = 0
					print temp
					self.create_states(temp, t_val, t_chance)
				temp = copy.deepcopy( current )
	
	def get_win_prob(self, s):
		return self.table[s]
	
	def next_move_predictor(self, s):
		next_states = {}
		temp = copy.deepcopy( s )
		for i,v in enumerate(s):
			if(v=='.'):
				temp[i] = 'X'
				next_states["".join(temp)] = self.get_win_prob("".join(temp))
			temp = copy.deepcopy(s)
		new_key = ""
		new_value = -1
		for key,value in next_states.iteritems():
			if value>new_value:
				new_value = value
				new_key = key
		if( random.randint(1,11)<4 and new_value != 1):
			for key,value in next_states.iteritems():
				if random.randint(1,3)%2==0:
					print "random picking"
					new_value = value
					new_key = key
					break
		self.table["".join(s)] = self.table["".join(s)] + \
						self.alpha*(self.table[new_key]-self.table["".join(s)])
		for idx,v in enumerate(new_key):
			s[idx] = v
		return s
	
	def lost(self, game_board, idx):
		new_key = "".join(game_board)
		game_board[idx] = '.'
		old_key = "".join(game_board)
		self.table["".join(old_key)] = self.table["".join(old_key)] + \
						self.alpha*(self.table[new_key]-self.table["".join(old_key)])
	
	def draw_game(self, game_board):
		for v in game_board:
			if(v=='.'):
				return False
		return True

states = States()
current = ['.','.','.','.','X','.','.','.','.']
# states.create_states(current, 'X', 1)
# states.store_table()
states.retrive_table()
# print states.table["".join(['X','.','.','.','.','.','.','.','.'])]
# print states.table["".join(['.','X','.','.','.','.','.','.','.'])]
# print states.table["".join(['.','.','X','.','.','.','.','.','.'])]
# print states.table["".join(['.','.','.','X','.','.','.','.','.'])]
# print states.table["".join(['.','.','.','.','X','.','.','.','.'])]
# print states.table["".join(['.','.','.','.','.','X','.','.','.'])]
# print states.table["".join(['.','.','.','.','.','.','X','.','.'])]
# print states.table["".join(['.','.','.','.','.','.','.','X','.'])]
# print states.table["".join(['.','.','.','.','.','.','.','.','X'])]
for key,val in states.table.iteritems():
	if val<0.5 and val!=0.0:
		print key,val
print ""
for key,val in states.table.iteritems():
	if val>0.5 and val!=1.0:
		print key,val

while(True):	
	game_board = copy.deepcopy(current)
	print game_board
	t = 1
	while(True):
		if t!=1:
			game_board = states.next_move_predictor(game_board)
			print game_board
			if( states.check_win(game_board) ):
				print "Comp Won"
				break
			if( states.draw_game(game_board) ):
				print "Draw"
				break
		t = 10
		idx = input()
		game_board[idx] = 'O'
		if( states.check_win(game_board) ):
			print game_board
			states.lost(game_board, idx)
			print "You Won"
			break
	states.store_table()