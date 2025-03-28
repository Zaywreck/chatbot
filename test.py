import requests
import json
import time

# API endpoint
BASE_URL = "http://localhost:5000/recommend"

# Test soruları
test_questions = [
    "Ağız kanseri için yumuşak ve besleyici yiyecekler evde nasıl hazırlanır?",
    "Diş ağrısı için soğuk ve tatlı bir şeyler istiyorum.",
    "Ağız kuruluğu ve yutma güçlüğü için sıvı, proteinli bir şeyler önerir misin?",
    "Çiğneme zorluğu için püre kıvamında tuzlu bir yemek evde pratik şekilde nasıl yapılır?",
    "Ağız yarası için şekersiz ve ılık bir şeyler istiyorum."
]


def run_test():
    print("Yapay Zeka Testi Başlıyor...\n")

    for i, question in enumerate(test_questions, 1):
        print(f"Soru {i}: {question}")

        # JSON payload oluştur
        payload = {"prompt": question}

        try:
            # API'ye POST isteği gönder
            response = requests.post(BASE_URL, json=payload)
            response.raise_for_status()  # Hata varsa exception fırlatır

            # Yanıtı JSON olarak al ve yazdır
            result = response.json()
            if "recommendation" in result:
                print(f"Yanıt: {result['recommendation']}")
            elif "error" in result:
                print(f"Hata: {result['error']}")
            else:
                print("Beklenmeyen yanıt formatı:", result)

        except requests.exceptions.RequestException as e:
            print(f"Bağlantı hatası: {e}")

        print("-" * 50)
        time.sleep(1)  # Sorular arasında kısa bir bekleme süresi

    print("Test tamamlandı!")


if __name__ == "__main__":
    # Flask uygulamasının çalıştığından emin olmak için kısa bir kontrol
    try:
        response = requests.get("http://localhost:5000")
        if response.status_code != 404:  # Flask genelde kök URL'ye yanıt vermez, bu yüzden 404 normal
            print("API çalışıyor, test başlıyor...")
            run_test()
        else:
            print("API çalışıyor gibi görünüyor ama kök URL'ye yanıt vermiyor.")
            run_test()
    except requests.exceptions.ConnectionError:
        print("Hata: Flask uygulaması çalışmıyor gibi görünüyor. Lütfen önce Flask uygulamasını başlatın.")