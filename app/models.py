from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Numeric,
    Enum,
    Text,
    func
)
from sqlalchemy.orm import relationship
from .database import Base
import enum
from uuid import uuid4


class UserRole(str, enum.Enum):
    user = "user"
    admin = "admin"


class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid4()), index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    balance = Column(Numeric(15, 2), default=100000.00, nullable=False)
    is_verified = Column(Boolean, default=False)
    is_frozen = Column(Boolean, default=False)
    role = Column(Enum(UserRole), default=UserRole.user, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    nin = Column(String, nullable=True)
    bvn = Column(String, nullable=True)
    phone_number = Column(String, nullable=True, unique=True)
    transaction_pin = Column(String, nullable=True)
    account_number = Column(Integer, nullable=False, unique=True)
    
    # Relationships
    sent_transactions = relationship(
        "Transaction",
        foreign_keys="[Transaction.sender_id]",
        back_populates="sender"
    )

    received_transactions = relationship(
        "Transaction",
        foreign_keys="[Transaction.receiver_id]",
        back_populates="receiver"
    )

    savings_accounts = relationship("Savings", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="user")


class TransactionType(str, enum.Enum):
    deposit = "deposit"
    withdrawal = "withdrawal"
    transfer = "transfer"
    savings_lock = "savings_lock"
    savings_release = "savings_release"
    interest = "interest"
    reversal = "reversal"


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()), index=True)

    sender_id = Column(String, ForeignKey("users.id"), nullable=True)
    receiver_id = Column(String, ForeignKey("users.id"), nullable=True)

    amount = Column(Numeric(15, 2), nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String, default="completed")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    sender = relationship(
        "User",
        foreign_keys=[sender_id],
        back_populates="sent_transactions"
    )

    receiver = relationship(
        "User",
        foreign_keys=[receiver_id],
        back_populates="received_transactions"
    )


class Savings(Base):
    __tablename__ = "savings"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()), index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    interest_rate = Column(Numeric(5, 2), default=5.00)
    locked_until = Column(DateTime(timezone=True), nullable=False)
    matured = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="savings_accounts")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()), index=True)
    action = Column(String, nullable=False)
    performed_by = Column(String, ForeignKey("users.id"), nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="audit_logs")

    def __repr__(self):
        return f"AuditLog(id={self.id}, action={self.action}, performed_by={self.performed_by}, timestamp={self.timestamp})"