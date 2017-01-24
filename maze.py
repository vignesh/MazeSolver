import json
import requests
import string
from urlparse import parse_qs, urlparse
from random import uniform


class Maze:

	def __init__(self):
		self.end = False  #bool to check if end is reached
		#self.first = True
		self.path = "" # keep track of path 
		#self.d = dict.fromkeys(string.ascii_lowercase, 0) #dictionary for all lowercase characters as keys and setting value to 0
		self.d = {} #declare empty dictionary 
		self.x = str(0) #start at x coordiante at 0
		self.y = str(0) #start at y coordiante at 0
		self.prevx = str(-1) #start at previous x coordiante at -1
		self.prevy = str(-1) #start at previous y coordiante at -1
		self.url = raw_input("Enter path for https://challenge.flipboard.com\n")
		self.parsed = urlparse(self.url) #parsed url 
		if self.parsed.path == '/step':
			self.step()
		elif self.parsed.path == '/check':
			self.check()
		elif self.parsed.path == '/start':
			self.random()
			self.start()
		else:
			print '404 Error - Invalid Request'

	def random(self):
		try:
			self.s = str(round(uniform(0, 10),2)) #generate random number between 0 and 10 with two decimal spots
			response = requests.get(url="https://challenge.flipboard.com/step?s="+self.s+"&x=0&y=0")
			data = json.loads(response.text)
		except (requests.exceptions.RequestException, ValueError, Exception) as e:
			self.random() #if there is an error reaching page generate new random number and  try again

	
	""""
	Psuedo Code for backtracking solution

	search({0, 0}, {})

	prev_coordinate
	vector<Coordinate> curr_path

	search(coordinate_to_check) {
	if coordinate_to_check == end:
	vector<Coordinate> is your final path

	if dead_end:
	curr_path += prev_coordinate
	return;

	for coordinate in adjacent_coordinate:
	if coordinate is not checked:
	curr_path += coordinate
	prev_coordinate = coordinate_to_check
	search(coordinate)

	# This should never run
	}"""

	"""
	Started putting together backtracking solution but ran out of time.

	prevletter = ""
	prevx = ""
	prevy = ""
	finalPath = ""
	def search(x,y):
		response = requests.get(url="https://challenge.flipboard.com/step?s=123456.5"+"&x="+self.x+"&y="+self.y)
		data = json.loads(response.text)

		if data['end'] == True:
			print finalPath
			return 

		if DEAD END:


		for adjacent in data['adjacent']:
			if (str(adjacent['x']),str(adjacent['y'])) not in self.d:
				x = str(adjacent['x'])
				y = str(adjacent['y'])
				finalPath += prevletter
				prevletter = data['letter']
		self.search(x,y)
	"""

	def start(self): #naive solution does not take account to backtracking...
		#response = requests.get(url="https://challenge.flipboard.com/step?s=1.49"+"&x="+self.x+"&y="+self.y)
		response = requests.get(url="https://challenge.flipboard.com/step?s=123456.5"+"&x="+self.x+"&y="+self.y)
		data = json.loads(response.text)
		if (self.x,self.y) not in self.d:
			self.path += data['letter']
			print data['letter']
			self.d[(self.x,self.y)] = self.depth
			print self.d

		if data['end'] == True:
			print self.path
			return self.path
		else:
			self.depth+=1
			for adjacent in data['adjacent']:
				if (str(adjacent['x']),str(adjacent['y'])) not in self.d:
					self.prevx = self.x
					self.prevy = self.y
					self.x = str(adjacent['x'])
					self.y = str(adjacent['y'])
					self.start()
	
	def step(self): #displays json on /step 
		try:
			resp = requests.get(url="https://challenge.flipboard.com"+self.url)
			data = json.loads(resp.text)
		except (requests.exceptions.RequestException, ValueError, Exception) as e:
			print e #prints error

	#/check?s=123456.5&guess=pqkefzvymrbtfqntnqkrdipik - True Example
	#/check?s=123456.5&guess=pqk - False Example
	def check(self):
		trueOutput = json.JSONEncoder().encode({'success': True}) #true output in json
		falseOutput = json.JSONEncoder().encode({'success': False}) #false ouput in json

		#iterate though guess and look up letters, if it is not matching in adjacent then it is false 
		query = parse_qs(urlparse(self.url).query, keep_blank_values=True) #parse url 
		self.s = query['s'][0] #maze id set to s
		self.guess = query['guess'][0] #maze path set to guess
		if (self.s or self.guess) == None: #check if both paramenters are present
			print json.loads(falseOutput)
			return json.loads(falseOutput)

		response = requests.get(url="https://challenge.flipboard.com/step?s="+self.s+"&x="+self.x+"&y="+self.y) #starts at (0,0)
		data = json.loads(response.text)
		if data['letter'] != self.guess[0]: #check first letter in path
			print json.loads(falseOutput)
			return json.loads(falseOutput)
		else:
			self.guess = self.guess[1:] #iterate +1 for guess
			length = len(data['adjacent']) #determine the initial adjacent points to (0,0)

		for letter in self.guess: #iterate through all letters
			counter = 0 #set counter to keep track of vertices attemtped
			if counter >= length: #if vertices attempted are
				print json.loads(falseOutput)
				return json.loads(falseOutput)
			#print "https://challenge.flipboard.com/step?s="+self.s+"&x="+self.x+"&y="+self.y+" --------current step"
			response = requests.get(url="https://challenge.flipboard.com/step?s="+self.s+"&x="+self.x+"&y="+self.y) #request current step
			data = json.loads(response.text) #load current step
			length = len(data['adjacent']) #determine how many adjacent points are present
			i = 0 #iterator to go through adjacent vertices
			for adjacent in data['adjacent']:
				#print "https://challenge.flipboard.com/step?s="+self.s+"&x="+str(data["adjacent"][i]['x'])+"&y="+str(data["adjacent"][i]['y'])+" --------adjacent step"
				response2 = requests.get(url="https://challenge.flipboard.com/step?s="+self.s+"&x="+str(data["adjacent"][i]['x'])+"&y="+str(data["adjacent"][i]['y'])) #request adjacent step
				data2 = json.loads(response2.text) #load adjacent step
				if data2['letter'] == letter:
					self.x = str(data["adjacent"][i]['x']) #set new point x value if letter is found
					self.y = str(data["adjacent"][i]['y']) #set new point y value if letter is found
					break #if we find matching letter then break to move onto next letter
				else:
					i+=1 #iterate to move next adjacent vertices
					counter+=1 #increment if not letter not in adjacent vertices

		if data2['end'] == True: #check if last point has end value of true
			print json.loads(trueOutput)
			return json.loads(trueOutput)
		else:
			print json.loads(falseOutput)
			return json.loads(falseOutput)

if __name__ == "__main__":
	instance = Maze()
