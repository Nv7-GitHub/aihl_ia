import numpy as np
import matplotlib.pyplot as plt
import math
from scipy import stats
from random import shuffle
import os

BEFORE = "before/info"
AFTER = "after/info"
N = 25

with open(BEFORE) as f:
  before = np.array(list(map(lambda x: float(x)/1000, f.read().strip().split("\n"))))
with open(AFTER) as f:
  after = np.array(list(map(lambda x: float(x)/1000, f.read().strip().split("\n"))))

before = np.array(list(map(math.log, before)))
after = np.array(list(map(math.log, after)))

def sample(vals: list[float], name: str):
  vals = vals.copy()
  if os.path.exists(name):
    with open(name) as f:
      return np.array(list(map(float, f.read().strip().split("\n"))))
  shuffle(vals)
  vals = vals[:N]
  with open(name, "w+") as f:
    f.write("\n".join(map(str, vals)))
  return vals[:N]


before = sample(before, "data/before.txt")
after = sample(after, "data/after.txt")

print("\n\n")
for i in range(len(before)):
  print(f"{round(before[i], 2)} & {round(after[i], 2)} \\\\")
print("\n\n")

print(np.mean(before), np.std(before), np.mean(after), np.std(after))
res = stats.ttest_ind(after, before, alternative="less")
print(res)