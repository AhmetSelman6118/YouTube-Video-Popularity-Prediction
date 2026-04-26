import pandas as pd
import os

def remove_outliers_iqr(df, column):
   
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    initial_count = len(df)
    df_filtered = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
    
    removed_count = initial_count - len(df_filtered)
    if removed_count > 0:
        print(f"{column} sütununda {removed_count} adet aykırı değer silindi.")
    
    return df_filtered

def run_preprocessing(input_file="data/raw/youtube_data.csv"):
    """
    Ham veriyi okur, temizler ve işlenmiş klasörüne kaydeder.
    """
    if not os.path.exists(input_file):
        print(f"Hata: {input_file} dosyası bulunamadı!")
        return

    df = pd.read_csv(input_file)
    print(f"İşlem öncesi veri sayısı: {len(df)}")

    df = df.dropna(subset=['view_count', 'like_count', 'comment_count'])

    df = remove_outliers_iqr(df, 'view_count')
    df = remove_outliers_iqr(df, 'like_count')

    os.makedirs("data/processed", exist_ok=True)
    output_path = "data/processed/youtube_data_cleaned.csv"
    df.to_csv(output_path, index=False)
    
    print(f"Temizlenmiş veri kaydedildi: {output_path}")
    print(f"Final veri seti boyutu: {len(df)}")
    return df

if __name__ == "__main__":
    run_preprocessing()