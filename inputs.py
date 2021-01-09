def to_iterable(x):
	return x.keys()

class Point:
	def __init__(self, name, lat, lng):
		self.name = name
		self.lat = lat
		self.lng = lng

dir = {
	'Casa': (4.727104, -74.075412),
	'Andes': (4.601434,-74.066141),
	'Javeriana': (4.628457, -74.064694),
	'La Sabana': (4.861376, -74.033159),
	'Externado': (4.595259, -74.068698),
	'Sergio Arboleda': (4.660935, -74.059748),
	'Nacional': (4.638076, -74.084119)
}

nodes = {i: Point(i, dir.get(i)[0], dir.get(i)[1]) for i in dir.keys()}