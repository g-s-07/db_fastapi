import json
import re
from app.auth.auth_bearer import JWTBearer
from app.models import ServerMetadata, ServerMetadataLogs
from sqlalchemy.orm import Session
from sqlalchemy import func, text, update
from app.database import get_db_1, get_db_2, get_db_3, create_engine
from fastapi import APIRouter, Depends
import pandas as pd,os
from sqlalchemy.dialects.postgresql import insert
from typing import List
from helpers.utility import execute_tasks_in_parallel, prepare_tasks


router = APIRouter()


@router.post("/server-data/", dependencies=[Depends(JWTBearer())], tags=["server_237"])
def add_server_metadata(db_1: Session = Depends(get_db_1), db_2: Session = Depends(get_db_2), db_3: Session = Depends(get_db_3)):
    all_db_query = '''SELECT datname FROM pg_database WHERE datistemplate = false ORDER BY datname;'''
    all_schema_query = '''SELECT schema_name FROM information_schema.schemata WHERE schema_name NOT LIKE 'pg_%' AND schema_name != 'information_schema' ORDER BY schema_name;'''

    def get_database_and_schemas(db: Session, server_ip: str) -> List[dict]:
        db_names = db.execute(text(all_db_query)).fetchall()
        db_names = [db_name[0] for db_name in db_names]
        db_schemas = []
        changes = []


        existing_server_ip = db_1.query(ServerMetadata).filter(ServerMetadata.server_name == server_ip).first()
        if existing_server_ip:
            server_data_json = existing_server_ip.server_data
            if isinstance(server_data_json, str):
                server_data_json = json.loads(server_data_json)
        else:
            server_data_json = []


        existing_db_names = {list(item.keys())[0] for item in server_data_json}
        deleted_databases = existing_db_names - set(db_names)
        if deleted_databases:
            for db_name in deleted_databases:
                server_data_json = [item for item in server_data_json if list(item.keys())[0] != db_name]
                changes.append({
                    "log": f"Database {db_name} was deleted from server {server_ip}"
                })


        for db_name in db_names:
            db_url_with_db = f"postgresql://{os.getenv('DB_CONFIG_237_USER')}:{os.getenv('DB_CONFIG_237_PASSWORD')}@{server_ip}:{os.getenv('DB_CONFIG_237_PORT')}/{db_name}"
            engine = create_engine(db_url_with_db)
            with engine.connect() as conn:
                result = conn.execute(text(all_schema_query))
                schema_names = [schema[0] for schema in result.fetchall()]

            existing_db = next((item for item in server_data_json if db_name in item), None)
            if existing_db:
                existing_schemas = existing_db[db_name]
                new_schemas = set(schema_names) - set(existing_schemas)
                deleted_schemas = set(existing_schemas) - set(schema_names)

                if new_schemas:
                    existing_db[db_name].extend(new_schemas)
                    changes.append({
                        "log": f"New schemas added to database {db_name}: {new_schemas} on server {server_ip}"
                    })
                if deleted_schemas:
                    existing_db[db_name] = [schema for schema in existing_db[db_name] if schema not in deleted_schemas]
                    changes.append({
                        "log": f"Schemas deleted from database {db_name}: {deleted_schemas} on server {server_ip}"
                    })
            else:
                server_data_json.append({db_name: schema_names})
                changes.append({
                    "log": f"New database {db_name} with schemas {schema_names} added to server {server_ip}"
                })


        db_1.execute(
            update(ServerMetadata)
            .where(ServerMetadata.server_name == server_ip)
            .values(server_data=server_data_json, updated_at=func.now())
        )
        db_1.commit()

        return changes


    all_changes = []
    all_changes.extend(get_database_and_schemas(db_1, os.getenv('DB_CONFIG_237_HOST')))
    all_changes.extend(get_database_and_schemas(db_2, os.getenv('DB_CONFIG_236_HOST')))
    all_changes.extend(get_database_and_schemas(db_3, os.getenv('DB_CONFIG_243_HOST')))


    if all_changes:
        changes_log = insert(ServerMetadataLogs).values(
            server_logs=[{"log": json.dumps(all_changes)}]
        )
        db_1.execute(changes_log)
        db_1.commit()
    else:
        no_changes_found = insert(ServerMetadataLogs).values(
            server_logs=[{"log": "No changes in databases or schemas on the servers"}]
        )
        db_1.execute(no_changes_found)
        db_1.commit()
        

    
    existing_server_data = db_1.query(ServerMetadata.server_name, ServerMetadata.server_data).all()
    tasks = prepare_tasks(existing_server_data)
    print(tasks)
    all_results = execute_tasks_in_parallel(tasks)
    print("done")
    
    
    
    
    

    # return {"databases_and_schemas": all_changes}
