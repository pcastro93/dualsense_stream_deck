# Dualsense Stream Deck

This is a simple application that allows you to control your computer using a DualSense controller.

## Features
- Create custom shortcuts for specific applications (name and/or title).
- Support for hotkeys and commands.
- Support for pressing multiple buttons to perform an action (e.g: L2 + Arrow Right to move an application to the right).
- Hierarchical precedence of shortcuts.
- Check the [sample configuration](#sample-configuration) for more details.

## Uses
- Google Meet (toggle mic and camera)
- Web browser (navigate between tabs, content, etc.)
- IDE (run project, debug, etc.)
- System (volume, brightness, etc.)

## TODO
- [ ] Pass config as argument
- [ ] Mode/flag to view app names and titles
- [ ] Run in the background
- [ ] Detect when a controller is connected (start, restart, etc)
- [ ] Logs


## Setup

#### Requirements
- [Uv](https://docs.astral.sh/uv/)
- [Python 3.13](https://www.python.org/downloads/)
- [Bash support](https://en.wikibooks.org/wiki/Bash_Shell_Scripting)
- [KDE](https://en.wikipedia.org/wiki/KDE)

#### Development

##### Environment
- Create a virtual environment
  ```sh
  uv venv
  ```

- Install dependencies:
  ```sh
  uv sync
  ```

- Install the package in editable mode once (from the root folder):
  ```sh
  uv pip install -e .
  ```

- Configure [dualsense-controller](https://github.com/yesbotics/dualsense-controller-python?tab=readme-ov-file#installation):

### Sample Configuration

```yaml
shortcuts_config:
  system:
    level: system
    shortcuts:
      - volume_down:
        button: create # select
        type: command
        command: qdbus org.kde.kglobalaccel /component/kmix invokeShortcut 'decrease_volume'
      - volume_up:
        button: options # start
        type: command
        command: qdbus org.kde.kglobalaccel /component/kmix invokeShortcut 'increase_volume'
      - volume_mute:
        button: ps # playstation
        type: command
        command: qdbus org.kde.kglobalaccel /component/kmix invokeShortcut 'mute'
      - move_app_right:
        buttons:
          - l2
          - arrow_right
        type: hotkey
        hotkeys:
          - win
          - right
      - move_app_left:
        buttons:
          - l2
          - arrow_left
        type: hotkey
        hotkeys:
          - win
          - left
      - maximize_app:
        buttons:
          - l2
          - arrow_up
        type: hotkey
        hotkeys:
          - win
          - pgup
      - minimize_app:
        buttons:
          - l2
          - arrow_down
        type: hotkey
        hotkeys:
          - win
          - pgdn
      - show_windows:
        buttons:
          - l2
          - square
        type: hotkey
        hotkeys:
          - win
          - w
      - close_window:
        buttons:
          - l2
          - circle
        type: hotkey
        hotkeys:
          - alt
          - f4
  chrome:
    level: application
    application:
      - name:
        contains: chrome
    shortcuts:
      - reload:
        button: triangle
        type: hotkey
        hotkeys:
          - ctrl
          - r
      - next_tab:
        button: r1
        type: hotkey
        hotkeys:
          - ctrl
          - pgdn
      - prev_tab:
        button: l1
        type: hotkey
        hotkeys:
          - ctrl
          - pgup
      - go_back:
        button: arrow_left
        type: hotkey
        hotkeys:
          - alt
          - left
      - go_forward:
        button: arrow_right
        type: hotkey
        hotkeys:
          - alt
          - right
      - close_tab:
        button: circle
        type: hotkey
        hotkeys:
          - ctrl
          - w
  chrome_meet:
    level: application
    application:
      - name:
        contains: chrome
      - title:
        contains: meet
    shortcuts:
      - toggle_mute:
        button: cross
        type: hotkey
        hotkeys:
          - ctrl
          - d
      - toggle_camera:
        button: square
        type: hotkey
        hotkeys:
          - ctrl
          - e
  zed:
    level: application
    application:
      - name:
        contains: zed
    shortcuts:
      - next_tab:
        button: r1
        type: hotkey
        hotkeys:
          - ctrl
          - pgdn
      - prev_tab:
        button: l1
        type: hotkey
        hotkeys:
          - ctrl
          - pgup
      - go_to_begining:
        button: arrow_up
        type: hotkey
        hotkeys:
          - ctrl
          - home
      - go_to_end:
        button: arrow_down
        type: hotkey
        hotkeys:
          - ctrl
          - end
      - close_file:
        button: circle
        type: hotkey
        hotkeys:
          - ctrl
          - 4
```

## Main Author

Send any comments, patches, and suggestions to: 
[Piettro Castro](https://www.linkedin.com/in/piettro-castro-844208117/)
