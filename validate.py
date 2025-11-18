
import sys
import os
from pathlib import Path

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_backend_dependencies():
    """Check if backend dependencies are installed"""
    print("\n📦 Checking backend dependencies...")
    dependencies = {
        'flask': 'Flask',
        'flask_cors': 'Flask-CORS',
        'pandas': 'pandas',
        'numpy': 'NumPy',
        'sklearn': 'scikit-learn',
        'scipy': 'SciPy',
    }
    
    all_installed = True
    for module, name in dependencies.items():
        try:
            __import__(module)
            print(f"  ✅ {name}")
        except ImportError:
            print(f"  ❌ {name} - Run: pip install -r backend/requirements.txt")
            all_installed = False
    
    return all_installed

def check_dataset():
    """Check if dataset exists"""
    print("\n📁 Checking dataset...")
    dataset_path = Path("backend/Mall_Customers.csv")
    if dataset_path.exists():
        print(f"  ✅ {dataset_path} found")
        return True
    else:
        print(f"  ❌ {dataset_path} not found")
        print("     Copy Mall_Customers.csv from parent directory to backend/")
        return False

def check_frontend_setup():
    """Check frontend setup"""
    print("\n🎨 Checking frontend setup...")
    
    # Check package.json
    if Path("frontend/package.json").exists():
        print("  ✅ package.json found")
    else:
        print("  ❌ package.json not found")
        return False
    
    # Check node_modules
    if Path("frontend/node_modules").exists():
        print("  ✅ node_modules found (dependencies installed)")
        return True
    else:
        print("  ⚠️  node_modules not found")
        print("     Run: cd frontend && npm install")
        return False

def check_directory_structure():
    """Check directory structure"""
    print("\n📂 Checking directory structure...")
    required_dirs = [
        "backend",
        "frontend/src",
        "frontend/public",
        "frontend/src/components"
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"  ✅ {dir_path}/")
        else:
            print(f"  ❌ {dir_path}/ missing")
            all_exist = False
    
    return all_exist

def main():
    print("=" * 50)
    print("🔍 Clustering Web App Setup Validator")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version),
        ("Directory Structure", check_directory_structure),
        ("Backend Dependencies", check_backend_dependencies),
        ("Dataset", check_dataset),
        ("Frontend Setup", check_frontend_setup),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"  ❌ Error: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {name}")
    
    print(f"\n{passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 Setup looks good! You can run:")
        print("   macOS/Linux: ./start.sh")
        print("   Windows:     start.bat")
        return 0
    else:
        print("\n⚠️  Please fix the issues above before running the app")
        return 1

if __name__ == "__main__":
    sys.exit(main())
