**Thank you for using pymf.**

Here are some tutorials to help you get started quickly.

****
**linear membership function**

Membership functions can be divided into linear and nonlinear. There are two types of linear equations: Triangular and Trapezoidal.
To use them you can refer to the following code.
First create the combination to be converted, and set the upper and lower limits of the conversion, then create a group of membership function combinations "head" and "end" parameters are the ratio of the leftmost and rightmost ends of the membership function.

```python
from pymf.pymf.linear import Container,Triangular,Trapezoidal
x = [1, 3, 6, 5, 2, 4, 3.5, 4.5, 1.2]

minx = [0 for _ in range(len(x))]

maxx = [6 for _ in range(len(x))]

mf = Container(head=1/6,end=1/6,maxlst=maxx,minlst=minx)

mf.add(Trapezoidal(p=1/6,beta=1/6))

mf.add(Triangular(p=1/6,end=True))

print(mf.transform(x))
```
****
**nonlinear membershipfunction**

Nonlinear equations are more commonly used, and pymf supports the use of Gaussian, Generalizedbell, Sigmoid, Left, and Right equations.
```python
from pymf.pymf.nonlinear import Fuzzy,Sigmoid_mf,Gaussian_mf
x = [1, 3, 6, 5, 2, 3]
min0 = [0 for _ in range(len(x)-1)]
max0 = [10 for _ in range(len(x)-1)]
mf = Fuzzy(minlst=min0,maxlst=max0)
mf.add(Sigmoid_mf(a=2, p=2/3))
mf.add(Gaussian_mf(p=1/2,sigma=1))
mf.add(Sigmoid_mf(a=-2, p=1/3))
x = mf.transform(x)
print(x)
mf.plot()
```