  * rename pack to repack
  * move student directories into a subdirectory (submissions? students?) to avoid name conflicts
    with repacked archive.
  * move repacked archive into a subdirectory (repacked? read-to-upload? graded-archive?)
  * consider moving other folders out of .kodiak and into root of project
  * implement and test other cases of repack
    * oldest-only
    * newest-only
    * number-newer
    * number-older
  * should "unpack" be "import"?



#  factor out common stuff from commands

I think they have stuff in common because the both have do work on/with a Project. A Project
is the directory that contains all the submissions (packed and unpacked) for a single Kodiak
assignment download.

Project will know the structure of the project (where things belong), and will provide services
for querying its contents and basic, low-level, manipulation of files.
