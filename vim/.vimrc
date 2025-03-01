" Basic Setup for Writing
set nocompatible              " Use Vim defaults
syntax enable                 " Enable syntax highlighting
set encoding=utf-8            " Use UTF-8 encoding
set fileencoding=utf-8        " Save files in UTF-8

" UI Configuration
set number                    " Show line numbers
set wrap                      " Wrap lines
set linebreak                 " Break lines at word boundaries
set showmatch                 " Highlight matching brackets
set laststatus=2              " Always show status line
set showcmd                   " Show command in bottom bar
set wildmenu                  " Visual autocomplete for command menu

" Writing-specific settings
set textwidth=80              " Line wrap at 80 characters
set colorcolumn=+1            " Highlight column after textwidth
set spell                     " Enable spell checking
set spelllang=en_us           " Set spell check language

" Text formatting
set tabstop=4                 " 4 space tab
set shiftwidth=4              " 4 space indentation
set softtabstop=4             " 4 space tab in insert mode
set autoindent                " Auto-indent new lines
set smartindent               " Smart autoindent when starting a new line

" Searching
set ignorecase                " Ignore case when searching
set smartcase                 " Become case sensitive when uppercase is used
set incsearch                 " Search as characters are entered
set hlsearch                  " Highlight search matches

" File management
set autoread                  " Reload files changed outside vim
set backup                    " Turn on backup
set backupdir=~/.vim/backup// " Store backups in specific directory
set directory=~/.vim/swap//   " Store swap files in specific directory
set undofile                  " Maintain undo history
set undodir=~/.vim/undo//     " Store undo files in specific directory

