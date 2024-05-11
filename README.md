# stt-windows

## Requirements

- windows 11
- python3
- pip
- ffmpeg

## Phyton packages

```powershell
pip install sounddevice numpy openai pynput scipy threading pydub plyer
```

## Usage

To use the `index.py` script for recording and transcribing audio:

1. **Setup**: Ensure all required packages are installed as listed in the "phyton packages" section above.
2. **Start the Script**: Run the script using Python:
  ```bash
  python index.py
  ```

  Or run the `stt.bat` file.
3. **Recording Controls**:
  - **Start Recording**: Double press the 'Ctrl' key quickly to start recording.
  - **Stop and Save Recording**: Double press the 'Ctrl' key again to stop the recording and save it.
  - **Alternate Recording**: Press the 'Alt' key to stop the current recording, save, transcribe, and start a new recording session immediately.

4. **Transcription**: The script automatically transcribes the audio using OpenAI's Whisper model once the recording is stopped and saved. The transcription will be typed out wherever your cursor is active, simulating keyboard typing.

5. **Notifications**: Notifications will appear to indicate the start and stop of recordings, and if the maximum recording length is reached (15 minutes). If the maximum recording length is reached, the script will stop the recording and you will lose the recording.
