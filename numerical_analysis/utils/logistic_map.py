import matplotlib.pyplot as plt 

a,b = 1,4
N,R = [],[]

plt.figure(figsize=(8,6))

while a <= b:
    x=0.5
    for i in range(100):
        x = a*x*(1-x)
        if i > 100/2:
            N.append(x)
            R.append(a)

    plt.plot(R, N, ',',  color="#4863A0")
    a += 0.005
    
plt.show()