import json
import concurrent.futures
from jose import  jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, Dict
from django.contrib.auth.hashers import make_password, check_password
from dotenv import load_dotenv
import os
from app.database import engine_237
from sqlalchemy import text




load_dotenv()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

load_dotenv()
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    pbkdf2_sha256__default_rounds=720_000
)

def verify_password(password: str, hashed_password: str):
    return check_password(password, hashed_password)

def get_password_hash(password: str):
    return make_password(password)

def create_access_token(data: Dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"expires": expire.isoformat()})  # Convert datetime to ISO 8601 string

    secret_key = os.getenv("secret")
    algorithm = os.getenv("algorithm")

    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    
    return encoded_jwt




def run_procedure(server_ip: str, db_name: str, schema_name: str):
    procedure_query = f'''SELECT database_history.fn_gather_table_info_schema_test('{server_ip}', '{db_name}', '{schema_name}');'''

    with engine_237.connect() as conn:
        result = conn.execute(text(procedure_query))
        print(result.fetchall())
        return {
            "server_ip": server_ip,
            "db_name": db_name,
            "schema_name": schema_name,
            "result": result.fetchall(),
        }

# Prepare tasks for all servers, databases, and schemas
def prepare_tasks(existing_data):
    tasks = []
    for server_name, server_data in existing_data:
        # server_data_json = json.loads(server_data)
        for db_entry in server_data:
            for db_name, schemas in db_entry.items():
                for schema_name in schemas:
                    tasks.append((server_name, db_name, schema_name))
                    break
                break
            break
          
    return tasks

# Execute tasks in parallel
def execute_tasks_in_parallel(tasks):
    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_task = {
            executor.submit(run_procedure, server_ip, db_name, schema_name): (server_ip, db_name, schema_name)
            for server_ip, db_name, schema_name in tasks
        }
        
        for future in concurrent.futures.as_completed(future_to_task):
            task = future_to_task[future]
            try:
                data = future.result()
                results.append(data)
            except Exception as exc:
                print(f"Task {task} generated an exception: {exc}")
    
    return results

# Prepare and run the tasks
