import random

with open("data.txt","r") as f_read:
    lines = f_read.readlines()

x = []
y = []
z = []
for line in lines:
    x.append(line.split()[0])
    y.append(line.split()[1])
    z.append(line.split()[2])

def measure(num):
    if str(num) in x:
        index = [idx for idx,x_ in enumerate(x) if x_== str(num)]
        idx = random.choice(index)
        low = y[idx]
        high = z[idx]
        return low,high
    else:
        high = num +5
        low = num-28
        return low,high

if __name__ == '__main__':
    low,high = measure(92)
    print(low,high)