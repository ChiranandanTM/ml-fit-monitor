import pandas as pd
import numpy as np

# Create a test dataset for "Good Fit"
np.random.seed(42)
X = np.random.randn(50, 4)
w = np.array([2, -1.5, 1, -0.5])
y = (X @ w > 0).astype(int)
y = np.where(np.random.rand(50) < 0.05, 1 - y, y)

df = pd.DataFrame(X, columns=['feature_1', 'feature_2', 'feature_3', 'feature_4'])
df['target'] = y

# Save as Excel
df.to_excel('test_excel_file.xlsx', index=False)
print("✓ Test Excel file created: test_excel_file.xlsx")
print(f"  Shape: {df.shape}")
print(f"  Class distribution: {df['target'].value_counts().to_dict()}")
