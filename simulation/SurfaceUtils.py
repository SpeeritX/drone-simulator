import pygame


def colorizeSurface(surface, color):
    rect = surface.get_rect()
    colorImage = pygame.Surface(rect.size).convert_alpha()
    colorImage.fill(color)
    colorImage.blit(surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    return colorImage


def blendColors(a, b, t):
    """ Linearly interpolates between colors a and b by t.
        t is clamped between 0 and 1. When t is 0 color is a. When t is 1 color is b.
        Applies calculated color on surface """
    result = tuple(a[i] + (b[i] - a[i]) * t for i in range(3))
    return result


def extendSurface(surface, size=4):
    """ Recommended to use for smooth edges
        size = 4 is optimal value for smooth edges """
    rect = surface.get_rect()
    newSurface = pygame.Surface((rect.size[0] + size, rect.size[1] + size), pygame.SRCALPHA).convert_alpha()
    newSurface.blit(surface, (size/2, size/2))
    return newSurface


def scaleSurface(sprite, size):
    spriteSize = sprite.get_rect().size
    xRatio = spriteSize[0] / size[0]
    yRatio = spriteSize[1] / size[1]
    ratio = min(xRatio, yRatio)
    new_size = (int(spriteSize[0] / ratio), int(spriteSize[1] / ratio))
    return pygame.transform.scale(sprite, new_size)


def _normVector(vector):
    magnitude = sum(i**2 for i in vector)**(1/2)
    return tuple(i/magnitude for i in vector)


def drawDashedLine(surface, color, start, end, width=1, length=1, shift=0):
    unit = _normVector((end[0]-start[0], end[1]-start[1]))
    shift = length * 2 - shift
    step = (unit[0] * length, unit[1] * length)
    pos = (start[0] - unit[0] * shift, start[1] - unit[1] * shift)
    while pos[0] <= end[0] and pos[1] <= end[1]:
        end_pos = (pos[0] + step[0], pos[1] + step[1])
        pygame.draw.line(surface, color, pos, end_pos, width)
        pos = (pos[0] + 2*step[0], pos[1] + 2*step[1])
