import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest
from unittest.mock import patch, MagicMock
from api import get_weather
import requests

# Teste positivo: resposta válida da API
@patch('api.requests.get')
def test_get_weather_sucesso(mock_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "main": {"temp": 25, "humidity": 80},
        "weather": [{"description": "céu limpo"}]
    }
    mock_get.return_value = mock_resp
    resultado = get_weather("Belo Horizonte", "fake_api_key")
    assert resultado == {
        "Temperature": 25,
        "Description": "céu limpo",
        "Humidity": 80
    }

# Teste negativo: status code diferente de 200
@patch('api.requests.get')
def test_get_weather_falha_status(mock_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 404
    mock_resp.json.return_value = {}
    mock_get.return_value = mock_resp
    resultado = get_weather("CidadeInvalida", "fake_api_key")
    assert resultado is None

# Teste negativo: resposta incompleta
@patch('api.requests.get')
def test_get_weather_resposta_incompleta(mock_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"main": {}, "weather": [{}]}
    mock_get.return_value = mock_resp
    with pytest.raises(KeyError):
        get_weather("Cidade", "fake_api_key")

# Teste negativo: cidade inexistente
@patch('api.requests.get')
def test_get_weather_cidade_inexistente(mock_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 404
    mock_resp.json.return_value = {"message": "city not found"}
    mock_get.return_value = mock_resp
    resultado = get_weather("CidadeQueNaoExiste", "fake_api_key")
    assert resultado is None

# Teste negativo: API key inválida
@patch('api.requests.get')
def test_get_weather_api_key_invalida(mock_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 401
    mock_resp.json.return_value = {"message": "Invalid API key"}
    mock_get.return_value = mock_resp
    resultado = get_weather("Belo Horizonte", "chave_invalida")
    assert resultado is None

# Teste negativo: resposta sem campo weather
@patch('api.requests.get')
def test_get_weather_sem_weather(mock_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"main": {"temp": 20, "humidity": 50}}
    mock_get.return_value = mock_resp
    with pytest.raises(KeyError):
        get_weather("Cidade", "fake_api_key")

# Teste negativo: resposta sem campo main
@patch('api.requests.get')
def test_get_weather_sem_main(mock_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"weather": [{"description": "nublado"}]}
    mock_get.return_value = mock_resp
    with pytest.raises(KeyError):
        get_weather("Cidade", "fake_api_key")

# Teste negativo: tipos errados nos campos
@patch('api.requests.get')
def test_get_weather_tipos_errados(mock_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"main": {"temp": "vinte", "humidity": "cinquenta"}, "weather": [{"description": 123}]}
    mock_get.return_value = mock_resp
    resultado = get_weather("Cidade", "fake_api_key")
    assert isinstance(resultado["Temperature"], str)
    assert isinstance(resultado["Description"], int)

# Teste negativo: resposta lenta (timeout)
@patch('api.requests.get')
def test_get_weather_timeout(mock_get):
    mock_get.side_effect = requests.exceptions.Timeout
    with pytest.raises(requests.exceptions.Timeout):
        get_weather("Cidade", "fake_api_key")
