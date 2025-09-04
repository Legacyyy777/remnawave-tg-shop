from aiogram.fsm.state import State, StatesGroup


class UserPromoStates(StatesGroup):
    waiting_for_promo_code = State()


class TermsAcceptanceStates(StatesGroup):
    waiting_for_terms_decision = State()