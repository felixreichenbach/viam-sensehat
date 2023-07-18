from typing import ClassVar, Mapping, Sequence, Any, Dict, Optional, cast
from typing_extensions import Self

from viam.module.types import Reconfigurable
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName, Vector3
from viam.resource.base import ResourceBase
from viam.resource.types import Model, ModelFamily

from viam.components.sensor import Sensor
from viam.logging import getLogger


from sense_emu import SenseHat

import time
import asyncio

LOGGER = getLogger(__name__)


class sensehat_sensors(Sensor, Reconfigurable):
    MODEL: ClassVar[Model] = Model(ModelFamily("rapi", "sensor"), "sensehat_sensors")

    # create any class parameters here, 'some_pin' is used as an example (change/add as needed)
    some_pin: int
    sensehat = SenseHat

    # Constructor
    @classmethod
    def new(cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        my_class = cls(config.name)
        my_class.reconfigure(config, dependencies)
        my_class.sensehat = SenseHat()
        return my_class

    # Validates JSON Configuration
    @classmethod
    def validate(cls, config: ComponentConfig):
        # here we validate config, the following is just an example and should be updated as needed
        some_pin = config.attributes.fields["some_pin"].number_value
        if some_pin == "":
            raise Exception("A some_pin must be defined")
        return

    # Handles attribute reconfiguration
    def reconfigure(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]):
        # here we initialize the resource instance, the following is just an example and should be updated as needed
        self.some_pin = int(config.attributes.fields["some_pin"].number_value)
        return

    """ Implement the methods the Viam RDK defines for the Sensor API (rdk:components:sensor) """

    async def get_readings(
        self, *, extra: Optional[Mapping[str, Any]] = None, timeout: Optional[float] = None, **kwargs
    ) -> Mapping[str, Any]:
        """
        Obtain the measurements/data specific to this sensor.

        Returns:
            Mapping[str, Any]: The measurements. Can be of any type.
        """

        measurements = {}

        if "sensors" in extra:
            for (key, values) in extra.items():
                for value in values:
                    try:
                        measurements[value] = getattr(self.sensehat, value)
                    except:
                        LOGGER.warn(f'No sensor "{value}" available!')
        else:
            measurements = {
                "temperature": self.sensehat.temperature,
                "humidity": self.sensehat.humidity,
                "pressure": self.sensehat.pressure,
                "gyroscope": self.sensehat.gyroscope,
                "compass": self.sensehat.compass,
                "accelerometer": self.sensehat.accelerometer,
                "orientation": self.sensehat.orientation
            }
        return measurements
