import numpy as np
import matplotlib.pyplot as plt
import math

BEFORE = "before/info"
AFTER = "after/info"
FREQLEN = 25

with open(BEFORE) as f:
  before = np.array(list(map(lambda x: float(x)/1000, f.read().strip().split("\n"))))
with open(AFTER) as f:
  after = np.array(list(map(lambda x: float(x)/1000, f.read().strip().split("\n"))))

def process(vals: list[int], l, r):
  print("\n\n")
  vals = np.array(list(map(math.log, vals))) # LOG THE DATA

  # Making the frequency tables
  """
  # <2SD, ... (FREQLEN-2), >2SD
  print(f"\\textless{l} & {len(vals[vals < l])} \\\\")
  binsize = round((r - l)/(FREQLEN-2), 2)
  for i in range(0, FREQLEN-2):
    lv = round(l + i*binsize, 2)
    rv = round(l + (i+1)*binsize, 2)
    print(f"{lv}-{rv} & {len(vals[np.logical_and(lv < vals, vals < rv)])} \\\\")
  
  r = l + binsize*FREQLEN
  print(f"\\textgreater{r} & {len(vals[vals > r])} \\\\")
  """
  print(f"mean: {np.mean(vals)}, stdev: {np.std(vals)}")

process(before, 2.5, 9)
process(after, 2, 8)
