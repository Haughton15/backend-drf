-- Insertar autores (solo si la tabla author existe)
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'library_author') THEN
        -- Primero limpiar posibles duplicados
        DELETE FROM library_author 
        WHERE id NOT IN (
            SELECT MIN(id) 
            FROM library_author 
            GROUP BY name
        );
        
        -- Luego insertar autores
        INSERT INTO library_author (name, birth_date, photo) VALUES
        ('Gabriel García Márquez', '1927-03-06', 'author/jisoo.jpg'),
        ('Jorge Luis Borges', '1899-08-24', 'author/jisoo_ZHQxH9r.jpg'),
        ('Julio Cortázar', '1914-08-26', NULL),
        ('Isabel Allende', '1942-08-02', NULL)
        ON CONFLICT (id) DO NOTHING;
    END IF;
END $$;

-- Insertar libros (solo si la tabla book existe y hay autores)
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'library_book') AND
       EXISTS (SELECT 1 FROM library_author WHERE name = 'Gabriel García Márquez') THEN
        INSERT INTO library_book (title, author_id, published_year, is_available) VALUES
        ('Cien años de soledad', (SELECT id FROM library_author WHERE name = 'Gabriel García Márquez' LIMIT 1), '1967-05-30', TRUE),
        ('El Aleph', (SELECT id FROM library_author WHERE name = 'Jorge Luis Borges' LIMIT 1), '1949-06-01', FALSE),
        ('Rayuela', (SELECT id FROM library_author WHERE name = 'Julio Cortázar' LIMIT 1), '1963-06-28', TRUE),
        ('La casa de los espíritus', (SELECT id FROM library_author WHERE name = 'Isabel Allende' LIMIT 1), '1982-01-01', TRUE)
        ON CONFLICT (id) DO NOTHING;
    END IF;
END $$;

-- Insertar préstamos (solo si la tabla loan y book existen)
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'library_loan') AND
       EXISTS (SELECT 1 FROM library_book WHERE title = 'El Aleph') THEN
        INSERT INTO library_loan (book_id, borrower_name, loan_date, return_date) VALUES
        ((SELECT id FROM library_book WHERE title = 'El Aleph' LIMIT 1), 'María González', '2023-05-10', NULL),
        ((SELECT id FROM library_book WHERE title = 'Cien años de soledad' LIMIT 1), 'Carlos Sánchez', '2023-06-15', '2023-07-01')
        ON CONFLICT (id) DO NOTHING;
    END IF;
END $$;