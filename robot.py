
import asyncio
import os
from dotenv import load_dotenv

from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.components.sensor import Sensor

"""
    Credentials are imported through a .env file with the following structure:
    ADDRESS=robot.organisation.viam.cloud
    SECRET=yoursecret
"""
load_dotenv()


async def connect():
    creds = Credentials(
        type='robot-location-secret',
        payload=os.getenv('SECRET'))
    opts = RobotClient.Options(
        refresh_interval=0,
        dial_options=DialOptions(credentials=creds)
    )
    return await RobotClient.at_address(os.getenv('ADDRESS'), opts)


async def main():
    robot = await connect()

    # SenseHat
    sensehat = Sensor.from_robot(robot, "sensehat")

    # You can use extra to filter the sensor readings as shown below or remove it for the full list
    measurements = await sensehat.get_readings(extra={"sensors": ["temperature","pressure", "humidity", "inexistant"]})
    print(f"Sensor values: {measurements}")

    # Don't forget to close the robot when you're done!
    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())
