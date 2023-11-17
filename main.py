import os
from analysis import analyze
import matplotlib.pyplot as plt
import math
import numpy as np

COMMAND = "combine"
DIRECTORY = "before"

files = os.listdir(DIRECTORY)
if COMMAND != "":
  files = [COMMAND]
pltsidelen = math.ceil(math.sqrt(len(files)))
_, ax = plt.subplots(nrows = pltsidelen, ncols = pltsidelen)
for i, command in enumerate(files):
  with open(f"{DIRECTORY}/{command}") as f:
    data = list(map(lambda x: float(x)/1000, f.read().strip().split("\n")))
    if COMMAND == "":
      plot = ax[i//pltsidelen, i % pltsidelen]
      plot.set_title(command)
    else:
      plot = plt
    analyze(command, np.array(data), plot)
plt.show()