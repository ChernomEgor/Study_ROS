#!/usr/bin/env python3
import rclpy
import math
from rclpy.node import Node
from std_msgs.msg import Int32
from turtlesim.msg import Pose
from turtlesim.srv import Spawn, Kill


class Listener_node(Node):
    def __init__(self):
        super().__init__("node_listener")
        self.distance = 3
        self.current_cnt_turtle = 1

        self.cnt_turtle = None
        self.xt = None
        self.yt = None
        self.theta_t = None
        self.x_past = None
        self.y_past = None
        self.current_distance = 0.0
        self.names_turtles = []

        self.cnt_subscriber = self.create_subscription(
            Int32, "cnt_turtles", self.get_cnt_turtles, 10
        )
        self.pose_subscriber = self.create_subscription(
            Pose, "/turtle1/pose", self.get_pose, 10
        )
        self.spawn_client = self.create_client(Spawn, "/spawn")
        self.kill_client = self.create_client(Kill, "/kill")

    def get_cnt_turtles(self, msg):
        self.cnt_turtle = msg.data

    def get_pose(self, msg):
        self.xt = msg.x
        self.yt = msg.y
        self.theta_t = msg.theta
        self.cnt_distance()

    def spawn_turtle(self):
        if not self.spawn_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn("Spawn service not available")
            return
        self.get_logger().info("Spawn333")
        # Формируем запрос
        request = Spawn.Request()
        request.x = self.xt
        request.y = self.yt
        request.theta = self.theta_t
        request.name = f"turtle{self.current_cnt_turtle + 1}"
        # Отправляем запрос и обрабатывает ответ
        spawn_future = self.spawn_client.call_async(request)
        self.get_logger().info("Spawn445")
        spawn_future.add_done_callback(self.spawn_callback)
        self.get_logger().info("Spawn444")

    def spawn_callback(self, future):
        try:
            response = future.result()
            self.names_turtles.append(response.name)
            if self.current_cnt_turtle > self.cnt_turtle:
                self.kill_turtle()
            self.get_logger().info(f"Created {response.name}")
        except Exception as e:
            self.get_logger().error(f"Spawn failed: {e}")

    def kill_turtle(self):
        if not self.kill_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn("Kill service not available")
            return
        if not self.names_turtles:
            self.get_logger().warn("No turtles to kill")
            return
        request = Kill.Request()
        request.name = self.names_turtles[0]

        kill_future = self.kill_client.call_async(request)
        kill_future.add_done_callback(self.kill_callback)

    def kill_callback(self, future):
        try:
            future.result()
            if self.names_turtles:
                self.names_turtles.pop(0)
            self.get_logger().info("Killed turtle")
        except Exception as e:
            self.get_logger().error(f"Kill failed: {e}")

    def cnt_distance(self):
        if self.x_past == None or self.y_past == None:
            self.x_past = self.xt
            self.y_past = self.yt
            return

        delta_x = self.xt - self.x_past
        delta_y = self.yt - self.y_past
        self.current_distance += math.sqrt(delta_x**2 + delta_y**2)
        self.x_past = self.xt
        self.y_past = self.yt

        if self.current_distance >= self.distance:
            self.current_distance = 0.0
            if self.cnt_turtle is None:
                return

            self.current_cnt_turtle += 1
            self.spawn_turtle()


def main(args=None):
    rclpy.init(args=args)
    node = Listener_node()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Listener_node stopped by user")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
