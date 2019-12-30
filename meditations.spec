# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['meditations.py'],
             pathex=['C:\\DIY\\meditations'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
			 
a.datas += [('./qt_ui/meditations.ui', './qt_ui/meditations.ui', 'DATA'),
		 ('./qt_ui/journal_entry.ui', './qt_ui/journal_entry.ui', 'DATA'),
		 ('./qt_ui/journal_reader.ui', './qt_ui/journal_reader.ui', 'DATA'),
		 ('./images/icon.png', './images/icon.png', 'DATA'),
		 ('./images/pen_icon.png', './images/pen_icon.png', 'DATA'),
         ('./images/read_icon.png', './images/read_icon.png', 'DATA')]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='meditations',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='meditations')
