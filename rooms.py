import pygame
from settings import *
from rooms_lists import *


class Room:
    def __init__(self, layout, level_position):
        self.layout = layout
        self.level_position = level_position


main_room = Room(main_room_layout, (1, 1))
right_room = Room(right_room_layout, (2, 1))
left_room = Room(left_room_layout, (0, 1))
top_room = Room(top_room_layout, (1, 0))
bottom_room = Room(bottom_room_layout, (1, 2))
top_left_room = Room(top_left_room_layout, (0, 0))
bottom_left_room = Room(bottom_left_room_layout, (0, 2))
top_right_room = Room(top_right_room_layout, (2, 0))
bottom_right_room = Room(bottom_right_room_layout, (2, 2))

rooms_dict = {
    top_room.level_position: top_room,
    top_left_room.level_position: top_left_room,
    bottom_left_room.level_position: bottom_left_room,
    left_room.level_position: left_room,
    main_room.level_position: main_room,
    right_room.level_position: right_room,
    top_right_room.level_position: top_right_room,
    bottom_right_room.level_position: bottom_right_room,
    bottom_room.level_position: bottom_room
}
