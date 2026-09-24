"""Composite overlays + color grade onto the source video with ffmpeg.
usage: python3 render.py SRC OVERLAY_DIR OUT [--still T TELOP_INDEX]"""
import json, subprocess, sys

src, ovdir, out = sys.argv[1:4]
cfg = json.load(open('telops.json', encoding='utf-8'))
GRADE = ("scale=1920:1080:flags=lanczos,"
         "eq=contrast=1.07:saturation=1.12:brightness=-0.01,"
         "vignette=angle=PI/5")

if '--still' in sys.argv:
    t, idx = float(sys.argv[-2]), int(sys.argv[-1])
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(t), '-i', src,
           '-i', f'{ovdir}/base.png', '-i', f'{ovdir}/telop_{idx:02d}.png',
           '-filter_complex', f'[0:v]{GRADE}[v];[v][1]overlay[a];[a][2]overlay',
           '-frames:v', '1', out]
    sys.exit(subprocess.call(cmd))

ins = ['-i', src, '-loop', '1', '-framerate', '60', '-i', f'{ovdir}/base.png']
fc = [f'[0:v]{GRADE}[g0]',
      # title + gradients fade in at 0.2s
      '[1:v]format=rgba,fade=t=in:st=0.2:d=0.6:alpha=1[base]',
      '[g0][base]overlay=shortest=1[v0]']
last = 'v0'
for i, tel in enumerate(cfg['telops']):
    ins += ['-i', f'{ovdir}/telop_{i:02d}.png']
    n = f'v{i+1}'
    fc.append(f"[{last}][{i+2}:v]overlay=enable='between(t,{tel['start']},{tel['end']})'[{n}]")
    last = n
fc.append('[0:a]highpass=f=80,loudnorm=I=-14:TP=-1.5:LRA=11[a]')
cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-stats', *ins,
       '-filter_complex', ';'.join(fc), '-map', f'[{last}]', '-map', '[a]',
       '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p',
       '-r', '60', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000',
       '-movflags', '+faststart', out]
sys.exit(subprocess.call(cmd))
