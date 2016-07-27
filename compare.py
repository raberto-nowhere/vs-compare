import vapoursynth as vs

core = vs.get_core()

SOURCE = 'source.mkv'
ENCODE = 'encode.mkv'

# Return the source's video frames
def remux():
  return core.ffms2.Source(SOURCE)

# Return the encode's video frames
def encode():
  return core.ffms2.Source(ENCODE)

def fill_border(clip, t=0, r=0, b=0, l=0):
 return core.fb.FillBorders(clip=clip, top=t, right=r, bottom=b, left=l, mode="fillmargins")

def crop(clip, t=0, r=0, b=0, l=0):
  return core.std.CropRel(clip=clip, top=t, right=r, bottom=b, left=l)

# Select frames for testing
def select_frames(clip):
  n = clip.num_frames
  clip_skipped = core.std.SelectEvery(clip, cycle = n, offsets = list(range(10000, n)))
  clip_new = core.std.SelectEvery(clip_skipped, cycle = 2000, offsets = list(range(0, 50)))
  return core.std.AssumeFPS(clip_new, clip)

# Write Info to frames
def write_text(clip, name):
  clip = core.text.Text(clip, text = name, alignment=1)
  clip = core.text.FrameNum(clip, alignment=8)
  return core.text.FrameProps(clip, ["_PictType"])

# Return source with cropped black bars
def SelectAndCropSource(top=0, bottom=0):
  return select_frames(fill_border(crop(remux(), t = top, b = bottom), t=1, b=1))

# Compare two sets of frames when testing
# Arguments (both optional)
#   croptop: crop black bars from top of source frame
#   cropbottom: crop black bars from bottom of source frame
def PreFinalRangeComparison(croptop=0, cropbottom=0):
  clips = []
  
  r = SelectAndCropSource(croptop, cropbottom)
  r = write_text(r, 'SOURCE')
  clips.append(r)
  
  clip = encode()
  clip = write_text(clip, 'ENCODE @ crf18.5')
  clips.append(clip)
  
  return core.std.Interleave(clips, mismatch=True)

# Compare two sets of frames after the final encode is done
# Arguments (both optional)
#   croptop: crop black bars from top of source frame
#   cropbottom: crop black bars from bottom of source frame
def FinalRangeComparison(croptop=0, cropbottom=0):
  clips = []

  r = remux()
  r = crop(r, t=croptop, b=cropbottom)
  r = write_text(r, 'SOURCE')
  clips.append(r)
  
  clip = encode()
  clip = write_text(clip, 'ENCODE @ crf18.5')
  clips.append(clip)
  
  return core.std.Interleave(clips, mismatch=True)
  
output = FinalRangeComparison()
output.set_output()