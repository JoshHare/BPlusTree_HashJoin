# Python3 program for implementing B+ Tree

import math, random

# Node creation
class Node:
    def __init__(self, order):
        self.order = order
        self.values = []
        self.keys = []
        self.nextKey = None
        self.parent = None
        self.check_leaf = False

    # Insert at the leaf
    def insert_at_leaf(self, leaf, value, key):
        if (self.values):
            values = self.values
            for i in range(len(values)):
                if (value == values[i]):
                    self.keys[i].append(key)
                    break
                elif (value < values[i]):
                    self.values = self.values[:i] + [value] + self.values[i:]
                    self.keys = self.keys[:i] + [[key]] + self.keys[i:]
                    break
                elif (i + 1 == len(values)):
                    self.values.append(value)
                    self.keys.append([key])
                    break
        else:
            self.values = [value]
            self.keys = [[key]]


# B plus tree
class BplusTree:
    def __init__(self, order):
        self.root = Node(order)
        self.root.check_leaf = True

    # Insert operation
    def insert(self, value, key):
        value = int(value)
        key = int(key)
        print("Inserting key:", value)
        
        leaf = self.search(value)
        print("Starting insertion at node with values:", leaf.values)
        
        leaf.insert_at_leaf(leaf, value, key)

        if len(leaf.values) == leaf.order:
           # print("Overflow detected in node with values:", old_node.values)
            
            node1 = Node(leaf.order)
            node1.check_leaf = True
            node1.parent = leaf.parent  #make new sibling
            mid = int(math.ceil(leaf.order / 2)) - 1
            node1.values = leaf.values[mid :]
            node1.keys = leaf.keys[mid:]
            node1.nextKey = leaf.nextKey
            leaf.values = leaf.values[:mid ]
            leaf.keys = leaf.keys[:mid ]
            leaf.nextKey = node1    #split into two
            
            print("Node Overflowed. Splitting node:", leaf.values,"   ", node1.values)
            
            self.insert_in_parent(leaf, node1.values[0], node1)
        else:
            print("Node after insertion: ", leaf.values)
        print()


    # Search operation for different operations
    def search(self, value):
        current = self.root
        while(current.check_leaf == False): #if node is not a leaf (it can't have our final answer)
            currValues = current.values
            for i in range(len(currValues)): #iterate through the values
                if (int(value) == int(currValues[i])): 
                    #current = current.keys[i + 1]
                    current = current.keys[len(current.keys)-1]
                    break
                elif (int(value) < int(currValues[i])):
                    current = current.keys[i]
                    break
                elif (i + 1 == len(currValues)):
                    current = current.keys[len(current.keys)-1]
                    #current = current.keys[i + 1]
                    break
        return current

    # Find the node
    def find(self, value, key):
        l = self.search(value)
        for i, item in enumerate(l.values):
            if item == value:
                if key in l.keys[i]:
                    return True
                else:
                    return False
        return False

    def range_search(self, start, end):
        result = []

        # Find the starting leaf node for range search
        start_leaf = self.search(start)

        # Traverse leaf nodes until the end of the range
        current_leaf = start_leaf
        while current_leaf:
            for i, value in enumerate(current_leaf.values):
                if start <= value <= end:
                    # Add keys within the range
                    result.extend(current_leaf.keys[i])
                elif value > end:
                    # No need to continue if value exceeds the end of the range
                    print("Values between",start,"and",end,":",result)
                    return
            # Move to the next leaf node
            current_leaf = current_leaf.nextKey

        print("No values found")
    # Inserting at the parent
    def insert_in_parent(self, left, value, right):
       
       # print("Inserting in parent node. Current node values:", n.values)
        print("Inserting in parent node.","Splitting value:", value)
        
        if self.root == left:
            
            rootNode = Node(left.order)
            rootNode.values = [value]
            rootNode.keys = [left, right]
            self.root = rootNode
            left.parent = rootNode
            right.parent = rootNode
           
            # if not ndash.check_leaf:
            #     print("REMOVING",value)
            #     ndash.values.remove(value)
            
            print("Root node overflowed: New Root: ", rootNode.values, "Children of Root:",left.values, right.values)
            return
        
        parentNode = left.parent
        print("Parent: ",parentNode.values)
        parentKeys = parentNode.keys
        for i in range(len(parentKeys)):
            if parentKeys[i] == left:
                parentNode.values = parentNode.values[:i] + [value] + parentNode.values[i:]
                parentNode.keys = parentNode.keys[:i + 1] + [right] + parentNode.keys[i + 1:]
                if len(parentNode.values) == parentNode.order:
                    print("Parent node overflow detected.")
                    parentdash = Node(parentNode.order)
                    parentdash.parent = parentNode.parent
                    mid = int(math.ceil(parentNode.order / 2)) - 1
                    parentdash.values = parentNode.values[mid+1 :]
                    parentdash.keys = parentNode.keys[mid+1:]
                    value_ = parentNode.values[mid]
                    if mid == 0:
                        parentNode.values = parentNode.values[:mid+1 ]
                    else:
                        parentNode.values = parentNode.values[:mid]
                    parentNode.keys = parentNode.keys[:mid +1]
                    for j in parentNode.keys:
                        j.parent = parentNode
                    for j in parentdash.keys:
                        j.parent = parentdash

                    
                    print("Splitting parent node. Left node values:", parentNode.values)
                    print("Splitting parent node. Right node values:", parentdash.values)
                    
                    self.insert_in_parent(parentNode, value_, parentdash)
        print("Parent node after insertion:", parentNode.values)

        # Delete a node
    def delete(self, value, key):
        print("Delete", value)
        node_ = self.search(value) #find node that would have value to delete
        print("Looking at node", node_.values)

        temp = 0
        for i, item in enumerate(node_.values):
            if item == value:
                temp = 1 #flag that val has been found

                if key in node_.keys[i]: #if key exists in node
                    if len(node_.keys[i]) > 1: #list has multiple keys (safe to easily pop)
                        node_.keys[i].pop(node_.keys[i].index(key))
                    elif node_ == self.root: #node is root and only one key in node
                        node_.values.pop(i)
                        node_.keys.pop(i)
                    else:
                        node_.keys[i].pop(node_.keys[i].index(key))
                        del node_.keys[i]
                        node_.values.pop(node_.values.index(value))
                        self.deleteEntry(node_, value, key)
                else:
                    print("Value not in Key")
                    return
        if temp == 0:
            print("Value not in Tree")
            return

    def deleteEntry(self, node_, value, key):
        print()
        if not node_.check_leaf: #not a leaf node
            for i, item in enumerate(node_.keys): #find key associated with val being deleted
                if item == key:
                    node_.keys.pop(i)
                    break
            for i, item in enumerate(node_.values): #find val to be deleted
                if item == value:
                    print("Deleting value", item, "from node ", node_.values)
                    node_.values.pop(i)
                    break

        if self.root == node_ and len(node_.keys) == 1: #if deleting root and only one child is left, replace root w/child
            self.root = node_.keys[0]
            node_.keys[0].parent = None
            del node_
            return
        #if node needs redistribution
        elif (len(node_.keys) < int(math.ceil(node_.order / 2)) and node_.check_leaf == False) or (len(node_.values) < int(math.ceil((node_.order - 1) / 2)) and node_.check_leaf == True):
            print("Node needs redistributing")
            is_predecessor = 0
            parentNode = node_.parent
            PrevNode = -1
            NextNode = -1
            PrevK = -1
            PostK = -1
            for i, item in enumerate(parentNode.keys): #iterate through keys of parent to find our node among the siblings

                if item == node_: #find neighboring nodes and values
                    if i > 0:
                        PrevNode = parentNode.keys[i - 1]
                        PrevK = parentNode.values[i - 1]

                    if i < len(parentNode.keys) - 1:
                        NextNode = parentNode.keys[i + 1]
                        PostK = parentNode.values[i]

            if PrevNode == -1: #no predecessor, so we merge with successor
                ndash = NextNode
                value_ = PostK
            elif NextNode == -1: #no successor, so we merge with predecessor
                is_predecessor = 1
                ndash = PrevNode
                value_ = PrevK
            else: #select node that is the least full for merging
                if len(node_.values) + len(NextNode.values) < node_.order:
                    ndash = NextNode
                    value_ = PostK
                else:
                    is_predecessor = 1
                    ndash = PrevNode
                    value_ = PrevK

            if len(node_.values) + len(ndash.values) < node_.order:#if we can merge without overflow, merge
                print("Merging", node_.values, "and",ndash.values, "with  no overflow")
                if is_predecessor == 0:
                    node_, ndash = ndash, node_
                ndash.keys += node_.keys
                if not node_.check_leaf:
                    ndash.values.append(value_)
                else:
                    ndash.nextKey = node_.nextKey
                ndash.values += node_.values

                if not ndash.check_leaf:
                    for j in ndash.keys:
                        j.parent = ndash

                self.deleteEntry(node_.parent, value_, node_) #recursively call to adjust if necessary
                del node_
            else: #cannot merge w/o overflow, must redistribute
                if is_predecessor == 1: #we should merge with predecessor
                    if not node_.check_leaf:
                        ndashpm = ndash.keys.pop(-1)
                        ndashkm_1 = ndash.values.pop(-1) #get last from neighbor 
                        node_.keys = [ndashpm] + node_.keys
                        node_.values = [value_] + node_.values
                        parentNode = node_.parent
                        for i, item in enumerate(parentNode.values):
                            if item == value_:
                                p.values[i] = ndashkm_1
                                break
                    else:
                        ndashpm = ndash.keys.pop(-1)
                        ndashkm = ndash.values.pop(-1)
                        node_.keys = [ndashpm] + node_.keys
                        node_.values = [ndashkm] + node_.values
                        parentNode = node_.parent
                        for i, item in enumerate(parentNode.values):
                            if item == value_:
                                parentNode.values[i] = ndashkm
                                break
                else: #we should merge with sucessor
                    if not node_.check_leaf:
                        ndashp0 = ndash.keys.pop(0)
                        ndashk0 = ndash.values.pop(0) 
                        node_.keys = node_.keys + [ndashp0]
                        node_.values = node_.values + [value_]
                        parentNode = node_.parent
                        for i, item in enumerate(parentNode.values):
                            if item == value_:
                                parentNode.values[i] = ndashk0
                                break
                    else:
                        ndashp0 = ndash.keys.pop(0)
                        ndashk0 = ndash.values.pop(0)
                        node_.keys = node_.keys + [ndashp0]
                        node_.values = node_.values + [ndashk0]
                        parentNode = node_.parent
                        for i, item in enumerate(parentNode.values):
                            if item == value_:
                                parentNode.values[i] = ndash.values[0]
                                break

                if not ndash.check_leaf:#update parent child relationships
                    for j in ndash.keys:
                        j.parent = ndash
                if not node_.check_leaf:
                    for j in node_.keys:
                        j.parent = node_
                if not parentNode.check_leaf:
                    for j in parentNode.keys:
                        j.parent = parentNode

