import pygame
import random

"""_______________设置游戏参数_________________"""

GameWidth   = 800                       #游戏窗口宽
GameHeight  = 600                       #游戏窗口高
GameCol     = 80                        #游戏分辨率
GameRow     = 60                        #游戏分辨率
_done       = True                      #游戏状态开关
FPS         = 15                        #游戏帧频
_bgimg      = 'resource\\snake_bg.png'  #游戏背景图
_bodyimg    = 'resource\\body.png'      #小蛇身体图
_headimg    = 'resource\\head.png'      #小蛇头部图
_foodimg    = 'resource\\food.png'      #食物图
_move       = 'right'                   #默认移动方向
_eated      = False                     #是否吃到食物
_dead       = False                     #活着
_score      = 0                         #得分
"""_______________设置参数结束_________________"""


""" 将游戏切割 120行 100列 其中每个格子的像素为10 """

pygame.init()                           #初始化

_size       = GameWidth, GameHeight
_window     = pygame.display.set_mode(_size)
_display    = pygame.display
_clock      = pygame.time.Clock()

""" 设置游戏窗口左上角的标题 """
_display.set_caption('爱吃的小蛇蛇')
""" 创建坐标对象 """


class coordi:
    _row = 0
    _col = 0

    def __init__(self, _row, _col):
        self._col = _col
        self._row = _row


""" 背景坐标 """
_background = coordi(_row=0, _col=0)
""" 蛇头坐标 """
_head = coordi(_row=5, _col=5)
""" 蛇身坐标 """
_body = []
""" 食物随机出现 """


def generate_food(_head, _body=[], max_tries=100):
    """
    该函数用于生成新的食物随机坐标。

    Args:
        _head: coordi类型 表示蛇头的坐标
        _body: 可选参数，类型为列表，表示蛇的身体坐标列表，默认为空列表。
        max_tries: 可选参数 类型为整数 表示产生随机数的最大尝试次数 默认为100次。

    Returns:
        返回coordi类型 表示新生成的食物坐标 如果尝试次数已达最大值 则返回None。
    """
    # 生成新的食物随机坐标位置
    new_food_x = random.randint(0, GameRow - 1)
    new_food_y = random.randint(0, GameCol - 1)
    # 根据生成的随机坐标位置得到食物的coordi对象
    new_food = coordi(_row=new_food_x, _col=new_food_y)

    # 如果新食物与头部重合，则重新生成新的食物坐标
    if _head == new_food:
        max_tries -= 1
        if max_tries <= 0:
            # 如果尝试次数耗尽，则返回None
            return None
        else:
            """
            否则递归调用自身函数，重新生成新的食物坐标位置
            注意,这里递归调用函数时,需要将max_tries传递下去,确保函数不会一直循环下去。
            """
            return generate_food(_head, _body=_body, max_tries=max_tries)

    # 如果新食物的坐标已经存在于蛇的身体坐标列表中，则重新生成新的食物坐标
    if new_food in _body:
        max_tries -= 1
        if max_tries <= 0:
            # 如果尝试次数耗尽，则返回None
            return None
        else:
            """
            否则递归调用自身函数，重新生成新的食物坐标位置
            注意,这里递归调用函数时,需要将max_tries传递下去,确保函数不会一直循环下去。
            """
            return generate_food(_head, _body=_body, max_tries=max_tries)

    # 如果新的食物坐标不与蛇的任何一个坐标冲突，就返回新的食物坐标
    return new_food


""" 食物坐标 """
_food = generate_food(_head, _body)
""" 绘制方法 """


def rect(_coordi, _img, _relative=False):
    """
    在游戏窗口中绘制指定图像，并设置其位置。

    Args:
        _coordi: coordi类型，表示图像的坐标
        _img: 字符串类型，表示图像的文件路径

    Returns:
        无返回值。
    """
    # 计算图像左上角的坐标，使其在格子中居中显示
    img_width, img_height = pygame.image.load(_img).get_size()  # 获取图像宽和高
    if _relative:
        img_width, img_height = 0, 0
    left_pos = _coordi._col * (GameWidth /
                                GameCol) - img_width / 2  # 图片宽度作为偏移量
    top_pos = _coordi._row * (GameHeight /
                                GameRow) - img_height / 2  # 图片高度作为偏移量

    # 在游戏窗口中指定位置绘制指定图像
    _window.blit(pygame.image.load(_img), (left_pos, top_pos))    



"""按钮类"""


