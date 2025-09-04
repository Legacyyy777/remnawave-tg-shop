"""
Database migrations module.
Automatically runs migrations on startup.
"""

import logging
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from db.database_setup import get_async_session

logger = logging.getLogger(__name__)

# List of all migrations with their version numbers
MIGRATIONS = [
    ("001_add_terms_accepted", _migrate_add_terms_accepted),
]


async def run_migrations():
    """Run all pending database migrations."""
    logger.info("Starting database migrations...")
    
    async for session in get_async_session():
        try:
            # Create migrations table if it doesn't exist
            await _create_migrations_table(session)
            
            # Get list of applied migrations
            applied_migrations = await _get_applied_migrations(session)
            
            # Run pending migrations
            for migration_id, migration_func in MIGRATIONS:
                if migration_id not in applied_migrations:
                    logger.info(f"Running migration: {migration_id}")
                    await migration_func(session)
                    await _mark_migration_applied(session, migration_id)
                    logger.info(f"Migration {migration_id} completed")
                else:
                    logger.info(f"Migration {migration_id} already applied, skipping")
            
            logger.info("All migrations completed successfully")
            
        except Exception as e:
            logger.error(f"Migration failed: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()
        break


async def _create_migrations_table(session: AsyncSession):
    """Create migrations table to track applied migrations."""
    await session.execute(text("""
        CREATE TABLE IF NOT EXISTS migrations (
            id SERIAL PRIMARY KEY,
            migration_id VARCHAR(255) UNIQUE NOT NULL,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """))
    await session.commit()


async def _get_applied_migrations(session: AsyncSession) -> set:
    """Get list of already applied migrations."""
    result = await session.execute(text("SELECT migration_id FROM migrations"))
    return {row[0] for row in result.fetchall()}


async def _mark_migration_applied(session: AsyncSession, migration_id: str):
    """Mark migration as applied."""
    await session.execute(text("""
        INSERT INTO migrations (migration_id) VALUES (:migration_id)
    """), {"migration_id": migration_id})
    await session.commit()


async def _migrate_add_terms_accepted(session: AsyncSession):
    """Add terms_accepted column to users table if it doesn't exist."""
    try:
        # Check if column already exists
        result = await session.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'users' AND column_name = 'terms_accepted'
        """))
        existing_column = result.fetchone()
        
        if existing_column:
            logger.info("Column 'terms_accepted' already exists in users table")
            return
        
        # Add the column
        await session.execute(text("""
            ALTER TABLE users 
            ADD COLUMN terms_accepted BOOLEAN NOT NULL DEFAULT FALSE
        """))
        await session.commit()
        
        logger.info("Successfully added 'terms_accepted' column to users table")
        
    except Exception as e:
        logger.error(f"Error adding terms_accepted column: {e}")
        await session.rollback()
        raise


# Future migrations can be added here
# async def _migrate_add_new_feature(session: AsyncSession):
#     """Example of future migration."""
#     pass
