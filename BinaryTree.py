'''
This is a class for binary tree used in payoff lattice
'''

class BinaryTree:
    def __init__(self, root, q_u):
        self.data = {}
        self.q_u = q_u
        self.data[0] = {0: root}
        print("     Initialized. \nNotice:left child is for up case\n© J.Hu, 2025\n")
    
    # Bulk create a complete tree that contains level levels
    def bulk_create(self, level):
        if len(self.data) > 1:
            print("Warning, tree rewritten, here is the original tree")
            print(self)
        D = {}
        for le in range(level):
            d = {}
            for i in range(2 ** level):
                d[i] = None
            D[le] = d
        self.data = D
    
    def get_node(self, level, index):
        if level in self.data and index in self.data[level]:
            return self.data[level][index]
        print("Error: level, index does not exist in the tree!")
        return None
    
    def update_node(self, level, index, data):
        if level not in self.data or index not in self.data[level]:
            print("Error: level, index does not exist in the tree!")
            return
        self.data[level][index] = data
    
    # This function adds 1 or 2 children (left and right) 
    #   to the node level-th level with index in that level
    def add_child(self, level, index, left, right):
        if level not in self.data:
            print(f"Error: level {level} does not exist!")
        if index not in self.data[level]:
            print(f"Error: index {index} does not exist at level {level}!")
        levelNew = level + 1
        indexLeft = 2 * index
        indexRight = 2 * index + 1
        ## For left
        if left:
            if levelNew in self.data:
                if indexLeft in self.data[levelNew]:
                    print(f"Warning, left may be overwritten, here is the original data {self.data[levelNew][indexLeft]}.")
                self.data[levelNew][indexLeft] = left
            else:
                self.data[levelNew] = {indexLeft: left}
        ## For right
        if right:
            if levelNew in self.data:
                if indexRight in self.data[levelNew]:
                    print(f"Warning, right may be overwritten, here is the original data {self.data[levelNew][indexRight]}.")
                self.data[levelNew][indexRight] = right
            else:
                self.data[levelNew] = {indexRight: right}
    
    def sanity_check(self):
        if self.q_u > 1 or self.q_u < 0:
            print(f"Sanity check failed, q_u is not between 0 and 1.")
            return False
        total_level = len(self.data)
        for i in range(total_level):
            d = self.data[i]
            if len(d) != 2 ** i:
                print(f"Sanity check failed, due to inconsistence at level {i}.")
                return False 
        return True
    
    def is_leaf(self, level, index):
        if level + 1 not in self.data:
            return True
        if 2 * index not in self.data[level + 1] and 2 * index + 1 not in self.data[level + 1]:
            return True
        return False
    
    # Root has level 0 index 0
    def pv(self, level, index, r):
        if self.is_leaf(level, index):
            return self.data[level][index]
        left = (level + 1, 2 * index)
        right = (level + 1, 2 * index + 1)
        import numpy as np
        return self.pv(left[0], left[1], r) * self.q_u * np.e**(-r) + self.pv(right[0], right[1], r) * (1 - self.q_u) * np.e**(-r)
    
    def __str__(self):
        Returned_string = f"# of levels: {len(self.data)}"
        for level in range(len(self.data)):
            Returned_string += "\n"
            Returned_string += str(level)
            Returned_string += ":"
            for index in range(2 ** level):
                if index not in self.data[level]:
                    Returned_string += " n/a"
                Returned_string += f" {self.data[level][index]:.2f}"
        return Returned_string
    
    def copy_to(self, dest):
        dest.data = self.data
        dest.q_u = self.q_u
