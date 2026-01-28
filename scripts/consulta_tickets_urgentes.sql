-- Consulta de tickets abiertos con prioridad urgente
-- Este script devuelve el cliente, asunto y descripción de todos los tickets
-- que están en estado abierto y tienen prioridad urgente

SELECT cliente, asunto, descripcion 
FROM tickets 
WHERE estado = 'abierto' AND prioridad = 'urgente';
