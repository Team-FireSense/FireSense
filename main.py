import asyncio
import cv2
from mavsdk import System
from mavsdk.offboard import (OffboardError, PositionNedYaw)
from mavsdk.mission import (MissionItem, MissionPlan)
from utils import cameragazebo
from utils import directory_manager
import os


async def run():
    drone = System()
    # video = cv2.VideoCapture("udp://127.0.0.1:5600")
    # video = cv2.VideoCapture("udp://127.0.0.1:9999?overrun_nonfatal=1&fifo_size=50000000")
    await drone.connect(system_address="udp://:14540")
    # if vid_cam.isOpened() is False:
    #     print('[ERROR] Couldnt open the camera.')
    #     return
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Drone discovered")
            break
        await drone.action.arm()
        await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, 0.0, 0.0))
        try:
            await drone.offboard.start()
            print("Starting")
            await drone.action.set_takeoff_altitude(15)
            await drone.action.takeoff()
            # await drone.action.do_orbit(0,0.5)
            # save camera feed to assets/to_classify
            # classify camera feed
        except OffboardError as error:
            print(f"Starting offboard mode failed with error code: {error._result.result}")
            print("-- Disarming")
            await drone.action.disarm()
            return
        video = cameragazebo.Video()
        while True:
            # Wait for the next frame
            if not video.frame_available():
                continue
            frame = video.frame()
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        N_coord = 0
        E_coord = 0
        D_coord = -10  # -HOVERING_ALTITUDE
        yaw_angle = 0
        # await drone.offboard.set_position_ned(PositionNedYaw(N_coord, E_coord, D_coord, yaw_angle))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    path = os.path.join(directory_manager.parent_dir(os.getcwd()), 'assets', 'assets/to_classify')
    print(f"Directory where frames will be saved: {path}")
