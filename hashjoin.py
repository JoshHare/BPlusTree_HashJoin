import random


#Part 1: Data Generation
S = [(random.randint(10000, 50000), random.randint(1, 100)) for _ in range(5000)]

#Part 2: Virtual Disk I/O
def read_from_disk(relation, block_size):
    for i in range(0, len(relation), block_size):
        yield relation[i:i+block_size]

def write_to_disk(data, block_size):
    diskcount=0
    for i in range(0, len(data), block_size):
       # block = data[i:i+block_size]
        diskcount += 1
    return diskcount

#Part 3: Hash Function
def hash_function(value):
    return value % 15 

def cost(sizesmall, sizelarge):
    return 3* (sizesmall+sizelarge)

#Part 4: Join Algorithm
def two_pass_hash_join(R, S, block_size):
    #Hash S first
    hash_table = {}
    for block in read_from_disk(S, block_size): #iterate over blocks of tuples, get blocks from disk
        for tuple in block: #for each tuple in the block
            key = hash_function(tuple[0])   #hash
            if key not in hash_table:  #check if we need to initialize a list
                hash_table[key] = []
            hash_table[key].append(tuple)  #append to corresponding hash val

    # Hash R and then join
    result = []
    for block in read_from_disk(R, block_size): #get blocks from disk
        for tuple in block: #for each tuple in the block
            key = hash_function(tuple[1])   #hash
            if key in hash_table:   
                for s_tuple in hash_table[key]: 
                    if s_tuple[0] == tuple[1]: #for each matching hash tuple (b=b)
                        result.append((tuple[0], tuple[1], s_tuple[1]))  #append joined tuple [a,b,c]

    disk_io_count = write_to_disk(result, block_size)

    return result,disk_io_count

#Part 5: Experiments
def fivepointone():
    global diskcount
    diskcount = 0
    R = [(random.randint(1000, 5000), random.choice([tuple[0] for tuple in S])) for _ in range(1000)]
    joined,disks = two_pass_hash_join(R, S, block_size=8)
    picked = random.sample([tuple[0] for tuple in S], 20)
    picked = [tuple for tuple in joined if tuple[1] in picked]

    print("Tuples with picked B-values:",picked)
    print("Disks used:",cost(1000,5000))

def fivepointtwo():
   
    R = [(random.randint(1000, 5000), random.randint(20000, 30000)) for _ in range(1200)]
    joined,disks = two_pass_hash_join(R, S, block_size=8)
   #disks = len(R) // 8 + len(S) // 8

    print("All tuples in the join:",joined)
    print("Disks used", cost(1200,5000))

fivepointone()
fivepointtwo()
