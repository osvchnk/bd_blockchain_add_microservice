import hashlib
from typing import List

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa

from app.repositories.block import BlockRepository
from app.schemas import *


class BlockService:

    def __init__(self):
        self.repository = BlockRepository()

    async def create_block(self, transaction_list: List[str]):
        prev_hash = await self.get_prev_hash()
        date = datetime.now()
        block = BlockBaseSchema(date=date,
                                prev_hash=prev_hash,
                                transactions=transaction_list)

        hashed_block = await self.hash_block(block)
        signed_block = await self.sign_block(hashed_block)

        return await self.repository.create_block(signed_block)

    async def sign_block(self, hashed_block: BlockHashedSchema) -> BlockSignedSchema:
        hash = hashed_block.hash
        sign = hashlib.sha256(hash.encode()).hexdigest()*3
        signed_block = BlockSignedSchema(**hashed_block.dict(), admin_sign=sign)
        return signed_block

    async def hash_block(self, block: BlockBaseSchema) -> BlockHashedSchema:
        """
        date prev_hash transaction_list
        """
        sorted_transactions = sorted(block.transactions)
        s = f"{str(datetime.timestamp(block.date))} {block.prev_hash} {' '.join(sorted_transactions)}"
        hash = hashlib.sha256(s.encode()).hexdigest()
        return BlockHashedSchema(**block.dict(), hash=hash)

    async def get_prev_hash(self) -> str:
        last_block = await self.repository.get_last_block()
        last_block_schema = BlockOutSchema.from_orm(last_block)
        return last_block_schema.hash


if __name__ == "__main__":
    hashed_block = BlockHashedSchema(
        date=datetime.timestamp(datetime.now()),
        prev_hash="prev_hash",
        transactions=["hi"],
        hash="hash"
    )
    signed_block = BlockSignedSchema(**hashed_block.dict(),
                                     admin_sign="sign")
    print(signed_block)
