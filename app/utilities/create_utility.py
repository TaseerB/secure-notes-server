
from typing import Any, Dict

def schema_to_dict(schema_obj: Any) -> Dict[str, Any]:
    """
    Support both Pydantic v1 (dict()) and v2 (model_dump()).
    """
    if hasattr(schema_obj, "model_dump"):
        return schema_obj.model_dump()
    return schema_obj.dict()