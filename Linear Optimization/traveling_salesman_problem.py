from __future__ import print_function
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import request as r 
from geopy.distance import distance as d
from inputs import nodes, to_iterable
from functools import partial
import pandas as pd


#Define model_data Class
class Model_data:
	def __init__(self, vehicules, depot):
		self.distance_matrix = None
		self.vehicules = vehicules
		self.depot = depot

	def define_distance_matrix(self,nodes):		
		self.distance_matrix = list(map(partial(get_distance_matrix,node=nodes), to_iterable(nodes)))

#Create the distance matrix using Geopy
def get_distance_matrix(x,node):	
	values = list(map(partial(get_distance,X=x),to_iterable(node)))
	return values

def get_distance(y,X):
	location1 = nodes.get(X).lat,nodes.get(X).lng
	location2 = nodes.get(y).lat,nodes.get(y).lng
	return d(location1,location2).km

def distance_callback(from_index, to_index):
    from_node = manager.IndexToNode(from_index)
    to_node = manager.IndexToNode(to_index)
    return model.distance_matrix[from_node][to_node]

def print_solution(manager, routing, solution):
	print('Objective: {} kilometers'.format(solution.ObjectiveValue()))
	index = routing.Start(0)
	plan_output = 'Route for vehicle 0:\n'
	route_distance = 0
	locations = [l for l in to_iterable(nodes)]
	while not routing.IsEnd(index):
		plan_output += ' {} ->'.format(locations[index])
		previous_index = index
		index = solution.Value(routing.NextVar(index))
		route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
	#plan_output += ' {}\n'.format(manager.IndexToNode(index))
	plan_output += ' {}\n'.format(locations[0])
	print(plan_output)
	plan_output += 'Route distance: {} kilometers\n'.format(route_distance)



if __name__ == '__main__':
	vehicules = int(input('ingrese el número de vehiculos'))
	depot = int(input('Ingrese el nodo de inicio y retorno'))
	model = Model_data(vehicules=vehicules, depot=depot)
	model.define_distance_matrix(nodes)
	#Definir variables para el ruteo
	manager = pywrapcp.RoutingIndexManager(len(model.distance_matrix), model.vehicules, model.depot)
	#Crear el objeto de rounting
	routing = pywrapcp.RoutingModel(manager)
	#Definir la función para calcular las distancias
	transit_callback_index = routing.RegisterTransitCallback(distance_callback)  
	#Costo o distancia de cada arco
	routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
	# Configurar la heuristica
	search_parameters = pywrapcp.DefaultRoutingSearchParameters()    
	#search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.SWEEP)
	# Solucion
	solution = routing.SolveWithParameters(search_parameters)
	# Mostrar en pantalla la solución
	if solution:
		print_solution(manager, routing, solution)


	