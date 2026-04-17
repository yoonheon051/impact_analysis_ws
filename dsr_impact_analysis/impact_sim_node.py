import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from visualization_msgs.msg import Marker
from std_msgs.msg import Float64
import numpy as np
import math

class PickAndPlaceImpactSim(Node):
    def __init__(self):
        super().__init__('impact_sim_node')
        
        # Publishers
        self.joint_pub = self.create_publisher(JointState, 'joint_states', 10)
        self.marker_pub = self.create_publisher(Marker, 'impact_marker', 10)
        self.force_pub = self.create_publisher(Float64, 'estimated_force', 10)
        
        # Parameters
        self.dt = 0.01  # 100Hz
        self.timer = self.create_timer(self.dt, self.update_simulation)
        
        self.time = 0.0
        self.mass = 6.0  # M0609 가반하중 + 물체 무게 (kg)
        self.velocity = 1.0  # 초기 속도 (m/s)
        self.stopping = False
        self.stop_type = 'smooth'  # 'step' or 'smooth'
        
    def calculate_impact_force(self, accel):
        # F = m * a (단순화된 충격력 모델)
        return self.mass * abs(accel)

    def update_simulation(self):
        self.time += self.dt
        joint_state = JointState()
        joint_state.header.stamp = self.get_clock().now().to_msg()
        joint_state.name = ['joint_1', 'joint_2', 'joint_3', 'joint_4', 'joint_5', 'joint_6']
        
        # 1. 궤적 생성 (단순화를 위해 joint2만 움직임 가정)
        pos = [0.0] * 6
        
        if self.time > 2.0:  # 2초 후 정지 시작
            if self.stop_type == 'step':
                # 급정지: 0.02초 만에 정지
                accel = -self.velocity / 0.02 if self.velocity > 0 else 0
                self.velocity = max(0, self.velocity + accel * self.dt)
            else:
                # 부드러운 정지: 1.0초 동안 감속 (S-Curve 유사)
                accel = -1.0  # 일정 감속도
                self.velocity = max(0, self.velocity + accel * self.dt)
        else:
            accel = 0
            
        # 가상의 위치 업데이트 (속도 적분)
        pos[1] = self.velocity * self.time 
        joint_state.position = pos
        self.joint_pub.publish(joint_state)
        
        # 2. 충격력 계산 및 마커 표시
        force = self.calculate_impact_force(accel)
        self.publish_marker(force)
        
        # 데이터 모니터링용 토픽 발행
        msg = Float64()
        msg.data = force
        self.force_pub.publish(msg)

    def publish_marker(self, force):
        marker = Marker()
        marker.header.frame_id = "link_6"  # 로봇 끝단 프레임
        marker.type = Marker.TEXT_VIEW_FACING
        marker.text = f"Impact Force: {force:.2f} N"
        marker.scale.z = 0.1 # 글자 크기
        marker.color.a = 1.0
        marker.color.r = 1.0 if force > 150 else 0.0 # ISO 기준치 초과 시 빨간색
        marker.color.g = 1.0 if force <= 150 else 0.0
        self.marker_pub.publish(marker)

def main():
    rclpy.init()
    node = PickAndPlaceImpactSim()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()