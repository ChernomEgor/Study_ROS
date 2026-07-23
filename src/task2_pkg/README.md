# ROS2 Trajectory Generator and Controller

## Описание
Пакет `task2_pkg` для генерации траекторий и управления черепахой в turtlesim.

Задание 2. Механизмы publisher-subscriber и remapping
Сделать ноду (назвать её следует trajectory_generator), публикующую три топика с
подвижными точками-целями, представляющими собой пары координат (x, y). В первом
топике (требуемое название — gerono) такая точка должна описывать лемнискату Жероно
(https://en.wikipedia.org/wiki/Lemniscate_of_Gerono), во втором (lissajous) — фигуру Лиссажу
(https://en.wikipedia.org/wiki/Lissajous_curve) с параметрами δ = π/2, a = 3, b = 2; в третьем
(quadrifolium) – квадрифолий (https://en.wikipedia.org/wiki/Quadrifolium).
Далее следует запустить три ноды: trajectory_generator, controller_node и turtlesim_node. При
этом с помощью механизма remapping следует переподписать controller_node с топика
turtle_goal на топик gerono. В результате описанных действий черепашка должна начать
ездить по траектории, напоминающей лемнискату Жероно.
То же следует повторить и с двумя другими фигурами.
Ограничения на скорости движения черепашки, размеры фигур-траекторий и прочие
несущественные детали — на выбор программиста.

## Структура
task2_pkg/
├── task2_pkg/
│   ├── controller.py
│   └── generator.py
├── resource/
├── package.xml
└── setup.py

## Установка
```bash
cd ~/ros2_task2v2_ws
colcon build --packages-select task2_pkg
source install/setup.bash
```
# Команды
## Терминал 1
```bash
ros2 run turtlesim turtlesim_node
```
## Терминал 2
```bash
cd ~/ros2_task2v2_ws/src/task2_pkg/task2_pkg
python3 generator.py
```
## Терминал 3 вариант 1
```bash
cd ~/ros2_task2v2_ws/src/task2_pkg/task2_pkg
python3 controller.py --ros-args --remap /turtle_goal:=/gerono
```
## Терминал 3 вариант 2
```bash
cd ~/ros2_task2v2_ws/src/task2_pkg/task2_pkg
python3 controller.py --ros-args --remap /turtle_goal:=/lissajous
```
## Терминал 3 вариант 3
```bash
cd ~/ros2_task2v2_ws/src/task2_pkg/task2_pkg
python3 controller.py --ros-args --remap /turtle_goal:=/quadrifolium
```