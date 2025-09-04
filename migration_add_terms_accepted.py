#!/usr/bin/env python3
"""
Migration script to add terms_accepted field to users table.
Run this script to update the database schema.
"""

import asyncio
import logging
from sqlalchemy import text
from db.database_setup import get_async_session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def migrate_add_terms_accepted():
    """Add terms_accepted column to users table."""
    async for session in get_async_session():
        try:
            # Check if column already exists
            check_query = text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'users' AND column_name = 'terms_accepted'
            """)
            result = await session.execute(check_query)
            existing_column = result.fetchone()
            
            if existing_column:
                logger.info("Column 'terms_accepted' already exists in users table")
                return
            
            # Add the column
            alter_query = text("""
                ALTER TABLE users 
                ADD COLUMN terms_accepted BOOLEAN NOT NULL DEFAULT FALSE
            """)
            await session.execute(alter_query)
            await session.commit()
            
            logger.info("Successfully added 'terms_accepted' column to users table")
            
        except Exception as e:
            logger.error(f"Error during migration: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()
        break  # Only process one session


if __name__ == "__main__":
    asyncio.run(migrate_add_terms_accepted())
