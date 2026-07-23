def print_progress_bar(iteration: int, total: int, prefix: str = '', suffix: str = '', decimals: int = 1, length: int = 100, fill: str = '█', print_end: str = "\n") -> None:
    """
    Call in a loop to create a terminal progress bar.
    
    Args:
        iteration: Current iteration (Int)
        total: Total iterations (Int)
        prefix: Prefix string (Str)
        suffix: Suffix string (Str)
        decimals: Positive number of decimals in percent complete (Int)
        length: Character length of bar (Int)
        fill: Bar fill character (Str)
        print_end: End character (e.g. "\\r", "\\r\\n") (Str)
    """
    if total == 0:
        return
        
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    
    # We use \r to return to the start of the line and overwrite
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=print_end if iteration == total else '\r')
