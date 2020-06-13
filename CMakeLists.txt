cmake_minimum_required(VERSION 3.0.2)
project(ros_sharp_pose_publisher)

find_package(catkin REQUIRED)

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES ros_sharp_pose_publisher
#  CATKIN_DEPENDS other_catkin_pkg
#  DEPENDS system_lib
)

include_directories(
# include
# ${catkin_INCLUDE_DIRS}
)

catkin_install_python(PROGRAMS scripts/send_kinematics.py
        DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
        )