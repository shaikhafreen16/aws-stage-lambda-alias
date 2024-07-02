import boto3

lambda_client = boto3.client('lambda')

alias_name = 'your-stagevariable-name'

functions = []
paginator = lambda_client.get_paginator('list_functions')
for page in paginator.paginate():
    functions.extend(page['Functions'])


for function in functions:
    function_name = function['FunctionName']

    # Step 3: Check if 'your-stagevariable-name' alias already exists and points to a specific version
    try:
        alias_info = lambda_client.get_alias(
            FunctionName=function_name,
            Name=alias_name
        )

        # If alias exists and points to a specific version, skip updating it
        if 'FunctionVersion' in alias_info:
            print(f"Alias '{alias_name}' already exists for function '{function_name}' pointing to version '{alias_info['FunctionVersion']}'. Skipping update.")
            continue

    except lambda_client.exceptions.ResourceNotFoundException:
        # Alias does not exist, proceed to create a new alias and update it
        response = lambda_client.create_alias(
            FunctionName=function_name,
            Name=alias_name,
            FunctionVersion='your-alias-name'
        )
        new_version = response['FunctionVersion']
        print(f"Alias '{alias_name}' created for function '{function_name}' and pointed to version '{new_version}'.")