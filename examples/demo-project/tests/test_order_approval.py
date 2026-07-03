import unittest

from examples.demo_project_import import import_order_approval


order_approval = import_order_approval()
Order = order_approval.Order
OrderApprovalError = order_approval.OrderApprovalError
OrderApprovalService = order_approval.OrderApprovalService
OrderStatus = order_approval.OrderStatus


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
