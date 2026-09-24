"""Composite overlays + color grade onto the source video with ffmpeg.
usage: python3 render.py CONFIG SRC OVERLAY_DIR OUT
       python3 render.py CONFIG SRC OVERLAY_DIR still.png --still SECONDS"""
import json, subprocess, sys

cfg_path, src, ovdir, out = sys.argv[1:5]
cfg = json.load(open(cfg_path, encoding='utf-8'))
GRADE = ("scale=1920:1080:flags=lanczos,"
         "eq=contrast=1.07:saturation=1.12:brightness=-0.01,"
         "vignette=angle=PI/5")
FADE = 0.4

def active(item, t):
    return item['start'] <= t and (item['end'] is None or t < item['end'])

if '--still' in sys.argv:
    t = float(sys.argv[-1])
    layers = [f'{ovdir}/grad.png']
    layers += [f'{ovdir}/title_{i}.png' for i, x in enumerate(cfg['titles']) if active(x, t)]
    layers += [f'{ovdir}/telop_{i:02d}.png' for i, x in enumerate(cfg['telops']) if active(x, t)]
    ins = ['-ss', str(t), '-i', src] + sum((['-i', l] for l in layers), [])
    fc, last = [f'[0:v]{GRADE}[v0]'], 'v0'
    for i in range(len(layers)):
        fc.append(f'[{last}][{i+1}:v]overlay[v{i+1}]'); last = f'v{i+1}'
    sys.exit(subprocess.call(['ffmpeg', '-y', '-loglevel', 'error', *ins, '-filter_complex', ';'.join(fc),
                              '-map', f'[{last}]', '-frames:v', '1', out]))

ins = ['-i', src, '-loop', '1', '-framerate', '60', '-i', f'{ovdir}/grad.png']
fc = [f'[0:v]{GRADE}[g0]',
      '[1:v]format=rgba,fade=t=in:st=0.2:d=0.6:alpha=1[grad]',
      '[g0][grad]overlay=shortest=1[v0]']
last, n = 'v0', 2
for i, t in enumerate(cfg['titles']):
    # titles fade in (first one at 0.2s) and cross-fade when switching
    st = max(t['start'], 0.2)
    f = f'fade=t=in:st={st}:d={FADE}:alpha=1'
    if t['end'] is not None:
        f += f",fade=t=out:st={t['end'] - FADE / 2}:d={FADE / 2}:alpha=1"
    ins += ['-loop', '1', '-framerate', '60', '-i', f'{ovdir}/title_{i}.png']
    fc += [f'[{n}:v]format=rgba,{f}[t{i}]', f'[{last}][t{i}]overlay=shortest=1[vt{i}]']
    last, n = f'vt{i}', n + 1
for i, tel in enumerate(cfg['telops']):
    ins += ['-i', f'{ovdir}/telop_{i:02d}.png']
    fc.append(f"[{last}][{n}:v]overlay=enable='between(t,{tel['start']},{tel['end']})'[vs{i}]")
    last, n = f'vs{i}', n + 1
fc.append('[0:a]highpass=f=80,loudnorm=I=-14:TP=-1.5:LRA=11[a]')
sys.exit(subprocess.call(['ffmpeg', '-y', '-loglevel', 'error', '-stats', *ins,
       '-filter_complex', ';'.join(fc), '-map', f'[{last}]', '-map', '[a]',
       '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p',
       '-r', '60', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000',
       '-movflags', '+faststart', out]))
