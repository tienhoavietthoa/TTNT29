# fix_imports.py - Chạy từ frontend folder
import os
import re

files_to_fix = [
    "main.py",
    "config.py",
    "api/__init__.py",
    "api/client.py",
    "api/services/__init__.py",
    "api/services/auth_api.py",
    "api/services/user_api.py",
    "api/services/class_api.py",
    "api/services/attendance_api.py",
    "api/services/message_api.py",
    "api/services/contact_api.py",
    "core/__init__.py",
    "core/auth_manager.py",
    "core/app_manager.py",
    "core/utils.py",
    "ui/__init__.py",
    "ui/windows/__init__.py",
    "ui/windows/login_window.py",
    "ui/windows/teacher_dashboard_window.py",
    "ui/windows/admin_dashboard_window.py",
    "ui/windows/attendance_detail_window.py",
    "ui/windows/face_enrollment_window.py",
    "ui/windows/camera_widget.py",
    "ui/windows/message_window.py",
    "ui/components/__init__.py",
    "ui/components/custom_table_widget.py",
    "ui/components/filter_widget.py",
    "ui/dialogs/__init__.py",
    "assets/__init__.py",
    "assets/styles/__init__.py",
]

replacements = [
    (r'from frontend\.', 'from '),
    (r'import frontend\.', 'import '),
    (r'from \.frontend\.', 'from .'),
]

def fix_file(filepath):
    """Sửa import trong một file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)
        
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

print("=" * 50)
print("FIXING FRONTEND IMPORTS")
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