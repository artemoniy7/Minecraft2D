from __future__ import annotations

import json
from pathlib import Path

from blocks import Block


class BlockRegistry:
    def __init__(self, json_path: str | Path = "assets/blocks/blocks.json"):
        self.json_path = Path(json_path)
        self._blocks_by_name: dict[str, Block] = {}
        self._blocks_by_id: dict[int, Block] = {}

    def load(self) -> None:
        with open(self.json_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        blocks = data.get("blocks", data)

        if isinstance(blocks, dict):
            blocks = list(blocks.values())

        self._blocks_by_name.clear()
        self._blocks_by_id.clear()

        for block_data in blocks:
            block = Block.from_dict(block_data)
            self._blocks_by_name[block.internal_name] = block
            self._blocks_by_id[block.id] = block

    def get(self, internal_name: str) -> Block | None:
        return self._blocks_by_name.get(internal_name)

    def get_by_id(self, block_id: int) -> Block | None:
        return self._blocks_by_id.get(block_id)

    def all(self) -> list[Block]:
        return list(self._blocks_by_name.values())

    def __contains__(self, internal_name: str) -> bool:
        return internal_name in self._blocks_by_name
