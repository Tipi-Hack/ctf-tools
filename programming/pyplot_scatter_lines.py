from matplotlib import pyplot

file = open("coords").read().splitlines()

piece = 0
x_seq = []
y_seq = []

for line in file:
    (x, y, num) = line.split(',')
    x = int(x)
    y = int(y)
    num = int(num)
    if num != piece:
        pyplot.scatter(x_seq, y_seq)
        pyplot.plot(x_seq,y_seq)
        # pyplot.show()
        pyplot.savefig(f"{num}.png")
        pyplot.clf()
        piece = num
        x_seq = []
        y_seq = []

    x_seq.append(x)
    y_seq.append(y)
