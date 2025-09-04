import logging
from typing import TYPE_CHECKING
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from config.settings import Settings
from bot.middlewares.i18n import I18nMiddleware
from bot.states.user_states import TermsAcceptanceStates
from bot.keyboards.inline.user_keyboards import get_terms_acceptance_keyboard, get_back_to_main_menu_markup
from db.dal import user_dal

if TYPE_CHECKING:
    from bot.services.subscription_service import SubscriptionService

router = Router(name="user_terms_router")


async def show_terms_acceptance(
    target_event: Message | CallbackQuery,
    settings: Settings,
    i18n_data: dict,
    session: AsyncSession,
    subscription_service: SubscriptionService = None
):
    """Show terms acceptance dialog."""
    current_lang = i18n_data.get("current_language", settings.DEFAULT_LANGUAGE)
    i18n: I18nMiddleware = i18n_data.get("i18n_instance")
    
    if not i18n:
        logging.error("i18n_instance missing in show_terms_acceptance")
        return
    
    _ = lambda key, **kwargs: i18n.gettext(current_lang, key, **kwargs)
    
    text = f"**{_('terms_acceptance_title')}**\n\n{_('terms_acceptance_message')}"
    keyboard = get_terms_acceptance_keyboard(current_lang, i18n, settings)
    
    if isinstance(target_event, Message):
        await target_event.answer(text, reply_markup=keyboard, parse_mode="Markdown")
    elif isinstance(target_event, CallbackQuery):
        await target_event.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
        await target_event.answer()


@router.callback_query(F.data == "terms:accept")
async def handle_terms_accept(
    callback: CallbackQuery,
    state: FSMContext,
    settings: Settings,
    i18n_data: dict,
    session: AsyncSession,
    subscription_service: SubscriptionService = None
):
    """Handle terms acceptance."""
    user_id = callback.from_user.id
    current_lang = i18n_data.get("current_language", settings.DEFAULT_LANGUAGE)
    i18n: I18nMiddleware = i18n_data.get("i18n_instance")
    
    if not i18n:
        logging.error("i18n_instance missing in handle_terms_accept")
        await callback.answer("Error: Language service unavailable.", show_alert=True)
        return
    
    _ = lambda key, **kwargs: i18n.gettext(current_lang, key, **kwargs)
    
    try:
        # Update user's terms acceptance status
        await user_dal.update_user(session, user_id, {"terms_accepted": True})
        await session.commit()
        
        # Clear state
        await state.clear()
        
        # Send success message and show main menu
        from .start import send_main_menu
        await send_main_menu(callback, settings, i18n_data, subscription_service, session, is_edit=True)
        await callback.answer()
        
        logging.info(f"User {user_id} accepted terms of service")
        
    except Exception as e:
        logging.error(f"Error accepting terms for user {user_id}: {e}")
        await callback.answer(_("error_occurred_try_again"), show_alert=True)


@router.callback_query(F.data == "terms:decline")
async def handle_terms_decline(
    callback: CallbackQuery,
    state: FSMContext,
    settings: Settings,
    i18n_data: dict,
    session: AsyncSession
):
    """Handle terms decline."""
    current_lang = i18n_data.get("current_language", settings.DEFAULT_LANGUAGE)
    i18n: I18nMiddleware = i18n_data.get("i18n_instance")
    
    if not i18n:
        logging.error("i18n_instance missing in handle_terms_decline")
        await callback.answer("Error: Language service unavailable.", show_alert=True)
        return
    
    _ = lambda key, **kwargs: i18n.gettext(current_lang, key, **kwargs)
    
    # Clear state
    await state.clear()
    
    # Send decline message
    await callback.message.edit_text(
        text=_("terms_declined_message"),
        reply_markup=None,
        parse_mode="HTML"
    )
    await callback.answer()
    
    logging.info(f"User {callback.from_user.id} declined terms of service")
