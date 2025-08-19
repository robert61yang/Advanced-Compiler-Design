import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('results.csv')
df['result'] = df['result'].astype(int)
# print(df.head())
baseline = []
tdce = []
lvn = []
for i in range(len(df)):
    if df.iloc[i, 1] == 'baseline':
        baseline.append(df.iloc[i, 2])
    elif df.iloc[i, 1] == 'tdce':
        tdce.append(df.iloc[i, 2])
    elif df.iloc[i, 1] == 'lvn':
        lvn.append(df.iloc[i, 2])
        # breakpoint()
    
x = range(1, len(baseline) + 1)

plt.plot(x, baseline, label='Baseline', marker='o')
plt.plot(x, tdce, label='TDCE', marker='s')
plt.plot(x, lvn, label='LVN', marker='^')

# 加上標題和標籤
plt.title('Comparison of Baseline, TDCE, and LVN')
plt.xlabel('Index')
plt.ylabel('Values')

# 顯示圖例以標識不同的折線
plt.legend()

# 顯示圖表
plt.grid(True)  # 選擇性：加上格線
plt.show()
