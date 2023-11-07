import numpy as np

def analyze(command: str, times, plt):
  times = times[abs(times - np.mean(times)) < 2 * np.std(times)] # Reject outliers

  plt.hist(times.ravel(), bins=max(len(times)//100, 50))
  print(f"{command}: {np.mean(times)} (stddev: {np.std(times)})")