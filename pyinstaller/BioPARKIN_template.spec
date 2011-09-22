# -*- mode: python -*-
a = Analysis([os.path.join(HOMEPATH,'support\\_mountzlib.py'), os.path.join(HOMEPATH,'support\\useUnicode.py'), '..\\src\\BioPARKIN.py'],
             pathex=['D:\\programme\\pyinstaller-1.5'])
pyz = PYZ(a.pure)
exe = EXE( pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('dist', 'BioPARKIN.exe'),
          debug=False,
          strip=False,
          upx=True,
          console=True )
