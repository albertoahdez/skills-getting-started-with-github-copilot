# Análisis de Casos Extremos - Tests QA

## 📋 Resumen Ejecutivo

Se han identificado **múltiples casos extremos críticos** NO cubiertos en la aplicación actual. He implementado 13 nuevos tests que exponen estas vulnerabilidades.

---

## 🚨 Casos Extremos Implementados

### 1. **Validación de Dominio de Email** ❌ CRÍTICO
**Test:** `test_signup_with_invalid_domain()`

**Problema:** La aplicación NO valida que los emails sean del dominio `@mergington.edu`

**Ejemplos probados:**
- `student@gmail.com` ❌ Se acepta incorrectamente
- `admin@mergington.com` ❌ Se acepta incorrectamente  
- `test@` ❌ Se acepta incorrectamente

**Impacto:** Cualquiera puede registrarse, no solo estudiantes de la escuela.

---

### 2. **Email Vacío o con Solo Espacios** ❌ CRÍTICO
**Test:** `test_signup_with_empty_email()`

**Ejemplos probados:**
- `""` (vacío)
- `"   "` (solo espacios)
- `"\t"` (tab)
- `"\n"` (nueva línea)

**Impacto:** Datos inválidos en la base de datos.

---

### 3. **Email Malformado** ❌ CRÍTICO
**Test:** `test_signup_with_malformed_email()`

**Ejemplos probados:**
- `notanemail` (sin @)
- `@mergington.edu` (sin nombre)
- `student@@mergington.edu` (doble @)
- `student @mergington.edu` (espacios)

**Impacto:** Imposibilidad de contactar al estudiante.

---

### 4. **Actividad Llena (Capacidad Máxima)** ❌ CRÍTICO
**Test:** `test_signup_for_full_activity()`

**Problema:** NO se valida `max_participants` antes de agregar estudiantes.

**Escenario:**
- Chess Club tiene `max_participants: 12`
- Actualmente puede aceptar estudiantes #13, #14, #15...

**Impacto:** Sobrecupo de actividades, problemas logísticos.

---

### 5. **Inyección SQL** ⚠️ SEGURIDAD
**Test:** `test_signup_with_sql_injection_attempt()`

**Patrones probados:**
- `'; DROP TABLE activities; --@mergington.edu`
- `admin'--@mergington.edu`
- `1' OR '1'='1@mergington.edu`

**Estado:** Aunque usa diccionarios en memoria (no SQL), es importante validar para futura migración a BD.

---

### 6. **Cross-Site Scripting (XSS)** ⚠️ SEGURIDAD
**Test:** `test_signup_with_xss_attempt()`

**Patrones probados:**
- `<script>alert('xss')</script>@mergington.edu`
- `test<img src=x>@mergington.edu`
- `javascript:alert(1)@mergington.edu`

**Impacto:** Si estos datos se muestran en el frontend sin sanitización, pueden ejecutar código malicioso.

---

### 7. **Email Extremadamente Largo** ⚠️
**Test:** `test_signup_with_very_long_email()`

**Ejemplo:** Email de 1000+ caracteres

**Impacto:** Posible Denial of Service o problemas de rendimiento.

---

### 8. **Case Sensitivity en Nombres de Actividades** ℹ️
**Test:** `test_signup_activity_name_case_sensitive()`

**Ejemplo:** `"chess club"` vs `"Chess Club"`

**Resultado esperado:** 404 (no encontrado)

---

### 9. **Caracteres Especiales en Nombres de Actividad** ⚠️
**Test:** `test_signup_with_special_characters_in_activity()`

**Patrones probados:**
- `"Chess Club<script>"`
- `"../../../etc/passwd"` (path traversal)
- `"Chess%20Club"`

---

### 10. **Caracteres Unicode** ℹ️
**Test:** `test_signup_with_unicode_characters()`

**Ejemplos:**
- `stüdent@mergington.edu`
- `学生@mergington.edu`
- `тест@mergington.edu`

**Objetivo:** Verificar manejo internacional.

---

### 11. **Dar de Baja Usuario No Existente** ℹ️
**Test:** `test_unregister_nonexistent_user()`

**Escenario:** Intentar eliminar un email que nunca se registró.

---

### 12. **Condiciones de Carrera (Race Conditions)** ℹ️
**Test:** `test_concurrent_signups_same_user()`

**Escenario:** El mismo usuario intenta registrarse múltiples veces simultáneamente.

---

## 🔧 Correcciones Necesarias en `src/app.py`

### Prioridad 1: Validación de Email

```python
import re
from fastapi import HTTPException

def validate_email(email: str) -> str:
    """Validate email format and domain"""
    email = email.strip()
    
    # Check not empty
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")
    
    # Check length
    if len(email) > 254:  # RFC 5321
        raise HTTPException(status_code=400, detail="Email is too long")
    
    # Check basic format
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    
    # Check domain
    if not email.endswith('@mergington.edu'):
        raise HTTPException(
            status_code=400, 
            detail="Only @mergington.edu emails are allowed"
        )
    
    return email.lower()  # Normalize
```

### Prioridad 2: Validación de Capacidad

```python
@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate email
    email = validate_email(email)
    
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]

    # CHECK CAPACITY
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(
            status_code=400, 
            detail=f"Activity is full (max: {activity['max_participants']})"
        )

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(
            status_code=400, 
            detail="Student already signed up for this activity"
        )
    
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
```

---

## 📊 Resultados Esperados

### Tests que DEBERÍAN FALLAR ahora (antes de correcciones):
1. ✅ `test_signup_with_invalid_domain` - Acepta dominios incorrectos
2. ✅ `test_signup_with_empty_email` - Acepta emails vacíos
3. ✅ `test_signup_with_malformed_email` - Acepta emails malformados
4. ✅ `test_signup_for_full_activity` - Permite sobrecupo
5. ✅ `test_signup_with_very_long_email` - Acepta emails muy largos

### Tests que DEBERÍAN PASAR ahora:
1. ✅ `test_signup_activity_name_case_sensitive` - Ya maneja correctamente
2. ✅ `test_signup_with_special_characters_in_activity` - Retorna 404
3. ✅ `test_concurrent_signups_same_user` - Evita duplicados

---

## 🎯 Recomendaciones

### Inmediatas:
1. Implementar `validate_email()` 
2. Agregar validación de capacidad máxima
3. Ejecutar todos los tests

### A Mediano Plazo:
1. Agregar sanitización HTML para prevenir XSS
2. Implementar rate limiting para prevenir abuse
3. Agregar logging de intentos sospechosos
4. Considerar validación con biblioteca especializada (pydantic EmailStr)

### Testing:
```bash
# Ejecutar todos los tests
pytest tests/test_app.py -v

# Ejecutar solo tests de casos extremos
pytest tests/test_app.py -v -k "edge"

# Ver coverage
pytest tests/test_app.py --cov=src --cov-report=html
```

---

## 📝 Conclusión

Se identificaron **5 vulnerabilidades críticas** y **7 casos extremos adicionales**. Los tests implementados aseguran que:

✅ Solo emails `@mergington.edu` válidos se acepten  
✅ No se permita sobrecupo de actividades  
✅ Se rechacen inputs maliciosos o malformados  
✅ La aplicación maneje caracteres especiales de forma segura  

**Estado actual:** ❌ Múltiples tests fallarán hasta implementar las validaciones sugeridas.  
**Estado esperado:** ✅ Todos los tests deben pasar después de las correcciones.
