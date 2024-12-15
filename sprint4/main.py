from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from datetime import datetime
from database import get_db_connection  # Suponiendo que tienes esta función para conectar a la base de datos

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite solicitudes desde cualquier origen
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP
    allow_headers=["*"],  # Permite todos los encabezados
)

# Modelos de datos
class Grupo(BaseModel):
    id: Optional[int]
    nombre: str

class Persona(BaseModel):
    id: int
    nombre: str
    edad: int
    grupo_id: int

class Fichaje(BaseModel):
    persona_id: int
    tipo_fichaje: str  # "entrada" o "salida"
    fecha_hora: datetime

# Ruta principal con HTML
@app.get("/", response_class=HTMLResponse)
def read_root():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Gestión de Fichajes</title>
<style>
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        margin: 0;
        padding: 0;
        background-color: #f9f9f9;
        color: #333;
    }
    header {
        background-color: #0056b3;
        color: white;
        padding: 20px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    main {
        padding: 20px;
        max-width: 800px;
        margin: 0 auto;
    }
    section {
        margin-bottom: 20px;
        background-color: #fff;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    h2 {
        font-size: 1.5rem;
        margin-bottom: 10px;
        color: #0056b3;
    }
    label {
        display: block;
        margin-bottom: 5px;
        font-weight: bold;
    }
    input, select, button {
        width: 100%;
        padding: 10px;
        margin-bottom: 15px;
        border: 1px solid #ccc;
        border-radius: 4px;
        font-size: 1rem;
    }
    button {
        background-color: #0056b3;
        color: white;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    button:hover {
        background-color: #003d82;
    }
    ul {
        list-style-type: none;
        padding: 0;
    }
    li {
        padding: 10px;
        margin-bottom: 5px;
        background-color: #f1f1f1;
        border-radius: 4px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    li:hover {
        background-color: #e0e0e0;
    }
</style>
    </head>
    <body>
        <header>
            <h1>Gestión de Fichajes</h1>
        </header>
        <main>
            <section id="formulario-fichajes">
                <h2>Registrar Fichaje</h2>
                <form id="form-fichaje">
                    <label for="persona-id">ID de la Persona:</label>
                    <input type="number" id="persona-id" required />

                    <label for="tipo-fichaje">Tipo de Fichaje:</label>
                    <select id="tipo-fichaje" required>
                        <option value="entrada">Entrada</option>
                        <option value="salida">Salida</option>
                    </select>

                    <button type="submit">Registrar Fichaje</button>
                </form>
            </section>

            <section id="grupos">
                <h2>Grupos</h2>
                <ul id="lista-grupos"></ul>
            </section>

            <section id="personas">
                <h2>Personas</h2>
                <ul id="lista-personas"></ul>
            </section>

            <section id="fichajes">
                <h2>Fichajes</h2>
                <ul id="lista-fichajes"></ul>
            </section>

            <section id="buscar-fichajes">
    <h2>Buscar Fichajes</h2>
    <form id="form-buscar-fichajes">
        <label for="buscar-persona-id">ID de Persona:</label>
        <input type="number" id="buscar-persona-id" required />
        <button type="submit">Buscar Fichajes</button>
    </form>
</section>


            <section id="registro-persona">
    <h2>Registrar Nueva Persona</h2>
    <form id="form-persona">
        <label for="nombre">Nombre:</label>
        <input type="text" id="nombre" required />

        <label for="edad">Edad:</label>
        <input type="number" id="edad" required />

        <label for="grupo">Grupo:</label>
        <select id="grupo" required>
            <option value="1">Grupo A</option>
            <option value="2">Grupo B</option>
        </select>

        <button type="submit">Registrar Persona</button>
    </form>
</section>
        </main>

        <script>
            const API_URL = 'http://localhost:8000';

            // Registrar fichaje
            document.getElementById('form-fichaje').addEventListener('submit', async (event) => {
                event.preventDefault();

                const personaId = parseInt(document.getElementById('persona-id').value, 10);
                const tipoFichaje = document.getElementById('tipo-fichaje').value;
                const fechaHora = new Date().toISOString();

                try {
                // Enviar el fichaje a la API de FastAPI
                const response = await fetch(`${API_URL}/fichajes`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        persona_id: personaId,
                        tipo_fichaje: tipoFichaje,
                        fecha_hora: fechaHora
                    }),
                });

                // Comprobar si la respuesta es OK
                if (response.ok) {
                    const fichaje = await response.json();
                    alert(`Fichaje registrado con éxito: ID ${fichaje.id}`);
                    document.getElementById('form-fichaje').reset();
                } else {
                    const error = await response.json();
                    alert(`Error: ${error.detail}`);
                }
            } catch (error) {
                console.error("Error al registrar fichaje:", error);
                alert("Error al registrar fichaje.");
            }
        });

            // Cargar grupos
            async function cargarGrupos() {
                const response = await fetch(`${API_URL}/grupos`);
                const grupos = await response.json();
                const listaGrupos = document.getElementById('lista-grupos');
                listaGrupos.innerHTML = '';

                grupos.forEach(grupo => {
                    const li = document.createElement('li');
                    li.textContent = `ID: ${grupo.id} - ${grupo.nombre}`;
                    li.addEventListener('click', () => cargarPersonas(grupo.id));
                    listaGrupos.appendChild(li);
                });
            }
            
            cargarGrupos();

            // Cargar personas
            async function cargarPersonas(grupoId) {
                const response = await fetch(`${API_URL}/personas/${grupoId}`);
                const personas = await response.json();
                const listaPersonas = document.getElementById('lista-personas');
                listaPersonas.innerHTML = '';

                if (personas.length === 0) {
                    listaPersonas.textContent = 'No hay personas en este grupo.';
                } else {
                    personas.forEach(persona => {
                        const li = document.createElement('li');
                        li.textContent = `ID: ${persona.id} - ${persona.nombre}`;
                        listaPersonas.appendChild(li);
                    });
                }
            }

