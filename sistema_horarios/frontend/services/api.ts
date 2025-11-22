import { Horario } from '../types/escuela';; // Importamos los tipos del paso 1

const API_URL = 'http://127.0.0.1:8000/api';

export async function getHorarios(): Promise<Horario[]> {
  try {
    // cache: 'no-store' es vital para que no guarde datos viejos
    const res = await fetch(`${API_URL}/horarios/`, { cache: 'no-store' });
    
    if (!res.ok) {
      // Si Django da error (ej. 500 o 404), lanzamos una alerta
      throw new Error(`Error del servidor: ${res.status}`);
    }
    
    return res.json();
  } catch (error) {
    console.error("Error conectando con Django:", error);
    return []; // Si falla, regresamos una lista vacía para que no explote la app
  }
}