# Print the tree
def print_tree(self):
    queue = [self.root]

    while queue:
        level_size = len(queue)
        level_nodes = []

        for _ in range(level_size):
            node = queue.pop(0)
            level_nodes.append(node.values)

            if not node.check_leaf:
                for child in node.keys:
                    queue.append(child)

        print("Level:", level_nodes)
        print("-----------------------")

def generate_records(count):
    return random.sample(range(100000, 200001), count)

def build(tree,records):
    for record in records:
        tree.insert(record,record)

#########                   EXPERIMENTS          #######################################
#Experiment a: Generate 10.000 records
records = generate_records(10000)

#Experiment b: build B+Trees
dense13 = BplusTree(13)
build(dense13,records)

sparse13 = BplusTree(6) #sparse trees build at a halved order and then order is returned to normal for other ops
build(sparse13,records)
sparse13.order = 13

dense24 = BplusTree(24)
build(dense24,records)

sparse24 = BplusTree(12)
build(sparse24,records)
sparse24.order = 24

#Experimemts for dense 13
for i in range(2):
    asdf = input("Insert into dense 13")
    rand = generate_records(1)[0]
    dense13.insert(rand, rand)

for i in range(5):
    asdf=input("Randomly generated insert")
    rand = generate_records(1)[0]
    dense13.insert(rand, rand)
    asdf=input("Randomly generated delete")
    dense13.delete(rand, rand)

