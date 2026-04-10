import pandas as pd

features = pd.read_csv('features/features.csv')
train = pd.read_csv('train/train.csv')

combined = pd.merge(features, train, on=['Store', 'Date'], how='left')

combined.to_csv('walmart_combined.csv', index=False)
