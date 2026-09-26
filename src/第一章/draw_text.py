mport rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import math

class TurtleDrawText(Node):
    def __init__(self):
        super().__init__('turtle_draw_text')
        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.sub = self.create_subscription(Pose, '/turtle1/pose', self.pose_cb,10)
        self.pose = Pose()

    def pose_cb(self,msg):
        self.pose = msg

    def go_to(self,target_x,target_y,speed=1.0):
        twist = Twist()
        while True:
            dx = target_x - self.pose.x
            dy = target_y - self.pose.y
            dist = math.hypot(dx,dy)
            if dist < 0.05:
                break
            angle = math.atan2(dy,dx)
            twist.linear.x = speed
            twist.angular.z = 4*(angle - self.pose.theta)
            self.pub.publish(twist)
            rclpy.spin_once(self,timeout_sec=0.01)
        twist.linear.x=0.0
        twist.angular.z=0.0
        self.pub.publish(twist)

def main():
    rclpy.init()
    node = TurtleDrawText()
    #绘制单词 HI
    node.get_logger().info(f'开始绘制：HI')
    #字母H
    node.go_to(2,5)
    node.go_to(2,8)
    node.go_to(2,6.5)
    node.go_to(3.5,6.5)
    node.go_to(3.5,5)
    node.go_to(3.5,8)
    #字母I
    node.go_to(5,5)
    node.go_to(5,8)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
