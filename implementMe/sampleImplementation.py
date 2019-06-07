# Problem Set 11SC: Graph optimization
# Example Problem: Finding shortest paths through MIT buildings
# Name: Mohammad Ehsanul Karim
# Collaborators: Rasik Hasan
# Start: July 21, 2016; 11:41pm

import string
from graph import *
import Queue

#
# Problem 2: Building up the Campus Map
#
# Write a couple of sentences describing how you will model the
# problem as a graph)
#

#method that loads the map
def load_map(mapFilename):
    """
    Parses the map file and constructs a directed graph

    Parameters:
        mapFilename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive 
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a directed graph representing the map
    """
    
    print "Loading map from file..."

    digraph = WeightedDigraph()
    fileObject = open(mapFilename)
    
    for line in fileObject:
        line = line.split()

        srcNode = Node(line[0])
        dstNode = Node(line[1])
        distTot = int(line[2])
        distSun = int(line[3])
        weight = (distTot, distSun)

        digraph.addNode(srcNode)
        digraph.addNode(dstNode)
        digraph.addEdge(WeightedEdge(srcNode, dstNode, weight))

    return digraph

#Calculates the total outside distance traveled by the path.
#ouput: totaldistance
def pathDist(digraph, path):
    """
    Calculates the total distance traveled by the path.

    Parameters:
        digraph: instance of class Digraph or its subclass.
        path: A path is a list of Node objects.
        
    Returns:
        The total distance traveled by the path.
    """
    
    totalDist = 0

    
    if len(path) > 1:
        
        for ind in range(1, len(path)):
            srcNode = path[ind - 1] #confusion!!!!!!!!!!!
            endNode = path[ind]
            totalDist += digraph.getWeight(srcNode, endNode)[0]
        return totalDist

    return totalDist

#Calculates the total outside distance traveled by the path.
#ouput: totaloutdistance
def pathOutDist(digraph, path):
    """
    Calculates the total outside distance traveled by the path.

    Parameters:
        digraph: instance of class Digraph or its subclass.
        path: A path is a list of Node objects.

    Returns:
        The total outside distance traveled by the path.
    """
    
    totalOutDist = 0    
    
    if len(path) > 1:
        
        for ind in range(1, len(path)):
            srcNode = path[ind - 1]
            endNode = path[ind]
            totalOutDist += digraph.getWeight(srcNode, endNode)[1]
        return totalOutDist
            
    return totalOutDist

#Calculate the cost of the path.
#output: distTravel, outTravel
def pathCost(digraph, path):
    """
    Calculate the cost of the path.

    Parameters:
        digraph: instance of class Digraph or its subclass
        path: a candidate path; a path is a list of Node objects.        

    Returns:
        A tuple consisting of two values defining the cost of the
        transversed path. The two values are total distance traveled
        and total outside distance traveled.
    """
    
    
    distTravel = pathDist(digraph, path)
    outTravel = pathOutDist(digraph, path)

    return (distTravel, outTravel)

##Check if start and end node exists in the digraph
def checkNodesExist(digraph, src, end): #Check if start and end node exists in the digraph.
    """
    Check if start and end node exists in the digraph.
    
    Parameters:
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers
        (represented as integers)

    Returns: True or False    
    """
    
    hasSrcNode = digraph.hasNode(Node(src))
    hasEndNode = digraph.hasNode(Node(end))       

    if not (hasSrcNode and hasEndNode):
        raise ValueError('Start or end not in map.')

#
# Problem 3: Finding the Shortest Path using Brute Force Search
#
# State the optimization problem as a function to minimize
# and the constraints
#
# Rasik Hasan contribution starts here:

def bruteForceSearchHelper(digraph, start, end):
    """
    Finds all the paths from start to end using brute-force approach.    

    Parameters:
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)        

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        A list of all paths, which runs from start to end.
        For example: [path1, path2, ... ]
        
        A single path (example: path 1 for instance) from start to end,
        represented by a list of building numbers (in strings),
        [n_1, n_2, ..., n_k], where there exists an edge from n_i to n_(i+1)
        in digraph, for all 1 <= i < k.

        If there exists no path then returns a empty list.
    """
    
    stack = [[Node(start)]]
    checkNodesExist(digraph, start, end)
    
    while len(stack) != 0:
        tmpPath = stack.pop(0)
        start = tmpPath[-1]

        if start == Node(end): yield tmpPath

        else:
            for cNode in digraph.childrenOf(start):
                if cNode not in tmpPath:
                    updateTmpPath = tmpPath + [cNode]
                    stack = [updateTmpPath] + stack

