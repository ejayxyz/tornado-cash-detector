from dataclasses import dataclass
from typing import Optional

@dataclass(order=True, frozen=True)
class InnerTransaction:
    from_: str
    to: str
    gas: str
    value: str
    calls: Optional['InnerTransaction'] = None
    
@dataclass(order=True, frozen=True)
class Transaction:
    txHash: str
    result: InnerTransaction

@dataclass(order=True, frozen=True)
class TraceBlockResponse:
    id: int
    result: list[Transaction]