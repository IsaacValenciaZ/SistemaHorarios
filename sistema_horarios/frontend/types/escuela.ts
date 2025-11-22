// Define la estructura de los objetos que vienen de Django

export interface Profesor {
    id: number;
    nombre: string;
    email: string;
    especialidad: string;
}
  
export interface Materia {
    id: number;
    nombre: string;
    codigo: string;
}

export interface Salon {
    id: number;
    nombre: string;
    capacidad: number;
}

export interface Grupo {
    id: number;
    nombre: string;
}

export interface Periodo {
    id: number;
    nombre: string;
    activo: boolean;
}

// Este es el importante, combina todo lo anterior
export interface Horario {
    id: number;
    periodo: Periodo;
    grupo: Grupo;
    profesor: Profesor;
    materia: Materia;
    salon: Salon;
    dia: string;         // "LUN", "MAR", etc.
    hora_inicio: string; // "07:00:00"
    hora_fin: string;    // "09:00:00"
}