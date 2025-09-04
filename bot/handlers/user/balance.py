import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession

from bot.services.balance_service import BalanceService
from bot.keyboards.inline.user_keyboards import get_balance_keyboard, get_back_to_main_menu_markup
from config.settings import Settings
from bot.middlewares.i18n import I18nMiddleware


router = Router()


@router.callback_query(F.data == "main_action:balance")
async def handle_balance_callback(
    callback: CallbackQuery,
    session: AsyncSession,
    settings: Settings,
    i18n: I18nMiddleware
):
    """Handle balance button click."""
    user_id = callback.from_user.id
    lang = callback.from_user.language_code or settings.DEFAULT_LANGUAGE
    
    try:
        balance_service = BalanceService(session)
        balance = await balance_service.get_balance(user_id)
        
        _ = lambda key, **kwargs: i18n.gettext(lang, key, **kwargs)
        
        message_text = _("balance_info_title") + "\n\n" + _("balance_current_amount", balance=balance)
        
        keyboard = get_balance_keyboard(lang, i18n, settings.tribute_balance_url)
        
        await callback.message.edit_text(
            text=message_text,
            reply_markup=keyboard,
            parse_mode="HTML"
        )
        await callback.answer()
        
    except Exception as e:
        logging.error(f"Error handling balance callback for user {user_id}: {e}")
        _ = lambda key, **kwargs: i18n.gettext(lang, key, **kwargs)
        await callback.message.edit_text(
            text=_("balance_operation_failed"),
            reply_markup=get_back_to_main_menu_markup(lang, i18n),
            parse_mode="HTML"
        )
        await callback.answer()


@router.message(Command("balance"))
async def handle_balance_command(
    message: Message,
    session: AsyncSession,
    settings: Settings,
    i18n: I18nMiddleware
):
    """Handle /balance command."""
    user_id = message.from_user.id
    lang = message.from_user.language_code or settings.DEFAULT_LANGUAGE
    
    try:
        balance_service = BalanceService(session)
        balance = await balance_service.get_balance(user_id)
        
        _ = lambda key, **kwargs: i18n.gettext(lang, key, **kwargs)
        
        message_text = _("balance_info_title") + "\n\n" + _("balance_current_amount", balance=balance)
        
        keyboard = get_balance_keyboard(lang, i18n, settings.tribute_balance_url)
        
        await message.answer(
            text=message_text,
            reply_markup=keyboard,
            parse_mode="HTML"
        )
        
    except Exception as e:
        logging.error(f"Error handling balance command for user {user_id}: {e}")
        _ = lambda key, **kwargs: i18n.gettext(lang, key, **kwargs)
        await message.answer(
            text=_("balance_operation_failed"),
            reply_markup=get_back_to_main_menu_markup(lang, i18n),
            parse_mode="HTML"
        )
