import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from uncertainties import ufloat
import seaborn as sns
import os

## M/(10**7 M_☉) = 1.9*[s/(200 km/s)]**5.1
# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, 'datatr', 'my_data.csv')

df = pd.read_csv(data_path)

# Keep df as DataFrame and add new columns
df['log_sigma'] = np.log10(df['velDisp'])
df['log_sigma_err'] = df['velDispErr'] / (df['velDisp'] * np.log(10))
alpha = 8.33  # values from Kormendy & Ho 2013: alpha=8.33, beta=4.42
beta = 4.42

# Calculate log_MBH using the formula
log_MBH = alpha + beta * np.log10(df['velDisp'] / 200)

df['log_MBH'] = log_MBH

plt.figure(figsize=(10, 6))

# Create a density scatter plot
sns.regplot(data=df, x='log_sigma', y='log_MBH', 
            scatter_kws={'alpha':0.3, 's':10, 'color':'midnightblue'}, 
            line_kws={'color':'red', 'label':'Kormendy & Ho (2013)', 'linewidth':0.5})

# Add error bars for log_sigma_err
plt.errorbar(df['log_sigma'], df['log_MBH'], xerr=df['log_sigma_err'], 
             fmt='none', ecolor='gray', alpha=0.5, label='Error bars', 
             elinewidth=0.1, capsize=1)

plt.title('Estimated Black Hole Mass vs. Velocity Dispersion (SDSS z < 0.01)')
plt.xlabel(r'$\log_{10}(\sigma)$ [km/s]')
plt.ylabel(r'$\log_{10}(M_{BH}/M_{\odot})$')
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()

plt.savefig("/home/user/codes (mostly vsc)/astro/MBH_vs_sigma.png", dpi=1000)
plt.show()
plt.close()
