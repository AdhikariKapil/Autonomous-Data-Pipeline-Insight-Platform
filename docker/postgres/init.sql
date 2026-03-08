--DATABASE SEEDING
--This runs automatically for the first time postgres starts

--Create the book table
CREATE TABLE IF NOT EXISTS books (
  id SERIAL PRIMARY KEY,
  title VARCHAR(200) NOT NULL,
  author VARCHAR(100) NOT NULL,
  year INTEGER NOT NULL,
  rating FLOAT,
  notes TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Insert some sample books
INSERT INTO books (title, author, year, rating, notes) VALUES
('The Great Gatsby', 'F. Scott Fitzgerald', 1925, 4.5, 'Classic American novel'),
('1984', 'George Orwell', 1949, 4.8, 'Dystopian masterpiece'),
('To Kill a Mockingbird', 'Harper Lee', 1960, 4.7, 'Powerful story about justice'),
('Dune', 'Frank Herbert', 1965, 4.9, 'Best sci-fi ever'),
('The Hobbit', 'J.R.R. Tolkien', 1937, 4.8, 'Great adventure story');


--Create a function to update updated_at automatically
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = CURRENT_TIMESTAMP;
  RETURN NEW;
END;
$$ language 'plpgsql';


--Create a trigger to automatically update updated_at
--Before any row is updated in books,
--run update_updated_at_column()
CREATE TRIGGER update_books_updated_at
  BEFORE UPDATE ON books
  FOR EACH ROW
  EXECUTE FUNCTION update_books_updated_at();


--Creating indexes
CREATE INDEX idx_books_author ON books(author)
CREATE INDEX idx_books_years ON books(year)
CREATE INDEX idx_books_rating ON books(rating)


--Show that everything works
DO $$
BEGIN
  RAISE NOTICE '✔️Database initialized successfully with sample books.';
END $$
