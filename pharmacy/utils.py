from functools import wraps
from flask import redirect, url_for
from flask_login import current_user

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.rol not in roles:
                return redirect(url_for('dashboard.index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator



STATES = [
    "Aguascalientes", "Baja California", "Baja California Sur",
    "Campeche", "Chiapas", "Chihuahua", "Ciudad de México",
    "Coahuila", "Colima", "Durango", "Guanajuato", "Guerrero",
    "Hidalgo", "Jalisco", "Estado de México", "Michoacán",
    "Morelos", "Nayarit", "Nuevo León", "Oaxaca", "Puebla",
    "Querétaro", "Quintana Roo", "San Luis Potosí", "Sinaloa",
    "Sonora", "Tabasco", "Tamaulipas", "Tlaxcala", "Veracruz",
    "Yucatán", "Zacatecas"
]

CITIES = [
    "Aguascalientes", "Cancún", "Chihuahua", "Ciudad de México",
    "Ciudad Juárez", "Culiacán", "Durango", "Ecatepec",
    "Guadalajara", "Hermosillo", "León", "Mérida",
    "Mexicali", "Monterrey", "Morelia", "Naucalpan",
    "Nezahualcóyotl", "Oaxaca", "Puebla", "Querétaro",
    "Saltillo", "San Luis Potosí", "Tijuana", "Tlajomulco",
    "Tlalnepantla", "Toluca", "Torreón", "Veracruz",
    "Villahermosa", "Zapopan"
]