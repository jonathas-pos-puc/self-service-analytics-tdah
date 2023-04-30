from google.cloud import bigquery

def get_schemas_from_bigquery(project_id, dataset_name):
    client = bigquery.Client(project=project_id)
    dataset_ref = client.dataset(dataset_name)
    tables = list(client.list_tables(dataset_ref))

    schemas = {}
    for table in tables:
        table_ref = dataset_ref.table(table.table_id)
        table_obj = client.get_table(table_ref)
        schemas[table.table_id] = table_obj.schema

    return schemas

def schema_to_dbdiagram(schema, table_name):
    lines = [f"Table {table_name} {{"]

    for field in schema:
        field_name = field.name
        field_type = str(field.field_type).replace("FieldType.", "")
        lines.append(f"  {field_name} {field_type}")

    lines.append("}")
    return "\n".join(lines)

def generate_dbdiagram_code(schemas):
    return "\n\n".join(schema_to_dbdiagram(schema, table_name) for table_name, schema in schemas.items())

if __name__ == "__main__":
    # Substitua YOUR_PROJECT_ID pelo ID do seu projeto no Google Cloud
    project_id = "self-service-analytics-tdah"

    # Substitua YOUR_DATASET_NAME pelo nome do seu dataset
    dataset_name = "dw"

    schemas = get_schemas_from_bigquery(project_id, dataset_name)
    dbdiagram_code = generate_dbdiagram_code(schemas)

    print(dbdiagram_code)
