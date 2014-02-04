from bisect import bisect_left, bisect_right

class BPTree(object):
	def __init__(self, capacity):
		''' create an empty BPTree where each node has 
		capacity keys and capacity+1 pointers. 
		Each leaf has capacity keys. '''

		self._tree=BPTreeLeaf([],None, capacity)
		self._capacity=capacity

	def insert(self, key):
		''' insert key into our subtree '''
		pkey, ppointer = self._tree.insert(key)
		if pkey is not None:
			new_master_node = BPTreeNode([pkey], [self._tree, ppointer], self._capacity)
			self._tree = new_master_node

	def keys(self):
		''' return a list of all keys in self '''
		return self._tree.keys()
	
	def find(self, key):
		''' return whether key is in this BPTree '''
		return self._tree.find(key)

	def num_nodes(self):
		return self._tree.num_nodes()
	
	def num_leaves(self):
		return self._tree.num_leaves()
	
	def num_keys(self):
		return self._tree.num_keys()
	
	def height(self):
		return self._tree.height() + 1
	
	def stats(self):
		''' return a tuple consisting of (height, number of nodes, number of keys, number of leaves) in the tree '''
		return (self.height(), self.num_nodes(), self.num_leaves(), self.num_keys())
	
	def __str__(self):
		'''For visualization purposes'''
		s = ""
		for level in range(1, self.height() + 1):
			if level == 1:
				s += ' '*self.num_keys()*2 + str(self._tree) 
			elif level == self.height():
				leaf = self._tree._pointers[0]
				for i in range(self.height()-2):
					leaf = leaf._pointers[0]
					
				while leaf._next is not None:
				       s += str(leaf)+"->"
				       leaf = leaf._next
				s += str(leaf)
			elif level == 2:
				s += ' '*self.num_keys()
				for child in self._tree._pointers:
					s+= str(child) + " "
			elif level == 3:
				s += ' '*self.num_keys()
				for child in self._tree._pointers:
					for kid in child._pointers:
						s+= str(kid) + " "
			s += "\n"
		return s

class BPTreeNode(object):
	def __init__(self, keys, pointers, capacity):
		''' New BPTreeNode with keys=[key0,key1,..., keyK], pointers=[pointer0, pointer1,...,pointerK+1] '''

		self._keys = keys # in sorted order
		self._pointers = pointers # one more than the number of keys
		self._capacity = capacity

	def keys(self):
		''' return a list of all keys in the leaves of this subtree '''
		return self._pointers[0].keys()
	
	def find(self, key):
		''' return whether key is in this tree (at the appropriate leaf) '''
		return self._pointers[bisect_right(self._keys, key)].find(key)

	def insert_here(self, position, key, pointer): #inserting at node level
		''' insert key, at 'position' and pointer at 'position+1'
		return (None, None) if there is nothing to promote
		return (pkey, ppointer) if self splits, 
		(pkey, ppointer) this is the promoted key, and, 
		a pointer to the newly created BPTreeNode '''
		self._keys.insert(position, key)
		self._pointers.insert(position+1, pointer)
		
		cap = self._capacity
		split_index = (cap + 1)//2
		if len(self._keys) > cap:
			pkey = self._keys[split_index]
			self._keys.remove(pkey)
			
			new_lateral_node = BPTreeNode(self._keys[split_index:], self._pointers[split_index + 1:], cap)
			
			self._keys = self._keys[:split_index]
			self._pointers = self._pointers[:split_index + 1]
			
			return (pkey, new_lateral_node)
		return (None, None)

	def insert(self, key):
		''' insert key into this subtree
		return (None, None) if there is nothing to promote
		return (pkey, ppointer) if self splits '''
		
		# Insert down correct path 
		(pkey, ppointer) = self._pointers[bisect_right(self._keys, key)].insert(key)
                
		# Handle promotions
		if pkey is not None:
			position = bisect_left(self._keys, pkey)
			(promoted_key, new_lateral_node) = self.insert_here(position, pkey, ppointer) 
			return (promoted_key, new_lateral_node)
		return (None, None)

	def num_nodes(self):
		''' Number of nodes in this subtree including this one'''
		# Sum of num_nodes of each child plus 1
		return 1 + sum(map(lambda n: n.num_nodes(), self._pointers))
	
	def num_leaves(self):
		''' number of leaves in this subtree'''
		# Sum of num_leaves of each child
		return sum(map(lambda n: n.num_leaves(), self._pointers))
	
	def num_keys(self):
		''' number of keys in the leaves of this subtree'''
		# Map num_keys to each child node then sum the results
		return sum(map(lambda n: n.num_keys(), self._pointers))

	def height(self):
		''' height of this subtree'''
		return 1 + self._pointers[0].height()

	def __str__(self):
		return str(self._keys)
		
			
class BPTreeLeaf(object):
	def __init__(self, keys, next_leaf, capacity):
		self._keys = keys # in sorted order
		self._next = next_leaf # next BPTreeLeaf
		self._capacity = capacity

	def keys(self):
		''' return a list of all keys from here to the end of the linked list of BPTreeLeaf '''
		all_keys = []
		for element in self._keys:
			all_keys.append(element)
		current = self
		while current._next is not None:
			current = current._next
			all_keys.extend(current._keys)
		return all_keys

	
	def find(self, key):
		''' return whether key is in this leaf '''
		return key in self._keys

	def insert(self, key):
		''' insert key into self. A key should not appear twice in the BPTreeLeaf level
		return (None, None) if there is nothing to promote
		return (pkey, ppointer) if self splits 
		(pkey, ppointer) this is the promoted key, and, 
		a pointer to the newly created '''
		
		index = bisect_left(self._keys, key)
		if index == len(self._keys) or self._keys[index] != key:
			self._keys.insert(index, key)
		
		cap = self._capacity 
		split_index = (cap+1)//2
		
		if len(self._keys) > cap:
			new_leaf = BPTreeLeaf(self._keys[split_index:], self._next, cap)

			self._keys = self._keys[:split_index]
			self._next = new_leaf

			return (new_leaf._keys[0], new_leaf)
		return (None, None)

	def num_nodes(self):
		return 0
	
	def num_leaves(self):
		return 1
	
	def num_keys(self):
		return len(self._keys)
	
	def height(self):
		return 0

	def __str__(self):
		return str(self._keys)

Test_tree = BPTree(3)
for i in [3, 8, 15, 32, 4, 11, 21, 2, 4, 34, 6, 13, 25, 16, 30, 1, 17,\
          18, 24, 9, 22, 23, 5, 7, 19, 20, 39, 26, 31, 30]:
	Test_tree.insert(i)

