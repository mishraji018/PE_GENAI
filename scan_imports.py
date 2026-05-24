import os
import json
import ast
import sys

def get_imports_from_py(file_path):
    imports = set()
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=file_path)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.add(alias.name.split('.')[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.add(node.module.split('.')[0])
    except Exception:
        pass
    return imports

def get_imports_from_ipynb(file_path):
    imports = set()
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for cell in data.get('cells', []):
                if cell.get('cell_type') == 'code':
                    source = ''.join(cell.get('source', []))
                    try:
                        tree = ast.parse(source)
                        for node in ast.walk(tree):
                            if isinstance(node, ast.Import):
                                for alias in node.names:
                                    imports.add(alias.name.split('.')[0])
                            elif isinstance(node, ast.ImportFrom):
                                if node.module:
                                    imports.add(node.module.split('.')[0])
                    except:
                        pass
    except Exception:
        pass
    return imports

results = {}
base_dir = r"c:\Users\pmish\Desktop\2nd year notes\4th sem\Personal elective"
std_libs = set(sys.stdlib_module_names) if hasattr(sys, 'stdlib_module_names') else set()

for root, _, files in os.walk(base_dir):
    if any(ignore in root for ignore in ['.venv', 'venv', 'env', '.git', 'node_modules']):
        continue
    for file in files:
        path = os.path.join(root, file)
        rel_path = os.path.relpath(path, base_dir)
        if file.endswith('.py'):
            imps = get_imports_from_py(path)
        elif file.endswith('.ipynb'):
            imps = get_imports_from_ipynb(path)
        else:
            continue
            
        if imps:
            actual_pkgs = []
            for pkg in imps:
                if pkg in std_libs or pkg.startswith('_'): continue
                if pkg == 'cv2': actual_pkgs.append('opencv-python')
                elif pkg == 'PIL': actual_pkgs.append('pillow')
                elif pkg == 'bs4': actual_pkgs.append('beautifulsoup4')
                elif pkg == 'sklearn': actual_pkgs.append('scikit-learn')
                else: actual_pkgs.append(pkg)
            if actual_pkgs:
                results[rel_path] = list(set(actual_pkgs))

with open(os.path.join(base_dir, 'import_results.json'), 'w') as f:
    json.dump({'files': results}, f, indent=2)
print("SCAN COMPLETE")
