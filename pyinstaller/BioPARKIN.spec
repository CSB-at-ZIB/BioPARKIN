# -*- mode: python -*-
a = Analysis([os.path.join(HOMEPATH,'support\\_mountzlib.py'), os.path.join(HOMEPATH,'support\\useUnicode.py'), 'd:\\workspace\\BioPARKIN\\src\\BioPARKIN.py'],
             pathex=['D:\\workspace\\BioPARKIN\\pyinstaller'])
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
