# ROS2 Turtle Controller

## Описание
Пакет `task1_pkg` для управления черепахой в turtlesim.

Задание 1. Механизм publisher-subscriber

В соответствии с презентацией "A controller for to-point motion.pdf" реализовать ноду-контроллер (назвать её следует controller_node) для движения черепашки. Смысл задания в том, чтобы дать пользователю возможность публиковать через консоль точку-цель для черепашки в топик turtle_goal, в которую бы она после этого успешно доезжала.

Примечание: презентация изначально посвящена ROS 1, а потому в незначительных деталях может отличаться от ROS 2.

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
# Study_ROS
