import boto3

lambda_client = boto3.client('lambda')

functions = []
next_marker = None

while True:
    if next_marker:
        response = lambda_client.list_functions(Marker=next_marker)
    else:
        response = lambda_client.list_functions()

    functions.extend(response['Functions'])
    next_marker = response.get('NextMarker')

    if not next_marker:
        break

for function in functions:
    function_name = function['FunctionName']

    try:
        alias_name = 'your-stagevariable-name'
        alias_info = lambda_client.get_alias(
            FunctionName=function_name,
            Name=alias_name
        )
        

        if alias_info['FunctionVersion'] == 'your-alias-name':
            print(f"Alias '{alias_name}' already exists and points to the latest version for function '{function_name}'. Skipping creation.")
            continue
    
    except lambda_client.exceptions.ResourceNotFoundException:
        # Alias does not exist, create a new one
        lambda_client.create_alias(
            FunctionName=function_name,
            Name=alias_name,
            FunctionVersion='your-alias-name'
        )
        print(f"Alias '{alias_name}' created and pointed to the latest version for function '{function_name}'.")