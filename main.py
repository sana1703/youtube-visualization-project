# ------------------------------
# YouTube Statistics Project 
# Dataset: USvideos.csv
# ------------------------------

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# For advanced visualizations
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS
import squarify

# Setting file path and name
path = "C:/Users/SANA/Downloads/archive"
filename = "USvideos.csv"

# Change to working directory and load CSV
os.chdir(path)
df = pd.read_csv(filename)
print("Dataset loaded successfully!\n")
print(df.head())

# Displaying basic info about the DataFrame
print("\nBasic info about DataFrame:")
print(df.info())

# Show summary statistics
print("\nSummary statistics:")
print(df.describe())

# Show missing values per column
print("\nMissing values per column:")
print(df.isnull().sum())

# Removing duplicate rows
df = df.drop_duplicates()

# These columns should be numeric
numeric_cols = ['views', 'likes', 'dislikes', 'comment_count']

# Convert relevant columns to numeric (if not already)
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

print("\nData types for numeric columns after conversion:")
print(df[numeric_cols].dtypes)

# Impute missing values in different ways

# 1. Mean Imputation for numeric cols
df_mean = df.copy()
for col in numeric_cols:
    df_mean[col] = df_mean[col].fillna(df_mean[col].mean())
print("\nFilled missing values in numeric columns with their means.")

# 2. Attribute-based (category-wise mean) imputation for 'views' and 'likes'
df_group = df.copy()
df_group['views'] = df_group.groupby('category_id')['views'].transform(lambda x: x.fillna(x.mean()))
df_group['likes'] = df_group.groupby('category_id')['likes'].transform(lambda x: x.fillna(x.mean()))
print("Filled missing 'views' and 'likes' by category mean.")

# 3. Fill some object/text fields with simple default
df_simple = df.copy()
df_simple = df_simple.fillna({"description": "No Description", "tags": "No Tags"})
print("Filled missing 'description' and 'tags' with default text.")

# For most analysis, pick core columns only
use_cols = ['video_id','title','channel_title','category_id','views','likes','dislikes','comment_count']
data = df[use_cols]
print("\nCore dataset preview:")
print(data.head())

# ---- GROUPBY STUDIES ----

# 1. Total views per category
views_by_cat = data.groupby('category_id')['views'].sum().reset_index()
print("\nTotal Views by Category:")
print(views_by_cat)

plt.figure(figsize=(8,5))
plt.bar(views_by_cat['category_id'], views_by_cat['views'])
plt.title("Total Views by Category")
plt.xlabel("Category ID")
plt.ylabel("Views")
plt.show()

# 2. Average likes per channel, top 20 channels
likes_by_channel = data.groupby('channel_title')['likes'].mean().reset_index()
top20_likes = likes_by_channel.sort_values('likes', ascending=False).head(20)
print("\nAverage Likes (Top 20 Channels):")
print(top20_likes)

plt.figure(figsize=(10,5))
plt.barh(top20_likes['channel_title'], top20_likes['likes'])
plt.title("Average Likes for Top 20 Channels")
plt.xlabel("Average Likes")
plt.ylabel("Channel")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

# 3. Like-to-view ratio per category
like_view = data.groupby('category_id').agg({
    'likes': 'sum',
    'views': 'sum'
}).reset_index()
like_view['like_percent'] = (like_view['likes'] / like_view['views']) * 100
print("\nLike-to-view percent per category:")
print(like_view)

plt.figure(figsize=(8,5))
plt.plot(like_view['category_id'], like_view['like_percent'], marker="o")
plt.title("Like % by Category")
plt.xlabel("Category ID")
plt.ylabel("Like %")
plt.show()

# ---- PIVOT TABLES ----

# Pivot 1: Views by category & channel
pivot1 = pd.pivot_table(data, values='views', index='category_id', columns='channel_title', aggfunc='sum')
print("\nPivot Table 1 (Views):")
print(pivot1)

# Pivot 2: Mean likes per category & channel
pivot2 = pd.pivot_table(data, values='likes', index='category_id', columns='channel_title', aggfunc='mean')
print("\nPivot Table 2 (Likes):")
print(pivot2)

# Pivot 3: Dislike counts per category & channel
pivot3 = pd.pivot_table(data, values='dislikes', index='category_id', columns='channel_title', aggfunc='sum')
print("\nPivot Table 3 (Dislikes):")
print(pivot3)

# ---- MERGING & CONCATENATION ----

# Merge views and like % per category
merge_df = pd.merge(
    views_by_cat,
    like_view[['category_id', 'like_percent']],
    on='category_id',
    how='inner'
)
print("\nMerged DataFrame (Views and Like %):")
print(merge_df.head())

# Concatenate (for demonstration) a few rows from mean- and group-imputed DataFrames
concat_df = pd.concat([df_mean.head(5), df_group.head(5)])
print("\nConcatenated DataFrame (from imputed samples):")
print(concat_df)


# ---- ADVANCED VISUALIZATIONS ----

# Correlation heatmap for numeric columns
plt.figure(figsize=(6,4))
corr = df[['views', 'likes', 'dislikes', 'comment_count']].corr()
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm')
plt.title("Correlation Heatmap")
plt.show()

# Wordcloud for video titles
text = " ".join(str(t) for t in df['title'].dropna())
wordcloud = WordCloud(width=800, height=400,
                      background_color='white',
                      stopwords=STOPWORDS,
                      colormap='viridis').generate(text)
plt.figure(figsize=(10,5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title("Word Cloud of Video Titles")
plt.show()

# Treemap: Views per category
views_per_cat = df.groupby('category_id')['views'].sum().reset_index()
sizes = views_per_cat['views']
labels = [f"{cat}\n{views:,.0f}" for cat, views in zip(views_per_cat['category_id'], views_per_cat['views'])]
plt.figure(figsize=(14, 7))
squarify.plot(sizes=sizes, label=labels, alpha=.8, color=plt.cm.Paired.colors)
plt.title("Treemap: Total Views per Category")
plt.axis('off')
plt.show()


# ---- FINAL INFERENCES ----

print("\n\n--------- FINAL INFERENCE ---------\n")
print("""
1. Some categories, like entertainment & music, have much higher views than others.

2. Pivot tables show certain channels get much more engagement, depending on category.

3. Combining different group and imputed DataFrames makes it easier to compare analyses.

Overall, there are clear patterns in likes, views, and dislikes by category on US YouTube.
""")

