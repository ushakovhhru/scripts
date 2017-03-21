set -o vi

fullhostname="$(hostname -f)"
function c() {
  echo -n '\[\e[38;5;'
  echo -n "$1"
  echo -n 'm\]'
}
function x() {
  echo -n '\[\e[0m\]'
}
export PS1="$(c 64)\u$(x)@$(c 60)${fullhostname}$(x):$(c 197)\w$(c 96)\$ $(x)"
unset -f c x

export LESS="-X"

# made with make-dircolors
export LS_COLORS="rs=0:di=38;5;137:ln=38;5;244:mh=38;5;33:pi=38;5;33:so=38;5;33:do=38;5;33:bd=38;5;33:cd=38;5;33:or=38;5;9:su=38;5;33:sg=38;5;33:ca=38;5;33:tw=38;5;33:ow=38;5;33:st=38;5;33:ex=38;5;71:*.tar=38;5;24:*.tgz=38;5;24:*.arc=38;5;24:*.arj=38;5;24:*.taz=38;5;24:*.lha=38;5;24:*.lz4=38;5;24:*.lzh=38;5;24:*.lzma=38;5;24:*.tlz=38;5;24:*.txz=38;5;24:*.tzo=38;5;24:*.t7z=38;5;24:*.zip=38;5;24:*.z=38;5;24:*.Z=38;5;24:*.dz=38;5;24:*.gz=38;5;24:*.lrz=38;5;24:*.lz=38;5;24:*.lzo=38;5;24:*.xz=38;5;24:*.bz2=38;5;24:*.bz=38;5;24:*.tbz=38;5;24:*.tbz2=38;5;24:*.tz=38;5;24:*.deb=38;5;24:*.rpm=38;5;24:*.jar=38;5;24:*.war=38;5;24:*.ear=38;5;24:*.sar=38;5;24:*.rar=38;5;24:*.alz=38;5;24:*.ace=38;5;24:*.zoo=38;5;24:*.cpio=38;5;24:*.7z=38;5;24:*.rz=38;5;24:*.cab=38;5;24:*.jpg=38;5;133:*.jpeg=38;5;133:*.gif=38;5;133:*.bmp=38;5;133:*.pbm=38;5;133:*.pgm=38;5;133:*.ppm=38;5;133:*.tga=38;5;133:*.xbm=38;5;133:*.xpm=38;5;133:*.tif=38;5;133:*.tiff=38;5;133:*.png=38;5;133:*.svg=38;5;133:*.svgz=38;5;133:*.mng=38;5;133:*.pcx=38;5;133:*.mov=38;5;133:*.mpg=38;5;133:*.mpeg=38;5;133:*.m2v=38;5;133:*.mkv=38;5;133:*.webm=38;5;133:*.ogm=38;5;133:*.mp4=38;5;133:*.m4v=38;5;133:*.mp4v=38;5;133:*.vob=38;5;133:*.qt=38;5;133:*.nuv=38;5;133:*.wmv=38;5;133:*.asf=38;5;133:*.rm=38;5;133:*.rmvb=38;5;133:*.flc=38;5;133:*.avi=38;5;133:*.fli=38;5;133:*.flv=38;5;133:*.gl=38;5;133:*.dl=38;5;133:*.xcf=38;5;133:*.xwd=38;5;133:*.yuv=38;5;133:*.cgm=38;5;133:*.emf=38;5;133:*.axv=38;5;133:*.anx=38;5;133:*.ogv=38;5;133:*.ogx=38;5;133:*.aac=38;5;206:*.au=38;5;206:*.flac=38;5;206:*.m4a=38;5;206:*.mid=38;5;206:*.midi=38;5;206:*.mka=38;5;206:*.mp3=38;5;206:*.mpc=38;5;206:*.ogg=38;5;206:*.ra=38;5;206:*.wav=38;5;206:*.axa=38;5;206:*.oga=38;5;206:*.spx=38;5;206:*.xspf=38;5;206:"

export GREP_OPTIONS="--color=auto"
