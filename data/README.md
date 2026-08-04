# Data Directory

This directory contains runtime data used by AI Career Manager.

Contents are **not** source code and should generally **not** be committed to Git.

## SQLite Database

The primary database is:

```
ai_career_manager.db
```

It is created automatically by:

```python
initialize_database()
```

No manual setup is required.

---

## Inspecting the Database

### List tables

```bash
sqlite3 data/ai_career_manager.db
```

```sql
.tables
```

---

### View table schema

```sql
.schema jobs
```

---

### View all rows

```sql
SELECT * FROM jobs;
```

---

### Count jobs

```sql
SELECT COUNT(*) FROM jobs;
```

---

### Exit SQLite

```sql
.quit
```

---

## Development Notes

The database schema is managed by the application.

Current milestone:

**Milestone 3 – Job History & Application Tracking**

Current database responsibilities:

- store original job descriptions
- preserve job history
- support future application tracking

Additional tables and fields will be added incrementally as the project evolves.

---

## Git

The database file should not normally be committed.

Suggested `.gitignore` entries:

```gitignore
data/*.db
data/*.sqlite
data/*.sqlite3
```

---

## Future

This directory may eventually contain:

```
data/
    ai_career_manager.db
    backups/
    exports/
    imports/
```

as AI Career Manager grows.