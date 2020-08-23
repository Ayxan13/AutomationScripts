#What is this?

A tool to manually run Qt-UIC on a .UI file.

#How to use?

```
python RunUic.py --set-uic Path/To/Uic/uic.exe
python RunUic.py --set-ui-dir Path/To/ProjectDir/WithUiFiles
python RunUic.py --run SomeFile.ui # generates ui_SomeFile.h
```

#How does this speed up the process?

Once set-up, you can quickly do `python RunUic.py --SomeFile.ui` without finding the project folder and finding the UIC.exe and so on.