// Registrar nueva persona
    document.getElementById('form-persona').addEventListener('submit', async (event) => {
        event.preventDefault();

        const nombre = document.getElementById('nombre').value;
        const edad = parseInt(document.getElementById('edad').value, 10);
        const grupoId = parseInt(document.getElementById('grupo').value, 10);

        // Verifica si los datos son válidos
        if (!nombre || edad <= 0 || !grupoId) {
            alert("Por favor, rellene todos los campos correctamente.");
            return;
        }

        try {
            const response = await fetch(`${API_URL}/personas`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ nombre, edad, grupo_id: grupoId })
            });

            if (response.ok) {
                const persona = await response.json();
                alert(`Persona registrada con éxito: ${persona.nombre}`);
                cargarGrupos();  // Recargar los grupos para que la persona se muestre
                document.getElementById('form-persona').reset();
            } else {
                // Manejo adecuado del error para que no salga [object Object]
                const error = await response.json();
                alert(`Error: ${error.detail}`);
            }
        } catch (error) {
            console.error("Error al registrar persona:", error);
            alert("Error al registrar persona.");
        }
    });


            // Cargar fichajes
            async function cargarFichajes() {
                const response = await fetch(`${API_URL}/fichajes`);
                const fichajes = await response.json();
                const listaFichajes = document.getElementById('lista-fichajes');
                listaFichajes.innerHTML = '';

                fichajes.forEach(fichaje => {
                    const li = document.createElement('li');
                    li.textContent = `ID Persona: ${fichaje.persona_id} - Tipo: ${fichaje.tipo_fichaje} - Fecha: ${fichaje.fecha_hora}`;
                    listaFichajes.appendChild(li);
                });
            }

            // Buscar fichajes por persona
            document.getElementById('form-buscar-fichajes').addEventListener('submit', async (event) => {
                event.preventDefault();
                const personaId = parseInt(document.getElementById('buscar-persona-id').value, 10);

                const response = await fetch(`${API_URL}/fichajes/${personaId}`);
                const fichajes = await response.json();
                const listaFichajes = document.getElementById('lista-fichajes');
                listaFichajes.innerHTML = '';

                if (fichajes.length === 0) {
                    listaFichajes.textContent = 'No hay fichajes registrados para esta persona.';
                } else {
                    fichajes.forEach(fichaje => {
                        const li = document.createElement('li');
                        li.textContent = `Tipo: ${fichaje.tipo_fichaje} - Fecha: ${fichaje.fecha_hora}`;
                        listaFichajes.appendChild(li);
                    });
                }
            });

            // Inicializar la carga de grupos
            cargarGrupos();
            cargarFichajes();
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)



# Endpoints API

@app.get("/grupos", response_model=List[Grupo])
def get_grupos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM grupo;")
    grupos = cursor.fetchall()
    cursor.close()
    conn.close()
    return grupos

@app.get("/personas/{grupo_id}", response_model=List[Persona])
def get_personas_by_grupo(grupo_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM persona WHERE grupo_id = %s;", (grupo_id,))
    personas = cursor.fetchall()
    cursor.close()
    conn.close()
    return personas

@app.get("/fichajes/{persona_id}", response_model=List[Fichaje])
def get_fichajes_by_persona(persona_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM fichaje WHERE persona_id = %s;", (persona_id,))
    fichajes = cursor.fetchall()
    cursor.close()
    conn.close()
    return fichajes

@app.post("/fichajes", response_model=Fichaje)
async def create_fichaje(fichaje: Fichaje):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO fichaje (persona_id, tipo_fichaje, fecha_hora)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (fichaje.persona_id, fichaje.tipo_fichaje, fichaje.fecha_hora))
        conn.commit()
        fichaje_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return {**fichaje.dict(), "id": fichaje_id}
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Error al registrar fichaje: {str(e)}")

@app.post("/personas", response_model=Persona)
async def create_persona(persona: Persona):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO persona (nombre, edad, grupo_id)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (persona.nombre, persona.edad, persona.grupo_id))
        conn.commit()
        persona_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return {**persona.dict(), "id": persona_id}
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Error al registrar persona: {str(e)}")