import requests

# Exemplo: API pública de piadas
url = "https://official-joke-api.appspot.com/random_joke"


def teste_1():
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print(f"{data['setup']} - {data['punchline']}")
    else:
        print("Erro ao acessar a API:", response.status_code)

def testar_2():
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "setup" in data and "punchline" in data:
            print("✅ Teste passou: API retornou piada válida.")
        else:
            print("❌ Teste falhou: resposta não contém os campos esperados.")
    else:
        print("❌ Teste falhou: erro ao acessar API. Status:", response.status_code)


teste_1()
testar_2()