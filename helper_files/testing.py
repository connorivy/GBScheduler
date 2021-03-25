class ParametersDefinedByUser:
	def __init__(self, **kwargs):
		self.val2 = kwargs.get('val2',"default value")
	