def bruteForceSearch(digraph, start, end, maxTotalDist, maxDistOutdoors):
    """
    Finds the shortest path from start to end using brute-force approach.
    The total distance travelled on the path must not exceed maxTotalDist, and
    the distance spent outdoor on this path must not exceed maxDisOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    shortest = None
    filteredPath = []
    
    for path in bruteForceSearchHelper(digraph, start, end):
        pathCostValues = pathCost(digraph, path)
        if pathCostValues[0] <= maxTotalDist:
            if pathCostValues[1] <= maxDistOutdoors:
                filteredPath.append(path)

    for path in filteredPath:
        pathCostValues = pathCost(digraph, path)
        if pathCostValues[0] <= maxTotalDist:
            shortest = path
            maxTotalDist = pathCostValues[0]

    if shortest == None:
        raise ValueError('No path found!')
    else: return shortest

def shortestPathDFS(digraph, start, end, maxTotalDist, maxDistOutdoors):
    """
    Finds the shortest path from start to end using depth-first search approach.
    The total distance travelled on the path must not exceed maxTotalDist, and
    the distance spent outdoor on this path must not exceed maxDisOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    stepcount=0
    output = None
    
    stack = [[Node(start)]]
    stackDist = [0]
    stackOutDist = [0]
    checkNodesExist(digraph, start, end)
    
    while len(stack) != 0:
        stepcount+=1
        tmpPath = stack.pop(0)
        tmpPathDist = stackDist.pop(0)
        tmpPathOutDist = stackOutDist.pop(0)
        #print len(stack)
        
        
        start = tmpPath[-1]
        #print start
        
        
        if start == Node(end):
            
            if output == None or tmpPathDist < maxTotalDist:
                output = tmpPath
                outputDist, outputOutDist = tmpPathDist, tmpPathOutDist
                maxTotalDist= outputDist

        else:
            for cNode in digraph.childrenOf(start):
                if cNode not in tmpPath:
                    updateTmpPathDist = tmpPathDist + digraph.getWeight(start, cNode)[0]
                    updateTmpPathOutDist = tmpPathOutDist + digraph.getWeight(start, cNode)[1]


                    if updateTmpPathDist <= maxTotalDist:
                        if updateTmpPathOutDist <= maxDistOutdoors:
                    
                            updateTmpPath = tmpPath + [cNode]
                            stack = [updateTmpPath] + stack
                            stackDist = [updateTmpPathDist] + stackDist
                            stackOutDist = [updateTmpPathOutDist] + stackOutDist
    
    if output == None or len(output) <= 1:
        raise ValueError('Path not found!')
    else: return output, stepcount

def shortestPathBFS(digraph, start, end, maxTotalDist, maxDistOutdoors):
    output = None
    stepcount=0
    que = Queue.Queue()
    que.put([Node(start)])
    queDist=Queue.Queue()
    queDist.put(0)
    queOutDist = Queue.Queue()
    queOutDist.put(0)
    checkNodesExist(digraph, start, end)

    while not que.empty():
        stepcount+=1
        tmpPath = que.get()
        tmpPathDist = queDist.get()
        tmpPathOutDist = queOutDist.get()
        # print len(stack)


        start = tmpPath[-1]
        # print start


        if start == Node(end):

            if output == None or tmpPathDist < maxTotalDist:
                output = tmpPath
                outputDist, outputOutDist = tmpPathDist, tmpPathOutDist
                maxTotalDist = outputDist

        else:
            for cNode in digraph.childrenOf(start):
                if cNode not in tmpPath:
                    updateTmpPathDist = tmpPathDist + digraph.getWeight(start, cNode)[0]
                    updateTmpPathOutDist = tmpPathOutDist + digraph.getWeight(start, cNode)[1]

                    if updateTmpPathDist <= maxTotalDist:
                        if updateTmpPathOutDist <= maxDistOutdoors:
                            updateTmpPath = tmpPath + [cNode]
                            # print stack
                            que.put(updateTmpPath)
                            # print stack
                            queDist.put(updateTmpPathDist)
                            queOutDist.put(updateTmpPathOutDist)

    if output == None or len(output) <= 1:
        raise ValueError('Path not found!')
    else:
        return output,stepcount


def stackDFS(digraph, start, end, maxTotalDist, maxDistOutdoors):
    output = None
    stepcount=0
    que = Queue.LifoQueue()
    que.put([Node(start)])
    queDist = Queue.LifoQueue()
    queDist.put(0)
    queOutDist = Queue.LifoQueue()
    queOutDist.put(0)
    checkNodesExist(digraph, start, end)

    while not que.empty():
        stepcount+=1
        tmpPath = que.get()
        tmpPathDist = queDist.get()
        tmpPathOutDist = queOutDist.get()
        # print len(stack)


        start = tmpPath[-1]
        # print start


        if start == Node(end):

            if output == None or tmpPathDist < maxTotalDist:
                output = tmpPath
                outputDist, outputOutDist = tmpPathDist, tmpPathOutDist
                maxTotalDist = outputDist

        else:
            for cNode in digraph.childrenOf(start):
                if cNode not in tmpPath:
                    updateTmpPathDist = tmpPathDist + digraph.getWeight(start, cNode)[0]
                    updateTmpPathOutDist = tmpPathOutDist + digraph.getWeight(start, cNode)[1]


                    if updateTmpPathDist <= maxTotalDist:
                        if updateTmpPathOutDist <= maxDistOutdoors:
                            updateTmpPath = tmpPath + [cNode]
                            # print stack
                            que.put(updateTmpPath)
                            # print stack
                            queDist.put(updateTmpPathDist)
                            queOutDist.put(updateTmpPathOutDist)

    if output == None or len(output) <= 1:
        raise ValueError('Path not found!')
    else:
        return output,stepcount





