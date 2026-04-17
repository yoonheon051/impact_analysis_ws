# bash
# ros2 launch dsr_impact_analysis impact_sim.launch.py

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
    # 1. 패키지 이름 및 경로 설정
    # 현재 분석용 패키지와 URDF가 위치한 패키지 경로를 지정합니다.
    pkg_name = 'dsr_impact_analysis'
    pkg_path = get_package_share_directory(pkg_name)

    # 2. xacro 파일 경로 지정 (내 패키지로 복사해온 URDF 사용)
    # m0609_rg2.urdf.xacro 파일이 urdf 폴더 내에 있어야 합니다.
    xacro_file = os.path.join(pkg_path, 'urdf', 'm0609.urdf.xacro')

    # 3. xacro 명령 실행
    robot_description_content = Command(['xacro ', xacro_file])

    # 4. robot_state_publisher 노드 설정
    # 로봇의 URDF 정보를 받아 /tf 정보를 계산하고 발행합니다.
    rsp_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': ParameterValue(robot_description_content, value_type=str),
            'use_sim_time': False
        }]
    )

    # 5. impact_sim_node (동역학 및 충격량 계산 노드)
    # joint_state_publisher_gui 대신 이 노드가 'joint_states'를 발행합니다.
    sim_node = Node(
        package=pkg_name,
        executable='impact_sim_node',
        name='impact_sim_node',
        output='screen',
        parameters=[{'use_sim_time': False}]
    )

    # 6. Rviz2 설정 및 실행 노드
    # 프로젝트 폴더 내 rviz/impact_config.rviz 파일이 있다면 해당 설정을 로드합니다.
    # 파일이 없다면 arguments 부분을 비우거나 기본 rviz를 띄웁니다.
    rviz_config_path = os.path.join(pkg_path, 'rviz', 'impact_config.rviz')
    
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        # rviz 설정 파일이 존재할 경우에만 로드 (없을 경우 기본 실행)
        arguments=['-d', rviz_config_path] if os.path.exists(rviz_config_path) else []
    )

    return LaunchDescription([
        rsp_node,
        sim_node,
        rviz_node,
    ])