# ROS2 Turtle Controller

## Описание
Пакет `task1_pkg` для управления черепахой в turtlesim.

Задание 1. Механизм publisher-subscriber

В соответствии с презентацией "A controller for to-point motion.pdf" реализовать ноду-контроллер (назвать её следует controller_node) движением черепашки. Смысл задания в том, чтобы дать пользователю возможность публиковать через консоль точку-цель для черепашки в топик turtle_goal, в которую бы она после этого успешно доезжала.

Примечание: презентация изначально посвящена ROS 1, а потому в незначительных деталях может отличаться от текущих реалий современных версий ROS 2.

## Структура
task1_pkg/
├── task1_pkg/
│   └── task1.py
├── resource/
├── package.xml
└── setup.py

## Установка
```bash
cd ~/ros2_task1_ws
colcon build --packages-select task1_pkg
source install/setup.bash
```
## Установка

### Терминал 1
```bash
ros2 run turtlesim turtlesim_node
```
### Терминал 2
```bash
ros2 run task1_pkg turtle_controller
```
### Терминал 3 (отправить цель)
```bash
ros2 topic pub /turtle_goal geometry_msgs/msg/Point "{x: 5.0, y: 5.0}"
```
