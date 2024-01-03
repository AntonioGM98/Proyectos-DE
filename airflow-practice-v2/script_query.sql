SELECT cl.name, cl.surname, cl.email, cl.pnr 
FROM clients cl
JOIN tickets t ON cl.pnr = t.pnr
JOIN vuelos v ON t.op_code  = v.op_code  
WHERE cl.mkt_permission = 1 AND v.flight_status = 'CANCELED'
AND (
	(LENGTH(t.seat) = 2 AND CAST(SUBSTRING(t.seat, 1,1) AS INT) <= 15) OR 
    (LENGTH(t.seat) = 3 AND CAST(substring(t.seat, 1,2) AS INT) <= 15)
);