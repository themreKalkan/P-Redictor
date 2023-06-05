import yfinance as yf
import pandas
from datetime import datetime
import ml_regression
import ml_arima

anlik_tarih = datetime.now()
yil = anlik_tarih.year
ay = anlik_tarih.month
gun = anlik_tarih.day

last_date = str(yil)+"-"+str(ay)+"-"+str(gun)

# Verileri çekmek istediğiniz sembolü belirleyin
sembol = str(input("Hisse: "))
sembol = sembol+".IS"

print("Tarihi Girin (YIL-AY-GÜN)")
st_date = str(input(": "))

veriler = yf.download(sembol, start=st_date, end=last_date)
#print(veriler.head())
final_datas = veriler.values.tolist()
#print(len(final_datas))
#print(final_datas[len(final_datas)-1])

def get_now():
    return final_datas[len(final_datas)-1][3]

def get_strt():
    return final_datas[0][3]

def get_high():
    max_value = float("-INF")
    for hgh in final_datas:
        if hgh[1] > max_value:
            max_value = float(hgh[1])
    return max_value

def get_low():
    min_value = float("INF")
    for lww in final_datas:
        if lww[2] < min_value:
            min_value = float(lww[2])
    return min_value

def get_pp():
    lowest = get_low()
    highest = get_high()
    now = get_now()
    return (highest+lowest+now)/3

def get_volume_now():
    return final_datas[len(final_datas) - 1][5]

def get_volume_low():
    min_value = float("INF")
    for lww in final_datas:
        if lww[5] < min_value:
            min_value = float(lww[5])
    return min_value

def get_volume_high():
    max_value = float("-INF")
    for hgh in final_datas:
        if hgh[5] > max_value:
            max_value = float(hgh[5])
    return max_value

def get_volume_med():
    med_value = 0
    for hgh in final_datas:
        med_value = med_value+hgh[5]

    return med_value/len(final_datas)

def get_general_volume():
    start_value = final_datas[0][5]
    final_value = final_datas[len(final_datas)-1][5]
    return ((final_value-start_value)/start_value)*100

def get_daily_trend():
    gen_trend = 0
    for fnn in final_datas:
        temp_trend = ((fnn[3]-fnn[0])/fnn[0])*100
        gen_trend = gen_trend+temp_trend
    return gen_trend/len(final_datas)

def get_daily_volume():
    gen_vol = 0
    for i in range(len(final_datas)):
        if(i == len(final_datas)-1):
            return gen_vol/len(final_datas)

        temp_vol = ((final_datas[i+1][5]-final_datas[i][5])/final_datas[i][5])*100
        gen_vol = gen_vol+temp_vol

def get_res1():
    return (2*get_pp())-get_low()

def get_supp1():
    return (2*get_pp())-get_high()

def get_res2():
    return get_pp()+(get_high()-get_low())

def get_supp2():
    return get_pp()-(get_high()-get_low())


def get_general_trend():
    start_value = get_strt()
    final_value = get_now()
    return ((final_value-start_value)/start_value)*100

def get_data_close():
    new_datas = []
    for gnn in final_datas:
        new_datas.append(gnn[3])
    return new_datas


print("Makine Öğrenmesi ile tahmin edilecek gün sayısını girin")
pred_day = int(input(": "))
prediction_data = ml_regression.calculate_lineer(pred_day*1,veriler=get_data_close())
prediction_data2 = ml_arima.get_ml_arima(pred_day*100,veriler=get_data_close())
print(prediction_data2)
def get_topic_point():
    now_data = get_now()
    strt_data = get_strt()
    high_data = get_high()
    low_data = get_low()
    main_point = 0
    lop_data = ((now_data-strt_data)/strt_data)*100
    if(lop_data > 0):
        main_point = main_point+1

    if(get_volume_med() < get_volume_now()):
        main_point = main_point+1

    if(get_general_volume() > 0):
        main_point = main_point+1

    if(get_daily_trend() > 0):
        main_point = main_point+1

    if(get_daily_volume() > 0):
        main_point = main_point+1

    if(get_general_trend() > 0):
        main_point = main_point+1

    if(prediction_data > now_data):
        main_point = main_point+1

    if(((get_res1()-now_data)/now_data)*100 < 20):
        main_point = main_point+1

    if (((get_supp1() - now_data) / now_data) * 100 > 20):
        main_point = main_point + 1


    return (main_point/9)*100


print("Hissede:")
print("Pivot: ",get_pp())
print("İlk Direnç: ",get_res1())
print("İlk Destek: ",get_supp1())
print("Mevcut Hisse Fiyatı: ",get_now())
print("Hisse Hacmi: ",get_volume_now())
print("Ortalama Hisse Hacmi: ",get_volume_med())
print("Günlük Trend Değerleri: ",get_daily_trend())
print("Genel Trend Değerleri: ",get_general_trend())
print("Yorumlar: ")
shft_data = (prediction_data+prediction_data2)/2
print(f"Sonraki {pred_day} gün içinde hissenin fiyatının en düşük {prediction_data} ile {shft_data} arasında olması bekleniyor.")
new_predict = prediction_data2 *(((get_topic_point())/10)+100)/100
print(f"Beklenen ortalama değer {new_predict} olarak hesaplanmıştır.")
print(f"Bu hisseyi Yüzde(%) {get_topic_point()} oranla almanız tavsiye ediliyor.")
print(" ")
print("----------------------!!!!!!!!----------------------")
print("Oranlar ve fiyatlar hesaplanırken girdiğiniz tarihten itibaren günümüze kadar olan veriler kullanılır.")
print("Bu verilere Pivot Hesaplamaları, Tavan-Taban Değerler, Hissenin Hacim Değerleri, Hissenin Trendine Dair Hesaplamaları dahildir")

