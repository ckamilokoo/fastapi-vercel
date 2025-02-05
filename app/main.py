from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from supabase import create_client, Client
import os
from dotenv import load_dotenv
import bcrypt
from app.database import supabase
from fastapi.middleware.cors import CORSMiddleware


# Cargar variables de entorno
load_dotenv()

# Inicializar FastAPI y cliente de Supabase
app = FastAPI()


# Habilitar CORS en la aplicación
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir peticiones de cualquier origen
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los headers
)


print(supabase)

# Modelo para el usuario
class User(BaseModel):
    email: str
    password: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/register")
async def register(user: User):
    try:
        print(f"Attempting to register user: {user.email}")

        # Crear el usuario en Supabase Auth
        response = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password,
        })

        # Inspeccionar respuesta
        print(f"Supabase response: {response}")

        # Verificar si hay errores en la respuesta
        if hasattr(response, "error") and response.error:
            raise HTTPException(status_code=400, detail=str(response.error))

        # Verificar si el usuario se creó correctamente
        if not hasattr(response, "user") or response.user is None:
            raise HTTPException(status_code=400, detail="User registration failed")

        return {"message": "User created successfully", "user": response.user}
    
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred during registration")



@app.post("/login")
async def login(user: User):
    try:
        print(f"Attempting login for user: {user.email}")

        # Intentar iniciar sesión en Supabase
        response = supabase.auth.sign_in_with_password({
            "email": user.email,
            "password": user.password
        })

        # Inspeccionar la respuesta
        print(f"Supabase response: {response}")

        # Verificar si el inicio de sesión fue exitoso
        if not hasattr(response, "user") or response.user is None:
            raise HTTPException(status_code=400, detail="Invalid credentials")

        return {"message": "Login successful", "user": response.user}

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred during login")


@app.post("/logout")
async def logout():
    # Cerrar sesión del usuario
    response = supabase.auth.sign_out()
    
    return {"message": "Logout successful"}
