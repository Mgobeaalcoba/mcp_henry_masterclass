-- SQLite
   SELECT cliente, asunto, descripcion 
   FROM tickets 
   WHERE estado = 'abierto' AND prioridad = 'urgente';

-- SQLite
-- Tickets abiertos y urgentes de SecureNet
    SELECT cliente, asunto, descripcion 
    FROM tickets 
    WHERE estado = 'abierto' AND prioridad = 'urgente' AND cliente = 'SecureNet';
