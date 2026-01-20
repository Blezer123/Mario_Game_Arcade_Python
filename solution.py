def human_read_format(size):
    if size < 1024:
        return f'{size}Б'
    if size < 1024 ** 2:
        return f'{round(size / 1024)}КБ'
    if size < 1024 ** 3:
        return f'{round(size / 1024 ** 2)}МБ'
    if size < 1024 ** 4:
        return f'{round(size / 1024 ** 3)}ГБ'