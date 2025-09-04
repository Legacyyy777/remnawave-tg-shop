import logging
from typing import Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from db.dal.user_dal import (
    get_user_balance,
    update_user_balance,
    add_to_user_balance,
    subtract_from_user_balance,
    get_user_by_id
)


class BalanceService:
    """Service for managing user balance operations."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_balance(self, user_id: int) -> float:
        """Get user's current balance."""
        return await get_user_balance(self.session, user_id)
    
    async def set_balance(self, user_id: int, amount: float) -> bool:
        """Set user's balance to a specific amount."""
        if amount < 0:
            logging.warning(f"Attempted to set negative balance for user {user_id}: {amount}")
            return False
        
        success = await update_user_balance(self.session, user_id, amount)
        if success:
            logging.info(f"Set balance for user {user_id} to {amount}")
        return success
    
    async def add_balance(self, user_id: int, amount: float) -> Optional[float]:
        """Add amount to user's balance and return new balance."""
        if amount <= 0:
            logging.warning(f"Attempted to add non-positive amount to user {user_id}: {amount}")
            return None
        
        new_balance = await add_to_user_balance(self.session, user_id, amount)
        if new_balance is not None:
            logging.info(f"Added {amount} to user {user_id} balance. New balance: {new_balance}")
        return new_balance
    
    async def subtract_balance(self, user_id: int, amount: float) -> Optional[float]:
        """Subtract amount from user's balance if sufficient funds available."""
        if amount <= 0:
            logging.warning(f"Attempted to subtract non-positive amount from user {user_id}: {amount}")
            return None
        
        new_balance = await subtract_from_user_balance(self.session, user_id, amount)
        if new_balance is not None:
            logging.info(f"Subtracted {amount} from user {user_id} balance. New balance: {new_balance}")
        else:
            logging.warning(f"Insufficient balance for user {user_id} to subtract {amount}")
        return new_balance
    
    async def can_afford(self, user_id: int, amount: float) -> bool:
        """Check if user has sufficient balance for a purchase."""
        current_balance = await self.get_balance(user_id)
        return current_balance >= amount
    
    async def get_balance_info(self, user_id: int) -> Dict[str, Any]:
        """Get comprehensive balance information for a user."""
        user = await get_user_by_id(self.session, user_id)
        if not user:
            return {"error": "User not found"}
        
        return {
            "user_id": user_id,
            "balance": user.balance or 0.0,
            "username": user.username,
            "first_name": user.first_name
        }
