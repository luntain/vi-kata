set nocompatible

filetype plugin indent on

set encoding=utf-8
set fencs=ucs-bom,utf-8,cp1250
set shiftwidth=4
set tabstop=4
set expandtab
set visualbell
set noerrorbells
set ignorecase
set smartcase
set autoindent
set nocindent
set smartindent
set ruler
set incsearch		" do incremental searching
set whichwrap=<,>,h,l
set guioptions=a
set backspace=2
set history=50
set wildmenu
set nobackup
set langmenu=none
set guioptions-=T
set exrc " read _vimrc in current directory
set textwidth=76
set scrolloff=5
syntax on
set hlsearch
set noswapfile
" don't loose undo stack when leaving the buffer (edited file)
set hidden

" I sometime miss ctrl-[
inoremap <C-p> <Esc>
