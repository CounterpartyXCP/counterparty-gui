**@ouziel-slama or @adamkrellenstein:**

- Quality Assurance
- Update `CHANGELOG.md`
- Update `APP_VERSION` in `counterpartygui/__init__.py`
- Merge develop into Master
- Build binaries:
    * In a new VM install Windows dependencies (http://counterparty.io/docs/windows/)
    * Install PyQT5 (http://www.riverbankcomputing.com/software/pyqt/download5)
    * `git clone https://github.com/CounterpartyXCP/counterparty-gui.git`
    * `pip install -r requirements.txt`
    * `cd counterparty-gui`
    * check and update filenames in the begining of `freeze.py`
    * `python freeze.py bdist_msi`
- Generate MD5 hash of the MSI file
- Tag and Sign Release (include MD5 hash in message)
- Write [Release Notes](https://github.com/CounterpartyXCP/counterparty-gui/releases)
- Upload MSI file in [Github Release](https://github.com/CounterpartyXCP/counterparty-gui/releases)

**@ivanazuber:**:

- Post to [Official Forums](https://forums.counterparty.io/discussion/445/new-version-announcements-counterparty-and-counterpartyd), Skype, [Gitter](https://gitter.im/CounterpartyXCP)
- Post to social media
- SMS and mailing list notifications
