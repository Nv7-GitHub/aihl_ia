import numpy as np
import matplotlib.pyplot as plt
import math
from scipy import stats

BEFORE = "before/info"
AFTER = "after/info"
FREQLEN = 25

with open(BEFORE) as f:
  before = np.array(list(map(lambda x: float(x)/1000, f.read().strip().split("\n"))))
with open(AFTER) as f:
  after = np.array(list(map(lambda x: float(x)/1000, f.read().strip().split("\n"))))

def process(vals: list[float], l, r, errval):
  print("\n\n")
  vals = np.array(list(map(math.log, vals))) # LOG THE DATA
  dist = stats.norm(np.mean(vals), np.std(vals))

  # Making the frequency tables
  # <2SD, ... (FREQLEN-2), >2SD
  lexp = int(dist.cdf(l) * len(vals))
  lobs = len(vals[vals < l])
  print(f"\\textless{l} & {lobs} & {lexp} \\\\")
  binsize = round((r - l)/(FREQLEN-2), 2)
  f_obs = [lobs]
  f_exp = [lexp]
  for i in range(0, FREQLEN-2):
    lv = l + i*binsize
    rv = l + (i+1)*binsize
    obs = len(vals[np.logical_and(lv < vals, vals < rv)])
    exp = int((dist.cdf(rv) - dist.cdf(lv))*(len(vals) + errval))
    f_obs.append(obs)
    f_exp.append(exp)
    print(f"{round(lv, 2)}-{round(rv, 2)} & {obs} & {exp} \\\\")
  
  r = l + binsize*FREQLEN

  robs = len(vals[vals > r])
  rexp = int((1-dist.cdf(r)) * len(vals))
  f_exp.append(rexp)
  err = np.sum(f_exp) - (np.sum(f_obs) + robs)
  robs += err
  f_obs.append(robs)
  print(f"\\textgreater{r} & {robs} & {rexp}\\\\")


  res = stats.chisquare(f_obs, f_exp, ddof = 2)
  print(f"mean: {np.mean(vals)}, stdev: {np.std(vals)}, chisquare: {res.statistic}, p: {res.pvalue}, df: {FREQLEN - 1 - 2}, ERROR: {err}")

process(before, 2.5, 9, 52)
process(after, 2, 8, 118)
