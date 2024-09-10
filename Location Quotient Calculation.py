import pandas as pd


df = pd.read_excel('D:/gisdata/canal/final/analysis/modern/classify/modern_R20.xlsx')


total_city = df['log_Count_mail'].sum() + df['log_Count_tem'].sum() + df['log_Count_rest'].sum() + df['log_Count_tour'].sum() + df['log_Count_shopping'].sum() + df['log_Count_cul'].sum() + df['log_Count_living'].sum() + df['log_Count_hosp'].sum() + df['log_Count_govern'].sum()


df['Total'] = df['log_Count_mail'] + df['log_Count_tem'] + df['log_Count_rest'] + df['log_Count_tour'] + df['log_Count_shopping'] + df['log_Count_cul'] + df['log_Count_living'] + df['log_Count_hosp'] + df['log_Count_govern']

df['LQ_MAI'] = (df['log_Count_mail'] / df['Total']) / (df['log_Count_mail'].sum() / total_city)
df['LQ_TEM'] = (df['log_Count_tem'] / df['Total']) / (df['log_Count_tem'].sum() / total_city)
df['LQ_REST'] = (df['log_Count_rest'] / df['Total']) / (df['log_Count_rest'].sum() / total_city)
df['LQ_TOUR'] = (df['log_Count_tour'] / df['Total']) / (df['log_Count_tour'].sum() / total_city)
df['LQ_SHOPPING'] = (df['log_Count_shopping'] / df['Total']) / (df['log_Count_shopping'].sum() / total_city)
df['LQ_CUL'] = (df['log_Count_cul'] / df['Total']) / (df['log_Count_cul'].sum() / total_city)
df['LQ_LIVING'] = (df['log_Count_living'] / df['Total']) / (df['log_Count_living'].sum() / total_city)
df['LQ_HOS'] = (df['log_Count_hosp'] / df['Total']) / (df['log_Count_hosp'].sum() / total_city)
df['LQ_GOV'] = (df['log_Count_govern'] / df['Total']) / (df['log_Count_govern'].sum() / total_city)


df['Max_LQ_Type'] = df[['LQ_MAI', 'LQ_TEM', 'LQ_REST', 'LQ_TOUR', 'LQ_SHOPPING', 'LQ_CUL', 'LQ_LIVING', 'LQ_HOS', 'LQ_GOV']].idxmax(axis=1)


df['Max_LQ_Type'] = df['Max_LQ_Type'].map({
    'LQ_MAI': 'type1',
    'LQ_TEM': 'type2',
    'LQ_REST': 'type3',
    'LQ_TOUR': 'type4',
    'LQ_SHOPPING': 'type5',
    'LQ_CUL': 'type6',
    'LQ_LIVING': 'type7',
    'LQ_HOS': 'type8',
    'LQ_GOV': 'type9',
})


df.to_excel('modern_lq.xlsx', index=False)