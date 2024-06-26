from enum import Enum

USER_ROLE = (
    ('Admin', 'Admin'),
    ('Manager', 'Manager'),
)

GENDER_OPTION = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)

TOKEN_TYPE = (
    ('CreateToken', 'CreateToken'),
    ('ResetToken', 'ResetToken'),
)

USER_ROLE_CHOICES = (
    ('Admin', 'Admin'),
    ('Admin View Only', 'Admin View Only'),
    ('Divisional Head', 'Divisional Head'),
    ('Agent Network Manager', 'Agent Network Manager'),
    ('Regional Leader', 'Regional Leader'),
    ('Relationship Officer', 'Relationship Officer'),
    ('Super Agent', 'Super Agent'),
    ('Agent', 'Agent'),
    ('Tele-Marketer', 'Tele-Marketer'),
    ('NSIP-Manager', 'NSIP-Manager'),
    ('Merchant Manager', 'Merchant Manager'),
    ('CSO', 'CSO'),
    ('MaComm', 'MaComm'),
    ('Risk and Compliance', 'Risk and Compliance'),
    ('Settlement and Reconciliation', 'Settlement and Reconciliation'),
    ('OSHIS Supervisor', 'OSHIS Supervisor'),
    ('Merchant Supervisor', 'Merchant Supervisor'),
)


class PinEnum(Enum):
    Transaction = 'Transaction'
    Transfer = 'Transfer'


def default_role():
    return ['Admin']
