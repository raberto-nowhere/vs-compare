import vapoursynth as vs

core = vs.get_core()

SOURCE = 'source.mkv'
ENCODE = 'encode.mkv'

def remux():
  return core.ffms2.Source(SOURCE)
  
def encode():
  return core.ffms2.Source(ENCODE)

def fill_border(clip, t=0, r=0, b=0, l=0):
 return core.fb.FillBorders(clip=clip, top=t, right=r, bottom=b, left=l, mode="fillmargins")

def crop(clip, t=0, r=0, b=0, l=0):
  return core.std.CropRel(clip=clip, top=t, right=r, bottom=b, left=l)

def select_frames(clip):
  n = clip.num_frames
  clip_skipped = core.std.SelectEvery(clip, cycle = n, offsets = list(range(10000, n)))
  clip_new = core.std.SelectEvery(clip_skipped, cycle = 2000, offsets = list(range(0, 50)))
  return core.std.AssumeFPS(clip_new, clip)

def write_text(clip, name):
  clip = core.text.Text(clip, text = name, alignment=1)
  clip = core.text.FrameNum(clip, alignment=8)
  return core.text.FrameProps(clip, ["_PictType"])

def final_source_old():
  return select_frames(fill_border(crop(remux(), t=20, b=20), t=1, b=1))

def final_source_new(top, bottom):
  return select_frames(fill_border(crop(remux(), t = top, b = bottom), t=1, b=1))

def final_encode():
  return select_frames(fill_border(encode()))
  
def compare():
  clips = []
  min = 16
  max = 31

  for i in range(min, max):
    x = 15 + 0.2 * i

    if i % 2 == 0:
      r = final_source_old()
      r = crop(r, t=2, b=2)
      r = write_text(r, 'Remux')
      clips.append(r)

    clip = core.ffms2.Source(ENCODE.format(x))
    clip = crop(clip, t=2, b=2)
    clip = write_text(clip, '{0}.mkv'.format(x))
    clips.append(clip)

  if (max - min - 1) % 2 == 0:
    r = final_source_old()
    r = crop(r, t=2, b=2)
    r = write_text(r, 'Remux')
    clips.append(r)

  return core.std.Interleave(clips, mismatch=True)

def comparet():
  clips = []
  
  r = final_source_new(0, 0)
  #r = crop(r, t=2, b=2)
  r = write_text(r, 'SOURCE')
  clips.append(r)
  
  clip = encode()
  #clip = crop(clip, t=20, b=20)
  clip = write_text(clip, 'ENCODE @ crf18.5')
  clips.append(clip)
  
  return core.std.Interleave(clips, mismatch=True)
  
output = comparet()
output.set_output()
