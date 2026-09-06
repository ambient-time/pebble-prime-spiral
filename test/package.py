"""Validate the six-target PBW and evidence before staging a local review package.

Copyright 2026 Luke Steuber. MIT License. No upload or physical-watch connection.
"""
import hashlib
import json
from pathlib import Path
import re
import shutil
import zipfile

from libpebble2.util.stm32_crc import crc32

ROOT=Path(__file__).resolve().parent.parent
TARGETS={'basalt','chalk','diorite','emery','flint','gabbro'}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    pbw=ROOT/'build'/f'{ROOT.name}.pbw'
    digest=sha(pbw)
    source=json.loads((ROOT/'package.json').read_text())
    reports={}
    with zipfile.ZipFile(pbw) as z:
        assert z.testzip() is None,'Corrupt PBW'
        info=json.loads(z.read('appinfo.json'))
        assert info['uuid']==source['pebble']['uuid']
        assert info['versionLabel']==source['version']
        assert info['watchapp']['watchface'] is True
        assert info['companyName']=='Luke Steuber'
        assert not info['capabilities'] and not info['appKeys']
        assert set(info['targetPlatforms'])==TARGETS
        for platform in sorted(TARGETS):
            manifest=json.loads(z.read(platform+'/manifest.json'))
            for key in ('application','resources'):
                item=manifest[key];data=z.read(platform+'/'+item['name'])
                assert len(data)==item['size'],f'{platform} {key} size'
                assert crc32(data)==item['crc'],f'{platform} {key} CRC'
            report=json.loads((ROOT/f'build/evidence/{platform}-report.json').read_text())
            assert report['pbwSHA256']==digest,f'{platform} evidence is stale'
            assert report['secondsChanged'] and report['naturalNoonRollover'] and report['naturalMidnightRollover']
            assert all((ROOT/file).is_file() for file in report['frames'])
            reports[platform]=report
    out=ROOT/'release';out.mkdir(exist_ok=True)
    shutil.copy2(pbw,out/f'prime-spiral-{source["version"]}.pbw')
    evidence=ROOT/'evidence';evidence.mkdir(exist_ok=True)
    summary={'version':source['version'],'pbwSHA256':digest,'platforms':{}}
    for platform,report in reports.items():
        archived=dict(report)
        archived['frames']=['evidence/'+Path(f).name for f in report['frames'] if not Path(f).stem.endswith('-boot')]
        (evidence/f'{platform}-report.json').write_text(json.dumps(archived,indent=2)+'\n')
        for name in report['frames']:
            file=ROOT/name
            if file.stem.endswith('-boot'):continue # This is firmware UI, not the watchface.
            shutil.copy2(file,evidence/file.name)
        samples=[tuple(map(int,m.groups())) for line in report['logs']
                 if (m:=re.search(r'ms=(\d+) heap=(\d+) frames=',line))]
        summary['platforms'][platform]={'capturedAt':report['capturedAt'],
            'loggedRenderMS':{'min':min(s[0] for s in samples),'max':max(s[0] for s in samples)},
            'minimumLoggedFreeHeapBytes':min(s[1] for s in samples),
            'naturalNoonRollover':True,'naturalMidnightRollover':True,
            'cadenceFrames':report['cadenceFrames']}
    summary['limits']='Production PBW tested in isolated native emulators. Physical-watch battery/readability and CloudPebble build are separate checks; see the publication record for store state.'
    (evidence/'validation.json').write_text(json.dumps(summary,indent=2)+'\n')
    archive=out/f'prime-spiral-{source["version"]}-source.zip'
    files=[ROOT/name for name in ('package.json','wscript','Makefile','README.md','LICENSE','.gitignore','.gitattributes')]
    # Independent-build proof names this archive's hash and stays outside it.
    excluded={'independent-build.json','independent-build.log'}
    for directory in ('src','resources','reference','test','tools','evidence'):
        files.extend(p for p in (ROOT/directory).rglob('*') if p.is_file()
                     and '__pycache__' not in p.parts and p.name not in excluded)
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for file in sorted(files):z.write(file,file.relative_to(ROOT))
        assert z.testzip() is None
    (out/'SHA256SUMS').write_text(''.join(f'{sha(p)}  {p.name}\n' for p in sorted(out.iterdir()) if p.suffix in ('.pbw','.zip')))
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
