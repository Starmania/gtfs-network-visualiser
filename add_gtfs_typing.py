try:
    import google.transit.gtfs_realtime_pb2 as gtfs
except ImportError:
    print("Please install the required packages by running 'pip install -r requirements.txt'")
    exit(-1)

TYPING_CONTENT = "\n".join((
    '',
    '# Add typing to gtfs file so linting is happy',
    'import typing',
    'if typing.TYPE_CHECKING:',
    '  from google.protobuf.message import Message',
    '  from enum import Enum',
    '  class FeedMessage(Message):',
    '    def __init__(self) -> None:',
    '      self.entity: typing.List[FeedEntity] = []',
    '  class FeedEntity(Message): # MessageMeta',
    '    def __init__(self) -> None:',
    '      self.vehicle: VehiclePosition = None',
    '      self.id = ""',
    '  class VehiclePosition(Message): # MessageMeta',
    '    class VehicleStopStatus(Enum):',
    '      INCOMING_AT = 0',
    '      STOPPED = 1',
    '    def __init__(self) -> None:',
    '      self.trip: TripDescriptor = None',
    '      self.vehicle: VehicleDescriptor = None',
    '      self.position: Position = None',
    '      self.stop_id: str = ""',
    '      self.current_status: VehiclePosition.VehicleStopStatus = VehiclePosition.VehicleStopStatus.INCOMING_AT',
    '      self.timestamp: int = 0',
    '  class Position(Message): # MessageMeta',
    '    def __init__(self) -> None:',
    '      self.latitude: float = 0.0',
    '      self.longitude: float = 0.0',
    '  class TripDescriptor(Message): # MessageMeta',
    '    class ScheduleRelationship(Enum):',
    '      SCHEDULED = 0',
    '    def __init__(self) -> None:',
    '      self.trip_id: str = ""',
    '      self.route_id: str = ""',
    '      self.direction_id: int = 0',
    '      self.schedule_relationship: TripDescriptor.ScheduleRelationship = TripDescriptor.ScheduleRelationship.SCHEDULED',
    '  class Alert(Message): ... # MessageMeta',
    '  class TimeRange(Message): ... # MessageMeta',
    '  class FeedHeader(Message): ... # MessageMeta',
    '  class TripUpdate(Message): # MessageMeta',
    '    class StopTimeEvent(Message): ...',
    '    class StopTimeUpdate(Message): # MessageMeta',
    '      class StopSequence(Enum):',
    '        def __init__(self) -> None:',
    '          self.SCHEDULED = 0',
    '          self.SKIPPED = 1',
    '          self.NO_DATA = 2',
    '          self.UNSCHEDULED = 3',
    '      class ScheduleRelationship(Enum):',
    '        def __init__(self) -> None:',
    '          self.SCHEDULED = 0',
    '          self.SKIPPED = 1',
    '          self.NO_DATA = 2',
    '          self.UNSCHEDULED = 3',
    '      def __init__(self) -> None:',
    '        self.stop_sequence: TripUpdate.StopTimeUpdate.StopSequence = TripUpdate.StopTimeUpdate.StopSequence.SCHEDULED',
    '        self.stop_id: str = ""',
    '        self.arrival: TripUpdate.StopTimeEvent = None',
    '        self.departure: TripUpdate.StopTimeEvent = None',
    '        self.schedule_relationship: TripUpdate.StopTimeUpdate.ScheduleRelationship = TripUpdate.StopTimeUpdate.ScheduleRelationship.SCHEDULED',
    '    def __init__(self) -> None:',
    '      self.trip = TripDescriptor()',
    '      self.stop_time_update: typing.List[TripUpdate.StopTimeUpdate] = []',
    '  class VehicleDescriptor(Message): ... # MessageMeta',
    '  class EntitySelector(Message): ... # MessageMeta',
    '  class TranslatedString(Message): ... # MessageMeta'
))

# Add typing to gtfs file if needed
try:
    with open(gtfs.__file__, 'r+', encoding="utf8") as f:
        if not "TYPE_CHECKING" in f.read():
            f.write(TYPING_CONTENT)
except PermissionError:
    print("Please run this script as an administrator to add typing to the gtfs file.")
    print("Or be normal and use a virtual environment.")
    exit(-1)
