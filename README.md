# game-of-life

Игра в жизнь с графическим интерфейсом, написанном на tkinter. Если вы не знакомы с этой zero-player игрой, то прочитать о ней можно на [wiki](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life).

## Установка

Приложение поддерживает все те же операционные системы, что и tkinter, то есть MacOS, Linux, Windows:

1.  Установите python3 (Если что-то не работает, то ставьте python 3.9 так как на нём разрабатывалось данное приложение);

2. Скачайте репозиторий с github, например используя **Code→Download Zip** или введя в консоль:

   ```git clone https://github.com/Grafit24/game-of-life.git```

## Запуск и использование

Чтобы запустить приложение достаточно запустить app.py (кликнув по нему два раза, если вы поставили в загрузщике python нужную галочку). Или открыв консоль в папке приложения ввести команду на Windows:

```python <путь к папке>/app.py ```

и для Linux, MacOS:

```python3 <путь к папке>/app.py ```

Запустив приложения вы увидите это:

![image-20220105004603180](/images/img1.png)

Управление простое:

- Чтобы добавить клетку нажмите ЛКМ;
- чтобы удалить ПКМ;
- чтобы перемещаться по полю двигайте мышью с зажатым колёсиком.

Начать симуляцию можно нажав `Start Cycle` завершить `Stop Cycle`, при этом важно, что `Stop Cycle` останавливает симуляция и ОЧИЩАЕТ поле, будьте внимательны! Управлять временем перехода между шагами можно введя в поле время в миллесекундах и нажав на `Set Delay` (изменять время можно в любой момент). 

Также если все клетки умирают это не останавливает цикл, в любом случае придётся нажать `Stop Cycle`.
