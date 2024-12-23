import pandas as pd
import json

input_file = "all_server_db_schema.csv"

data = pd.read_csv(input_file)

result = []
for server_name, group in data.groupby("server_name"):
    server_data = []
    for db_name, sub_group in group.groupby("server_data"):
        schemas = sub_group["schema"].tolist()
        server_data.append({db_name: schemas})
    result.append(
        {
            "server_name": str(server_name), 
            "server_data": json.dumps(server_data),
            # "created_at": func.now(),
            # "updated_at": func.now()
        }
    )

output_df = pd.DataFrame(result)

output_file = "output1.csv"
output_df.to_csv(output_file, index=False)

print("Processed data saved to", output_file)
