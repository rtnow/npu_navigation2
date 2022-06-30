import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node

def generate_launch_description():
# .................. Configurable Arguments .....................

    use_sim_time = True
    map_saver_params_file = 'npu_map.yaml'
    #map_saver_params_file = 'npu_map.yaml'
# ...............................................................


    pkg_dir = get_package_share_directory('nav2_bringup')
    map_save_config = os.path.join(pkg_dir, '/home/rtnow/ros2_ws/src/npu_navigation2/maps', map_saver_params_file)


    return LaunchDescription([

        DeclareLaunchArgument("use_sim_time", default_value=str(use_sim_time), description="Use simulation/Gazebo clock"),
        DeclareLaunchArgument("map_saver_params_file", default_value=map_save_config, description="Map Saver Configuration File"),

        Node(
            package='nav2_map_server',
            executable='map_server',
            name='map_server',
            output='screen',
            emulate_tty=True,  
            parameters=[{'use_sim_time':True},
                        {'yaml_filename': map_saver_params_file}
                        ]),

        Node(
            package='nav2_lifecycle_manager',
            executable='lifecycle_manager',
            name='lifecycle_manager',
            output='screen',
            emulate_tty=True,  
            parameters=[
                {'use_sim_time': LaunchConfiguration('use_sim_time')},
                {'autostart': True},
                {'node_names': ['map_server']}]
            ),

    ])
