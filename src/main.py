'''
 =======================================================================
 ····Y88b···d88P················888b·····d888·d8b·······················
 ·····Y88b·d88P·················8888b···d8888·Y8P·······················
 ······Y88o88P··················88888b·d88888···························
 ·······Y888P··8888b···88888b···888Y88888P888·888·88888b·····d88b·······
 ········888······"88b·888·"88b·888·Y888P·888·888·888·"88b·d88P"88b·····
 ········888···d888888·888··888·888··Y8P··888·888·888··888·888··888·····
 ········888··888··888·888··888·888···"···888·888·888··888·Y88b·888·····
 ········888··"Y888888·888··888·888·······888·888·888··888··"Y88888·····
 ·······························································888·····
 ··························································Y8b·d88P·····
 ···························································"Y88P"······
 =======================================================================

 -----------------------------------------------------------------------
Author       : 焱铭
Date         : 2025-11-13 13:10:34 +0800
LastEditTime : 2025-11-13 16:37:15 +0800
Github       : https://github.com/YanMing-lxb/
FilePath     : /PHE_FlipOptimizer/src/main.py
Description  : 
 -----------------------------------------------------------------------
'''

import math
from typing import Dict, Any


def tool_phe_flip(
    spacing_a: float,
    spacing_b: float,
    length: float,
    width: float,
    thinkness: float,
    fillet_radius: float,
) -> Dict[str, Any]:
    """
    计算板式换热器的翻边参数优化结果
    
    该函数基于给定的板片参数，计算出优化后的翻边偏移量、角度等参数，
    用于指导板片制造中的翻边工艺设计。

    Parameters
    ----------
    spacing_a : float
        A侧通道间距(mm)，即当B板叠在A板上时，A侧的通道间距
    spacing_b : float
        B侧通道间距(mm)，即当A板叠在B板上时，B侧的通道间距
    length : float
        板片长度(mm)，B板固定，根据翻边参数调整A板的实际长度
    width : float
        板片宽度(mm)，B板固定，根据翻边参数调整A板的实际宽度
    thinkness : float
        板片厚度(mm)，A板和B板的板片厚度，通常为固定值
    fillet_radius : float
        圆角半径(mm)，B板固定，根据翻边参数调整A板的圆角半径

    Returns
    -------
    Dict[str, Any]
        包含优化后各项参数的字典：
        - offset: 翻边偏移量(mm)
        - angle: 翻边角度(度)
        - flip_angle: 翻边角度(度)，等于90+angle
        - draft_angle: 拔模角度(度)，等于angle
        - length: 优化后板片长度(mm)
        - width: 优化后板片宽度(mm)
        - fillet_radius: 优化后圆角半径(mm)
    """
    
    opposite = 2 * thinkness
    hypotenuse = spacing_a + spacing_b + 2 * thinkness
    angle = math.degrees(math.asin(opposite / hypotenuse))

    # 计算翻边偏移量
    hypotenuse_min = spacing_a + thinkness - hypotenuse / 2 
    offset = hypotenuse_min * math.tan(math.radians(angle))

    flip_angle = 90 + angle
    draft_angle = angle
    length = length - 2* offset
    width = width - 2 * offset
    fillet_radius = fillet_radius - offset
    
    return {
        "offset": offset, 
        "angle": angle, 
        "flip_angle": flip_angle, 
        "draft_angle": draft_angle, 
        "length": length, 
        "width": width, 
        "fillet_radius": fillet_radius
    }


# ANSI颜色代码
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def get_user_input(prompt: str, value_type: type = float) -> float:
    """
    获取用户输入并验证类型
    
    Parameters
    ----------
    prompt : str
        提示信息
    value_type : type
        期望的数据类型
        
    Returns
    -------
    float
        用户输入的有效数值
    """
    while True:
        try:
            user_input = input(Colors.OKCYAN + prompt + Colors.ENDC)
            return value_type(user_input)
        except ValueError:
            print(Colors.FAIL + "输入无效，请重新输入！" + Colors.ENDC)


def print_result(params: dict, result: dict):
    """
    打印计算结果
    
    Parameters
    ----------
    params : dict
        输入参数字典
    result : dict
        计算结果字典
    """
    
    # 打印计算结果
    print("-" * 40)
    print(Colors.OKGREEN + Colors.BOLD + "优化结果:" + Colors.ENDC)
    print(Colors.OKBLUE + f"  板片等距偏移量: {result['offset']:.4f} mm" + Colors.ENDC)
    print(Colors.OKBLUE + f"  翻边角度: {result['flip_angle']:.2f} deg" + Colors.ENDC)
    print(Colors.OKBLUE + f"  拔模角度:  {result['draft_angle']:.2f} deg" + Colors.ENDC)
    print(Colors.WARNING + f"  优化后板片长度: {result['length']:.4f} mm" + Colors.ENDC)
    print(Colors.WARNING + f"  优化后板片宽度: {result['width']:.4f} mm" + Colors.ENDC)
    print(Colors.WARNING + f"  优化后圆角半径: {result['fillet_radius']:.4f} mm" + Colors.ENDC)
    print("=" * 40)
    print(Colors.OKCYAN + ' '*30 + "by YanMing" + Colors.ENDC)


def main():
    print("=" * 40)
    print(Colors.OKGREEN + Colors.BOLD + "板式换热器翻边计算工具" + Colors.ENDC)
    print("=" * 40)
    print(Colors.OKCYAN + "请输入参数：" + Colors.ENDC)
    
    # 获取用户输入
    params = {
        'spacing_a': get_user_input(" A 侧通道间距 (mm): "),
        'spacing_b': get_user_input(" B 侧通道间距 (mm): "),
        'length': get_user_input(" 板片长度 (mm): "),
        'width': get_user_input(" 板片宽度 (mm): "),
        'thinkness': get_user_input(" 板片厚度 (mm): "),
        'fillet_radius': get_user_input(" 圆角半径 (mm): ")
    }
    
    # 计算结果
    result = tool_phe_flip(**params)
    
    # 显示结果
    print_result(params, result)
    
    # 等待用户按键退出
    input(Colors.OKCYAN + "\n按任意键退出..." + Colors.ENDC)


if __name__ == "__main__":
    main()