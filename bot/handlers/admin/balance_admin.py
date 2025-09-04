import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession

from bot.services.balance_service import BalanceService
from db.dal.user_dal import get_user_by_id, get_user_by_username
from bot.keyboards.inline.admin_keyboards import get_admin_panel_keyboard
from bot.middlewares.i18n import I18nMiddleware
from config.settings import Settings


router = Router()


class BalanceManagementStates(StatesGroup):
    waiting_for_user = State()
    waiting_for_add_amount = State()
    waiting_for_subtract_amount = State()
    waiting_for_set_amount = State()


@router.callback_query(F.data == "admin_balance_management")
async def handle_balance_management_callback(
    callback: CallbackQuery,
    settings: Settings,
    **data
):
    """Handle balance management button click."""
    i18n_data = data.get("i18n_data", {})
    i18n = i18n_data.get("i18n_instance")
    current_language = i18n_data.get("current_language", settings.DEFAULT_LANGUAGE)
    
    if not i18n:
        logging.error("I18n middleware not found in data")
        await callback.answer("Error: I18n not available")
        return
    
    _ = lambda key, **kwargs: i18n.gettext(current_language, key, **kwargs)
    
    await callback.message.edit_text(
        text=_("admin_balance_user_prompt"),
        reply_markup=None,
        parse_mode="HTML"
    )
    await callback.answer()
    
    await callback.message.answer(
        text=_("admin_balance_user_prompt"),
        parse_mode="HTML"
    )
    
    # Set state to wait for user input
    from aiogram.fsm.context import FSMContext
    state = FSMContext(callback.bot, callback.from_user.id, callback.message.chat.id)
    await state.set_state(BalanceManagementStates.waiting_for_user)


@router.message(BalanceManagementStates.waiting_for_user)
async def handle_user_input(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
    settings: Settings,
    **data
):
    """Handle user ID or username input for balance management."""
    i18n_data = data.get("i18n_data", {})
    i18n = i18n_data.get("i18n_instance")
    current_language = i18n_data.get("current_language", settings.DEFAULT_LANGUAGE)
    
    if not i18n:
        logging.error("I18n middleware not found in data")
        await message.answer("Error: I18n not available")
        return
    
    _ = lambda key, **kwargs: i18n.gettext(current_language, key, **kwargs)
    
    user_input = message.text.strip()
    
    # Try to find user by ID or username
    user = None
    try:
        # Try as user ID first
        if user_input.isdigit():
            user = await get_user_by_id(session, int(user_input))
        else:
            # Try as username
            clean_username = user_input.lstrip("@")
            user = await get_user_by_username(session, clean_username)
    except Exception as e:
        logging.error(f"Error finding user {user_input}: {e}")
    
    if not user:
        await message.answer(_("admin_balance_user_not_found"))
        return
    
    # Store user info in state
    await state.update_data(
        target_user_id=user.user_id,
        target_user_display=f"@{user.username}" if user.username else f"{user.first_name or 'Unknown'}"
    )
    
    # Get current balance
    balance_service = BalanceService(session)
    current_balance = await balance_service.get_balance(user.user_id)
    
    # Show user info and options
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    builder = InlineKeyboardBuilder()
    
    builder.button(
        text=_("admin_balance_add_button"),
        callback_data="admin_balance_add"
    )
    builder.button(
        text=_("admin_balance_subtract_button"),
        callback_data="admin_balance_subtract"
    )
    builder.button(
        text=_("admin_balance_set_button"),
        callback_data="admin_balance_set"
    )
    builder.button(
        text=_("back_to_admin_panel_button"),
        callback_data="admin_panel"
    )
    builder.adjust(1)
    
    user_info_text = _(
        "admin_balance_user_info",
        user_display=f"@{user.username}" if user.username else f"{user.first_name or 'Unknown'}",
        balance=current_balance
    )
    
    await message.answer(
        text=user_info_text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )
    
    await state.clear()


@router.callback_query(F.data == "admin_balance_add")
async def handle_balance_add_callback(
    callback: CallbackQuery,
    state: FSMContext,
    settings: Settings,
    **data
):
    """Handle add balance button click."""
    i18n_data = data.get("i18n_data", {})
    i18n = i18n_data.get("i18n_instance")
    current_language = i18n_data.get("current_language", settings.DEFAULT_LANGUAGE)
    
    if not i18n:
        logging.error("I18n middleware not found in data")
        await callback.answer("Error: I18n not available")
        return
    
    _ = lambda key, **kwargs: i18n.gettext(current_language, key, **kwargs)
    
    state_data = await state.get_data()
    user_display = state_data.get("target_user_display", "Unknown")
    
    await callback.message.edit_text(
        text=_("admin_balance_add_prompt", user_display=user_display),
        reply_markup=None,
        parse_mode="HTML"
    )
    await callback.answer()
    
    await state.set_state(BalanceManagementStates.waiting_for_add_amount)


@router.callback_query(F.data == "admin_balance_subtract")
async def handle_balance_subtract_callback(
    callback: CallbackQuery,
    state: FSMContext,
    settings: Settings,
    **data
):
    """Handle subtract balance button click."""
    i18n_data = data.get("i18n_data", {})
    i18n = i18n_data.get("i18n_instance")
    current_language = i18n_data.get("current_language", settings.DEFAULT_LANGUAGE)
    
    if not i18n:
        logging.error("I18n middleware not found in data")
        await callback.answer("Error: I18n not available")
        return
    
    _ = lambda key, **kwargs: i18n.gettext(current_language, key, **kwargs)
    
    state_data = await state.get_data()
    user_display = state_data.get("target_user_display", "Unknown")
    
    await callback.message.edit_text(
        text=_("admin_balance_subtract_prompt", user_display=user_display),
        reply_markup=None,
        parse_mode="HTML"
    )
    await callback.answer()
    
    await state.set_state(BalanceManagementStates.waiting_for_subtract_amount)


