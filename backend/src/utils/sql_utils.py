def dict_to_sql_columns_and_values(obj: dict) -> tuple[str, str]:
    columns, values = [], []
    for column, value in obj.items():
        columns.append(column)

        if value is None:
            values.append("NULL")
        elif isinstance(value, str):
            value = value.replace("'", "''")
            values.append(f"'{value}'")
    
    return (
        f"({','.join(columns)})",
        f"({','.join(values)})"
    )