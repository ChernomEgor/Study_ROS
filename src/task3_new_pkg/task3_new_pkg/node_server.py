#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
from turtlesim.srv import SetPen


class Server_node(Node):
    def __init__(self):
        super().__init__("node_server")
        self.cnt_turtle = None
        self.defolt_cnt = 5
        self.timer = self.create_timer(
            1.0, self.publish_n
        )  # публикует каждую секунду123

        self.client_service = self.create_service(SetPen, "set_n", self.callback_service)
        self.cnt_turtles_publisher = self.create_publisher(Int32, "cnt_turtles", 10)

        msg = Int32()
        msg.data = self.defolt_cnt
        self.cnt_turtles_publisher.publish(msg)

    def publish_n(self):
        msg = Int32()
        if self.cnt_turtle is None:
            return
        msg.data = self.cnt_turtle
        self.cnt_turtles_publisher.publish(msg)

    def callback_service(self, request, response):
        n = request.r
        if n > 0:
            self.cnt_turtle = n

            msg = Int32()
            msg.data = self.cnt_turtle
            self.cnt_turtles_publisher.publish(msg)
            self.get_logger().info(f"Published initial N={self.defolt_cnt}")
        return response


def main(args=None):
    rclpy.init(args=args)
    node = Server_node()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Server_node stopped by user")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