def dijkstraaWithoutOutsidedistance(digraph, start, end, maxTotalDist, maxDistOutdoors):
        output = None
        stepcount = 0
        que = Queue.PriorityQueue()
        que.put([Node(start)],0)
        queDist = 0
        checkNodesExist(digraph, start, end)
        tmpPathDist = 0

        while not que.empty():
            stepcount += 1
            tmpPath = que.get()




            start = tmpPath[-1]
            #print start


            if start == Node(end):

                if output == None or tmpPathDist < maxTotalDist:
                    output = tmpPath
                    outputDist = tmpPathDist
                    maxTotalDist = outputDist

            else:
                for cNode in digraph.childrenOf(start):
                    if cNode not in tmpPath:
                        updateTmpPathDist = tmpPathDist + digraph.getWeight(start, cNode)[0]
                        if updateTmpPathDist <= maxTotalDist:

                                updateTmpPath = tmpPath + [cNode]
                                que.put(updateTmpPath,updateTmpPathDist)


        if output == None or len(output) <= 1:
            raise ValueError('Path not found!')
        else:
            return output, stepcount

def dijkstraaWithOutsideDistance(digraph, start, end, maxTotalDist, maxDistOutdoors):
    output = None
    stepcount = 0
    que = Queue.PriorityQueue()
    queDist = 0
    queOutDist = 0
    que.put([[Node(start)],queDist,queOutDist], queDist)



    checkNodesExist(digraph, start, end)

    while not que.empty():
        stepcount+=1
        gue=que.get()
        tmpPath = gue[0]
        tmpPathDist = gue[1]
        tmpPathOutDist = gue[2]



        start = tmpPath[-1]



        if start == Node(end):

            if output == None or tmpPathDist < maxTotalDist:
                output = tmpPath
                outputDist, outputOutDist = tmpPathDist, tmpPathOutDist
                maxTotalDist = outputDist

        else:
            for cNode in digraph.childrenOf(start):
                if cNode not in tmpPath:
                    updateTmpPathDist = tmpPathDist + digraph.getWeight(start, cNode)[0]
                    updateTmpPathOutDist = tmpPathOutDist + digraph.getWeight(start, cNode)[1]

                    if updateTmpPathDist <= maxTotalDist:
                        if updateTmpPathOutDist <= maxDistOutdoors:
                            updateTmpPath = tmpPath + [cNode]
                            que.put([updateTmpPath, updateTmpPathDist,updateTmpPathOutDist], updateTmpPathDist)

    if output == None or len(output) <= 1:
        raise ValueError('Path not found!')
    else:
        return output,stepcount


# Test the codes.
import time


print "start =32, End =56"
START = 32
END = 56

LARGEDIST1 = 1000000
LARGEDIST2 = 0

digraph = load_map('mit_map.txt')

print "Brutus"
start = time.time()
print bruteForceSearch(digraph, START, END, LARGEDIST1, LARGEDIST2), time.time() - start

print "DFS List"
start = time.time()
print shortestPathDFS(digraph, START, END, LARGEDIST1, LARGEDIST2), time.time() - start

print "DFS Stack"
start = time.time()
print stackDFS(digraph, START, END, LARGEDIST1, LARGEDIST2), time.time() - start

print "BFS Queue"
start = time.time()
print shortestPathBFS(digraph, START, END, LARGEDIST1, LARGEDIST2), time.time() - start

print "new Dijkstra"
start = time.time()
print dijkstraaWithOutsideDistance(digraph, START, END, LARGEDIST1, LARGEDIST2), time.time() - start

print "\nstart =14, End =68"
START = 14
END = 68

LARGEDIST1 = 1000000
LARGEDIST2 = 0

digraph = load_map('mit_map.txt')

print "Brutus"
start = time.time()
print bruteForceSearch(digraph, START, END, LARGEDIST1, LARGEDIST2), time.time() - start

print "DFS List"
start = time.time()
print shortestPathDFS(digraph, START, END, LARGEDIST1, LARGEDIST2), time.time() - start

print "DFS Stack"
start = time.time()
print stackDFS(digraph, START, END, LARGEDIST1, LARGEDIST2), time.time() - start

print "BFS Queue"
start = time.time()
print shortestPathBFS(digraph, START, END, LARGEDIST1, LARGEDIST2), time.time() - start

print "new Dijkstra"
start = time.time()
print dijkstraaWithOutsideDistance(digraph, START, END, LARGEDIST1, LARGEDIST2), time.time() - start






