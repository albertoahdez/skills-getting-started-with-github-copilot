#!/usr/bin/env python3
"""
Quick validation test script - No pytest required
Tests the validate_email function directly
"""

import sys
sys.path.insert(0, '/home/alberto/DataX/skills-getting-started-with-github-copilot')

from src.app import validate_email, activities
from fastapi import HTTPException

def test_validation(email, should_pass=True):
    """Test a single email validation"""
    try:
        result = validate_email(email)
        if should_pass:
            print(f"✅ PASS: '{email}' → '{result}'")
            return True
        else:
            print(f"❌ FAIL: '{email}' should have been rejected but was accepted")
            return False
    except HTTPException as e:
        if not should_pass:
            print(f"✅ PASS: '{email}' → Rejected: {e.detail}")
            return True
        else:
            print(f"❌ FAIL: '{email}' should have been accepted but was rejected: {e.detail}")
            return False

def main():
    print("=" * 70)
    print("🧪 VALIDACIÓN DE EMAILS - TEST RÁPIDO")
    print("=" * 70)
    
    passed = 0
    failed = 0
    
    print("\n📧 EMAILS VÁLIDOS (deberían pasar):")
    print("-" * 70)
    valid_emails = [
        "student@mergington.edu",
        "john.doe@mergington.edu",
        "test_user@mergington.edu",
        "user123@mergington.edu",
    ]
    for email in valid_emails:
        if test_validation(email, should_pass=True):
            passed += 1
        else:
            failed += 1
    
    print("\n❌ EMAILS INVÁLIDOS (deberían ser rechazados):")
    print("-" * 70)
    
    print("\n1. Dominio incorrecto:")
    invalid_domain = [
        "student@gmail.com",
        "teacher@yahoo.com",
        "admin@mergington.com",
        "test@mergingtown.edu",
    ]
    for email in invalid_domain:
        if test_validation(email, should_pass=False):
            passed += 1
        else:
            failed += 1
    
    print("\n2. Formato malformado:")
    malformed = [
        "notanemail",
        "@mergington.edu",
        "student@@mergington.edu",
        "student @mergington.edu",
    ]
    for email in malformed:
        if test_validation(email, should_pass=False):
            passed += 1
        else:
            failed += 1
    
    print("\n3. Vacíos o espacios:")
    empty = ["", "   ", "\t"]
    for email in empty:
        if test_validation(email, should_pass=False):
            passed += 1
        else:
            failed += 1
    
    print("\n4. Email muy largo:")
    long_email = "a" * 1000 + "@mergington.edu"
    if test_validation(long_email, should_pass=False):
        passed += 1
    else:
        failed += 1
    
    print("\n" + "=" * 70)
    print(f"📊 RESULTADOS: {passed} ✅ pasaron, {failed} ❌ fallaron")
    print("=" * 70)
    
    print("\n🎯 VERIFICACIÓN DE CAPACIDAD:")
    print("-" * 70)
    chess = activities["Chess Club"]
    current = len(chess["participants"])
    max_cap = chess["max_participants"]
    print(f"Chess Club: {current}/{max_cap} participantes")
    if current < max_cap:
        print(f"✅ Hay {max_cap - current} lugares disponibles")
    else:
        print(f"❌ Actividad llena")
    
    print("\n✅ Script completado!")
    
    if failed == 0:
        print("🎉 ¡Todas las validaciones funcionan correctamente!")
        return 0
    else:
        print(f"⚠️  {failed} validaciones fallaron")
        return 1

if __name__ == "__main__":
    sys.exit(main())
