"""Build the released source archive in an independent directory and compare payloads.

Copyright 2026 Luke Steuber. MIT License.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import struct
import subprocess
import tempfile
import zipfile

ROOT=Path(__file__).resolve().parent.parent
TARGETS=('basalt','chalk','diorite','emery','flint','gabbro')
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def normalize(data):
    result=bytearray(data)
    assert result[:6]==b'PBLAPP'
    # SDK 4.33.1 app header: CRC at 0x14, resource timestamp at 0x7c.
    # The following ELF note must identify a 20-byte GNU build ID before ignoring it.
    assert struct.unpack('<III',result[132:144])==(4,20,3)
    assert result[144:148]==b'GNU\0'
    for start,end in ((20,24),(124,128),(148,168)):result[start:end]=b'\0'*(end-start)
    return bytes(result)
def main(pebble):
    source=json.loads((ROOT/'package.json').read_text())
    slug=source['name'];version=source['version']
    archive=ROOT/'release'/f'{slug}-{version}-source.zip'
    production=ROOT/'release'/f'{slug}-{version}.pbw'
    temp=Path(tempfile.mkdtemp(prefix=slug+'-independent-'))
    checkout=temp/slug;checkout.mkdir()
    try:
        with zipfile.ZipFile(archive) as z:
            assert z.testzip() is None
            assert all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in z.namelist())
            z.extractall(checkout)
        process=subprocess.run(['make','build','PEBBLE='+pebble],cwd=checkout,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        (ROOT/'evidence/independent-build.log').write_text(process.stdout)
        assert process.returncode==0,'Independent build failed; see evidence/independent-build.log'
        rebuilt=checkout/'build'/f'{slug}.pbw'
        proof={'sourceZipSHA256':sha(archive),'productionPBWSHA256':sha(production),'independentPBWSHA256':sha(rebuilt),
               'sdk':'4.33.1','hostTestsPassed':True,'sixTargetBuildPassed':True,'payloadChecks':{}}
        with zipfile.ZipFile(production) as a,zipfile.ZipFile(rebuilt) as b:
            assert json.loads(a.read('appinfo.json'))==json.loads(b.read('appinfo.json'))
            for target in TARGETS:
                old=a.read(target+'/pebble-app.bin');new=b.read(target+'/pebble-app.bin')
                assert normalize(old)==normalize(new),target+' code differs'
                assert a.read(target+'/app_resources.pbpack')==b.read(target+'/app_resources.pbpack'),target+' resources differ'
                proof['payloadChecks'][target]={'codeIdenticalOutsideCRCResourceTimestampAndGNUBuildID':True,
                    'resourcesIdentical':True,'changedCodeByteOffsets':[i for i,(x,y) in enumerate(zip(old,new)) if x!=y]}
        proof['scope']='Independent unpacked source archive. SDK build metadata can change the rebuilt PBW hash. No physical-watch or publication check.'
        (ROOT/'evidence/independent-build.json').write_text(json.dumps(proof,indent=2)+'\n')
        print(json.dumps(proof,indent=2))
    finally:shutil.rmtree(temp)
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--pebble',default='pebble')
    main(parser.parse_args().pebble)
