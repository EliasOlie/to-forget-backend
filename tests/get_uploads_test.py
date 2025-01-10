from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))
from app import app  # Altere para o nome do seu módulo

client = TestClient(app)

def test_get_uploads_success():
    files = {'files': ('test_file.txt', b'conteudo do arquivo')}
    response = client.post("/s3/upload?user_id=testuser_permanent", files=files)
    
    response = client.get("/s3/uploads/testuser_permanent")
    assert response.status_code == 200
    assert "files" in response.json()

def test_get_uploads_no_files():
    response = client.get("/s3/uploads/empty_test_user")
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "Nenhum arquivo encontrado."