import numpy as np
import matplotlib.pyplot as plt
import math

BEFORE = "before/info"
AFTER = "after/info"
FREQLEN = 100

with open(BEFORE) as f:
  before = np.array(list(map(lambda x: float(x)/1000, f.read().strip().split("\n"))))
with open(AFTER) as f:
  after = np.array(list(map(lambda x: float(x)/1000, f.read().strip().split("\n"))))

fig, ax = plt.subplots(nrows = 1, ncols = 2)

def process(vals: list[int], plt, name: str):
  vals = np.array(list(map(math.log, vals))) # LOG THE DATA

  print(f"{name} n: {len(vals)}, stddev: {np.std(vals)}, mean: {np.mean(vals)}")

  #vals = vals[abs(vals - np.mean(vals)) < 4 * np.std(vals)] # SHOW IF NOT DOING LOG

  plt.hist(vals.ravel(), bins=FREQLEN)
  plt.set_title(name)
  plt.set_xlabel("ln(time)")
  plt.set_ylabel("Frequency")

process(before, ax[0], "Sample 1")
process(after, ax[1], "Sample 2")

fig.set_size_inches(10, 5)

#plt.show()
plt.savefig("plot.png")