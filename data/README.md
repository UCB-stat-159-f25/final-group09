# Data Directory

## Files

### Raw Data
- `CDC_drug_overdose_deaths_raw_data.csv` - Original CDC data on drug overdose deaths (1999-2018)

### Processed Data  
- `overdose_age_data_clean.csv` - Cleaned data filtered by age groups
- `overdose_race_data_clean.csv` - Cleaned data filtered by race/ethnicity

### Data Processing
- `LoadOverdoseData.ipynb` - Notebook that downloads, cleans, and processes the raw CDC data

## Data Source
National Center for Health Statistics, CDC. Drug overdose deaths in the United States, 1999-2018.

## Data Description
The dataset contains drug overdose death rates per 100,000 population, categorized by:
- Drug type (all drugs, opioids, heroin, synthetic opioids, methadone)
- Demographics (sex, age group, race/Hispanic origin)  
- Time period (1999-2018)
