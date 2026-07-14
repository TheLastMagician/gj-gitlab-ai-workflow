import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from order_approval import (  # noqa: E402
    Order,
    OrderApprovalError,
    OrderApprovalService,
    OrderStatus,
)


class OrderApprovalServiceTest(unittest.TestCase):
    def setUp(self):
        self.service = OrderApprovalService()

    def test_submit_moves_draft_order_to_pending(self):
        order = Order(id="O-1001", applicant="alice", amount=1200)

        self.service.submit(order)

        self.assertEqual(order.status, OrderStatus.PENDING)

    def test_approve_pending_order(self):
        order = self.service.submit(Order(id="O-1002", applicant="alice", amount=1200))

        self.service.approve(order, approver="bob")

        self.assertEqual(order.status, OrderStatus.APPROVED)
        self.assertEqual(order.approver, "bob")

    def test_reject_pending_order_requires_reason(self):
        order = self.service.submit(Order(id="O-1003", applicant="alice", amount=1200))

        with self.assertRaises(OrderApprovalError):
            self.service.reject(order, approver="bob", reason=" ")

    def test_applicant_cannot_approve_own_order(self):
        order = self.service.submit(Order(id="O-1004", applicant="alice", amount=1200))

        with self.assertRaises(OrderApprovalError):
            self.service.approve(order, approver="alice")

    def test_approved_order_cannot_be_reapproved(self):
        order = self.service.submit(Order(id="O-1005", applicant="alice", amount=1200))
        self.service.approve(order, approver="bob")

        with self.assertRaises(OrderApprovalError):
            self.service.approve(order, approver="carol")


if __name__ == "__main__":
    unittest.main()
