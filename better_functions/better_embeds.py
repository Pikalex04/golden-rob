from discord import Embed

from random import choice


# TODO: make the colors editable in a settings file
def embed_color():
    return choice([0xFFD700, 0xDC143C, 0x2194FF, 0xFF9421, 0xA146F3, 0x008C45, 0xCD212A])


# TODO: make the emoji editable in a settings file
def error_embed(description):
    """Makes an embed for errors."""
    return Embed(description='<:error:1230541997824147467> | ' + description, color=embed_color())


# TODO: make the emoji editable in a settings file
def loading_embed(description):
    """Makes an embed for loading instances."""
    return Embed(description='<a:loading:1230201783817863168> | ' + description, color=embed_color())


def timeout_embed(user):
    """Makes an embed to let the user know they took too long to respond."""
    return error_embed(f'{user.mention}, you took too long! Please try again.')


def simple_embed(description):
    """Makes an embed with only a description."""
    return Embed(description=description, color=embed_color())


# TODO: make the emoji editable in a settings file
def success_embed(description):
    """Makes an embed for successful responses."""
    return Embed(description='<:success:1230888794450952263> | ' + description, color=embed_color())
