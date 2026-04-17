🐊dsr_impact_analysis

두산로봇 M0609와 OnRobot RG2 그리퍼를 활용한 로봇 충격량 분석 및 시뮬레이션 패키지입니다. 본 패키지는 독립적인 실행을 위해 모든 모델 데이터(URDF, Meshes)를 내재화하고 있습니다.


환경 설정 (Environment)
OS: Ubuntu 22.04 (Jammy Jellyfish)

ROS 2: Humble Hawksbill

Hardware: HP Victus 16-d1xxx (Intel Core i7, RTX 3060)

Tools: VS Code, ROS 2 Launch, Rviz2

패키지 구조 (Directory Structure)
빌드 에러 방지를 위해 모든 메쉬 파일을 평면 구조(Flat)로 관리합니다.


Plaintext
dsr_impact_analysis/
├── launch/
│   └── impact_sim.launch.py   # 시뮬레이션 통합 실행 파일
├── meshes/                    # 모든 .dae, .stl 파일 (하위 폴더 없음)
├── urdf/
│   └── m0609.urdf.xacro      # 로봇 및 그리퍼 통합 모델
├── src/
│   └── impact_sim_node.py    # 충격량 계산 및 관절 제어 노드
├── package.xml
├── setup.py                  # 리소스 빌드 및 설치 설정
└── README.md


설치 및 빌드 (Installation & Build)

1. 워크스페이스 준비
Bash
mkdir -p ~/impact_analysis_ws/src
cd ~/impact_analysis_ws/src


2. 의존성 및 빌드
메쉬 폴더 구조 에러를 방지하기 위해 build와 install 폴더를 초기화한 후 빌드하는 것을 권장합니다.

Bash
cd ~/impact_analysis_ws
rm -rf build install log
colcon build --symlink-install
source install/setup.bash

실행 방법 (Usage)
시뮬레이션 및 Rviz 확인
직접 작성한 충격량 분석 노드와 Rviz를 동시에 실행합니다.

Bash
ros2 launch dsr_impact_analysis impact_sim.launch.py

주요 해결 과제 (Troubleshooting)
1. Package Not Found 에러
원인: 워크스페이스 경로 중첩(cobot_ws/src 내부에 생성)으로 인한 인식 오류.

해결: ~/impact_analysis_ws/src 표준 경로로 패키지를 이동하여 해결.

2. Meshes 복사 에러 (can't copy ... doesn't exist or not a regular file)
원인: setup.py의 glob 방식이 하위 폴더(Recursive) 복사를 지원하지 않음.

해결: meshes/ 내부의 하위 폴더(rg2, gripper 등)를 모두 제거하고 파일들을 최상위로 이동(Flattening)한 후, URDF 내 경로를 수정함.

3. 로봇 형상 미출력 (No Transform)
원인: joint_state_publisher 부재 또는 URDF 내 Mesh 경로 불일치.

해결: launch 파일에 상태 발행 노드를 추가하고, URDF 내의 package:// 경로를 본 패키지 명칭에 맞게 일괄 수정함.
