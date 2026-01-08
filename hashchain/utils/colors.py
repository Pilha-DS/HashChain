"""Utilitário para formatação de cores no terminal."""
from typing import Optional


class ColorFormatter:
    """Formata strings com cores ANSI para terminal."""
    
    COLOR_ALIASES = {
        "r": "31m",  # red
        "g": "32m",  # green
        "y": "33m",  # yellow
        "b": "34m",  # blue
        "p": "35m",  # purple
        "c": "36m",  # cyan
        "w": "37m",  # white
        "bl": "30m",  # black
        "gr": "90m",  # gray
    }
    
    RESET = '\033[0m'
    BOLD = '\033[1m'
    ITALIC = '\033[3m'
    
    @classmethod
    def format(
        cls,
        color: str = "",
        bold: bool = False,
        italic: bool = False,
        underline: bool = False,
        faint: bool = False
    ) -> str:
        """
        Formata código de cor ANSI.
        
        Args:
            color: Cor desejada (r, g, y, b, p, c, w, bl, gr)
            bold: Aplicar negrito
            italic: Aplicar itálico
            underline: Aplicar sublinhado
            faint: Aplicar estilo fraco
            
        Returns:
            Código ANSI formatado
        """
        if not color and not bold and not italic and not underline and not faint:
            return cls.RESET
        
        if not color:
            color_code = "37m"
        elif color.lower() in cls.COLOR_ALIASES:
            color_code = cls.COLOR_ALIASES[color.lower()]
        else:
            color_code = "37m"
        
        style = ""
        if bold:
            style += "1;"
        if faint:
            style += "2;"
        if italic:
            style += "3;"
        if underline:
            style += "4;"
        if not style:
            style = "0;"
        
        return f"\033[{style}{color_code}"
    
    @classmethod
    def c(
        cls,
        color: str = "",
        bold: bool = False,
        italic: bool = False,
        underline: bool = False,
        faint: bool = False
    ) -> str:
        """Alias para format()."""
        return cls.format(color, bold, italic, underline, faint)

