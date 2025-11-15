"""
CRAG System Setup Verification
==============================

This script verifies that the Legal CRAG system is properly set up.
"""

import sys
import os


def check_files():
    """Check that all required files exist"""
    print("\n" + "="*60)
    print("FILE CHECK")
    print("="*60)

    required_files = [
        'legal_crag.py',
        'test_legal_crag.py',
        'example_crag_usage.py',
        'CRAG_README.md',
        'Requirements.txt'
    ]

    all_exist = True
    for file in required_files:
        exists = os.path.exists(file)
        status = "✓" if exists else "✗"
        print(f"{status} {file}")
        if not exists:
            all_exist = False

    return all_exist


def check_dependencies():
    """Check that required Python packages are installed"""
    print("\n" + "="*60)
    print("DEPENDENCY CHECK")
    print("="*60)

    required_packages = [
        ('openai', 'OpenAI API client'),
        ('anthropic', 'Anthropic API client (optional)'),
        ('dotenv', 'Environment variable loading')
    ]

    all_installed = True
    for package, description in required_packages:
        try:
            __import__(package)
            print(f"✓ {package:15s} - {description}")
        except ImportError:
            print(f"✗ {package:15s} - {description} [NOT INSTALLED]")
            if package != 'anthropic':  # anthropic is optional
                all_installed = False

    return all_installed


def check_api_keys():
    """Check that API keys are configured"""
    print("\n" + "="*60)
    print("API KEY CHECK")
    print("="*60)

    from dotenv import load_dotenv
    load_dotenv()
    if os.path.exists('env'):
        load_dotenv('env', override=True)

    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")

    if openai_key:
        print(f"✓ OPENAI_API_KEY found ({openai_key[:8]}...)")
        has_key = True
    else:
        print("✗ OPENAI_API_KEY not found")
        has_key = False

    if anthropic_key:
        print(f"✓ ANTHROPIC_API_KEY found ({anthropic_key[:8]}...)")
    else:
        print("~ ANTHROPIC_API_KEY not found (optional)")

    return has_key


def check_imports():
    """Check that CRAG modules can be imported"""
    print("\n" + "="*60)
    print("IMPORT CHECK")
    print("="*60)

    try:
        from legal_crag import (
            LegalCRAG,
            SimpleVectorDB,
            CRAGResponse,
            GradeLevel,
            DocumentGrade,
            ValidationResult
        )
        print("✓ legal_crag module imports successfully")
        print("✓ All classes available:")
        print("  - LegalCRAG")
        print("  - SimpleVectorDB")
        print("  - CRAGResponse")
        print("  - GradeLevel")
        print("  - DocumentGrade")
        print("  - ValidationResult")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False


def print_next_steps(files_ok, deps_ok, keys_ok, imports_ok):
    """Print next steps based on what's missing"""
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)

    if files_ok and deps_ok and keys_ok and imports_ok:
        print("✓ All checks passed! System is ready to use.")
        print("\nRun the tests:")
        print("  python test_legal_crag.py")
        print("\nRun the examples:")
        print("  python example_crag_usage.py")
        return True
    else:
        print("✗ Some checks failed. Follow these steps:\n")

        if not files_ok:
            print("1. Missing files - ensure all CRAG files are present")

        if not deps_ok:
            print("2. Install dependencies:")
            print("   pip install -r Requirements.txt")

        if not keys_ok:
            print("3. Set up API keys:")
            print("   Create a .env file with:")
            print("   OPENAI_API_KEY=sk-your-key-here")
            print("   or:")
            print("   export OPENAI_API_KEY='sk-your-key-here'")

        if deps_ok and not imports_ok:
            print("4. Fix import errors - check Python version (3.8+)")

        return False


def main():
    print("="*60)
    print("LEGAL CRAG SYSTEM - SETUP VERIFICATION")
    print("="*60)

    # Run all checks
    files_ok = check_files()

    try:
        deps_ok = check_dependencies()
    except:
        deps_ok = False
        print("\n⚠️  Could not check dependencies (python-dotenv needed)")

    try:
        keys_ok = check_api_keys()
    except:
        keys_ok = False
        print("\n⚠️  Could not check API keys")

    try:
        imports_ok = check_imports()
    except:
        imports_ok = False

    # Print summary and next steps
    all_ok = print_next_steps(files_ok, deps_ok, keys_ok, imports_ok)

    # Exit with appropriate code
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
