from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class InnerTransaction:
    from_: str
    to: str
    gas: str
    value: str
    calls: Optional['InnerTransaction'] = None
    
@dataclass(frozen=True)
class Transaction:
    txHash: str
    result: InnerTransaction

@dataclass(frozen=True)
class TraceBlockResponse:
    id: int
    result: list[Transaction]