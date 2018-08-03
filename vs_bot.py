import copy
import pickle
import random

class States:
	table = {}
	alpha = 0.5
	player1 = 0
	player2 = 0
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
		if( random.randint(1,11)<5 and new_value != 1):
			for key,value in next_states.iteritems():
				if random.randint(1,100)<=50==0:
					new_value = value
					new_key = key
					break
		self.table["".join(s)] = self.table["".join(s)] + \
						self.alpha*(self.table[new_key]-self.table["".join(s)])
		for idx,v in enumerate(new_key):
			s[idx] = v
		return s

	def next_move_predictor_player2(self,s):
		next_states = {}
		temp = copy.deepcopy( s )
		for i,v in enumerate(s):
			if(v=='.'):
				temp[i] = 'O'
				next_states["".join(temp)] = self.get_win_prob("".join(temp))
			temp = copy.deepcopy(s)
		new_key = ""
		new_value = 2
		for key,value in next_states.iteritems():
			if value<new_value:
				new_value = value
				new_key = key
		if( random.randint(1,11)<5 and new_value != 0):
			for key,value in next_states.iteritems():
				if random.randint(1,100)<=50:
					new_value = value
					new_key = key
					break
		for idx,v in enumerate(new_key):
			s[idx] = v
		return s
			
	def lost(self, game_board1, game_board2):
		new_key = "".join(game_board2)
		old_key = "".join(game_board1)
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

while(True):
	for x in xrange(1,10000):	
		game_board = copy.deepcopy(current)
		i = 1
		game_board1 = copy.deepcopy(game_board)
		# game_board1[random.randint(1,9)-1] = 'X'
		while(True):
			if i!= 1:
				game_board1 = states.next_move_predictor(game_board)
				if( states.check_win(game_board1) ):
					# states.player1 += 1
					break
				if( states.draw_game(game_board1) ):
					states.lost(game_board, game_board1)
					# states.player2 += 1
					break
			i = 2
			game_board2 = states.next_move_predictor_player2(game_board1)
			if( states.check_win(game_board2) ):
				states.lost(game_board1, game_board2)
				# states.player2 += 1
				break
			game_board = game_board2
	# print "Player1 {}".format( states.player1 )
	# print "player2 {}".format( states.player2 )
	states.store_table()
	print "saved"