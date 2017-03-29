
import numpy as np
import random
import math
import matplotlib.pyplot as plt


# TODO: so far the only param quantity that matters is the product BETA * J, combine params into ratio's
# TODO: find criterion for equilibrium
# TODO: implement functions to measure quantities (below) as function of T (KB * T / J) and external magnetic field (B mu / J)
#		TODO: dim-less E per spin (E / JN)
#		TODO: dim-less Magnetization per spin (m / mu N)
# 		TODO: dim-less specific heat (c / K_B)
#		TODO: dim-less susceptibility per spin (chi / mu^2 N)


### PARAMETERS ###

N = 100
T = 300 # Kelvin
BETA = (1.0 / (1.38064852 * T)) * math.pow(10, 23) # find how to set this
J = 1 # e-20 # everything is normalized w.r.t. this, set to 1
H = 1

MCS = 50000 # number of Monte Carlo steps


### FUNCTIONS ###

def get_energy(ising_array):
	energy_accumulator = 0
	last_element = 0
	for current_element in ising_array:
		energy_accumulator += -J * last_element * current_element
		last_element = current_element
	return energy_accumulator

### MAIN ###

ising_array = np.zeros(N, dtype='int32')
for i in range(N):
	ising_array[i] = 2 * random.randint(0, 1) - 1 # initialize to +/- 1
	

energy_list = []
for i in range(MCS):
	flip_index = random.randint(0, N - 1)
	
	# get delta_E
	delta_E = 0
	candidate = -ising_array[flip_index]
	if flip_index > 0:
		left_element = ising_array[flip_index - 1]
		delta_E += -J * left_element * candidate
	if flip_index < N - 1:
		right_element = ising_array[flip_index + 1]
		delta_E += -J * candidate * right_element
	
	# update ising_array
	if delta_E < 0:
		ising_array[flip_index] = candidate
	elif random.random() < math.exp(-BETA * delta_E): 
		ising_array[flip_index] = candidate
	# else no change
	
	energy_list.append(get_energy(ising_array))

plt.plot(energy_list)
plt.show()
