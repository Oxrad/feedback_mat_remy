# Script pour initialiser la base de données via psql (si Python échoue)
# Exécuter dans le dossier backend/

Write-Host "`n=== Initialisation de la base via PostgreSQL (psql) ===" -ForegroundColor Cyan

# Vérifier si psql est disponible
Write-Host "`n1. Vérification de psql..." -ForegroundColor Yellow
try {
    $psqlVersion = psql --version
    Write-Host "   ✅ psql trouvé: $psqlVersion" -ForegroundColor Green
} catch {
    Write-Host "   ❌ psql n'est pas dans le PATH" -ForegroundColor Red
    Write-Host "`n   Pour ajouter psql au PATH:" -ForegroundColor Yellow
    Write-Host "   1. Trouver le dossier bin de PostgreSQL (ex: C:\Program Files\PostgreSQL\15\bin)" -ForegroundColor White
    Write-Host "   2. Ajouter ce chemin à la variable PATH" -ForegroundColor White
    Write-Host "   3. Redémarrer PowerShell" -ForegroundColor White
    exit 1
}

# Vérifier si la base existe
Write-Host "`n2. Vérification de la base de données..." -ForegroundColor Yellow
$dbCheck = psql -U postgres -lqt 2>$null | Select-String -Pattern "feelback_db"
if ($dbCheck) {
    Write-Host "   ✅ Base 'feelback_db' trouvée" -ForegroundColor Green
} else {
    Write-Host "   ❌ Base 'feelback_db' non trouvée" -ForegroundColor Red
    Write-Host "   Création de la base..." -ForegroundColor Yellow
    psql -U postgres -c "CREATE DATABASE feelback_db ENCODING 'UTF8';"
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ Base créée avec succès" -ForegroundColor Green
    } else {
        Write-Host "   ❌ Échec de la création de la base" -ForegroundColor Red
        exit 1
    }
}

# Créer le fichier SQL s'il n'existe pas
Write-Host "`n3. Préparation du script SQL..." -ForegroundColor Yellow
if (-not (Test-Path "init_feelback.sql")) {
    @'
-- Script SQL pour créer la base de données FeelBack

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

INSERT INTO order_status (id, description) 
VALUES
    (1, 'En preparation'),
    (2, 'Expediee'),
    (3, 'En cours de livraison'),
    (4, 'Livree'),
    (5, 'Retournee')
ON CONFLICT (id) DO NOTHING;

INSERT INTO questions (id, title, maximum_grade) 
VALUES
    (1, 'Evaluer de 1 a 5 le respect du delai de livraison', 5),
    (2, 'Evaluer de 1 a 5 l etat de votre colis a sa reception', 5),
    (3, 'Evaluer de 1 a 5 le comportement du livreur', 5)
ON CONFLICT (id) DO NOTHING;

SELECT 'Nombre de statuts:' AS Info, COUNT(*) AS Total FROM order_status;
SELECT 'Nombre de questions:' AS Info, COUNT(*) AS Total FROM questions;
'@ | Out-File -FilePath init_feelback.sql -Encoding UTF8 -NoNewline
    Write-Host "   ✅ Fichier init_feelback.sql créé" -ForegroundColor Green
} else {
    Write-Host "   ✅ Fichier init_feelback.sql trouvé" -ForegroundColor Green
}

# Exécuter le script SQL
Write-Host "`n4. Exécution du script SQL..." -ForegroundColor Yellow
$env:PGCLIENTENCODING = "UTF8"
psql -U postgres -d feelback_db -f init_feelback.sql

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ ✅ ✅ Base de données initialisée avec succès !" -ForegroundColor Green
    
    # Vérification
    Write-Host "`n5. Vérification des tables..." -ForegroundColor Yellow
    psql -U postgres -d feelback_db -c "\dt"
    
    Write-Host "`n6. Contenu des tables..." -ForegroundColor Yellow
    Write-Host "`nStatuts de commande:" -ForegroundColor Cyan
    psql -U postgres -d feelback_db -c "SELECT * FROM order_status ORDER BY id;"
    
    Write-Host "`nQuestions:" -ForegroundColor Cyan
    psql -U postgres -d feelback_db -c "SELECT * FROM questions ORDER BY id;"
    
    Write-Host "`n=== Initialisation terminée ===" -ForegroundColor Green
    Write-Host "`nVous pouvez maintenant:" -ForegroundColor White
    Write-Host "   1. Tester l'API: fastapi dev main.py" -ForegroundColor Yellow
    Write-Host "   2. Accéder à http://localhost:8000" -ForegroundColor Yellow
    Write-Host "   3. Documentation: http://localhost:8000/docs" -ForegroundColor Yellow
    
} else {
    Write-Host "`n❌ Échec de l'initialisation" -ForegroundColor Red
    Write-Host "`nDépannage:" -ForegroundColor Yellow
    Write-Host "   1. Vérifiez que PostgreSQL est démarré" -ForegroundColor White
    Write-Host "   2. Vérifiez le mot de passe de l'utilisateur 'postgres'" -ForegroundColor White
    Write-Host "   3. Essayez de vous connecter manuellement:" -ForegroundColor White
    Write-Host "      psql -U postgres -d feelback_db" -ForegroundColor Gray
}