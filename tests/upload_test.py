from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))
from app import app

client = TestClient(app)

def test_upload_files_success():
    files = {'files': ('test_file.txt', b'conteudo do arquivo')}
    response = client.post("/s3/upload?user_id=testuser", files=files)

    assert response.status_code == 200
    assert "message" in response.json()
    assert "files" in response.json()
    assert len(response.json()['files']) > 0

def test_upload_files_without_files():

    response = client.post("/s3/upload?user_id=testuser")
    
    assert response.status_code == 422
    