class Button:
    """
    英文注释：This class represents a button that can be clicked by the player.

    中文注释：该类表示一个可以被玩家点击的按钮。
    """

    def __init__(self, text, x, y, width, height, 
                    color, hover_color, font,
                    font_size):
        """
        初始化按钮。

        Args:
            text: 字符串类型，表示按钮上显示的文本内容。
            x: 整型，表示按钮左上角的x坐标。
            y: 整型，表示按钮左上角的y坐标。
            width: 整型，表示按钮的宽度。
            height: 整型，表示按钮的高度。
            color: 元组类型，表示按钮的颜色，元组中包含3个整型数值，分别表示R、G、B分量。
            hover_color: 元组类型，表示当鼠标悬停在按钮上时按钮的颜色。
            font: 字符串类型，表示按钮文本的字体。
            font_size: 整型，表示按钮文本的字体大小。

        Returns：
            无返回值。
        """
        # 对实例变量进行赋值
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.font.SysFont(font, font_size)
        self.surface = self.font.render(self.text, True,
                                        (50, 50, 50))  # 创建按钮文本的surface对象
        self.rect = pygame.Rect(self.x, self.y, self.width,
                                self.height)  # 创建按钮的rect对象

    def draw(self, screen, mouse_pos):
        """
        在屏幕上绘制按钮，并根据鼠标状态切换颜色。

        Args:
            screen: 游戏窗口对象，表示按钮将在其上绘制。
            mouse_pos: 元组类型，鼠标当前的位置坐标。

        Returns:
            无返回值。
        """
        if self.rect.collidepoint(mouse_pos):
            # 当鼠标悬停在按钮上时，绘制更改颜色后的按钮
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            # 否则，绘制按钮
            pygame.draw.rect(screen, self.color, self.rect)

        # 在按钮中央绘制文本
        # 获取按钮文本的宽度和高度
        text_width, text_height = self.surface.get_size()
        # 将文本绘制在图形中央位置
        screen.blit(self.surface,
                    (
                        self.x + (self.width - text_width) / 2, 
                        self.y + (self.height - text_height) / 2)
                    )

    def is_clicked(self, mouse_pos):
        """
        判断鼠标是否点击了按钮，并返回点击结果。

        Args:
            mouse_pos: 元组类型，鼠标当前的位置坐标。

        Returns:
            返回True表示鼠标点击了按钮，False表示鼠标没有点击按钮。
        """
        return self.rect.collidepoint(mouse_pos)


reset_button = Button(
    "再来一局",  # 按钮文本
    GameWidth // 2 - 50,  # 按钮左上角x坐标
    350,  # 按钮左上角y坐标
    120,  # 按钮宽度
    50,  # 按钮高度
    (255, 255, 255),  # 按钮颜色
    (200, 200, 200),  # 鼠标悬停时按钮颜色
    "方正粗黑宋简体",  # 按钮文本字体
    24  # 按钮文本字体大小
)
""" 主循环 """
while _done:
    """ 捕捉事件 """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            _done = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and _move != "down":
                _move = "up"
            elif event.key == pygame.K_DOWN and _move != "up":
                _move = "down"
            elif event.key == pygame.K_LEFT and _move != "right":
                _move = "left"
            elif event.key == pygame.K_RIGHT and _move != "left":
                _move = "right"
        elif event.type == pygame.MOUSEBUTTONDOWN and reset_button.is_clicked(
                pygame.mouse.get_pos()):
            _dead = False
            _score = 0
            FPS = 15
            _move = 'right'
            _head = coordi(_row=5, _col=5)
            _food = generate_food(_head, _body)
    """ 吃东西 """
    if _head._col == _food._col and _head._row == _food._row:
        _eated = True
        _score += 1
        _food = generate_food(_head, _body)
    """ 移动蛇 """
    if _eated:
        _body.insert(0, coordi(_row=_head._row, _col=_head._col))
    elif len(_body) > 0:
        _body.insert(0, coordi(_row=_head._row, _col=_head._col))
        _body.pop()
    if _move == 'left':
        """ 向左移动 蛇头所在行坐标 - 1 """
        _head._col -= 1
    elif _move == 'right':
        """ 向右移动 蛇头所在行坐标 + 1 """
        _head._col += 1
    elif _move == 'up':
        """ 向上移动 蛇头所在列坐标 - 1 """
        _head._row -= 1
    elif _move == 'down':
        """ 向下移动 蛇头所在列坐标 + 1 """
        _head._row += 1
    """ 撞墙检测 """
    if _head._col < 0 or _head._col > GameCol or _head._row < 0 or _head._row > GameRow:
        _dead = True
    for _block in _body:
        if _block._col == _head._col and _block._row == _head._row:
            _dead = True
    """ 绘制背景图 """
    rect(_background, _bgimg, True)
    """ 绘制食物 """
    rect(_food, _foodimg)
    _eated = False
    """ 绘制蛇身 """
    if len(_body) > 0:
        for body in _body:
            rect(body, _bodyimg)
    """ 绘制蛇头 """
    rect(_head, _headimg)
    score_render = pygame.font.SysFont(
        '方正粗黑宋简体',
        20
        ).render('得分:' + str(_score), True,(0, 0, 0))
    _window.blit(score_render, (10, 10))
    if _dead:
        _fontpos = GameWidth // 2 - 90, GameHeight // 2 - 100
        _gameover = pygame.font.SysFont('方正粗黑宋简体',
                                        50).render('游戏结束', True, (0, 0, 0))
        _window.blit(_gameover, _fontpos)
        FPS = 0
        _body = []
        _head = coordi(_row=-10, _col=0)
        _food = coordi(_row=GameRow, _col=GameCol)
        reset_button.draw(_window, pygame.mouse.get_pos())
    _display.flip()
    if _score > 10:
        FPS += _score // 10
    _clock.tick(FPS)
pygame.quit()