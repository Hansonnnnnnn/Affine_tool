"""
颜色工具模块，用于在终端中输出彩色文本
"""
import sys

# Windows 终端颜色支持初始化
if sys.platform == "win32":
    # Windows 10+ 支持 ANSI 转义码，但需要启用虚拟终端处理
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        # 启用虚拟终端处理
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except:
        pass  # 如果失败，继续使用 ANSI 码（Windows 10+ 通常已经支持）

# ANSI 转义码
class Colors:
    """颜色常量"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    # 基础颜色
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # 亮色
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'

def colorize(text: str, color: str, bold: bool = False) -> str:
    """给文本添加颜色"""
    result = color
    if bold:
        result += Colors.BOLD
    result += text + Colors.RESET
    return result

# 便捷函数
def title(text: str) -> str:
    """标题样式 - 青色加粗"""
    return colorize(text, Colors.BRIGHT_CYAN, bold=True)

def success(text: str) -> str:
    """成功信息 - 绿色"""
    return colorize(text, Colors.BRIGHT_GREEN)

def error(text: str) -> str:
    """错误信息 - 红色"""
    return colorize(text, Colors.BRIGHT_RED)

def warning(text: str) -> str:
    """警告信息 - 黄色"""
    return colorize(text, Colors.BRIGHT_YELLOW)

def info(text: str) -> str:
    """信息 - 蓝色"""
    return colorize(text, Colors.BRIGHT_BLUE)

def highlight(text: str) -> str:
    """高亮文本 - 亮白色加粗"""
    return colorize(text, Colors.BRIGHT_WHITE, bold=True)

def key_value(key: str, value: str) -> str:
    """键值对格式 - 键用青色，值用亮白色"""
    return f"{colorize(key, Colors.CYAN)}: {highlight(value)}"

def separator() -> str:
    """分隔线 - 青色"""
    return colorize("=" * 30, Colors.CYAN)
