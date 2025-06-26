# PostgreSQL Migration Guide for EmpowerLex

This guide provides step-by-step instructions for migrating EmpowerLex from SQLite to PostgreSQL.

## Why Migrate to PostgreSQL?

### Advantages of PostgreSQL over SQLite:

1. **Concurrency**: Supports multiple simultaneous write operations
2. **Scalability**: Can handle large datasets and high traffic
3. **Advanced Features**: 
   - Full-text search capabilities
   - JSONB for efficient JSON operations
   - Advanced indexing (GIN, GiST)
   - Triggers and stored procedures
4. **Network Access**: Can be accessed remotely
5. **Production Ready**: Better for production deployments
6. **Performance**: Optimized query planner and parallel processing

## Prerequisites

1. **PostgreSQL Installation**:
   - Ubuntu/Debian: `sudo apt-get install postgresql postgresql-contrib`
   - macOS: `brew install postgresql`
   - Windows: Download from https://www.postgresql.org/download/windows/

2. **Python Dependencies**:
   ```bash
   pip install psycopg2-binary alembic
   ```

## Migration Steps

### Step 1: Install PostgreSQL Dependencies

```bash
cd EmpowerLex
pip install -r requirements.txt
```

### Step 2: Set Up PostgreSQL Database

#### Option A: Automated Setup
```bash
python scripts/setup_postgres.py
```

#### Option B: Manual Setup
```sql
-- Connect to PostgreSQL as superuser
sudo -u postgres psql

-- Create user and database
CREATE USER empowerlex WITH PASSWORD 'empowerlex_password';
CREATE DATABASE empowerlex OWNER empowerlex;
GRANT ALL PRIVILEGES ON DATABASE empowerlex TO empowerlex;
\q
```

### Step 3: Configure Environment

Create or update your `.env` file:

```env
# Database Configuration
DATABASE_URL=postgresql://empowerlex:empowerlex_password@localhost:5432/empowerlex

# PostgreSQL specific settings
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=empowerlex
POSTGRES_PASSWORD=empowerlex_password
POSTGRES_DB=empowerlex

# API Keys
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# JWT Settings
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# App Settings
DEBUG=True
APP_NAME=Legal Aid Platform
```

### Step 4: Run Database Migrations

```bash
# Create new migration for PostgreSQL schema
alembic revision --autogenerate -m "postgresql_migration"

# Apply migrations
alembic upgrade head
```

### Step 5: Migrate Data (Optional)

If you have existing data in SQLite:

```bash
# Run the migration script
python scripts/migrate_to_postgres.py
```

### Step 6: Test the Application

```bash
# Test database connection
python -c "from app.database import test_db_connection; test_db_connection()"

# Start the application
uvicorn app.main:app --reload
```

## Key Changes Made

### 1. Database Models

- **UUID Fields**: Changed `case_id` from String to UUID type
- **JSONB**: Replaced JSON with JSONB for better performance
- **Cascade Deletes**: Added proper cascade relationships
- **Indexing**: Added GIN indexes for JSONB fields

### 2. Database Connection

- **Connection Pooling**: Added PostgreSQL-specific connection pooling
- **Error Handling**: Enhanced error handling and logging
- **Configuration**: Environment-based database URL selection

### 3. Application Code

- **UUID Handling**: Updated routes to handle UUID fields properly
- **JSON Operations**: Removed manual JSON serialization/deserialization
- **Error Validation**: Added UUID format validation

## Performance Optimizations

### 1. Indexing Strategy

```sql
-- Composite indexes for common queries
CREATE INDEX idx_case_user_status ON cases(user_id, status);
CREATE INDEX idx_case_category_status ON cases(category, status);

-- GIN indexes for JSONB fields
CREATE INDEX idx_case_applicable_laws_gin ON cases USING gin(applicable_laws);
CREATE INDEX idx_case_suggested_ngos_gin ON cases USING gin(suggested_ngos);
CREATE INDEX idx_case_next_steps_gin ON cases USING gin(next_steps);
```

### 2. Connection Pooling

```python
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600
)
```

### 3. Query Optimization

- Use JSONB operators for efficient JSON queries
- Leverage PostgreSQL's built-in JSON functions
- Utilize proper indexing for common query patterns

## Troubleshooting

### Common Issues

1. **Connection Errors**:
   ```bash
   # Check PostgreSQL service
   sudo systemctl status postgresql
   
   # Check connection
   psql -h localhost -U empowerlex -d empowerlex
   ```

2. **Permission Errors**:
   ```sql
   -- Grant necessary permissions
   GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO empowerlex;
   GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO empowerlex;
   ```

3. **Migration Errors**:
   ```bash
   # Reset migrations
   alembic downgrade base
   alembic upgrade head
   ```

### Performance Monitoring

```sql
-- Check slow queries
SELECT query, mean_time, calls 
FROM pg_stat_statements 
ORDER BY mean_time DESC 
LIMIT 10;

-- Check index usage
SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;
```

## Production Deployment

### 1. Environment Variables

```env
DATABASE_URL=postgresql://user:password@host:port/database
POSTGRES_HOST=your-production-host
POSTGRES_PORT=5432
POSTGRES_USER=your-production-user
POSTGRES_PASSWORD=your-secure-password
POSTGRES_DB=empowerlex_prod
```

### 2. Security Considerations

- Use strong passwords
- Enable SSL connections
- Configure firewall rules
- Regular backups
- Monitor connection limits

### 3. Backup Strategy

```bash
# Create backup
pg_dump -h localhost -U empowerlex empowerlex > backup.sql

# Restore backup
psql -h localhost -U empowerlex empowerlex < backup.sql
```

## Rollback Plan

If you need to rollback to SQLite:

1. **Update Environment**:
   ```env
   DATABASE_URL=sqlite:///./app.db
   ```

2. **Restore Original Models**:
   - Revert UUID fields to String
   - Change JSONB back to JSON
   - Remove PostgreSQL-specific indexes

3. **Run Migrations**:
   ```bash
   alembic downgrade base
   alembic upgrade head
   ```

## Support

For issues related to PostgreSQL migration:

1. Check the logs: `tail -f /var/log/postgresql/postgresql-*.log`
2. Review application logs
3. Test database connectivity
4. Verify environment variables

## Next Steps

After successful migration:

1. **Monitor Performance**: Use PostgreSQL monitoring tools
2. **Optimize Queries**: Analyze slow queries and optimize
3. **Set Up Replication**: Consider read replicas for scaling
4. **Backup Strategy**: Implement automated backups
5. **Security Hardening**: Review and enhance security measures 