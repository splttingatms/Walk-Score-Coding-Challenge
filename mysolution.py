import fileinput


class DirectedGraph:
    def __init__(self):
        self.adjIn = []     # adjacency-list of input vertices
        self.adjOut = []    # adjacency-list of output vertices
        self.index = {}     # dictionary to convert symbol to index
        self.symbol = []    # array to convert index to symbol
        self.V = 0          # count of vertices in graph (including lazy-deleted nodes)

    def addEdge(self, v, w):
        if v not in self.index:
            self.addVertex(v)

        if w not in self.index:
            self.addVertex(w)

        if w in self.adjacentOutOf(v):
            return # do not allow parallel edges

        vi = self.index[v]
        wi = self.index[w]

        self.adjOut[vi].append(wi)
        self.adjIn[wi].append(vi)

    def addVertex(self, v):
        if v in self.index:
            return

        self.index[v] = self.V
        self.symbol.append(v)
        self.V += 1
        self.adjIn.append([])
        self.adjOut.append([])

    def removeVertex(self, v):
        vi = self.index.pop(v)
        # lazy delete to avoid shifting index values
        self.symbol[vi] = None

        for inNeighbor in self.adjIn[vi]:
            self.adjOut[inNeighbor].remove(vi)
        self.adjIn[vi] = None

        for outNeighbor in self.adjOut[vi]:
            self.adjIn[outNeighbor].remove(vi)
        self.adjOut[vi] = None

    def adjacentOutOf(self, v):
        vi = self.index[v]
        return [self.symbol[x] for x in self.adjOut[vi]]

    def adjacentInTo(self, v):
        vi = self.index[v]
        return [self.symbol[x] for x in self.adjIn[vi]]

    def indegree(self, v):
        vi = self.index[v]
        return len(self.adjIn[vi])

    def outdegree(self, v):
        vi = self.index[v]
        return len(self.adjOut[vi])

    def vertices(self):
        return self.index.keys()

    def __str__(self):
        result = ""
        for vs in self.vertices():
            indegree = self.indegree(vs)
            outdegree = self.outdegree(vs)
            adjacent = ', '.join(self.adjacentOutOf(vs))
            result += "{} ({}, {}): {}\n".format(vs, indegree, outdegree, adjacent)
        return result.strip("\n")


def get(lst, index, default=None):
    try:
        return lst[index]
    except IndexError:
        return default


class Remover:
    def __init__(self, digraph):
        self.digraph = digraph

        verticesToEliminate = []
        # must iterate twice to differentiate isolated vertices and vertices that turn isolated after removing adjacent
        for vs in digraph.vertices():
            if digraph.indegree(vs) == 1 and digraph.outdegree(vs) == 1:
                verticesToEliminate.append(vs)

        for vs in verticesToEliminate:
            inNeighbor = get(digraph.adjacentInTo(vs), 0, None)
            outNeighbor = get(digraph.adjacentOutOf(vs), 0, None)

            digraph.removeVertex(vs)

            if inNeighbor is not outNeighbor:
                digraph.addEdge(inNeighbor, outNeighbor)


graph = DirectedGraph()
for line in fileinput.input():
    v, w = line.strip().split('\t')
    graph.addEdge(v, w)

Remover(graph)
for v in graph.vertices():
    for w in graph.adjacentOutOf(v):
        print("{}\t{}".format(v, w))
