segment_image
import math
import random

# Threshold function
# THRESHOLD = lambda size, c: c / size

class Graph:
    
    def __init__(self, nrows, ncols):
        self.nrows = nrows
        self.ncols = ncols
        self.nvertices = nrows * ncols
        self.nedges = 0
        self.graph = []
        self.parent = []
        self.rank = []
        self.size = []
        self.num_components = 0

    # Adds edge to graph
    def addEdge(self, a, b, w):
        self.graph.append([a, b, w])

    # Function to find the component of x
    # Returns the parent node of the component
    def find(self, x):
        if self.parent[x] == x:
            return x
        return self.find(self.parent[x])
    
    # Joins two components x and y
    def join(self, x, y):
        x_root = self.find(x)
        y_root = self.find(y)
        if self.rank[x_root] < self.rank[y_root]:
            self.parent[x_root] = y_root
            self.size[y_root] += self.size[x_root]
        elif self.rank[x_root] > self.rank[y_root]:
            self.parent[y_root] = x_root
            self.size[x_root] += self.size[y_root]
        else:
            self.parent[y_root] = x_root
            self.rank[x_root] += 1
            self.size[x_root] += self.size[y_root]
        self.num_components -= 1
        
    def segment_image(self, src, c, min_size):
        """Segments a image
        input parameters:
        src: source image
        c: constant for threshold function
        min_size: minimum component size in the graph required.
        """
        temp = 0
        for i in range(0, self.nrows):
            for j in range(0, self.ncols):
                if j < self.ncols - 1:
                    a = i * self.ncols + j
                    b = i * self.ncols + (j + 1)
                    w = self.pixel_diss(src, i, j, i, j+1)
                    self.nedges += 1
                    self.addEdge(a, b, w)
                if i < self.nrows - 1:
                    a = i * self.ncols + j
                    b = (i + 1) * self.ncols + j
                    w = self.pixel_diss(src, i, j, i+1, j)
                    self.nedges += 1
                    self.addEdge(a, b, w)
                if (i < self.nrows - 1) and (j < self.ncols - 1):
                    a = i * self.ncols + j
                    b = (i + 1) * self.ncols + (j + 1)
                    w = self.pixel_diss(src, i, j, i + 1, j + 1)
                    self.nedges += 1
                    self.addEdge(a, b, w)
                if (i < self.nrows - 1) and (j > 0):
                    a = i * self.ncols + j
                    b = (i + 1) * self.ncols + (j - 1)
                    w = self.pixel_diss(src, i, j, i + 1, j - 1)
                    self.nedges += 1
                    self.addEdge(a, b, w)
        # print("number of rows cols edges is %d %d %d" % self.nrows, self.ncols, self.nedges)
        print("size of graph is : %d " % len(self.graph))
        self.process_graph(c)
        # post process small components
        for i in range(0, self.nedges):
            u, v, w = self.graph[i]
            a = self.find(u)
            b = self.find(v)
            if ((a != b) and ((self.size[a] < min_size) or (self.size[b] < min_size))):
                self.join(a, b)
        
        rand_colors = []
        for i in range(0, self.nvertices):
            rand_colors.append(self.random_rgb())
        
        for i in range(0, self.nrows):
            for j in range(0, self.ncols):
                comp = self.find(i * self.ncols + j)
                src[i][j][0] = rand_colors[comp][0]
                src[i][j][1] = rand_colors[comp][1]
                src[i][j][2] = rand_colors[comp][2]
        print("number of components are: %d" % self.num_components)
        return src



                
    def process_graph(self, c):
        """the components, where each component represents a image segment."""
        # Sort all the edges in non-decreasing order of the weight
        self.graph =  sorted(self.graph,key=lambda item: item[2])

        threshold = []

        # Create initial components with 1 element
        for v in range(0, self.nvertices):
            self.parent.append(v)
            self.rank.append(0)
            self.size.append(1)
            self.num_components += 1
            threshold.append(self.THRESHOLD(1, c))
        
        for i in range(0, self.nedges):
            u, v, w = self.graph[i]

            # Components connected by this edge
            a = self.find(u)
            b = self.find(v)
            if a != b:
                if ((w <= threshold[a]) and	(w <= threshold[b])):
                    self.join(a, b)
                    a = self.find(a)
                    threshold[a] = w + self.THRESHOLD(self.size[a], c)

    def pixel_diss(self, src, x1, y1, x2, y2):
        return math.sqrt(math.pow((src[x1][y1][0] - src[x2][y2][0]), 2) + math.pow((src[x1][y1][1] - src[x2][y2][1]), 2) + math.pow((src[x1][y1][2] - src[x2][y2][2]), 2) )

    def random_rgb(self):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return [b, g, r]
    
    def THRESHOLD(self, size, c):
        return c / size