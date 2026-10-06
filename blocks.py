from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Block:
    """Runtime representation of a block loaded from blocks.json."""

    id: int
    internal_name: str
    name: str
    texture: str

    is_solid: bool = True
    has_collision: bool = True
    transparent: bool = False

    hardness: float = 0.0
    blast_resistance: float = 0.0

    can_be_broken: bool = True
    harvest_tool: str | None = None

    drops: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)

    extra: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Block":
        known_fields = {
            'id', 'internal_name', 'name', 'texture',
            'is_solid', 'has_collision', 'transparent',
            'hardness', 'blast_resistance', 'can_be_broken',
            'harvest_tool', 'drops', 'tags'
        }

        extra = {
            key: value
            for key, value in data.items()
            if key not in known_fields
        }

        return cls(
            id=data['id'],
            internal_name=data['internal_name'],
            name=data['name'],
            texture=data['texture'],
            is_solid=data.get('is_solid', True),
            has_collision=data.get('has_collision', True),
            transparent=data.get('transparent', False),
            hardness=data.get('hardness', 0.0),
            blast_resistance=data.get('blast_resistance', 0.0),
            can_be_broken=data.get('can_be_broken', True),
            harvest_tool=data.get('harvest_tool'),
            drops=data.get('drops', []),
            tags=data.get('tags', []),
            extra=extra,
        )

    def is_air(self) -> bool:
        return self.internal_name == 'air'
