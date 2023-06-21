import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import async_session
from app.models.block import Block, TransactionInBlock
from app.schemas import BlockSignedSchema, BlockCreateSchema


class BlockRepository:

    def __init__(self):
        self.session: AsyncSession = async_session()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session is not None:
            await self.session.close()

    async def create_block(self, block: BlockSignedSchema):
        block_create_schema = BlockCreateSchema(**block.dict())
        new_block = Block(**block_create_schema.dict())
        self.session.add(new_block)
        await self.session.commit()
        await self.session.refresh(new_block)

        trs = []
        for transaction in block.transactions:
            trs.append(TransactionInBlock(hash=transaction, block_id=new_block.id))
        self.session.add_all(trs)

        await self.session.commit()

    async def get_last_block(self) -> Block:
        query = (
            select(Block).
            order_by(-Block.id).
            limit(1)
        )
        result = await self.session.execute(query)
        return result.scalars().one()


async def func():
    async with BlockRepository() as repo:
        result = await repo.get_last_block()
        print(BlockSignedSchema.from_orm(result))


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(func())
