from __future__ import print_function
import random,math,time,numpy,scipy
import cPickle as pickle

class NeuralNet:
	def __init__(self, inputs, size, output, depth, max_depth=-1, file=None):
		#"""
		#Hyper parameters
		#""" 
		self._input_layer_size = inputs
		self._hidden_layers = len(size)
		self._hidden_layers_size = size
		self._output_layer_size = output
		self._depth = depth
		if max_depth == -1:
			self._max_depth = depth
		else:
			self._max_depth = max_depth
			
		self.N = []
		self.W = []
		
		self.history_count = 0
		self.history_a = []
		self.history_z = []
		
		#"""
		#If this is not a bottom tier fractal net generate a neural net framework
		#to create that variable sequence in the neural sequence
		#"""
		if self._depth > 1:
			n_w = []
			for hls in range(self._input_layer_size):
				n = NeuralNet(inputs, size, size[0], depth-1, self._max_depth, None)
				n_w.append(n)
				if self._max_depth == depth:
					p_out = 'Initializing Random Brain: '+str(int((((hls+1)*1.0)/self._input_layer_size)*100))+'%'
					print (p_out, end='\r')
			self.N.append(n_w)
			if self._depth == self._max_depth:
				print('')
			for hl in range(self._hidden_layers):
				n_w = []
				for hls in range(self._hidden_layers_size[hl]):
					if self._depth == self._max_depth:
						p_out = 'Computing Neural Flow Pathway Generation: '
						p_out += str(hl+1)+' / '+str(self._hidden_layers)+' - '
						p_out += str(int((hls+1)*1.0/self._hidden_layers_size[hl]*100))+'%'
						print (p_out, end='\r')
					thl = (hl+1)%(len(size))
					if thl == 0:
						thl_v = output
					else:
						thl_v = size[thl]
					n = NeuralNet(inputs, size, thl_v, depth-1, self._max_depth, None)
					n_w.append(n)
				self.N.append(n_w)
				if self._depth == self._max_depth:
					print('')
			n_w = []
			for hls in range(self._output_layer_size):
				if self._max_depth == depth:
					p_out = 'Finalizing Computational Overload: '
					p_out += str(int((hls+1)*1.0/self._output_layer_size*100))+'%'
					print (p_out, end='\r')
				n = NeuralNet(inputs, size, output, depth-1, self._max_depth, None)
				n_w.append(n)
			self.N.append(n_w)
			if self._max_depth == depth:
				print('')
		
		#"""
		#If the net is a bottom tier net then create the variable matrices that are required
		#"""
		else:
			for w in range(self._hidden_layers+1):
				if w == 0:
					y = numpy.random.rand(self._input_layer_size,
										self._hidden_layers_size[0])*2-20
				elif w == self._hidden_layers:
					y = numpy.random.rand(self._hidden_layers_size[w-1],
										self._output_layer_size)*2-20
				else:
					y = numpy.random.rand(self._hidden_layers_size[w-1],
										self._hidden_layers_size[w])*2-2
				self.W.append(y)
		
		if file != None:
			try:
				print('Load sequence initialized...')
				self.filename = file
				self.load_manager()
				print('Load Complete')
			except IOError:
				print('AI File not found. Using default random values')
	#"""
	#This is if the variables are ever desired to be seen. Word of warning, the spam is real
	#There are 50 variables in the input control matrix, each array of 5 is generated by a sub net,
	#which has another 50 variables in that input control matrix, 
	#"""		
	def print_out(self):
		for N in self.N:
			for n in N:
				n.print_out()
		print(self.W)
	
	#"""
	#The pass down forward function is the main excecute function for the neural network
	#It loops through the subnets (if available) and generates its own weighted net. It then passes
	#A generated weighted net to the forward function
	#"""
	def pass_down_forward(self, X):
		for hl in range(len(self.N)-1):
			z_w = []
			p_m = 1.0
			for hls in self.N[hl]:
				if self._depth == self._max_depth:
					p_out = 'Neural Processing Step: '
					p_out += str(hl+1)+' / '+str(len(self.N)-1)+' - '
					p_out += str(int(p_m/len(self.N[hl])*100))+'%'
					print(p_out, end='\r')
					p_m+=1
				z = hls.pass_down_forward(X)
				z_w.append(z[0])
			self.W.append(z_w)
			if self._depth == self._max_depth:
				print('')
		return self.forward(X)
	
	#"""
	#Loop through the weighted network and do matrix multiplication through
	#"""
	def forward(self, X):
		self.z = []
		self.a = []
		t = 0
		for w in range(len(self.W)):
			t+=1
			if w == 0:
				z = numpy.dot(X, self.W[0])
			else:
				if len(self.a[w-1][0]) == 4:
					print(len(self.a))
					print(len(self.W))
					print(t)
				z = numpy.dot(self.a[w-1], self.W[w])  
			self.z.append(z)
			self.a.append(self.sigmoid(z)) 
		return self.a[len(self.a)-1]
	
	#"""
	#Sigmoid resets the variable to a value between -1 and 1
	#"""
	def sigmoid(self, z):
		return 1/(1+numpy.exp(-z))
		
	#"""
	#Sigmoid prime for reverse algorithmic learning
	#"""
	def sigmoid_prime(self, z):
		return numpy.exp(-z)/((1+numpy.exp(-z))**2)
		
	#"""
	#The cost function prime
	#This is the control function for the main pass_down_forward loop
	#"""
	def cost_function(self, X, y):
		self.yHat = self.pass_down_forward(X)
		J = 0.5*sum((y-self.yHat)**2)
		return J
		
	def cost_function_prime(self, X, y, top=True):
		if top==True:
			self.yHat = self.pass_down_forward(X)
		
		delta = [] #numpy.multiply(-(y-self.yHat), self.sigmoid_prime(self.z[]))
		dJdW = [] #numpy.dot(self.a[].T, delta[len(delta)-1])
		"""
		Start by working in reverse from the top most layer. Take yHat and do the first delta protocol.
		Get the dJdW for that particular set, make alterations and pass those down the chain. 
		"""
		if self.depth > 1:
			z_count = len(self.z)-1
			for z in range(z_count):
				dT = numpy.multiply(-(y-self.a[z_count-z]), self.sigmoid_prime(self.z[z_count-z]))
				delta.append(dT)
				dJdW.append(numpy.dot(self.a[z_count-z], dT))
				for n in self.N:
					n.cost_function_prime(X, y, False)
		
		z_count = len(self.W)-1
		new_weights = []
		for w in range(self.W):
			n_w = self.W[w]+dJdW[z_count-w]
			new_weights.append(n_w)
		self.W = new_weights
		
	def save_manager(self):
		file = open(self.filename, 'wb')
		self.save(file)
		
	def save(self, file):
		pickle.dump(self.W, file)
		for network in self.N:
			for n in network:
				n.save(file)
			
	def load_manager(self):
		file = open(self.filename, 'rb')
		self.load(file)
		
	def load(self, file):
		self.W = pickle.load(file)
		for network in self.N:
			for n in network:
				n.load(file)
				
	def clear_history(self):
		self.history_a = self.a
		self.history_z = self.z
		self.history_count += 1
		if self._depth > 1:
			self.W = []