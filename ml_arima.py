import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

def get_ml_arima(gelecek_adim_sayisi,veriler):
    # Verileri pandas serisine dönüştürme
    veri_serisi = pd.Series(veriler)

    # ARIMA modelini eğitme
    model = ARIMA(veri_serisi, order=(1, 1, 1))
    model_fit = model.fit()

    # Gelecekteki değerleri tahmin etme
    gelecek_adim_sayisi = 90  # Tahmin etmek istediğimiz adım sayısı
    tahminler = model_fit.forecast(steps=gelecek_adim_sayisi)
    tahminler = tahminler.to_list()

    return tahminler[len(tahminler) - 1]
