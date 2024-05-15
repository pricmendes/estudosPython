class Fila:
	def __init__(self):
		# Inicializa uma lista vazia para representar a fila
		self.fila = []
	def enqueue(self, item):
		# Adiciona um item ao final da fila
		self.fila.append(item)
		print(f"{item} foi adicionado à fila.")

	def dequeue(self):
		# Remove e retorna o item do ínicio da fila

		if not self.fila_vazia():
			item = self.fila.pop(0)
			print(f"{item} foi removido da fila.")
			return item

		else:
			print("A fila está vazia. Nenhum item para remover.")
			return None

	def fila_vazia(self):
		# Verifica se a fila está vazia
		return len(self.fila) == 0

	def tamanho(self):
		# Retorna o tamanho da fila
		return len(self.fila)

	def mostrar_fila(self):
		# Exibe todos os elementos da fila
		print("Fila atual: ", self.fila)


# Demonstração de uso da fila
fila = Fila()
fila.enqueue(1)
fila.enqueue(2)
fila.enqueue(3)
fila.mostrar_fila()

fila.dequeue()
fila.mostrar_fila()

fila.dequeue()
fila.dequeue()
fila.dequeue() # Tentativa de remover de uma fila vazia