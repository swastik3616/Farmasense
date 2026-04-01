# MongoDB Migration Strategy

Unlike SQL databases that demand rigid schema `ALTER` scripts, NoSQL migrations are heavily code-driven.

## Automated Schema Upgrades
Since we adopted **Beanie ODM** (powered by Pydantic):
1. **Adding Fields:** Simply add an `Optional[str] = None` field into your `app/models/documents.py`. Pydantic handles legacy documents gracefully.
2. **Deleting Fields:** Remove the property from `documents.py`. MongoDB retains the physical data without interfering.
3. **Indexing:** The inner `Settings` class dictates indices. 
   - Note: The first time `migrate.py` or the app starts, Beanie crawls the definitions and **generates indexes** in MongoDB safely in the background.

## Running Migrations
We provide `migrations/migrate.py` as an isolated administrative entrypoint.

Always perform data migrations *before* booting the server if you are making massive back-fills:

```bash
cd backend
python -m migrations.migrate
```

*This guarantees indexes are constructed without slowing down the active production request loop.*
