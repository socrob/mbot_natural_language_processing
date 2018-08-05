cmake_minimum_required(VERSION 2.8.3)
project(mbot_nlu)

find_package(catkin REQUIRED COMPONENTS
  message_generation
)

add_message_files(
  DIRECTORY ros/msg
  FILES
    Slot.msg
    ActionSlot.msg
    ActionSlotArray.msg
)

catkin_python_setup()

generate_messages()

catkin_package(
  CATKIN_DEPENDS
)
