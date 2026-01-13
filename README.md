# Car Rental API

Aplikacja przeznaczona do zarządzania wynajmem samochodów, obsługująca procesy od rejestracji po płatności i opinie.

## Lista funkcjonalności

- zarządzanie ofertami samochodów(CRUD),
- system rezerwacji z walidacją terminów, dostępności i zarządzania statusem,
- system opinii i ocen dla wypożyczonych pojazdów,
- integracja z bramką płatniczą Stripe (tryb sandbox),

## Stos technologiczny

- Python 3.12.7
- PostgreSQL 17.0
- Docker

## Konfiguracja

Aplikacja wymaga pliku `.env` w folderze `rentapi/` o następującej strukturze:

```env
DB_HOST="db"
DB_NAME="app"
DB_USER="postgres"
DB_PASSWORD="pass"
STRIPE_SECRET_KEY="sk_test_klucz"
```
