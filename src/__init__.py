"""
This file registers the model with the Python SDK.
"""

from viam.components.sensor import Sensor
from viam.resource.registry import Registry, ResourceCreatorRegistration

from .sensehat_sensors import sensehat_sensors

Registry.register_resource_creator(Sensor.SUBTYPE, sensehat_sensors.MODEL, ResourceCreatorRegistration(sensehat_sensors.new, sensehat_sensors.validate))
