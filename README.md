# brutha

## Description

*brutha* is an answer to the utter failure of sound conversion tools.

It will flawlessly transcode lossless files or copy lossy files,
to a provided directory, with a "synchronization" behavior.

By carefully keeping the files' timestamps, it also allows that destination
to be easily rsynced elsewhere, and thus avoid any useless transfers.

Due to the usage of formats with Ogg containers, no tags are lost in the
process of converting FLAC to Ogg Vorbis.

Since transcoding requires a lot of CPU time, it is useful to run
as many jobs as possible in parallel. *brutha* will try to make use of
powerful, time-tested tools (either *GNU make*, *GNU parallel*,
or similar implementations) to do so.
It's not perfect but good enough while keeping it simple.

To our knowledge, no other solution can fully:

* avoid encoding again files that were already processed at an earlier run
* convert only lossless files (no lossy to lossy)
* keep the directory structure
* handle a huge number of files
* handle parallel job execution (and not crash)
* use the proper Ogg Vorbis settings (setting quality and not average bitrate)
* guarantee usage of the highest quality resampling algorithms
* save space for lossy files by using hardlinks or reflinks
* not be an annoying GUI

To sum up, *brutha* is a music converter tailored to audiophiles,
who want to convert their huge collections to more portable destinations,
with the highest quality/size ratio in mind.

*brutha* is very simple and rests on the shoulders of giants:
FLAC, Ogg Vorbis, sox, Python, mutagen, GNU Make, GNU Parallel, Bash, etc.

## Requirements

The first one is space. Since you can store locally all the source
files, we suppose you also can store the smaller destination files
locally. Alternatively, you will be able to sync to a portable player, a
remote filesystem (NFS, sshfs, etc.) without issues except lower
performance.

### Software requirements

* Python 3 (3.2 or later)
* [python-mutagen](http://pypi.python.org/pypi/mutagen)
* [sox](http://sox.sourceforge.net/)
* for parallel runs, either
  [GNU make](http://www.gnu.org/software/make/make.html) or
  [GNU parallel](http://www.gnu.org/software/parallel/) or
  a similar implementation

Optional:
* [vorbisgain](https://sjeng.org/vorbisgain.html) for `--gain`

## Usage

    brutha [options] SOURCE DESTINATION

`brutha -h` provides help for all available options.

You can run `python -m brutha` to use it without installing.

### Default values

*brutha* tries to detect how many cores you have
(run `brutha -h` to check the default for `-j`).
It also tries to use a parallel method
(`make` or `parallel` instead of `sh`) if available.

By default, it does not run or delete anything; when you are experienced
with its usage, you will likely call it with `-x` (execute) and `-d` (delete).

### Examples

A typical use would be:

    brutha -d -x -q6 -R44100 -B16 ~/Music /mnt/portable_music_player/Music

This downsamples music to 16/44 as most portable players don't handle
24/96 well (-R44100 -B16), encodes FLAC to Ogg at a reasonable quality (-q6),
deletes old unwanted files (-d), and executes the commands right away (-x).

### Recommendations

Since encoding eats a lot of CPU, you should start it at a low priority.
The simplest way is to run `nice -n19 brutha` instead of only *brutha*.

### Symbolic links

brutha ignores symbolic links by default, but can follow links outside
of the source path, or inside the source path, using options `--outside`
and `--inside`.

This is modelled after mpd's `follow_outside_symlinks` and
`follow_inside_symlinks` options.

## Changes

+ 1.1.1
  - Fix some corner cases with directory walking.
+ 1.1.0
  - Add sox option to guard against clipping.
  - Add options to create hardlinks or reflinks.
  - Make parallel the default if available.
  - Code and documentation improvements.
  - Support for newer parallel versions.
+ 1.0.2
  - Code improvements.
  - Show defaults in command-line help.
+ 1.0.1
  - Bugfixes.

## Future

*brutha* is considered feature-complete.

If you want to help, here are some possibilities:

* Support other formats (currently only FLAC to Ogg Vorbis, with Ogg
  Vorbis and MP3 as exact copies).
* Make mutagen optional (only required for frequency / bit depth checks).
* Support downmixing (5.1 to 2.0 for instance)

Contributions can be sent in the form of git patches, to
<laurent@bachelier.name>.
