from pydantic import BaseModel, Field, EmailStr, constr
from uuid import UUID
from typing import Optional


class PaymentNotify(BaseModel):
    merchant_id: UUID = Field(..., description="ID Вашего магазина")
    invoice_id: UUID = Field(..., description="ID заказа в нашей системе")
    order_id: constr(min_length=1, max_length=64) = Field(..., description="Идентификатор заказа в Вашей системе")
    amount: float = Field(..., description="Сумма заказа")
    currency: str = Field(...,
                          pattern=r'^(RUB|UAH|EUR|USD)$', description="Валюта заказа. Доступные значения: RUB, UAH, EUR, USD")
    profit: float = Field(..., description="Сумма зачисленная Вам на баланс в RUB")
    commission: float = Field(..., description="Сумма комиссии магазина в RUB")
    commission_client: float = Field(..., description="Сумма комиссии клиента в RUB")
    commission_type: str = Field(...,
                                 description="Формат соотношения: Комиссия магазина:Комиссия покупателя Пример: 100:0")
    sign: str = Field(...,
                      description="Подпись заказа (SHA256 Хеш). Методика формирования подписи в скрипте оповещения")
    method: str = Field(..., description="Кодовое название платежной системы (см. способы оплаты)")
    desc: constr(min_length=1, max_length=512) = Field(..., description="Описание заказа")
    email: Optional[EmailStr] = Field(None, description="E-Mail покупателя")
    us_key: constr(min_length=1, max_length=2056) = Field(..., description="")
