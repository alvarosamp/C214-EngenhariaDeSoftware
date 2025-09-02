import sys
import os
import pytest
from unittest.mock import MagicMock
import requests

# Adiciona o diretório atual ao sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from api import get_weather  # Importa depois do sys.path

# --- FIXTURE PARA MOCK DE requests.get ---
@pytest.fixture
def mock_requests_get(monkeypatch):
    def _mock_get(mock_resp):
        def fake_get(*args, **kwargs):
            return mock_resp
        monkeypatch.setattr("requests.get", fake_get)
    return _mock_get

# --- TESTES ---

def test_get_weather_sucesso(mock_requests_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "main": {"temp": 25, "humidity": 80},
        "weather": [{"description": "céu limpo"}]
    }
    mock_requests_get(mock_resp)
    resultado = get_weather("Belo Horizonte", "fake_api_key")
    assert resultado == {
        "Temperature": 25,
        "Description": "céu limpo",
        "Humidity": 80
    }

def test_get_weather_falha_status(mock_requests_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 404
    mock_resp.json.return_value = {}
    mock_requests_get(mock_resp)
    resultado = get_weather("CidadeInvalida", "fake_api_key")
    assert resultado is None

def test_get_weather_resposta_incompleta(mock_requests_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"main": {}, "weather": [{}]}
    mock_requests_get(mock_resp)
    with pytest.raises(KeyError):
        get_weather("Cidade", "fake_api_key")

def test_get_weather_cidade_inexistente(mock_requests_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 404
    mock_resp.json.return_value = {"message": "city not found"}
    mock_requests_get(mock_resp)
    resultado = get_weather("CidadeQueNaoExiste", "fake_api_key")
    assert resultado is None

def test_get_weather_api_key_invalida(mock_requests_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 401
    mock_resp.json.return_value = {"message": "Invalid API key"}
    mock_requests_get(mock_resp)
    resultado = get_weather("Belo Horizonte", "chave_invalida")
    assert resultado is None

def test_get_weather_sem_weather(mock_requests_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"main": {"temp": 20, "humidity": 50}}
    mock_requests_get(mock_resp)
    with pytest.raises(KeyError):
        get_weather("Cidade", "fake_api_key")

def test_get_weather_sem_main(mock_requests_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"weather": [{"description": "nublado"}]}
    mock_requests_get(mock_resp)
    with pytest.raises(KeyError):
        get_weather("Cidade", "fake_api_key")

def test_get_weather_tipos_errados(mock_requests_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "main": {"temp": "vinte", "humidity": "cinquenta"},
        "weather": [{"description": 123}]
    }
    mock_requests_get(mock_resp)
    resultado = get_weather("Cidade", "fake_api_key")
    assert isinstance(resultado["Temperature"], str)
    assert isinstance(resultado["Description"], int)

def test_get_weather_timeout(monkeypatch):
    def fake_get(*args, **kwargs):
        raise requests.exceptions.Timeout
    monkeypatch.setattr("requests.get", fake_get)
    with pytest.raises(requests.exceptions.Timeout):
        get_weather("Cidade", "fake_api_key")

# --- TESTES POSITIVOS ADICIONAIS ---

def test_get_weather_temp_negativa(mock_requests_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "main": {"temp": -5, "humidity": 60},
        "weather": [{"description": "neve"}]
    }
    mock_requests_get(mock_resp)
    resultado = get_weather("Moscou", "fake_api_key")
    assert resultado == {
        "Temperature": -5,
        "Description": "neve",
        "Humidity": 60
    }

def test_get_weather_humidity_zero(mock_requests_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "main": {"temp": 30, "humidity": 0},
        "weather": [{"description": "seco"}]
    }
    mock_requests_get(mock_resp)
    resultado = get_weather("Deserto", "fake_api_key")
    assert resultado == {
        "Temperature": 30,
        "Description": "seco",
        "Humidity": 0
    }

def test_get_weather_description_unicode(mock_requests_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "main": {"temp": 18, "humidity": 90},
        "weather": [{"description": "chuva ☔"}]
    }
    mock_requests_get(mock_resp)
    resultado = get_weather("CidadeUnicode", "fake_api_key")
    assert resultado == {
        "Temperature": 18,
        "Description": "chuva ☔",
        "Humidity": 90
    }

# --- TESTES NEGATIVOS ADICIONAIS ---

def test_get_weather_main_none(mock_requests_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "main": None,
        "weather": [{"description": "nublado"}]
    }
    mock_requests_get(mock_resp)
    with pytest.raises(TypeError):
        get_weather("Cidade", "fake_api_key")

def test_get_weather_weather_none(mock_requests_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "main": {"temp": 22, "humidity": 70},
        "weather": None
    }
    mock_requests_get(mock_resp)
    with pytest.raises(TypeError):
        get_weather("Cidade", "fake_api_key")

def test_get_weather_weather_empty_list(mock_requests_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "main": {"temp": 22, "humidity": 70},
        "weather": []
    }
    mock_requests_get(mock_resp)
    with pytest.raises(IndexError):
        get_weather("Cidade", "fake_api_key")

def test_get_weather_json_raises_exception(monkeypatch):
    class FakeResp:
        status_code = 200
        def json(self):
            raise ValueError("Erro ao decodificar JSON")
    def fake_get(*args, **kwargs):
        return FakeResp()
    monkeypatch.setattr("requests.get", fake_get)
    with pytest.raises(ValueError):
        get_weather("Cidade", "fake_api_key")
