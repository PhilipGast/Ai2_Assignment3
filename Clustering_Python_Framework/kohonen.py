import math
import random
import sys


class Cluster:
    """This class represents the clusters, it contains the
    prototype (the mean of all it's members) and memberlists with the
    ID's (which are Integer objects) of the datapoints that are member
    of that cluster."""
    def __init__(self, dim, prototype):
        self.prototype = prototype
        self.current_members = set()

class Kohonen:
    def __init__(self, n, epochs, traindata, testdata, dim):
        self.n = n
        self.epochs = epochs
        self.traindata = traindata
        self.testdata = testdata
        self.dim = dim

        # initialize a map with random value between 0 to 1
        # A 2-dimensional list of clusters. Size == N x N
        self.clusters = [[Cluster(dim, [random.uniform(0, 1) for _ in range(dim)]) for _ in range(n)] for _ in range(n)]
        # Threshold above which the corresponding html is prefetched
        self.prefetch_threshold = 0.5
        self.initial_learning_rate = 0.8
        # The accuracy and hitrate are the performance metrics (i.e. the results)
        self.accuracy = 0
        self.hitrate = 0

    def train(self):
        # Step 1: initialize map with random vectors (A good place to do this, is in the initialisation of the clusters)
        # Repeat 'epochs' times:
        #     Step 2: Calculate the squareSize and the learningRate, these decrease lineary with the number of epochs.
        #     Step 3: Every input vector is presented to the map (always in the same order)
        #     For each vector its Best Matching Unit is found, and :
        #         Step 4: All nodes within the neighbourhood of the BMU are changed, you don't have to use distance relative learning.
        # Since training kohonen maps can take quite a while, presenting the user with a progress bar would be nice
        print("--- train ---")
        for i in range(self.epochs):
            sys.stdout.write('\r')
            sys.stdout.write("[%-60s] %d%%" % ('=' * int(60 * (i + 1) /self.epochs), (100 * (i + 1) / self.epochs)))
            sys.stdout.flush()
            sys.stdout.write(", epoch %d" % (i + 1))
            sys.stdout.flush()
            # learning rate to update neighbor weights
            learning_rate = self.initial_learning_rate*(1 - i/self.epochs)
            # radius of neighbors need to be changed
            radius = (self.n / 2) * (1 - i / self.epochs)
            for idx, data in enumerate(self.traindata):
                x, y = self.find_bmu(data)
                self.clusters[x][y].current_members.add(idx)
                self.update_bmu_neighborhood(x, y, radius, learning_rate, data)
        print("--- finished training ---")

    def find_bmu(self, data):
        # function to loop through the map and find the best matching prototype with minimum euclidean distance
        min_dist = math.inf
        for i in range(self.n):
            for j in range(self.n):
                vec = self.clusters[i][j].prototype
                dist = self.distance(vec, data)
                if dist < min_dist:
                    min_dist = dist
                    x = i
                    y = j
        return x, y

    def update_bmu_neighborhood(self, x, y, radius, learning_rate, data):
        for i in range( 0 if x - int(radius) < 0 else x - int(radius),
                        self.n if x + int(radius) > self.n else x + int(radius)):
            for j in range(0 if y - int(radius) < 0 else y - int(radius),
                           self.n if y + int(radius) > self.n else y + int(radius)):
                for k in range(self.dim):
                    self.clusters[i][j].prototype[j] = self.clusters[i][j].prototype[k] * (1 - learning_rate) + data[k]*learning_rate

    def test(self):
        # iterate along all clients
        # for each client find the cluster of which it is a member
        print("--- test ---")
        hits = 0
        prefetched_requests = 0
        total_requests = 0
        for data in self.testdata:
            x, y = self.find_bmu(data)
            for i in range(self.dim):
                if self.clusters[x][y].prototype[i] > self.prefetch_threshold:
                    prefetched_requests += 1
                if self.clusters[x][y].prototype[i] > self.prefetch_threshold or data[i] == 1:
                    total_requests += 1
                if self.clusters[x][y].prototype[i] > self.prefetch_threshold and data[i] == 1:
                    hits += 1
        self.hitrate = prefetched_requests / total_requests if total_requests != 0 else 0
        self.accuracy = hits / prefetched_requests if prefetched_requests != 0 else 0
        # get the actual testData (the vector) of this client
        # iterate along all dimensions
        # and count prefetched htmls
        # count number of hits
        # count number of requests
        # set the global variables hitrate and accuracy to their appropriate value


    def print_test(self):
        print("Prefetch threshold =", self.prefetch_threshold)
        print("Hitrate:", self.hitrate)
        print("Accuracy:", self.accuracy)
        print("Hitrate+Accuracy =", self.hitrate+self.accuracy)

    def print_members(self):
        for i in range(self.n):
            for j in range(self.n):
                print("Members cluster", (i, j), ":", self.clusters[i][j].current_members)

    def print_prototypes(self):
        for i in range(self.n):
            for j in range(self.n):
               print("Prototype cluster", (i, j), ":", self.clusters[i][j].prototype)

    def distance(self, vector_a, vector_b):
        dist = math.sqrt(sum([(a - b) ** 2 for a, b in zip(vector_a, vector_b)]))
        return dist