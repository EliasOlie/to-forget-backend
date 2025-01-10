from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))
from app import app  # Altere para o nome do seu módulo

client = TestClient(app)

def test_delete_file_success():
    # Testa a deleção de um arquivo existente
    response = client.delete("/s3/delete/testuser/test_file.txt")
    
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()['message'] == "Arquivo test_file.txt deletado com sucesso."
    
def test_delete_file_not_found():
    # Testa a tentativa de deletar um arquivo que não existe
    # A AWS retorna 200 mesmo que o arquivo não exista, so não retorna
    # 200 caso dê algum error
    response = client.delete("/s3/delete/testuser/non_existent_file.txt")
    
    assert response.status_code == 200  # Arquivo não encontrado
    assert "Arquivo" in response.json()['message']
    