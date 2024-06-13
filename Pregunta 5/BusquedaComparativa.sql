-- ================================================
-- Bloque 1: Crear la Tabla de Alumnos e Insertar Datos
-- ================================================
-- En este bloque se crea la tabla 'alumno' y se insertan datos de ejemplo.
-- ================================================

-- Crear la tabla de alumnos
CREATE TABLE alumno
(
    id INT,
    nombre VARCHAR(20),
    paterno VARCHAR(20)
);

-- Insertar datos de ejemplo
INSERT INTO alumno VALUES (43, 'Martha', 'Gonzalez');
INSERT INTO alumno VALUES (4, 'Marta', 'Perez');

-- ================================================
-- Bloque 2: Crear la Tabla Temporal para Comparación
-- ================================================
-- En este bloque se crea una tabla temporal llamada 'nombre_comparacion'
-- para almacenar la comparación de los nombres.
-- ================================================

-- Declarar variables
DECLARE @nombre1 VARCHAR(20), @nombre2 VARCHAR(20), @sql NVARCHAR(2000);
DECLARE @contador INT, @longitud INT;

-- Asignar valores a las variables
SET @nombre1 = 'Martha';
SET @nombre2 = 'Marta';

-- Determinar la longitud máxima entre los nombres
SET @longitud = LEN(@nombre1);
IF LEN(@nombre2) > @longitud SET @longitud = LEN(@nombre2);

-- Crear la estructura de la tabla temporal
SET @sql = 'CREATE TABLE nombre_comparacion (';
SET @contador = 1;
WHILE @contador <= @longitud
BEGIN
    SET @sql = @sql + 'caracter' + CAST(@contador AS VARCHAR(2)) + ' CHAR(1),';
    SET @contador = @contador + 1;
END
SET @sql = LEFT(@sql, LEN(@sql) - 1) + ')';

-- Ejecutar la creación de la tabla temporal
EXEC sp_executesql @sql;

-- ================================================
-- Bloque 3: Insertar las Comparaciones en la Tabla Temporal
-- ================================================
-- En este bloque se insertan los caracteres de los nombres en la tabla temporal.
-- ================================================

-- Declarar variables adicionales
DECLARE @caracter1 CHAR(1), @caracter2 CHAR(1);
DECLARE @nombre1 VARCHAR(20), @nombre2 VARCHAR(20), @sql NVARCHAR(2000);
DECLARE @contador INT, @longitud INT;

-- Asignar valores a las variables
SET @nombre1 = 'Martha';
SET @nombre2 = 'Marta';

-- Determinar la longitud máxima entre los nombres
SET @longitud = LEN(@nombre1);
IF LEN(@nombre2) > @longitud SET @longitud = LEN(@nombre2);

-- Inicializar el contador
SET @contador = 1;

