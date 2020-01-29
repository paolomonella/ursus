" All system-wide defaults are set in $VIMRUNTIME/debian.vim and sourced by
" the call to :runtime you can find below.  If you wish to change any of those
" settings, you should do it in this file (/etc/vim/vimrc), since debian.vim
" will be overwritten everytime an upgrade of the vim packages is performed.
" It is recommended to make changes after sourcing debian.vim since it alters
" the value of the 'compatible' option.

" This line should not be removed as it ensures that various options are
" properly set to work with the Vim-related packages available in Debian.
runtime! debian.vim

" Uncomment the next line to make Vim more Vi-compatible
" NOTE: debian.vim sets 'nocompatible'.  Setting 'compatible' changes numerous
" options, so any other options should be set AFTER setting 'compatible'.
"set compatible

" Vim5 and later versions support syntax highlighting. Uncommenting the next
" line enables syntax highlighting by default.
if has("syntax")
  syntax on
endif

" If using a dark background within the editing area and syntax highlighting
" turn on this option as well
set background=dark

" Uncomment the following to have Vim jump to the last position when
" reopening a file
"if has("autocmd")
"  au BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$") | exe "normal! g'\"" | endif
"endif

" Ho inserito quanto segue per configurare il plugin xmledit
" e scegliere lo shortcut per l'autocompletamento dei tag in xml.
" Queste righe vanno inserite prima del comando 'ftplugin'
let xml_tag_completion_map = "<C-l>"
" let xml_jump_string = "`"

" Uncomment the following to have Vim load indentation rules and plugins
" according to the detected filetype.
if has("autocmd")
  filetype plugin indent on
endif

" The following are commented out as they cause vim to behave a lot
" differently from regular Vi. They are highly recommended though.
"set showcmd		" Show (partial) command in status line.
"set showmatch		" Show matching brackets.
set ignorecase		" Do case insensitive matching
"set smartcase		" Do smart case matching
"set incsearch		" Incremental search
"set autowrite		" Automatically save before commands like :next and :make
"set hidden		" Hide buffers when they are abandoned
"set mouse=a		" Enable mouse usage (all modes)

" Source a global configuration file if available
if filereadable("/etc/vim/vimrc.local")
  source /etc/vim/vimrc.local
endif

" Con queste due linee abilito il line folding per i file XML
"let g:xml_syntax_folding=1
"au FileType xml setlocal foldmethod=syntax
"

" Con le righe seguenti salvo le macro per la trascrizione di Orso
"
let @a='vyi,A,2,pam,o'
let @b='o§§§cicciobello§§§?<lbyy/§§§cicciobello§§§pkddf"f"i'
let @c=':w | ! /home/ilbuonme/ursus/ursusMarkDown.py'
"let @d=':set indentexpr=A0<pc type=",">·</pc>0f,'
let @d=':set indentexpr=o<pc type=",">·</pc>0f,'
let @e=':set indentexpr=i,÷,,est,o'
"let @f=':set indentexpr=A0<pc type=",">·</pc>o'
"let @f=':set indentexpr=A0<pc type=",">·</pc>o'
let @f=':set indentexpr=o<pc type=","></pc>0f,'
let @g='I<gap reason="illegible" quantity="f i" unit="lxea"/>o'
let @h='@wk0f>a<hi rend="larger">la</hi>0/larger'
"let @i='o<pc type=".">ï</pc>	<pc type="space"> </pc>k0f.'
let @i='/xml:idhd/>'
let @j='i<hi rend="larger">la</hi>0/larger'
let @k='a the source Priscian, Ars grammatica K.2..a'
let @m=':set indentexpr=o<milestone n="urn:cts:latinLit:stoa0234a.stoa001:2..xxx" type="source" unit="Keil"/>0fxcw'
let @n='o<note type="emendation">§</note>0f§xi'
"let @n='@wk0/<\/wi<note type="script">§</note>k0f§xi'
let @o='k0f0xj'
let @p='@wk0f"lvlhU'
"let @q=':set indentexpr=A0<pc type="quote">·</pc>o'
let @q=':set indentexpr=A0o<pc type="quote">·</pc>o'
let @r='I<ref cRef="Priscianus.Inst.K.2.53.8-Priscianus.Inst.K.2.53.12" type="source">0f"f"f"'
"let @s='o	<pc type="space"> </pc>o'
let @s='i	<pc type="space"> </pc>o'
let @t='@wk0f-xf-xik@b'
let @u='O<unclear cert="medium" reason="faded">jo</unclear>'
"let @x='@wk0f i type="alphabemes"'
let @v='0f"ld/"i,'
"let @v='i,ul,-,uel,0'
let @x='@wk0f i type="alphabemes"jdd2k@qdd@q2kf0xjo'
let @w=':set indentexpr=:s/v/u/geyypk:s/æ/ae/gej:s/ae/e/gekI<w n="A">JxA</w>	<pc type="space"> </pc>'
"let @z=':set indentexpr=o<pc type=",">·</pc>o'
"let @z=':set indentexpr=0f<i<note type="source">The source Priscian, Ars grammatica K.2._. has: </note>k0f_xi'
"let @z='?<w V/<\/wyPO<choice><sic>/<w nO</sic><corr cert="high">/<\/wo</corr></choice>?<notendd/<note cert="high"dd/<\/corrP?xml:idfx'
let @z=':set pastekjjddkkpkJxyypkO<choice><�kb	<sic>jI		o	</sc�kbic>o	<corr cert="high">jI		jI		/type=icert="high" o	</corr></choice>?choice>nO/xml:idn/"n'
