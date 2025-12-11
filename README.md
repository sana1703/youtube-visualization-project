# YouTube Trending Data Analysis & Visualization

This project performs exploratory data analysis (EDA) and visualization on the **US YouTube Trending Videos dataset**.  
It includes data cleaning, handling missing values, statistical summaries, pivot table analysis, and multiple visual insights.

---

##  Dataset Information

The dataset **is not included in this repository** due to file size.  
Please download it manually from Kaggle:

🔗 https://www.kaggle.com/datasets/datasnaek/youtube-new

After downloading, place the file **USvideos.csv** in the same folder as `main.py`.

---

##  Project Overview

This project explores patterns and trends in YouTube’s US trending videos.  
Key operations include:

###  Data Cleaning
- Removing duplicate rows  
- Type conversion for numeric columns  
- Handling missing values using:
  - Mean imputation  
  - Category-wise imputation  
  - Simple text imputation for description and tags  

###  Exploratory Data Analysis (EDA)
- Total views per category  
- Average likes per channel (Top 20)  
- Like-to-view percentage  
- Summary pivot tables  

---

##  Visualizations

The script generates several insightful visualizations, including:

- Bar charts  
- Horizontal bar charts  
- Line charts  
- Correlation heatmap  
- Word cloud of video titles  
- Treemap of views grouped by category  

All visual outputs appear automatically when running the script.

---

##  Technologies Used

- **Python**
- **Pandas**
- **NumPy**
- **Matplotlib**
- **Seaborn**
- **WordCloud**
- **Squarify**

---

##  How to Run the Project

1. Download the dataset (`USvideos.csv`) from the link above  
2. Place the dataset in the same directory as `main.py`  
3. Install required libraries if needed:
   
   pip install pandas numpy matplotlib seaborn wordcloud squarify

4. Run the script:
5. All charts, visualizations, and printed outputs will appear automatically.

---

## 📁 Project Structure
main.py
README.md


*(Dataset not included — download separately)*

---

##  Key Insights

- Entertainment and music categories generate significantly higher view counts.  
- Some channels consistently show high engagement in terms of likes and comments.  
- Clear relationships exist between views, likes, dislikes, and comment counts.  
- Visualizations reveal noticeable differences in performance across categories.  

---





