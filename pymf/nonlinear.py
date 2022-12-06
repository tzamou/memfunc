import numpy as np
import matplotlib.pyplot as plt
#模糊化------------------------------------------------------------------------------------------------------------


class Gaussian_mf:
    def __init__(self,p,sigma,m=2):
        """
        :param x: obs
        :param c: 位移
        :param sigma: 函數的寬度(sigma)
        :param m: 預設2
        :return:
        """
        self.sigma = sigma
        self.m = m
        self.c = None
        self.p = p
    def calculate(self,obs):
        return np.exp((-1/2)*abs((obs-self.c)/self.sigma)**self.m)
    def plot(self, x_down, x_up):
        x = np.arange(x_down, x_up, 0.01)
        y = np.exp((-1/2)*abs((x-self.c)/self.sigma)**self.m)
        plt.plot(x, y)

class GeneralizedBell_mf:
    def __init__(self,a,p,b=2):
        """
        :param a: 函數的寬度
        :param b: 上面的平坦度
        :param c: x軸平移
        """
        self.a = a
        self.b = b
        self.c = None
        self.p = p
    def calculate(self,obs):
        return 1 / (1 + abs((obs - self.c) / self.a) ** (2 * self.b))

    def plot(self, x_down, x_up):
        x = np.arange(x_down, x_up, 0.01)
        y = 1 / (1 + abs((x - self.c) / self.a) ** (2 * self.b))
        plt.plot(x, y)

class Sigmoid_mf:
    def __init__(self,a,p):
        """
        :param x: obs
        :param a: 坡度斜率
        :param c: 平移
        """
        self.a = a
        self.c = None
        self.p = p
    def calculate(self,obs):
        return 1/(1+np.exp(-self.a*(obs-self.c)))

    def plot(self,x_down,x_up):
        x = np.arange(x_down,x_up,0.01)
        y = 1/(1+np.exp(-self.a*(x-self.c)))
        plt.plot(x,y)

class Left_mf:
    def __init__(self,p,alpha):
        """
        :param x:
        :param c:
        :param alpha:
        """
        self.c = None
        self.p = p
        self.alpha = alpha
    def calculate(self, obs):
        return (self.c-np.sqrt(max(0,1-obs**2)))/self.alpha
    def plot(self,x_down,x_up):
        x = np.arange(x_down,x_up,0.01)
        y = (self.c-np.sqrt(max(0,1-x**2)))/self.alpha
        plt.plot(x,y)

class Right_mf:
    def __init__(self,p,beta):
        """
        :param x: obs
        :param c:
        :param beta:
        """
        self.c = None
        self.p = p
        self.beta = beta
    def calculate(self, obs):
        return np.exp(-1*abs((obs-self.c)/self.beta)**3)
    def plot(self,x_down,x_up):
        x = np.arange(x_down,x_up,0.01)
        y = np.exp(-1*abs((x-self.c)/self.beta)**3)
        plt.plot(x,y)


class Fuzzy:
    def __init__(self,maxlst,minlst,name=[]):
        self.mf = []
        self.min_array = minlst
        self.max_array = maxlst
        self.name = name

    def add(self,mf):
        self.mf.append(mf)

    def transform(self,x):
        fuzzylist = np.zeros((len(x), len(self.mf)))
        for i in range(len(x)):
            self._calculate(x[i], self.min_array[i], self.max_array[i], fuzzylist[i])
        return fuzzylist.flatten()

    def _calculate(self,x,min,max,fuzlst):
        for index, mf in enumerate(self.mf):
            mf.c = min+(max-min)*mf.p
            fuzlst[index] = mf.calculate(x)

    def plot(self):
        for i in range(len(self.max_array)):
            plt.gca()
            for mf in self.mf:
                try:
                    plt.title(self.name[i])
                except:
                    plt.title('Membership func')
                mf.c = self.min_array[i] + (self.max_array[i] - self.min_array[i]) * mf.p
                mf.plot(self.min_array[i],self.max_array[i])
            plt.show()
