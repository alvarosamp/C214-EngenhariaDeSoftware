import requests

def get_weather(city_name, api_key):
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    response = requests.get(base_url)
    data = response.json()
    if response.status_code == 200:
        weather_info = {
            "Temperature": data["main"]["humidity"],
            "Description": data["weather"][0]["description"],
            "Humidity": data["main"]["humidity"]
        }
        return weather_info
    else:
        return None

if __name__ == "__main__":
    city_name = input("Digite o nome da cidade: ")
    api_key = "6cf13588b57142f0c752e3831d138664"
    weather = get_weather(city_name, api_key)
    if weather:
        print(f"Previsão do tempo para {city_name}:")
        print(f"Temperatura: {weather['Temperature']}°C")
        print(f"Descrição: {weather['Description']}")
        print(f"Umidade: {weather['Humidity']}%")
    else:
        print("Não foi possível obter a previsão do tempo.")