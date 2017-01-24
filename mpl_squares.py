import matplotlib.pyplot as plt

squares = [n * n for n in range(1, 6)]

# plt.plot(squares, linewidth = 5)

plt.title("Square Numbers", fontsize = 24)
plt.xlabel("Value", fontsize = 14)
plt.ylabel("Square of Value", fontsize = 14)

plt.scatter(range(1,6), [n * n for n in range(1, 6)], s = 100)

plt.show()