import numpy as np
import matplotlib.pyplot as plt
#模糊化------------------------------------------------------------------------------------------------------------

class Triangular_mf:
    def __init__(self,min_array,max_array,x,alpha=1/8,n=2):
        """
        :param min_array:
        :param max_array:
        :param x:
        :param alpha: 最左邊和最右邊佔的比例
        :param n: n+1為由幾條function組合的
        """
        self.n = n
        self.alpha = alpha
        self.min_array = min_array
        self.max_array = max_array
        self.x = x
    def transform(self):
        fuzzylist = np.zeros((len(self.x), self.n+1))
        for i in range(len(self.x)):
            self._triangular_mf(self.x[i],self.min_array[i],self.max_array[i],fuzzylist[i])
        return fuzzylist.flatten()
    def _triangular_mf(self,x,min_x,max_x,fuzlst):
        assert (self.alpha < 1/2) and (self.alpha > 0),'The range of alpha should be greater than 0 and less than 1/2'
        d0 = min_x + (max_x - min_x) * self.alpha
        delta = (1 - 2*self.alpha) / self.n
        d1 = d0+(max_x-min_x) * delta
        if x<=d0:
            fuzlst[0] = 1
            return None
        for i in range(self.n):
            if (x>d0 and x<=d1):
                fuzlst[i] = (x - d1) / (d0 - d1)
                fuzlst[i+1] = (x - d0) / (d1 - d0)
                return None
            d0 = d1
            d1 = d0+(max_x-min_x) * delta
        if (x>d1):
            fuzlst[-1] = 1

class Trapezoidal_mf:
    def __init__(self, min_array, max_array, x, alpha=1/8 , beta=1/8, n=2):
        """
        :param min_array:
        :param max_array:
        :param x: input number
        :param alpha: 最左邊和最右邊佔的比例
        :param beta: 梯形上底佔的比例
        :param n:
        """
        self.n = n
        self.alpha = alpha
        self.beta = beta
        self.min_array = min_array
        self.max_array = max_array
        self.x = x

    def transform(self):
        fuzzylist = np.zeros((len(self.x), self.n + 1))
        for i in range(len(self.x)):
            self._trapezoidal_mf(self.x[i], self.min_array[i], self.max_array[i], fuzzylist[i])
        return fuzzylist.flatten()
        # print(fuzzylist.flatten(),len(fuzzylist.flatten()))


    def _trapezoidal_mf(self, x, min_x, max_x, fuzlst):
        assert (self.alpha < 1 / 2) and (self.alpha > 0), 'The range of alpha should be greater than 0 and less than 1/2'
        d0 = min_x + (max_x - min_x) * self.alpha
        delta = (1 - 2 * self.alpha-(self.n-1)*self.beta) / self.n
        d1 = d0 + (max_x - min_x) * delta
        d2 = d1 + (max_x - min_x) * self.beta
        if x <= d0:
            fuzlst[0] = 1
            return None
        for i in range(self.n):
            if (x > d0 and x <= d1):
                fuzlst[i] = (x - d1) / (d0 - d1)
                fuzlst[i+1] = (x - d0) / (d1 - d0)
                return None
            elif (x > d1 and x <= d2):
                fuzlst[i+1] = 1
                return None
            d0 = d2
            d1 = d0 + (max_x - min_x) * delta
            d2 = d1 + (max_x - min_x) * self.beta
        if (x > d1):
            fuzlst[-1] = 1

class _Left:
    def __init__(self,p):
        self.p = p
        self.type = 'left'
class _Right:
    def __init__(self,p):
        self.p = p
        self.type = 'right'
class Triangular:
    def __init__(self,p,end=False):
        self.p = p
        self.end = end
        self.type='triangular'
class Trapezoidal:
    def __init__(self,p,beta,end=False):
        self.p = p
        self.beta = beta
        self.end = end
        self.type='trapezoidal'
class Container:
    def __init__(self,head,end,maxlst,minlst):
        self.mf=[_Left(head),_Right(end)]
        self.s=head+end
        self.end=False
        self.min_array = minlst
        self.max_array = maxlst

    def add(self,func):
        assert self.end==False,'The value range of the membership function is out of range, the sum of the parameter "p" must be less than 1.'
        self.mf.insert(-1,func)
        if func.type!='trapezoidal':
            self.s += func.p
        else:
            self.s += func.p
            self.s += func.beta
        if func.end:
            assert self.s <= 1, f'Membership function range out of range'
            self.end=True
    def transform(self,x):
        assert self.end==True, 'The membership function has not been edited yet, the parameter "end=True" of the last equation.'
        fuzzylist = np.zeros((len(x), len(self.mf)))
        for i in range(len(x)):
            self._calculate(x[i], self.min_array[i], self.max_array[i], fuzzylist[i])
        return fuzzylist.flatten()
    def _calculate(self,x,min,max,fuzlst):
        d1=min
        for index, mf in enumerate(self.mf):
            d0=d1
            d1=d0+(max-min)*mf.p
            if mf.type=='triangular':
                if x > d0 and x <= d1:
                    fuzlst[index-1] = (x-d1)/(d0-d1)
                    fuzlst[index] = (x-d0)/(d1-d0)
                    return None
            elif mf.type=='trapezoidal':
                d2=d1+(max-min)*mf.beta
                if x>d0 and x<=d1:
                    fuzlst[index-1] = (x-d1)/(d0-d1)
                    fuzlst[index] = (x-d0)/(d1-d0)
                    return None
                elif x>d1 and x<=d2:
                    fuzlst[index]=1
                    return None
                d1=d2
            elif mf.type == 'left':
                if x >= d0 and x <= d1:
                    fuzlst[index] = 1
                    return None
            elif mf.type=='right':
                if x > d0 and x < d1:
                    fuzlst[index-1] = (x-d1)/(d0-d1)
                    fuzlst[index] = (x-d0)/(d1-d0)
                    return None
                elif x >= d1 and x <= max:
                    fuzlst[index]=1
                    return None


