import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point
class Trajectory_generator(Node):
    def __init__(self):
        super().__init__("trajectory_generator")
        self.xg = None
        self.yg = None
        self.step = 0.15
        self.t = math.pi

        self.gerono_publisher = self.create_publisher(Point, "gerono", 10)
        self.lissajous_publisher = self.create_publisher(Point, "lissajous", 10)
        self.quadrifolium_publisher = self.create_publisher(Point, "quadrifolium", 10)
        
        self.timer = self.create_timer(0.5, self.control_loop)

    def gerno_alg(self):
        """Лемниската Героно"""
        a = 3.0

        self.xg = a * math.cos(self.t) / (1 + math.sin(self.t)**2)
        self.yg = a * math.sin(self.t) * math.cos(self.t) / (1 + math.sin(self.t)**2)

    def lissajous_alg(self):
        """Фигура Лиссажу"""
        A = 3.0
        B = 3.0
        a = 3  # частота по X
        b = 2  # частота по Y
        delta = math.pi / 2
        
        self.xg = A * math.sin(a * self.t + delta)
        self.yg = B * math.sin(b * self.t)
    
    def quadrifolium_alg(self):
        """Квадрифолий"""
        r = math.cos(2 * self.t)

        self.xg = r * math.cos(self.t) * 3.0
        self.yg = r * math.sin(self.t) * 3.0

    def control_loop(self):
        # Героно
        self.gerno_alg()
        gerono_msg = Point()
        gerono_msg.x = self.xg + 5.5
        gerono_msg.y = self.yg + 5.5
        self.gerono_publisher.publish(gerono_msg)

        # Лиссажу
        self.lissajous_alg()
        msg_liss = Point()
        msg_liss.x = self.xg + 5.5
        msg_liss.y = self.yg + 5.5
        self.lissajous_publisher.publish(msg_liss)

        # Квадрифолий
        self.quadrifolium_alg()
        msg_quad = Point()
        msg_quad.x = self.xg + 5.5
        msg_quad.y = self.yg + 5.5
        self.quadrifolium_publisher.publish(msg_quad)

        self.t += self.step
        if self.t > 2 * math.pi:
            self.t = 0  # Зацикливаем траекторию

def main(args=None):
    rclpy.init(args=args)
    node = Trajectory_generator()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Generator stopped by user")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()