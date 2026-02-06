# Fragrance Analytics Dashboard 🧴

An interactive dashboard for analyzing the Fragrantica.com Fragrance Dataset from Kaggle.

## Features

- **Overview Analytics**: Rating distribution, gender categories, and rating/review analysis
- **Ratings Analysis**: Detailed statistics, top-rated fragrances, and most-reviewed products
- **Top Brands**: Brand popularity and average ratings
- **Geographic Distribution**: Country-based fragrance analysis
- **Notes Analysis**: Most common fragrance notes (top, middle, base) and main accords

## Dataset

Download the **Fragrantica.com Fragrance Dataset** from Kaggle:
- [Dataset Link](https://www.kaggle.com/datasets/olgagmiufana1/fragrantica-com-fragrance-dataset)
- Download the `fra_cleaned.csv` file
- Place it in the project directory (same folder as `app.py`)

## Setup Instructions

### 1. Install Python (if not already installed)
- Download from [python.org](https://www.python.org/)
- Ensure Python 3.8+ is installed

### 2. Install Dependencies

Open PowerShell in the project folder and run:

```powershell
pip install -r requirements.txt
```

### 3. Download the Dataset

1. Go to [Kaggle Dataset Page](https://www.kaggle.com/datasets/olgagmiufana1/fragrantica-com-fragrance-dataset)
2. Download `fra_cleaned.csv`
3. Place the file in: `c:\Users\EK\Desktop\data viz project\`

### 4. Run the Dashboard

```powershell
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`

## Features Included

- 📊 **5 Main Tabs**:
  - Overview: High-level statistics and visualizations
  - Ratings Analysis: Detailed rating insights
  - Top Brands: Brand performance metrics
  - Geographic: Country-based analysis
  - Notes Analysis: Fragrance composition insights

- 🔍 **Interactive Filters**:
  - Filter by brand, country, and gender
  - Real-time dashboard updates

- 📈 **Visualizations**:
  - Interactive charts and graphs
  - Scatter plots, bar charts, histograms, and pie charts
  - Data tables with sortable columns

## File Structure

```
data viz project/
├── app.py              # Main dashboard application
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── fra_cleaned.csv    # Dataset (download from Kaggle)
```

## Requirements

- Python 3.8+
- Streamlit
- Pandas
- Plotly
- NumPy

## Troubleshooting

**Dataset not found error?**
- Ensure `fra_cleaned.csv` is in the same directory as `app.py`
- Check the file name is exactly `fra_cleaned.csv` (case-sensitive on some systems)

**Module not found error?**
- Run `pip install -r requirements.txt` again
- Ensure you're in the correct project directory

## License

Data sourced from Kaggle under CC BY-NC-SA 4.0 license.

---

Enjoy exploring the fragrance data! 🌸
