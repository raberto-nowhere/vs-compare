# Usage:
#   Set SOURCE and ENCODE variables and call either FinalRangeComparison()
#   or PreFinalRangeComparison()
#   FinalRangeComparison()   : Compare final encode against source
#   PreFinalRangeComparison(): Compare test encode against source
#            output = FinalRangeComparison()
#            output = PreFinalRangeComparison()
#            output.set_output()
#
# Thanks to someusername for this script

import vapoursynth as vs

core = vs.get_core()

SOURCE = 'source.mkv'
ENCODE = 'encode.mkv'
SOURCETEXT = 'SOURCE'
ENCODETEXT = 'ENCODE @ crfx'

# Return the source's video frames
def source():
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
  return select_frames(fill_border(crop(source(), t = top, b = bottom), t=1, b=1))

# Compare the source and encode!
# Arguments:
#  s = source
#  e = encode
#  croptop = crop black bars from top of source frame
#  cropbottom = crop black bars from bottom of source frame
def Compare(s, e, croptop, cropbottom):
  clips = []

  s = write_text(s, SOURCETEXT)
  clips.append(s)

  e = write_text(e, ENCODETEXT)
  clips.append(e)

  return core.std.Interleave(clips, mismatch=True)

# Calls Compare() on two sets of frames (test encode and source) when testing
# Arguments (both optional)
#   croptop: crop black bars from top of source frame
#   cropbottom: crop black bars from bottom of source frame
def PreFinalRangeComparison(croptop=0, cropbottom=0):
  s = SelectAndCropSource(croptop, cropbottom)
  return Compare(s, encode(), croptop, cropbottom)

# Calls Compare() two sets of frames after the final encode is done
# Arguments (both optional)
#   croptop: crop black bars from top of source frame
#   cropbottom: crop black bars from bottom of source frame
def FinalRangeComparison(croptop=0, cropbottom=0):
  s = source()
  s = crop(s, t=croptop, b=cropbottom)
  return Compare(s, encode(), croptop, cropbottom)

output = PreFinalRangeComparison()
output.set_output()
