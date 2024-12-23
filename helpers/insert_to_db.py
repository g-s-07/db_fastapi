import psycopg2
from psycopg2 import sql
import json,os
# DATABASE = os.getenv('DATABASE_LOGS')
# ENDPOINT_2 = os.getenv('DB_CONFIG_43_HOST')  
# USER_2 = os.getenv('DB_CONFIG_43_USER')
# PASSWORD_2 = os.getenv('DB_CONFIG_43_PASSWORD')
# PORT_2 = os.getenv('DB_CONFIG_43_PORT')
# import os
# from dotenv import load_dotenv
# load_dotenv()
def insert_log(payload,DATABASE,USER_2,PASSWORD_2,ENDPOINT_2,PORT_2, status=0):
    conn = psycopg2.connect(
        dbname=DATABASE,
        user=USER_2,
        password=PASSWORD_2,
        host=ENDPOINT_2,
        port = PORT_2
    )
    try:
        with conn.cursor() as cursor:
            if status is None:
                insert_query = """
                INSERT INTO public.amazon_extraction_logs (payload)
                VALUES (%s)
                """
                cursor.execute(insert_query, (json.dumps(payload),))
            else:
                insert_query = """
                INSERT INTO public.amazon_extraction_logs (payload, status)
                VALUES (%s, %s)
                """
                cursor.execute(insert_query, (json.dumps(payload), status))
            
            conn.commit()
            msg = "Data inserted successfully."
            print(msg)
            return msg
    except Exception as e:
        print(f"Error in inserting data: {e}")
        conn.rollback()
        return e
    finally:
        conn.close()

if __name__ == "__main__":
    sample_payload = {'product_list': {'task_id': 1002, 'total_count': 1584 , 'processed_count': 691, 'extracted_count': 1539127, 'pending_count': 862, 'missed_count': 31, 'previous_count': 'N/A', 'inserted_count': 'N/A'}, 'product_details': {'task_id': 1002, 'total_count': 139891, 'processed_count': 100289, 'extracted_count': 100289, 'pending_count': 39247, 'missed_count': 351, 'previous_count': 139891, 'inserted_count': 0}, 'seller_details': {'task_id': 1002, 'total_count': 13861, 'processed_count': 13798, 'extracted_count': 13796, 'pending_count': 60, 'missed_count': 3, 'previous_count': 13798, 'inserted_count': 64}}    
    insert_log(sample_payload)