for i in range(5):
    asdf=input("Randomly generated search")
    rand = generate_records(1)[0]
    if(dense13.find(rand,rand)):
      print("Found", rand)
    else:
      print("Not found:", rand)

#Experimemts for dense 24
for i in range(2):
    asdf = input("Insert into dense 24")
    rand = generate_records(1)[0]
    dense24.insert(rand, rand)

for i in range(5):
    asdf=input("Randomly generated insert")
    rand = generate_records(1)[0]
    dense24.insert(rand, rand)
    asdf=input("Randomly generated delete")
    dense24.delete(rand, rand)

for i in range(5):
    asdf=input("Randomly generated search")
    rand = generate_records(1)[0]
    if(dense24.find(rand,rand)):
      print("Found", rand)
    else:
      print("Not found:", rand)

#Experimemts for sparse 13
for i in range(2):
    asdf = input("Delete into dense 24")
    rand = random.choice(records)
    sparse13.delete(rand, rand)

for i in range(5):
    asdf=input("Randomly generated insert")
    rand = generate_records(1)[0]
    sparse13.insert(rand, rand)
    asdf=input("Randomly generated delete")
    sparse13.delete(rand, rand)

for i in range(5):
    asdf=input("Randomly generated search")
    rand = generate_records(1)[0]
    if(sparse13.find(rand,rand)):
      print("Found", rand)
    else:
      print("Not found:", rand)

#Experimemts for sparse 24
for i in range(2):
    asdf = input("Delete into sparse 24")
    rand = random.choice(records)
    sparse24.delete(rand, rand)

for i in range(5):
    asdf=input("Randomly generated insert")
    rand = generate_records(1)[0]
    sparse24.insert(rand, rand)
    asdf=input("Randomly generated delete")
    sparse24.delete(rand, rand)

for i in range(5):
    asdf=input("Randomly generated search")
    rand = generate_records(1)[0]
    if(sparse24.find(rand,rand)):
      print("Found", rand)
    else:
      print("Not found:", rand)


# record_len = 3
# bplustree = BplusTree(record_len)
# bplustree.insert('33', '33')
# bplustree.insert('21', '21')
# bplustree.insert('31', '31')
# bplustree.insert('41', '41')
# bplustree.insert('10', '10')
# bplustree.insert('15', '15')
# print_tree(bplustree)
# bplustree.insert('44', '44')
# bplustree.insert('11', '11')
# bplustree.insert('7', '7')
# bplustree.insert('1', '1')
# bplustree.insert('2', '2')
# bplustree.insert('3', '3')
# bplustree.insert('5', '5')
# bplustree.delete(7,7)
# bplustree.delete(2,2)
# print_tree(bplustree)


