# importing package
import matplotlib.pyplot as plt
import numpy as np

# create data
no_participants = 5
telegraphed_cooking = [90, 80, 75, 70, 85]
casual_cooking = [60, 50, 65, 40, 50]
width = 0.40

# plot data in grouped manner of bar type
x = np.arange(1,1+no_participants)
plt.bar(x - 0.2, telegraphed_cooking, width, label = "Intentionally Telegraphed Moves")
plt.bar(x + 0.2, casual_cooking, width, label = "Casual Cooking Behaviour")
plt.legend()
plt.xlabel("Participant Number")
plt.ylabel("Action Replication Success Rate [%]")

plt.show()