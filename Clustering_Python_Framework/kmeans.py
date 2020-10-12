"""kmeans.py"""
import math
import random



class Cluster:
    """This class represents the clusters, it contains the
    prototype (the mean of all it's members) and memberlists with the
    ID's (which are Integer objects) of the datapoints that are member
    of that cluster. You also want to remember the previous members so
    you can check if the clusters are stable."""

    def __init__(self, dim):
        self.prototype = [0.0 for _ in range(dim)]
        self.current_members = set()
        self.previous_members = set()

class KMeans:

    def __init__(self, k, traindata, testdata, dim):
        self.traindata = traindata
        self.testdata = testdata
        self.dim = dim

        # Threshold above which the corresponding html is prefetched
        self.prefetch_threshold = 0.5

        # An initialized list of k clusters
        self.clusters = [Cluster(dim) for _ in range(k)]
        print(len(self.clusters[0].prototype))
        print(len(traindata))
        print(len(traindata[0]))
        print(self.clusters[0].prototype[0])
        print(self.clusters[0].current_members)
        # The accuracy and hitrate are the performance metrics (i.e. the results)
        self.accuracy = 0
        self.hitrate = 0

    def initialize(self):
        for i in range(len(self.clusters)):
            self.clusters[i].prototype= self.traindata[i]

    def clear_cluster(self):
        for idx, data in enumerate(self.clusters):
            data.previous_members = data.current_members
            data.current_members = set()

    def assign_data(self):
        for idx, data in enumerate(self.traindata):
            min_dist = math.inf
            min_cluster = self.clusters[0]
            for j in range(len(self.clusters)):
                if self.distance(data, self.clusters[j].prototype) < min_dist:
                    min_cluster = self.clusters[j]
                    min_dist = self.distance(data, self.clusters[j].prototype)
            min_cluster.current_members.add(idx)

    def update_center(self):
        updated = False
        for idx, cluster in enumerate(self.clusters):
            current_center = cluster.prototype
            for j in range(self.dim):
                centroid = 0
                for i, data in enumerate(cluster.current_members):
                    centroid += self.traindata[data][j]
                cluster.prototype[j] = centroid/(len(cluster.current_members))
            if current_center != cluster.prototype:
                updated = True
        return updated

    def train(self):
        # implement k-means algorithm here:
        # Step 1: Select an initial random partioning with k clusters
        print("--- train ---")
        self.initialize()
        updated = True
        while updated:
            # Step 2: Generate a new partition by assigning each datapoint to its closest cluster center
            self.clear_cluster()
            self.assign_data()
            # Step 3: recalculate cluster centers
            updated = self.update_center()
            # Step 4: repeat until cluster membership stabilizes


    def test(self):
        print("--- test ---")
        hits = 0
        prefetched_requests = 0
        total_requests = 0
        for idx, d in enumerate(self.testdata):
            min_dist = math.inf
            for data in self.clusters:
                if self.distance(data.prototype, d) < min_dist:
                    min_dist = self.distance(data.prototype, d)
                    best_cluster = data
            for i in range(self.dim):
                if best_cluster.prototype[i] > self.prefetch_threshold:
                    prefetched_requests += 1
                if best_cluster.prototype[i] > self.prefetch_threshold or d[i] == 1:
                    total_requests += 1
                if best_cluster.prototype[i] > self.prefetch_threshold and d[i] == 1:
                    hits += 1
        self.hitrate = prefetched_requests / total_requests if total_requests != 0 else 0
        self.accuracy = hits / prefetched_requests if prefetched_requests != 0 else 0
        # iterate along all clients. Assumption: the same clients are in the same order as in the testData
        # for each client find the cluster of which it is a member
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
        print("Hitrate+Accuracy =", self.hitrate + self.accuracy)

    def print_members(self):
        for i, cluster in enumerate(self.clusters):
            print("Members cluster", i, ":", cluster.current_members)

    def print_prototypes(self):
        for i, cluster in enumerate(self.clusters):
            print("Prototype cluster", i, ":", cluster.prototype)

    def distance(self, vector_a, vector_b):
        dist = math.sqrt(sum([(a - b) ** 2 for a, b in zip(vector_a, vector_b)]))
        return dist