-- Insertar los caracteres en la tabla temporal
WHILE @contador <= @longitud
BEGIN
    SET @caracter1 = SUBSTRING(@nombre1, @contador, 1);
    SET @caracter2 = SUBSTRING(@nombre2, @contador, 1);

    -- Manejar los casos donde uno de los nombres es más corto
    IF @caracter1 IS NULL SET @caracter1 = ' ';
    IF @caracter2 IS NULL SET @caracter2 = ' ';

    -- Insertar el primer carácter
    SET @sql = 'INSERT INTO nombre_comparacion (caracter' + CAST(@contador AS VARCHAR(2)) + ') VALUES (''' + @caracter1 + ''')';
    EXEC sp_executesql @sql;

    -- Actualizar el carácter si es diferente
    SET @sql = 'UPDATE nombre_comparacion SET caracter' + CAST(@contador AS VARCHAR(2)) + ' = ''' + @caracter2 + ''' WHERE caracter' + CAST(@contador AS VARCHAR(2)) + ' IS NULL';
    EXEC sp_executesql @sql;

    -- Incrementar el contador
    SET @contador = @contador + 1;
END

-- ================================================
-- Bloque 4: Realizar la Comparación y Mostrar Resultados
-- ================================================
-- En este bloque se seleccionan y muestran las diferencias entre los nombres.
-- ================================================

-- Mostrar matriz de comparacion
SELECT * FROM nombre_comparacion

-- Mostrar diferencias
SELECT * FROM nombre_comparacion WHERE caracter1 != caracter2;


-- ================================================
-- Bloque 5: Crear Tabla de Comparación y Comparar Nombres
-- ================================================
-- En este bloque se crea una tabla llamada 'nombre' y se insertan los valores
-- 1 en las posiciones donde los caracteres de los nombres son iguales.
-- ================================================
DECLARE @caracter1 CHAR(1), @caracter2 CHAR(1);
DECLARE @nombre1 VARCHAR(20), @nombre2 VARCHAR(20), @sql NVARCHAR(2000);
DECLARE @contador INT, @longitud INT;

-- Asignar valores a las variables
SET @nombre1 = 'Martha';
SET @nombre2 = 'Marta';

-- Determinar la longitud máxima entre los nombres
SET @longitud = LEN(@nombre1);
IF LEN(@nombre2) > @longitud SET @longitud = LEN(@nombre2);

-- Crear la tabla 'nombre'
SET @sql = 'CREATE TABLE nombre (';
SET @contador = 1;
WHILE @contador <= @longitud
BEGIN
    SET @sql = @sql + 'm' + CAST(@contador AS VARCHAR(2)) + ' INT,';
    SET @contador = @contador + 1;
END
SET @sql = LEFT(@sql, LEN(@sql) - 1) + ')';
EXEC sp_executesql @sql;



-- Comparar y actualizar la tabla 'nombre'
DECLARE @caracter1 CHAR(1), @caracter2 CHAR(1);
DECLARE @nombre1 VARCHAR(20), @nombre2 VARCHAR(20), @sql NVARCHAR(2000);
DECLARE @contador INT, @longitud INT;

-- Asignar valores a las variables
SET @nombre1 = 'Martha';
SET @nombre2 = 'Marta';

-- Determinar la longitud máxima entre los nombres
SET @longitud = LEN(@nombre1);
IF LEN(@nombre2) > @longitud SET @longitud = LEN(@nombre2);
SET @contador = 1;
WHILE @contador <= @longitud
BEGIN
    IF SUBSTRING(@nombre1, @contador, 1) = SUBSTRING(@nombre2, @contador, 1)
    BEGIN
        SET @sql = 'INSERT INTO nombre (m' + CAST(@contador AS VARCHAR(2)) + ') VALUES (1)';
    END
    ELSE
    BEGIN
        SET @sql = 'INSERT INTO nombre (m' + CAST(@contador AS VARCHAR(2)) + ') VALUES (NULL)';
    END
    EXEC sp_executesql @sql;
    SET @contador = @contador + 1;
END

-- ================================================
-- Bloque 6: Mostrar Resultados y Sumar Coincidencias
-- ================================================
-- En este bloque se seleccionan y muestran las coincidencias de los nombres
-- y se suman las columnas para determinar el número total de coincidencias.
-- ================================================

-- Mostrar la tabla 'nombre'
SELECT * FROM nombre;

-- Sumar las coincidencias de cada columna
SELECT COALESCE(SUM(m1), 0) AS suma_m1,
       COALESCE(SUM(m2), 0) AS suma_m2,
       COALESCE(SUM(m3), 0) AS suma_m3,
       COALESCE(SUM(m4), 0) AS suma_m4,
       COALESCE(SUM(m5), 0) AS suma_m5,
       COALESCE(SUM(m6), 0) AS suma_m6
FROM nombre;

-- Sumar total de las coincidencias de las columnas
SELECT COALESCE(SUM(m1), 0)+
       COALESCE(SUM(m2), 0)+
       COALESCE(SUM(m3), 0)+
       COALESCE(SUM(m4), 0)+
       COALESCE(SUM(m5), 0)+
       COALESCE(SUM(m6), 0) AS COINCIDENCIAS
FROM nombre;
-- ================================================
-- Fin del Código
-- ================================================
-- Este archivo SQL muestra cómo crear un agente inteligente que compara dos nombres
-- y almacena las coincidencias en una tabla para su análisis.
-- ================================================
