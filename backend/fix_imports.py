# fix_imports.py - Chạy từ backend folder
import os
import re

# Danh sách các file cần sửa
files_to_fix = [
    "database.py",
    "config.py",
    "routers/__init__.py",
    "routers/auth_router.py",
    "routers/user_router.py",
    "routers/class_router.py",
    "routers/attendance_router.py",
    "routers/message_router.py",
    "routers/contact_router.py",
    "models/__init__.py",
    "models/auth_models.py",
    "models/user_models.py",
    "models/class_models.py",
    "models/attendance_models.py",
    "models/face_models.py",
    "models/message_models.py",
    "models/contact_models.py",
    "schemas/__init__.py",
    "crud/__init__.py",
    "crud/auth_crud.py",
    "crud/user_crud.py",
    "crud/class_crud.py",
    "crud/attendance_crud.py",
    "crud/message_crud.py",
    "crud/contact_crud.py",
    "crud/face_crud.py",
    "services/__init__.py",
    "services/auth_service.py",
    "services/user_service.py",
    "services/class_service.py",
    "services/attendance_service.py",
    "services/message_service.py",
    "services/contact_service.py",
    "services/face_recognition_service.py",
    "core/__init__.py",
    "core/security.py",
    "core/dependencies.py",
    "core/exceptions.py",
    "main.py",
]

# Pattern để thay thế
replacements = [
    # Loại bỏ "from backend."
    (r'from backend\.', 'from '),
    (r'import backend\.', 'import '),
    # Loại bỏ "from \.backend"
    (r'from \.backend\.', 'from .'),
]

def fix_file(filepath):
    """Sửa import trong một file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply replacements
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)
        
        # Nếu có thay đổi, ghi lại file
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Fixed: {filepath}")
            return True
        else:
            print(f"- No changes: {filepath}")
            return False
    except Exception as e:
        print(f"✗ Error in {filepath}: {e}")
        return False

# Chạy fix cho tất cả files
print("=" * 50)
print("FIXING BACKEND IMPORTS")
print("=" * 50)

fixed_count = 0
for filepath in files_to_fix:
    full_path = os.path.join(os.getcwd(), filepath)
    if os.path.exists(full_path):
        if fix_file(full_path):
            fixed_count += 1
    else:
        print(f"⚠ Not found: {filepath}")

print("=" * 50)
print(f"Fixed {fixed_count} files!")
print("=" * 50)