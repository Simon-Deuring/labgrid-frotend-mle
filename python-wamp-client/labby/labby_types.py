"""
Types used throughout labby
"""

from abc import abstractmethod
from typing import Dict, List, Optional, Set, Tuple
from autobahn.asyncio.wamp import ApplicationSession
from attr import attrs, attrib


TargetName = str
ExporterName = str
PlaceName = str
ResourceName = str
GroupName = str
PlaceKey = Tuple[TargetName, PlaceName]
# Serializable labby arrer (LabbyError converted to json string)
SerLabbyError = Dict
Resource = Dict
Place = Dict
PowerState = Dict


class Session(ApplicationSession):
    """
    Forward declaration for Labby session
    """

    def __init__(self, *args, **kwargs) -> None:
        self.resources: Optional[Dict] = None
        self.places: Optional[Dict] = None
        self.acquired_places: List[PlaceName] = []
        self.power_states: Optional[List] = None
        self.reservations: Dict = {}
        self.to_refresh: Set = set()
        self.user_name : str
        super().__init__(*args, **kwargs)


class LabbyType:
    @abstractmethod
    def to_json(self):
        """
        convert to json serializable dict
        """


@attrs
class LabbyPlace(LabbyType):
    name: str = attrib()
    acquired_resources: List[str] = attrib()
    exporter: str = attrib()
    power_state: bool = attrib()

    def to_json(self):
        return {
            "name": self.name,
            "acquired_resources": self.acquired_resources,
            "exporter": self.exporter,
            "power_state": self.power_state,
        }
