"""kmeans.py"""

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


def euclidean_distance(pt1, pt2):
    distance = 0
    for i in range(len(pt1)):
        distance += (pt1[i] - pt2[i]) ** 2
    return distance ** 0.5


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

    def train(self):
        # implement k-means algorithm here:
        # Step 1: Select an initial random partioning with k clusters
        for i in range(len(self.clusters)):
            for j in range(len(self.clusters[0].prototype)):
                self.clusters[i].prototype[j] = random.random()

        print(self.clusters[0].prototype)
        # Step 2: Generate a new partition by assigning each datapoint to its closest cluster center
        distance = [10, 10, 10]
        for i in range(len(self.traindata)):
            for j in range(len(self.clusters)):
                distance[j] = euclidean_distance(self.traindata[i], self.clusters[j].prototype)
            #print(distance, i)
            min_distance = distance[0]
            num = 0
            for d in range(len(distance)):
                if distance[d] < min_distance:
                    num = d
            #print(num)
            self.clusters[num].current_members.add(i)

        # Step 3: recalculate cluster centers
        for i in range(len(self.clusters)):
            for j in range(len(self.clusters[i].prototype)):
                centroid = 0
                for k in range(len(self.clusters[i].current_members)):
                    l1 = list(self.clusters[i].current_members)
                    centroid += self.traindata[l1[k]][j]
                self.clusters[i].prototype[j] = centroid/(len(self.clusters[i].current_members))


        # Step 4: repeat until cluster membership stabilizes
        if self.clusters[0].previous_members == self.clusters[0].current_members:
            break
        pass

    def test(self):

        # iterate along all clients. Assumption: the same clients are in the same order as in the testData
        # for each client find the cluster of which it is a member
        # get the actual testData (the vector) of this client
        # iterate along all dimensions
        # and count prefetched htmls
        # count number of hits
        # count number of requests
        # set the global variables hitrate and accuracy to their appropriate value
        pass

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
