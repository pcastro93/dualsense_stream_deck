import pywinctl as pwc
from tabulate import tabulate


def get_active_window():
    try:
        return pwc.getActiveWindow()
    except Exception as e:
        print(f"Error getting active window: {e}")
        return None


def get_all_windows():
    try:
        return pwc.getAllWindows()
    except Exception as e:
        print(f"Error getting all windows: {e}")
        return None


def print_all_windows_data():
    """Prints all windows data in a table format"""
    windows = get_all_windows()
    if windows:
        windows_data = [[w.getAppName(), w.title] for w in windows]
        print(
            tabulate(windows_data, headers=["App Name", "Title"], tablefmt="fancy_grid")
        )
    else:
        print("No windows found")
