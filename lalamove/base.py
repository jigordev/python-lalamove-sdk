from pydantic import BaseModel, ConfigDict


def to_camel_case(string: str) -> str:
    components = string.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


class LalamoveBaseModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel_case, 
        populate_by_name=True,
        from_attributes=True,
    )
