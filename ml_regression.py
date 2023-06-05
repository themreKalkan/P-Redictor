import numpy as np
from sklearn.linear_model import LinearRegression


def calculate_lineer(gelecek_gunler,veriler):
    dolar_verileri = np.array(veriler)
    y = dolar_verileri.reshape(-1, 1)
    # X ve y değerlerini ayarlayın
    X = np.arange(1, len(dolar_verileri) + 1).reshape(-1, 1)  # Bağımsız değişkenler (1'den N'ye kadar sayılar)
    # Bağımlı değişkenler (dolar değerleri)

    # Lineer regresyon modelini oluşturun ve eğitin
    model = LinearRegression()
    model.fit(X, y)

    # Gelecekteki tahminler için yeni X değerleri oluşturun

    X_gelecek = np.arange(len(dolar_verileri) + 1, len(dolar_verileri) + 1 + gelecek_gunler).reshape(-1, 1)

    # Gelecekteki dolar tahminlerini yapın
    dolar_tahminleri = model.predict(X_gelecek)

    # Sonuçları yazdırın
    for i, tahmin in enumerate(dolar_tahminleri):
        gun = len(dolar_verileri) + i + 1
        if(i == gelecek_gunler-1):
            return tahmin[0]
