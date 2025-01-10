from fastapi import APIRouter, File, UploadFile, HTTPException
import boto3
from botocore.exceptions import ClientError
from config import BUCKET_NAME

s3_router = APIRouter(
    prefix="/s3",
    tags=["AWS S3"]
)

def get_s3_client():
    """
    Retorna o cliente S3. Pode ser configurado para ambientes diferentes.
    """
    return boto3.client('s3', region_name='us-east-2')

s3_client = get_s3_client()

def generate_presigned_url(file_name: str, expiration: int = 3600):
    """
    Gera uma URL pré-assinada para acesso temporário ao arquivo no S3.
    - file_name: Chave do arquivo no S3.
    - expiration: Tempo de validade da URL em segundos.
    """
    try:
        print(f"Gerando URL pré-assinada para o arquivo: {file_name}")
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': file_name},
            ExpiresIn=expiration
        )
        print(f"URL pré-assinada gerada com sucesso para o arquivo: {file_name}")
        return response
    except ClientError as e:
        print(f"Erro ao gerar URL pré-assinada para o arquivo: {file_name} - Erro: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao gerar link pré-assinado: {e}")

@s3_router.post("/upload")
async def upload_files(
    files: list[UploadFile] = File(...), 
    user_id: str = ""
):
    """
    Endpoint para upload de múltiplos arquivos.
    - user_id: Identificador do usuário ou "anonymous_id".
    """
    print(f"Recebendo upload de {len(files)} arquivo(s) para o usuário: {user_id}")
    file_details = []
    
    for file in files:
        file_content = await file.read()
        file_name = f"{user_id}/{file.filename}"
        print(f"Preparando upload do arquivo: {file_name}")

        try:
            s3_client.put_object(Bucket=BUCKET_NAME, Key=file_name, Body=file_content)
            print(f"Arquivo {file_name} enviado com sucesso para o bucket {BUCKET_NAME}")

            presigned_url = generate_presigned_url(file_name)
            file_details.append({
                "file_name": file_name,
                "presigned_url": presigned_url
            })
            print(f"URL pré-assinada gerada para o arquivo: {file_name}")

        except ClientError as e:
            print(f"Erro ao enviar o arquivo {file.filename} para o bucket {BUCKET_NAME} - Erro: {e}")
            raise HTTPException(status_code=500, detail=f"Erro ao enviar arquivo {file.filename}: {e}")

    print(f"Upload concluído com sucesso para o usuário: {user_id}")
    return {
        "message": "Arquivos enviados com sucesso!",
        "files": file_details,
    }

@s3_router.get("/uploads/{user_id}")
def get_uploads(user_id: str):
    """
    Lista os uploads de um usuário, incluindo URLs pré-assinadas.
    """
    print(f"Buscando uploads para o usuário: {user_id}")
    try:
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=f"{user_id}/")
        if "Contents" not in response:
            print(f"Nenhum arquivo encontrado para o usuário: {user_id}")
            return {"message": "Nenhum arquivo encontrado."}

        files = response["Contents"]
        print(f"{len(files)} arquivo(s) encontrado(s) para o usuário: {user_id}")
        file_details = [
            {
                "file_name": file["Key"],
                "presigned_url": generate_presigned_url(file["Key"])
            }
            for file in files
        ]

        print(f"URLs pré-assinadas geradas para os arquivos do usuário: {user_id}")
        return {"files": file_details}
    except ClientError as e:
        print(f"Erro ao listar arquivos para o usuário: {user_id} - Erro: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao listar arquivos: {e}")

@s3_router.delete("/delete/{user_id}/{file_name}")
def delete_file(user_id: str, file_name: str):
    try:
        file_key = f"{user_id}/{file_name}"

        s3_client.delete_object(Bucket=BUCKET_NAME, Key=file_key)

        return {"message": f"Arquivo {file_name} deletado com sucesso."}
    except Exception as e:

        raise HTTPException(status_code=500, detail="Erro inesperado.")

