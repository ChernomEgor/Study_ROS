import rclpy
import math
from rclpy.node import Node
from geometry_msgs.msg import Point
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

class Controller_turtle(Node):
    def __init__(self):
        super().__init__("turtle_controller") # Добираем функции отца Node
        # Инициализируем переменные
        self.xg = None
        self.yg = None
        
        self.xt = None
        self.yt = None
        self.theta = None

        self.Kf = 1.0
        self.Kr = 2.0
 
        # Создаем 1 подписчика. Подключаем 1 подписчика Pose(pose), и 1 публикатора Twist(cmd_vel), и 1 таймер timer
        self.goal_turtle_subscription = self.create_subscription(Point, "turtle_goal", self.get_turtle_goal, 10)
        self.turtle_pose_subscription = self.create_subscription(Pose, "/turtle1/pose", self.get_turtle_pose,10)
        self.turtle_do_publisher = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.timer = self.create_timer(0.05, self.control_loop)

        
    def get_turtle_goal(self, msg): # Функция принимающая координаты цели
        self.xg = msg.x
        self.yg = msg.y
        self.get_logger().info(f"Goal x:{self.xg:.2f}, y:{self.yg:.2f}")

    def get_turtle_pose(self, msg): # Функция принимающая текущие координаты черепахи
        self.xt = msg.x
        self.yt = msg.y
        self.theta = msg.theta
        self.get_logger().info(f"Current pose x:{self.xt:.2f}, y:{self.yt:.2f}, theta:{self.theta:.2f}")

    def normalise_angle(self, alf): # Функция нормализирующая угол
        alf = alf % (2 * math.pi)
        if alf > math.pi:
            alf -= 2 * math.pi
        return alf
    
    def control_loop(self): 
        # Функция контролирующая все процессы
        if self.xg == None or self.yg == None: return

        if self.xt is None or self.yt is None or self.theta is None:
            self.get_logger().warn("Waiting for turtle pose data...", throttle_duration_sec=2.0)
            return
        p = math.sqrt((self.xg -self.xt)**2 + (self.yg -self.yt)**2)

        if p < 0.05: # Если черепаха у цели
            twist = Twist()
            twist.linear.x = 0.0
            twist.angular.z = 0.0
            self.turtle_do_publisher.publish(twist)

            self.get_logger().info("Goal is sucsess")
            self.xg = None
            self.yg = None
            return
        
        fi = math.atan2(self.yg - self.yt, self.xg - self.xt)
        alf = fi - self.theta
        self.get_logger().info(f"До нормализации: alf = {alf:.2f}")  
        alf = self.normalise_angle(alf)
        self.get_logger().info(f"После нормализации: alf = {alf:.2f}") 
        V = self.Kf * p * math.cos(alf)
        self.get_logger().info(f"Линейная скорость V: {V:.2f}")
        W = self.Kr * alf
        self.get_logger().info(f"Угловая скорость W: {W:.2f}")

        twist = Twist()
        twist.linear.x = V
        twist.angular.z = W
        self.turtle_do_publisher.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = Controller_turtle()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Controller stopped by user")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()