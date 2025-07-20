-- Insertar autores (solo si la tabla author existe)
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'library_author') THEN
        -- Insertar Gabriel García Márquez si no existe
        IF NOT EXISTS (SELECT 1 FROM library_author WHERE name = 'Gabriel García Márquez') THEN
            INSERT INTO library_author (name, birth_date, photo) 
            VALUES ('Gabriel García Márquez', '1927-03-06', 'author/jisoo.jpg');
        END IF;
        
        -- Insertar Jorge Luis Borges si no existe
        IF NOT EXISTS (SELECT 1 FROM library_author WHERE name = 'Jorge Luis Borges') THEN
            INSERT INTO library_author (name, birth_date, photo) 
            VALUES ('Jorge Luis Borges', '1899-08-24', 'author/jisoo_ZHQxH9r.jpg');
        END IF;
        
        -- Insertar Julio Cortázar si no existe
        IF NOT EXISTS (SELECT 1 FROM library_author WHERE name = 'Julio Cortázar') THEN
            INSERT INTO library_author (name, birth_date, photo) 
            VALUES ('Julio Cortázar', '1914-08-26', NULL);
        END IF;
        
        -- Insertar Isabel Allende si no existe
        IF NOT EXISTS (SELECT 1 FROM library_author WHERE name = 'Isabel Allende') THEN
            INSERT INTO library_author (name, birth_date, photo) 
            VALUES ('Isabel Allende', '1942-08-02', NULL);
        END IF;
    END IF;
END $$;

-- Insertar libros (solo si la tabla book existe y hay autores)
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'library_book') AND
       EXISTS (SELECT 1 FROM library_author WHERE name = 'Gabriel García Márquez') THEN
        
        -- Insertar Cien años de soledad si no existe
        IF NOT EXISTS (SELECT 1 FROM library_book WHERE title = 'Cien años de soledad') THEN
            INSERT INTO library_book (title, author_id, published_year, is_available) 
            VALUES (
                'Cien años de soledad', 
                (SELECT id FROM library_author WHERE name = 'Gabriel García Márquez' LIMIT 1), 
                '1967-05-30', 
                TRUE
            );
        END IF;
        
        -- Insertar El Aleph si no existe
        IF NOT EXISTS (SELECT 1 FROM library_book WHERE title = 'El Aleph') THEN
            INSERT INTO library_book (title, author_id, published_year, is_available) 
            VALUES (
                'El Aleph', 
                (SELECT id FROM library_author WHERE name = 'Jorge Luis Borges' LIMIT 1), 
                '1949-06-01', 
                FALSE
            );
        END IF;
        
        -- Insertar Rayuela si no existe
        IF NOT EXISTS (SELECT 1 FROM library_book WHERE title = 'Rayuela') THEN
            INSERT INTO library_book (title, author_id, published_year, is_available) 
            VALUES (
                'Rayuela', 
                (SELECT id FROM library_author WHERE name = 'Julio Cortázar' LIMIT 1), 
                '1963-06-28', 
                TRUE
            );
        END IF;
        
        -- Insertar La casa de los espíritus si no existe
        IF NOT EXISTS (SELECT 1 FROM library_book WHERE title = 'La casa de los espíritus') THEN
            INSERT INTO library_book (title, author_id, published_year, is_available) 
            VALUES (
                'La casa de los espíritus', 
                (SELECT id FROM library_author WHERE name = 'Isabel Allende' LIMIT 1), 
                '1982-01-01', 
                TRUE
            );
        END IF;
    END IF;
END $$;

-- Insertar préstamos (solo si la tabla loan y book existen)
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'library_loan') AND
       EXISTS (SELECT 1 FROM library_book WHERE title = 'El Aleph') THEN
        
        -- Verificar si el préstamo de 'El Aleph' ya existe
        IF NOT EXISTS (
            SELECT 1 FROM library_loan 
            WHERE book_id = (SELECT id FROM library_book WHERE title = 'El Aleph' LIMIT 1)
            AND loan_date = '2023-05-10'
        ) THEN
            INSERT INTO library_loan (book_id, borrower_name, loan_date, return_date) 
            VALUES (
                (SELECT id FROM library_book WHERE title = 'El Aleph' LIMIT 1), 
                'María González', 
                '2023-05-10', 
                NULL
            );
        END IF;
        
        -- Verificar si el préstamo de 'Cien años de soledad' ya existe
        IF NOT EXISTS (
            SELECT 1 FROM library_loan 
            WHERE book_id = (SELECT id FROM library_book WHERE title = 'Cien años de soledad' LIMIT 1)
            AND loan_date = '2023-06-15'
        ) THEN
            INSERT INTO library_loan (book_id, borrower_name, loan_date, return_date) 
            VALUES (
                (SELECT id FROM library_book WHERE title = 'Cien años de soledad' LIMIT 1), 
                'Carlos Sánchez', 
                '2023-06-15', 
                '2023-07-01'
            );
        END IF;
    END IF;
END $$;