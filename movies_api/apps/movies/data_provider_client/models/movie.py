from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="Movie")


@_attrs_define
class Movie:
    """
    Attributes:
        id (str):
        title (str):
        description (str):
        image_url (str):
        rating (float):
    """

    id: str
    title: str
    description: str
    image_url: str
    rating: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        title = self.title

        description = self.description

        image_url = self.image_url

        rating = self.rating

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "title": title,
                "description": description,
                "image_url": image_url,
                "rating": rating,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        title = d.pop("title")

        description = d.pop("description")

        image_url = d.pop("image_url")

        rating = d.pop("rating")

        movie = cls(
            id=id,
            title=title,
            description=description,
            image_url=image_url,
            rating=rating,
        )

        movie.additional_properties = d
        return movie

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
