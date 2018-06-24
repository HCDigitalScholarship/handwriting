class TestDataGenerator:
    def __init__(self):
        self.show_num = 1
        self.comp_num = 1

    def cosine(self, n=100, jitter=0.05):
        """
        Generates n pairs (x, cos(x)) with period of 16
        """
        import numpy as np
        import random as rand
        
        xs = [(np.pi*x/8) for x in range(n)]
        ys = [(np.cos(x, dtype="float16") + rand.random()*jitter) for x in xs]
        return(list(zip(xs, ys)))

    def sequential(self, n=100, jitter=0.05, direct="forward"):
        """
        Generates data in which y value is fully determined by last (or next) x value.
        Each x value is a random number drawn uniformly on the interval (0, 1). 
        Recommended to use n > 20 because first/last y-values (depending on direction) are not dependent on neighboring x-values.
        : param n : number of data points to generate
        : param jitter : scale of random jitter for y value
        : param direct : 
            val "forward": y[i] = x[i-1] + jitter
            val "reverse": y[i] = x[i+1] + jitter
        returns a list of length n of (x, y) tuples
        """
        import numpy as np
        import random as rand

        xs = [rand.random() for x in range(n)]

        if (direct == "forward"): 
            ys = [xs[i-1] + rand.random()*jitter for i in range(1, n)]
            ys = [0] + ys
        elif (direct == "reverse"):
            ys = [xs[i+1] + rand.random()*jitter for i in range(0,n-1)]
            ys = ys + [0]
        else:
            raise(ValueError, "Allowed values for direct: 'forward', 'reverse'")
        return list(zip(xs,ys))

    def show_data(self, data):
        """
        Shows a scatterplot of (x,y) data 
        given an list of format [(x1, y1), (x2, y2), ...]
        : param n : the data (list of tuples)
        """
        import matplotlib.pyplot as plt
        xs = [x for x, y in data]
        ys = [y for x, y in data]
        plt.scatter(xs, ys)
        plt.savefig("./Plot{}".format(self.show_num))
        plt.close()
        self.show_num += 1

    def show_comparison(self, data1, data2):
        """
        Shows a scatter plot comparing two sets of (x,y) data 
        given two lists each of format [(x1, y1), (x2, y2), ...]
        : param data1 : the first set (list of tuples)
        : param data2 : the second set (list of tuples)
        """
        import matplotlib.pyplot as plt
        xs = [x for x, y in data1] + [x for x, y in data2]
        ys = [y for x, y in data1] + [y for x, y in data2]

        color = ["r" for _ in range(len(data1))] + ["b" for _ in range(len(data2))]

        for i in range(len(xs)):
            plt.scatter(xs[i], ys[i], color=color[i])

        plt.savefig("./ComparisonPlot{}".format(self.comp_num))
        plt.close()
        self.comp_num += 1

if __name__ == '__main__':
    # view an example of the sequential data
    G = TestDataGenerator()
    data = G.sequential(n=5, jitter=0)
    print(data)


    
#G = TestDataGenerator()
#data = G.cosine(50)
#G.show_data(data)