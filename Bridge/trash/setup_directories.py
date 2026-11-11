import os

base = r'c:\Users\crmte\OneDrive\Desktop\Projects\Discovery_Engine'
kg_root = os.path.join(base, '05_Knowledge_Aggregator')
roles_dir = os.path.join(kg_root, 'roles')
converter_path = os.path.join(kg_root, 'axiomatic_converter.py')

# Check and create directories
for d in [roles_dir]:
    if not os.path.exists(d):
        os.makedirs(d)
        print(f'Created directory: {d}')
    else:
        print(f'Directory exists: {d}')

# Check if axiomatic_converter.py exists
if os.path.exists(converter_path):
    print(f'File exists: {converter_path}')
else:
    print(f'File does not exist: {converter_path}')

# Check roles directory contents
if os.path.exists(roles_dir):
    print('Roles dir contents:', os.listdir(roles_dir))
else:
    print('Roles directory does not exist yet')