@router.callback_query(F.data == "admin_balance_set")
async def handle_balance_set_callback(
    callback: CallbackQuery,
    state: FSMContext,
    settings: Settings,
    **data
):
    """Handle set balance button click."""
    i18n_data = data.get("i18n_data", {})
    i18n = i18n_data.get("i18n_instance")
    current_language = i18n_data.get("current_language", settings.DEFAULT_LANGUAGE)
    
    if not i18n:
        logging.error("I18n middleware not found in data")
        await callback.answer("Error: I18n not available")
        return
    
    _ = lambda key, **kwargs: i18n.gettext(current_language, key, **kwargs)
    
    state_data = await state.get_data()
    user_display = state_data.get("target_user_display", "Unknown")
    
    await callback.message.edit_text(
        text=_("admin_balance_set_prompt", user_display=user_display),
        reply_markup=None,
        parse_mode="HTML"
    )
    await callback.answer()
    
    await state.set_state(BalanceManagementStates.waiting_for_set_amount)


@router.message(BalanceManagementStates.waiting_for_add_amount)
async def handle_add_amount_input(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
    settings: Settings,
    **data
):
    """Handle add amount input."""
    i18n_data = data.get("i18n_data", {})
    i18n = i18n_data.get("i18n_instance")
    current_language = i18n_data.get("current_language", settings.DEFAULT_LANGUAGE)
    
    if not i18n:
        logging.error("I18n middleware not found in data")
        await message.answer("Error: I18n not available")
        return
    
    _ = lambda key, **kwargs: i18n.gettext(current_language, key, **kwargs)
    
    try:
        amount = float(message.text.strip())
        if amount <= 0:
            await message.answer(_("admin_balance_invalid_amount"))
            return
    except ValueError:
        await message.answer(_("admin_balance_invalid_amount"))
        return
    
    state_data = await state.get_data()
    target_user_id = state_data.get("target_user_id")
    
    if not target_user_id:
        await message.answer(_("admin_balance_user_not_found"))
        await state.clear()
        return
    
    try:
        balance_service = BalanceService(session)
        new_balance = await balance_service.add_balance(target_user_id, amount)
        
        if new_balance is not None:
            await message.answer(
                _("balance_add_success", amount=amount, new_balance=new_balance),
                parse_mode="HTML"
            )
        else:
            await message.answer(_("admin_balance_operation_error"))
    except Exception as e:
        logging.error(f"Error adding balance: {e}")
        await message.answer(_("admin_balance_operation_error"))
    
    await state.clear()


@router.message(BalanceManagementStates.waiting_for_subtract_amount)
async def handle_subtract_amount_input(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
    settings: Settings,
    **data
):
    """Handle subtract amount input."""
    i18n_data = data.get("i18n_data", {})
    i18n = i18n_data.get("i18n_instance")
    current_language = i18n_data.get("current_language", settings.DEFAULT_LANGUAGE)
    
    if not i18n:
        logging.error("I18n middleware not found in data")
        await message.answer("Error: I18n not available")
        return
    
    _ = lambda key, **kwargs: i18n.gettext(current_language, key, **kwargs)
    
    try:
        amount = float(message.text.strip())
        if amount <= 0:
            await message.answer(_("admin_balance_invalid_amount"))
            return
    except ValueError:
        await message.answer(_("admin_balance_invalid_amount"))
        return
    
    state_data = await state.get_data()
    target_user_id = state_data.get("target_user_id")
    
    if not target_user_id:
        await message.answer(_("admin_balance_user_not_found"))
        await state.clear()
        return
    
    try:
        balance_service = BalanceService(session)
        new_balance = await balance_service.subtract_balance(target_user_id, amount)
        
        if new_balance is not None:
            await message.answer(
                _("balance_subtract_success", amount=amount, new_balance=new_balance),
                parse_mode="HTML"
            )
        else:
            await message.answer(_("balance_insufficient_for_operation"))
    except Exception as e:
        logging.error(f"Error subtracting balance: {e}")
        await message.answer(_("admin_balance_operation_error"))
    
    await state.clear()


@router.message(BalanceManagementStates.waiting_for_set_amount)
async def handle_set_amount_input(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
    settings: Settings,
    **data
):
    """Handle set amount input."""
    i18n_data = data.get("i18n_data", {})
    i18n = i18n_data.get("i18n_instance")
    current_language = i18n_data.get("current_language", settings.DEFAULT_LANGUAGE)
    
    if not i18n:
        logging.error("I18n middleware not found in data")
        await message.answer("Error: I18n not available")
        return
    
    _ = lambda key, **kwargs: i18n.gettext(current_language, key, **kwargs)
    
    try:
        amount = float(message.text.strip())
        if amount < 0:
            await message.answer(_("balance_negative_amount"))
            return
    except ValueError:
        await message.answer(_("admin_balance_invalid_amount"))
        return
    
    state_data = await state.get_data()
    target_user_id = state_data.get("target_user_id")
    
    if not target_user_id:
        await message.answer(_("admin_balance_user_not_found"))
        await state.clear()
        return
    
    try:
        balance_service = BalanceService(session)
        success = await balance_service.set_balance(target_user_id, amount)
        
        if success:
            await message.answer(
                _("balance_set_success", amount=amount),
                parse_mode="HTML"
            )
        else:
            await message.answer(_("admin_balance_operation_error"))
    except Exception as e:
        logging.error(f"Error setting balance: {e}")
        await message.answer(_("admin_balance_operation_error"))
    
    await state.clear()
