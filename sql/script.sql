-- ==========================================
-- Script SQL: Creación de tabla PELICULAS
-- ==========================================

-- ? Eliminar la tabla si ya existe
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE peliculas CASCADE CONSTRAINTS';
EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE != -942 THEN -- -942 = tabla no existe
            RAISE;
        END IF;
END;
/

-- ? Crear tabla de películas
CREATE TABLE peliculas (
    id NUMBER PRIMARY KEY,
    titulo VARCHAR2(100) NOT NULL,
    descripcion VARCHAR2(500),
    poster VARCHAR2(500)
);

-- ? Crear secuencia para IDs (opcional, si quieres autoincremento)
CREATE SEQUENCE seq_peliculas START WITH 1 INCREMENT BY 1;

-- ? Trigger para insertar ID automático (opcional)
CREATE OR REPLACE TRIGGER trg_peliculas_id
BEFORE INSERT ON peliculas
FOR EACH ROW
WHEN (NEW.id IS NULL)
BEGIN
    :NEW.id := seq_peliculas.NEXTVAL;
END;
/

COMMIT;

SELECT * FROM PELICULAS;