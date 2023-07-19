"""
This file registers the model with the Python SDK.
"""

from viam.components.sensor import Sensor
from viam.resource.registry import Registry, ResourceCreatorRegistration

from .sensehat_viam import SensehatViam

Registry.register_resource_creator(Sensor.SUBTYPE, SensehatViam.MODEL, ResourceCreatorRegistration(SensehatViam.new, SensehatViam.validate))
