import asyncio
import cv2
from mavsdk import System
from mavsdk.offboard import (OffboardError, PositionNedYaw)
from mavsdk.mission import (MissionItem, MissionPlan)
from utils import cameragazebo
from utils import directory_manager
from mavsdk.action import OrbitYawBehavior
from enum import Enum
from mavsdk.telemetry import Position
from firesense_model import classifier
import os

FIRESENSE = os.getcwd()
PATH = os.path.join(os.getcwd(), 'assets', 'to_classify')


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
            await drone.action.set_takeoff_altitude(12)
            await drone.action.takeoff()
            await asyncio.sleep(10)
            fire_found = False
            behavior = OrbitYawBehavior(3)
            count = 0
            video = cameragazebo.Video()

            while not fire_found:
                await drone.action.do_orbit(0.1,1, behavior, 0,0,12)
                await asyncio.sleep(10)
                # save camera feed to assets/to_classify
                frame = video.frame()
                img_path = os.path.join(PATH, str(count)+".jpg")
                print("\n"+img_path)
                if not video.frame_available():
                    print("Frame not available")
                    continue
                else:
                    count += 1
                    print("count: " + str(count))
                # cv2.imshow('frame', frame)
                cv2.imwrite(img_path, frame)
                # classify camera feed
                classification, confidence = classifier.classify(img_path, classifier.MODEL)
                # if classification is 'fire', then  set fire_found to True as we've now found the fire and can start movign in this direction
                if classification == "a fire":
                    await drone.action.hold()
                    print("Fire detected")
                    fire_found = True
                else:
                    print("No fire detected")

            count = 0
            while fire_found:
                await drone.action.hold()
                # Move straight ahead by a small amount
                #await drone.action.go_to_location()
                # save camera feed to assets/to_classify
                frame = video.frame()
                img_path = os.path.join(PATH, str(count)+".jpg")
                print(img_path)
                if not video.frame_available():
                    print("Frame available")
                    continue
                else:
                    count += 1
                cv2.imwrite(img_path, frame)
                # classify camera feed
                classification, confidence = classifier.classify(img_path, classifier.MODEL)
                # if classification is 'not fire' then we've passed the fire and we can stop
                if classification == "not a fire":
                    await drone.action.hold()
                    print("Arrived at fire")
                    fire_found = False
                else:
                    print("Going towards fire")
                count += 1
        except OffboardError as error:
            print(f"Starting offboard mode failed with error code: {error._result.result}")
            print("-- Disarming")
            await drone.action.disarm()
            return

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
    print(f"Directory where frames will be saved: {PATH}")
