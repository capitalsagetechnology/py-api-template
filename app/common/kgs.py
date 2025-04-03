from cuid2 import Cuid

CUID_GENERATOR: Cuid = Cuid(length=24)


def generate_unique_id() -> str:
    return CUID_GENERATOR.generate()


def generate_wallet_code(length=8) -> str:
    generator: Cuid = Cuid(length=length)
    return generator.generate().upper()
