def dict_to_sql_columns_and_values(
    obj: dict, mode: str = 'insert'
) -> tuple[str, str]:
    columns, values = [], []
    for column, value in obj.items():
        columns.append(column)

        if value is None:
            values.append("NULL")
        elif isinstance(value, str):
            value = value.replace("'", "''")
            values.append(f"'{value}'")
        elif isinstance(value, (float, int)):
            values.append(str(value))
    
    if mode == 'update' and len(columns) == 1:
        return (
            f"{columns[0]}",
            f"{values[0]}"
        )

    return (
        f"({','.join(columns)})",
        f"({','.join(values)})"
    )