
def f(cpi):
    return 1000*(cpi/(cpi+1))

import matplotlib.pyplot as plt 

y = list(map(f, range(0, 100)))

print(y)

plt.plot(list(range(0, 100)), y)

plt.savefig("teste.png")

plt.show()
