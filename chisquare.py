import numpy as np
import matplotlib.pyplot as plt
import math
from scipy import stats

BEFORE = "before/info"
AFTER = "after/info"
FREQLEN = 25

fig, ax = plt.subplots(nrows = 1, ncols = 2)

with open(BEFORE) as f:
  before = np.array(list(map(lambda x: float(x)/1000, f.read().strip().split("\n"))))
with open(AFTER) as f:
  after = np.array(list(map(lambda x: float(x)/1000, f.read().strip().split("\n"))))

def calccdf(mu1, sd1, mu2, sd2, mu3, sd3, mu4, sd4, m1, m2, m3, m4, val):
  if mu2 == 0:
    return stats.norm(mu1, sd1).cdf(val)

  a = stats.norm(mu1, sd1)
  b = stats.norm(mu2, sd2)
  c = stats.norm(mu3, sd3)
  d = stats.norm(mu4, sd4)
  v = a.cdf(val)*m1 + b.cdf(val)*m2 + c.cdf(val)*m3 + d.cdf(val)*m4
  return v

def process(vals: list[float], l, r, errval, plt, mu1, sd1, mu2, sd2, mu3, sd3, mu4, sd4, m1, m2, m3, m4, name):
  print("\n\n")
  vals = np.array(list(map(math.log, vals))) # LOG THE DATA
  cdf = lambda x: calccdf(mu1, sd1, mu2, sd2, mu3, sd3, mu4, sd4, m1, m2, m3, m4, x)

  # Making the frequency tables
  # <2SD, ... (FREQLEN-2), >2SD
  lexp = int(cdf(l) * len(vals))
  if lexp == 0:
    lexp = 1
  lobs = len(vals[vals < l])
  xvals = [l]
  print(f"\\textless{l} & {lobs} & {lexp} \\\\")
  binsize = round((r - l)/(FREQLEN-1), 2)
  f_obs = [lobs]
  f_exp = [lexp]
  for i in range(0, FREQLEN-2):
    lv = l + i*binsize
    rv = l + (i+1)*binsize
    obs = len(vals[np.logical_and(lv < vals, vals < rv)])
    exp = int(round((cdf(rv) - cdf(lv))*(len(vals) + errval)))
    if exp == 0:
      exp = 1
    f_obs.append(obs)
    f_exp.append(exp)
    xvals.append((lv + rv)/2)
    print(f"{round(lv, 2)}-{round(rv, 2)} & {obs} & {exp} \\\\")
  
  r = l + binsize*(FREQLEN-2)
  xvals.append(r)

  robs = len(vals[vals > r])
  rexp = int((1-cdf(r)) * len(vals))
  if rexp == 0:
    rexp = 1
  f_exp.append(rexp)
  err = np.sum(f_exp) - (np.sum(f_obs) + robs)
  f_obs.append(robs)
  print(f"\\textgreater{r} & {robs} & {rexp}\\\\")


  #res = stats.chisquare(f_obs, f_exp, ddof = 2) # This doesn't work because there are slight rounding issues between the two
  stat = sum(map(lambda x, y: ((x - y)**2)/y, f_obs, f_exp))
  p = stats.chi2.pdf(stat, FREQLEN - 1 - 2)
  print(f"mean: {np.mean(vals)}, stdev: {np.std(vals)}, chisquare: {stat}, p: {p}, df: {FREQLEN - 1 - 2}, ERROR: {err}")

  # Plot
  plt.set_title(name)
  plt.set_xlabel("ln(time)")
  plt.set_ylabel("Frequency")
  plt.plot(xvals, f_obs, label = "Observed")
  plt.plot(xvals, f_exp, label = "Expected")

process(before, 2.5, 9, 0, ax[0], 6.06, 1.27, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "Sample 1") # 6.55, 0.27, 3, 0.17, 4.25, 0.3, 5.5, 0.2, 0.75, 0.05, 0.1, 0.1
process(after, 2, 8, 0, ax[1], 5.75, 1.24, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "Sample 2") # 6.35, 0.25, 4.2, 0.8, 5.6, 0.15, 0, 1, 0.7, 0.2, 0.1, 0

fig.set_size_inches(10, 5)
#plt.show()
plt.savefig("plot.png")
