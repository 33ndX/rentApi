# Car Rental API

Aplikacja przeznaczona do kompleksowego zarządzania wynajmem samochodów, obsługująca procesy od rejestracji po płatności i opinie.

## Lista funkcjonalności

- zarządzanie katalogiem dostępnych samochodów (CRUD),
- system rezerwacji z walidacją terminów i dostępności,
- integracja z bramką płatniczą Stripe (tryb sandbox),
- zarządzanie statusem rezerwacji (PENDING, CONFIRMED, IN_PROGRESS, COMPLETED, CANCELLED),
- system opinii i ocen dla wypożyczonych pojazdów,
- uwierzytelnianie użytkowników za pomocą tokenów JWT.

## Stos technologiczny

- Python 3.12.7
- FastAPI
- PostgreSQL 17.0
- SQLAlchemy 2.0 (Async ORM)
- Docker & Docker Compose

## Konfiguracja

Aplikacja wymaga pliku `.env` w folderze `rentapi/` o następującej strukturze:

```env
DB_HOST=db
DB_NAME=app
DB_USER=postgres
DB_PASSWORD=pass
STRIPE_SECRET_KEY=twoj_klucz_stripe
```
