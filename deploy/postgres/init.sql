-- Veritabanı ve kullanıcı zaten Docker Compose environment değişkenleri ile oluşturuluyor.
-- Bu script, gelecekte gerekebilecek ek şema veya rol oluşturma işlemleri için bir yer tutucudur.
-- Örneğin, farklı servisler için farklı roller veya şemalar oluşturulabilir.

-- Örnek: Read-only bir kullanıcı oluşturma
-- CREATE ROLE readonly_user WITH LOGIN PASSWORD 'readonly_password';
-- GRANT CONNECT ON DATABASE ossdb TO readonly_user;
-- GRANT USAGE ON SCHEMA public TO readonly_user;
-- GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly_user;

SELECT 'Veritabanı ve kullanıcı Docker Compose tarafından başarıyla oluşturuldu.';
