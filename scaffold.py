import os

app_name = 'lserp_customization'
base_dir = r'c:\Users\stripathi\OneDrive - LEAPSYS\Documents\GIT\lserp_customization'

dirs = [
    f'{app_name}',
    f'{app_name}/config',
    f'{app_name}/public',
    f'{app_name}/public/css',
    f'{app_name}/public/js',
    f'{app_name}/templates',
    f'{app_name}/templates/includes',
    f'{app_name}/www',
]

for d in dirs:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)

files = {
    'pyproject.toml': '''[project]
name = "lserp_customization"
authors = [
    { name = "LEAPSYS", email = "info@leapsys.net"}
]
description = "LSERP Customization"
requires-python = ">=3.10"
readme = "README.md"
dynamic = ["version"]
dependencies = [
    # "frappe~=15.0.0" # add frappe dependency if required
]

[build-system]
requires = ["flit_core >=3.4,<4"]
build-backend = "flit_core.buildapi"
''',
    'README.md': '''## LSERP Customization\n\nLSERP Customization app\n\n#### License\n\nMIT\n''',
    'requirements.txt': '',
    'license.txt': 'MIT License',
    '.gitignore': '''*.pyc
*.swp
.DS_Store
__pycache__/
*.egg-info/
dist/
build/
''',
    f'{app_name}/__init__.py': '''__version__ = '0.0.1'\n''',
    f'{app_name}/hooks.py': f'''app_name = "{app_name}"
app_title = "LSERP Customization"
app_publisher = "LEAPSYS"
app_description = "LSERP Customization"
app_email = "info@leapsys.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{{
# 		"name": "{app_name}",
# 		"logo": "/assets/{app_name}/logo.png",
# 		"title": "LSERP Customization",
# 		"route": "/{app_name}",
# 		"has_permission": "{app_name}.api.permission.has_app_permission"
# 	}}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/{app_name}/css/{app_name}.css"
# app_include_js = "/assets/{app_name}/js/{app_name}.js"

# include js, css files in header of web template
# web_include_css = "/assets/{app_name}/css/{app_name}.css"
# web_include_js = "/assets/{app_name}/js/{app_name}.js"
''',
    f'{app_name}/patches.txt': '',
    f'{app_name}/config/__init__.py': '',
    f'{app_name}/config/desktop.py': '''from frappe import _

def get_data():
\treturn [
\t\t{
\t\t\t"module_name": "LSERP Customization",
\t\t\t"type": "module",
\t\t\t"label": _("LSERP Customization")
\t\t}
\t]
''',
    f'{app_name}/config/docs.py': '''"""
Configuration for docs
"""

def get_context(context):
\tcontext.brand_html = "LSERP Customization"
'''
}

for filepath, content in files.items():
    with open(os.path.join(base_dir, filepath), 'w') as f:
        f.write(content)

print('App scaffolded successfully.')
