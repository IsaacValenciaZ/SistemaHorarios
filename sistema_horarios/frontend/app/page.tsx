import { getHorarios } from '../services/api';

// En lugar de '@/types/escuela', usa esto:
import { Horario } from '../types/escuela';

export default async function Home() {
  // 2. TIPADO EXPLÍCITO: Le decimos a Next.js "Esto es una lista de Horarios"
  // Si getHorarios falla, usamos una lista vacía [] por seguridad.
  const horarios: Horario[] = await getHorarios() || [];

  return (
    <main className="min-h-screen p-8 bg-gray-50 text-gray-800">
      <div className="max-w-6xl mx-auto">
        
        {/* Título */}
        <header className="mb-8 border-b pb-4 border-gray-300">
          <h1 className="text-4xl font-bold text-blue-700">Sistema de Horarios 📅</h1>
          <p className="text-gray-600 mt-2">Gestión escolar con Django y Next.js</p>
        </header>

        {/* Contenido */}
        {horarios.length === 0 ? (
          <div className="text-center py-10 bg-white rounded shadow">
            <p className="text-xl text-gray-500">No hay horarios registrados o no hay conexión.</p>
            <p className="text-sm text-gray-400 mt-2">Asegúrate de que tu backend Django esté corriendo.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            
            {horarios.map((h) => (
              <div key={h.id} className="bg-white border border-gray-200 rounded-lg shadow-md p-5 hover:shadow-lg transition-shadow">
                
                <div className="flex justify-between items-start mb-2">
                  {/* 3. OPERADOR SEGURO (?.): Usamos '?' por si algún dato viene null */}
                  <h2 className="text-xl font-bold text-gray-900">
                    {h.materia?.nombre || "Sin materia"}
                  </h2>
                  <span className="bg-blue-100 text-blue-800 text-xs font-semibold px-2.5 py-0.5 rounded">
                    {h.grupo?.nombre || "Sin grupo"}
                  </span>
                </div>

                <div className="space-y-2 text-sm text-gray-600">
                  <p className="flex items-center">
                    <span className="font-semibold w-20">Profesor:</span> 
                    {h.profesor?.nombre || "No asignado"}
                  </p>
                  <p className="flex items-center">
                    <span className="font-semibold w-20">Salón:</span> 
                    {h.salon?.nombre || "No asignado"}
                  </p>
                  
                  <div className="mt-4 pt-3 border-t border-gray-100 flex justify-between items-center">
                    <span className="font-bold text-lg text-gray-700">{h.dia}</span>
                    <span className="bg-gray-100 px-3 py-1 rounded text-gray-800 font-mono">
                      {/* Verificamos que hora_inicio exista antes de cortar el string */}
                      {h.hora_inicio ? h.hora_inicio.slice(0, 5) : "--:--"} 
                      {' - '} 
                      {h.hora_fin ? h.hora_fin.slice(0, 5) : "--:--"}
                    </span>
                  </div>
                </div>

              </div>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}