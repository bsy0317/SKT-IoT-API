# NUGU 스마트홈 API 서버 🏠💡

NUGU 스마트홈 디바이스를 제어하기 위한 비공식 API 서버입니다.  
반디스마트스위치 BDS03B에서 테스트되었으며, 현재는 전원 제어만 지원합니다.

## Prerequisites 🛠️

> `authorization`, `widgetId` 값은 Packet Capture를 통해 얻을 수 있습니다.
- NUGU 스마트홈에서 얻은 `authorization`  Key
- NUGU 스마트홈에서 얻은 `widgetId`  Value  

## Installation 🚀

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/smart-home-control-api.git
    ```

2. Navigate to the project directory:

    ```bash
    cd smart-home-control-api
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Configuration ⚙️

프로젝트 디렉토리에 `settings.ini` 파일이 필요합니다. `settings.ini` 파일은 `settings_sample.ini` 파일을 참고하여 작성하시면 됩니다.


## Usage ℹ️

### Windows 🖥️

1. Python dependencies를 설치합니다.
```bash
pip install -r requirements.txt
```

2.  `run_windows.bat` 스크립트를 실행합니다.
   ```bash
run_windows.bat
```

### Linux 🐧

1. Python dependencies를 설치합니다.
```bash
pip install -r requirements.txt
```

2. `run_linux.sh` 스크립트를 실행합니다.
```bash
./run_linux.sh
```

## Endpoints 📡

### Control Device

- **Endpoint:** `/controlDevice/<action>`
- **Methods:** GET
- **Description:** Controls the device by turning it on or off.
- **Actions:**
  - `on`: Turns the device on.
  - `off`: Turns the device off.

### Check Status

- **Endpoint:** `/controlDevice/status`
- **Methods:** GET
- **Description:** Checks the status of the device.

## License 📝

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
