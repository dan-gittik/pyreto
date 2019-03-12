from pyreto.dictionary import Dictionary


class Font(str):
    
    def __new__(cls, value):
        self = super(Font, cls).__new__(cls, '\x1b[{}m'.format(value))
        self.value = str(value)
        return self

    def __add__(self, other):
        if isinstance(other, type(self)):
            return type(self)(self.value + ';' + other.value)
        return super(Font, self).__add__(other)

    def __getitem__(self, name):
        return self + fonts[name]

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __call__(self, string):
        return self + string + fonts.RESET


fonts = Dictionary(

    RESET             = Font(0),
    BOLD              = Font(1),
    DIM               = Font(2),
    ITALIC            = Font(3),
    UNDERLINE         = Font(4),
    BLINK             = Font(5),
    REVERSE           = Font(7),
    HIDDEN            = Font(8),

    RESET_BOLD        = Font(21),
    RESET_DIM         = Font(22),
    RESET_ITALIC      = Font(23),
    RESET_UNDERLINE   = Font(24),
    RESET_BLINK       = Font(25),
    RESET_REVERSE     = Font(27),
    RESET_HIDDEN      = Font(28),

    BLACK             = Font(30),
    RED               = Font(31),
    GREEN             = Font(32),
    YELLOW            = Font(33),
    BLUE              = Font(34),
    MAGENTA           = Font(35),
    CYAN              = Font(36),
    WHITE             = Font(37),
    RESET_FOREGROUND  = Font(39),

    ON_BLACK          = Font(40),
    ON_RED            = Font(41),
    ON_GREEN          = Font(42),
    ON_YELLOW         = Font(43),
    ON_BLUE           = Font(44),
    ON_MAGENTA        = Font(45),
    ON_CYAN           = Font(46),
    ON_WHITE          = Font(47),
    RESET_BACKGROUND  = Font(49),

    BRIGHT_BLACK      = Font(90),
    BRIGHT_RED        = Font(91),
    BRIGHT_GREEN      = Font(92),
    BRIGHT_YELLOW     = Font(93),
    BRIGHT_BLUE       = Font(94),
    BRIGHT_MAGENTA    = Font(95),
    BRIGHT_CYAN       = Font(96),
    BRIGHT_WHITE      = Font(97),

    ON_BRIGHT_BLACK   = Font(100),
    ON_BRIGHT_RED     = Font(101),
    ON_BRIGHT_GREEN   = Font(102),
    ON_BRIGHT_YELLOW  = Font(103),
    ON_BRIGHT_BLUE    = Font(104),
    ON_BRIGHT_MAGENTA = Font(105),
    ON_BRIGHT_CYAN    = Font(106),
    ON_BRIGHT_WHITE   = Font(107),

)
