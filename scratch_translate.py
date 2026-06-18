def translate(query_processed, params):
    parts = query_processed.split("%s")
    query_final = ""
    new_params = []
    
    if params and len(params) == len(parts) - 1:
        param_idx = 0
        for i, part in enumerate(parts[:-1]):
            if part.endswith("ANY("):
                list_val = params[param_idx]
                if not isinstance(list_val, (list, tuple, set)):
                    list_val = [list_val]
                placeholders = ", ".join(["?"] * len(list_val))
                part = part[:-4].rstrip()
                if part.endswith("="):
                    part = part[:-1].rstrip()
                part = part + " IN ("
                query_final += part + placeholders
                new_params.extend(list_val)
            else:
                query_final += part + "?"
                new_params.append(params[param_idx])
            param_idx += 1
        query_final += parts[-1]
        params = tuple(new_params)
    else:
        for part in parts[:-1]:
            query_final += part + "?"
        query_final += parts[-1]
        
    query_final = query_final.replace("%%", "%")
    return query_final, params

print(translate("WHERE x = %s AND lower(d.management_source) = ANY(%s) AND z = %s", (1, [2, 3, 4], 5)))
print(translate("AND NOT (serial_number = ANY(%s))", ([2, 3],)))
