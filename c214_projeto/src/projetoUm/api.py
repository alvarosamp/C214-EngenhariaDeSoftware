import requests

# Exemplo: API pública de piadas
url = "https://official-joke-api.appspot.com/random_joke"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print(f"{data['setup']} - {data['punchline']}")
else:
    print("Erro ao acessar a API:", response.status_code)