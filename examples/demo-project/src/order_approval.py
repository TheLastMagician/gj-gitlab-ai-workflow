from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class OrderStatus(str, Enum):
    DRAFT = "draft"
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


@dataclass
class Order:
    id: str
    applicant: str
    amount: float
    status: OrderStatus = OrderStatus.DRAFT
    approver: str | None = None
    reject_reason: str | None = None


class OrderApprovalError(ValueError):
    pass


class OrderApprovalService:
    def submit(self, order: Order) -> Order:
        if order.status is not OrderStatus.DRAFT:
            raise OrderApprovalError("only draft orders can be submitted")
        order.status = OrderStatus.PENDING
        return order

    def approve(self, order: Order, approver: str) -> Order:
        self._ensure_pending(order)
        self._ensure_not_self_approval(order, approver)
        order.status = OrderStatus.APPROVED
        order.approver = approver
        order.reject_reason = None
        return order

    def reject(self, order: Order, approver: str, reason: str) -> Order:
        self._ensure_pending(order)
        self._ensure_not_self_approval(order, approver)
        if not reason.strip():
            raise OrderApprovalError("reject reason is required")
        order.status = OrderStatus.REJECTED
        order.approver = approver
        order.reject_reason = reason
        return order

    @staticmethod
    def _ensure_pending(order: Order) -> None:
        if order.status is not OrderStatus.PENDING:
            raise OrderApprovalError("only pending orders can be approved or rejected")

    @staticmethod
    def _ensure_not_self_approval(order: Order, approver: str) -> None:
        if order.applicant == approver:
            raise OrderApprovalError("applicant cannot approve their own order")
