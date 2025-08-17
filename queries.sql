-- 1) Providers per city
SELECT City, COUNT(*) AS provider_count
FROM Providers
GROUP BY City
ORDER BY provider_count DESC;

-- 2) Receivers per city
SELECT City, COUNT(*) AS receiver_count
FROM Receivers 
GROUP BY City
ORDER BY receiver_count DESC;

-- 3) Provider type with most donated quantity
SELECT p.Type AS provider_type, SUM(f.Quantity) AS total_quantity
FROM Food_Listings f    
JOIN Providers p ON f.Provider_ID = p.Provider_ID
GROUP BY p.Type
ORDER BY total_quantity DESC
LIMIT 1;

-- 4) Provider contact info for a given city (use parameter :city)
SELECT Provider_ID, Name, Contact, Address
FROM Providers
WHERE City = :city;

-- 5) Top receivers by number of claims
SELECT r.Receiver_ID, r.Name, COUNT(c.Claim_ID) AS num_claims
FROM Claims c
JOIN Receivers r ON c.Receiver_ID = r.Receiver_ID
GROUP BY r.Receiver_ID, r.Name
ORDER BY num_claims DESC
LIMIT 10;

-- 6) Total quantity of food available
SELECT COALESCE(SUM(Quantity),0) AS total_available_quantity
FROM Food_Listings;

-- 7) City with most food listings
SELECT Location AS city, COUNT(*) AS listings_count
FROM Food_Listings
GROUP BY Location
ORDER BY listings_count DESC
LIMIT 1;

-- 8) Most common food types (top 5)
SELECT Food_Type, COUNT(*) AS count_listings
FROM Food_Listings
GROUP BY Food_Type
ORDER BY count_listings DESC
LIMIT 5;

-- 9) Number of claims per food item
SELECT f.Food_ID, f.Food_Name, COUNT(c.Claim_ID) AS claim_count
FROM Food_Listings f
LEFT JOIN Claims c ON f.Food_ID = c.Food_ID
GROUP BY f.Food_ID, f.Food_Name
ORDER BY claim_count DESC;

-- 10) Provider with most completed claims
SELECT p.Provider_ID, p.Name, COUNT(c.Claim_ID) AS completed_claims
FROM Claims c
JOIN Food_Listings f ON c.Food_ID = f.Food_ID
JOIN Providers p ON f.Provider_ID = p.Provider_ID
WHERE c.Status = 'Completed'
GROUP BY p.Provider_ID, p.Name
ORDER BY completed_claims DESC
LIMIT 1;

-- 11) Percentage of claims by status
SELECT Status,
       COUNT(*) AS count_status,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM Claims), 2) AS pct_of_total
FROM Claims
GROUP BY Status;

-- 12) Average quantity claimed per receiver (completed claims only)
SELECT AVG(qty_claimed) AS avg_quantity_per_receiver FROM (
    SELECT c.Receiver_ID, SUM(f.Quantity) AS qty_claimed
    FROM Claims c
    JOIN Food_Listings f ON c.Food_ID = f.Food_ID
    WHERE c.Status = 'Completed'
    GROUP BY c.Receiver_ID
);

-- 13) Most claimed meal type
SELECT f.Meal_Type, COUNT(c.Claim_ID) AS claim_count
FROM Claims c
JOIN Food_Listings f ON c.Food_ID = f.Food_ID
GROUP BY f.Meal_Type
ORDER BY claim_count DESC;

-- 14) Total quantity donated by each provider (top 10)
SELECT p.Provider_ID, p.Name, SUM(f.Quantity) AS total_donated_quantity
FROM Food_Listings f
JOIN Providers p ON f.Provider_ID = p.Provider_ID
GROUP BY p.Provider_ID, p.Name
ORDER BY total_donated_quantity DESC
LIMIT 10;

-- 15) Food items near expiry within next 3 days
SELECT Food_ID, Food_Name, Quantity, Expiry_Date, Location, Provider_ID
FROM Food_Listings
WHERE DATE(Expiry_Date) <= DATE('now', '+3 days')
ORDER BY Expiry_Date ASC;
