#!/usr/bin/env python3
import rclpy
import math
from rclpy.node import Node
from turtle_interfaces.srv import LineSizes
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from turtlesim.msg import Color
from turtlesim.srv import SetPen
class Turtle_draw(Node):
    def __init__(self):
        super().__init__("turtle_draw")
        self.is_drawing = True
        self.dash_length = None
        self.gap_length = None
        self.prev_dash_length = None
        self.prev_gap_length = None

        self.distance_traveled = 0.0
        self.last_x = 0.0
        self.last_y = 0.0
        self.first_pose = True

        # Сервисы/подписки/публикаторы
        self.line_sizes_service = self.create_service(LineSizes, "line_sizes", self.init_line_sizes)
        self.pose_subscriber = self.create_subscription(Pose, "/turtle1/pose", self.get_pose, 10)
        self.turtle_do_publisher = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.color_sub = self.create_subscription(Color, '/turtle1/color_sensor', self.color_callback, 10)

        # Клиент для set_pen (СНАЧАЛА создаем)
        self.set_pen_client = self.create_client(SetPen, '/turtle1/set_pen')
        # Ждем сервис (опционально, но надежнее)
        while not self.set_pen_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for /turtle1/set_pen service...')

        # А теперь вызываем метод, который использует клиент
        self.set_pen_white()

        # Таймер в конце
        self.timer = self.create_timer(0.1, self.control_loop)


    def init_line_sizes(self, request: LineSizes.Request, response: LineSizes.Response):
        if self.prev_dash_length is None:
            self.prev_dash_length = 0.0
        if self.prev_gap_length is None:
            self.prev_gap_length = 0.0
        
        self.prev_dash_length = self.dash_length if self.dash_length is not None else 0.0
        self.prev_gap_length = self.gap_length if self.gap_length is not None else 0.0
        
        self.dash_length = request.dash_length
        self.gap_length = request.gap_length
        
        response.prev_dash_length = self.prev_dash_length
        response.prev_gap_length = self.prev_gap_length
        
        return response

    def color_callback(self, msg):
        pass
    
    def set_pen(self, draw):
        request = SetPen.Request()
        if draw:
            request.r = 255
            request.g = 255
            request.b = 255
            request.width = 1
            request.off = 0
        else:
            request.off = 1
        self.set_pen_client.call_async(request)

    def set_pen_white(self):
        request = SetPen.Request()
        request.r = 255
        request.g = 255
        request.b = 255
        request.width = 1
        request.off = 0
        self.set_pen_client.call_async(request)

    def get_pose(self, msg):
        if self.first_pose:
            self.last_x = msg.x
            self.last_y = msg.y
            self.first_pose = False
            
        else:
            dx = msg.x - self.last_x
            dy = msg.y - self.last_y
            distance = math.sqrt(dx*dx + dy*dy)
            if distance > 0.01:
                self.distance_traveled += distance
            self.last_x = msg.x
            self.last_y = msg.y
            self.get_logger().info(f"Пройдено: {distance:.4f}, всего: {self.distance_traveled:.2f}")
            
    def control_loop(self):
        if self.dash_length is None or self.gap_length is None:
            self.get_logger().warn("Параметры не установлены! Вызовите сервис /line_sizes")
            return
                # Всегда едем
        twist = Twist()
        twist.linear.x = 1.0
        twist.angular.z = 0.0

        self.get_logger().info(f"is_drawing={self.is_drawing}, distance={self.distance_traveled:.2f}")

        if self.is_drawing:
            # Штрих: едем и рисуем
            if self.distance_traveled >= self.dash_length:
                self.get_logger().info("Переключение: штрих -> пробел (поднимаем перо)")
                self.is_drawing = False
                self.set_pen(False)  # Поднимаем перо
        else:
            # Пробел: едем, но не рисуем
            if self.distance_traveled >= self.dash_length + self.gap_length:
                self.get_logger().info("Переключение: пробел -> штрих (опускаем перо)")
                self.is_drawing = True
                self.distance_traveled = 0.0
                self.set_pen(True)   # Опускаем перо
        
        self.turtle_do_publisher.publish(twist)

        
    
def main(args=None):
    rclpy.init(args=args)
    node = Turtle_draw()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Turtle_draw stopped by user")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()