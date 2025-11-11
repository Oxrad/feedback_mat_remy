CREATE TABLE IF NOT EXISTS order_status (
    id SERIAL PRIMARY KEY,
    description VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    tracking_number VARCHAR(50) UNIQUE NOT NULL,
    shipping_date DATE NOT NULL,
    estimated_delivery_date DATE NOT NULL,
    order_status_id INTEGER NOT NULL REFERENCES order_status(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS questions (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    maximum_grade INTEGER DEFAULT 5 NOT NULL
);

CREATE TABLE IF NOT EXISTS feedbacks (
    id SERIAL PRIMARY KEY,
    order_id INTEGER UNIQUE NOT NULL REFERENCES orders(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS grades (
    id SERIAL PRIMARY KEY,
    question_id INTEGER NOT NULL REFERENCES questions(id),
    feedback_id INTEGER NOT NULL REFERENCES feedbacks(id),
    grade INTEGER NOT NULL
);

INSERT INTO order_status (id, description) VALUES
    (1, 'En preparation'),
    (2, 'Expediee'),
    (3, 'En cours de livraison'),
    (4, 'Livree'),
    (5, 'Retournee')
ON CONFLICT (id) DO NOTHING;

INSERT INTO questions (id, title, maximum_grade) VALUES
    (1, 'Evaluer de 1 a 5 le respect du delai de livraison', 5),
    (2, 'Evaluer de 1 a 5 l etat de votre colis a sa reception', 5),
    (3, 'Evaluer de 1 a 5 le comportement du livreur', 5)
ON CONFLICT (id) DO NOTHING;

SELECT 'Tables creees!' AS Status;
SELECT COUNT(*) AS "Nombre de statuts" FROM order_status;
SELECT COUNT(*) AS "Nombre de questions" FROM questions;
