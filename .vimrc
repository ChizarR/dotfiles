" ------------
" -- BASICS --
" ------------
syntax on
" set cursorline
set colorcolumn=120
set mouse=a
set scrolloff=7
set updatetime=300
set path+=**
set clipboard=unnamedplus
set background=dark
set nowrap

set hlsearch
set ignorecase
set smartcase

" ----------
" -- TABS --
" ----------
set tabpagemax=5
set showtabline=2

" -----------
" -- SPLIT --
" -----------
set splitbelow
set splitright

" -----------
" -- FILES --
" -----------
set encoding=utf-8
set fileencoding=utf-8
set noswapfile
set nobackup
set nowritebackup
filetype plugin indent on

" -------------
" -- NUMBERS --
" -------------
set number
set relativenumber
set signcolumn=yes
set numberwidth=4

" ------------------
" -- TAB SETTINGS --
" ------------------
set expandtab
set smarttab
set tabstop=4
set shiftwidth=4

autocmd FileType html setlocal ts=2 sts=2 sw=2
autocmd FileType lua setlocal ts=2 sts=2 sw=2
autocmd FileType javascript setlocal ts=2 sts=2 sw=2
autocmd FileType typescript setlocal ts=2 sts=2 sw=2
autocmd FileType json setlocal ts=2 sts=2 sw=2
autocmd FileType cpp setlocal ts=2 sts=2 sw=2
autocmd FileType python setlocal colorcolumn=80

" ----------
" -- MAPS --
" ----------
" NERDTree
map <silent><SPACE>e :NERDTreeToggle<CR>

" Move between splited windows
noremap <C-h> <C-w>h 
noremap <C-j> <C-w>j 
noremap <C-k> <C-w>k 
noremap <C-l> <C-w>l 

" Resize splited window
noremap <silent> <C-Left> :vertical resize +2<CR>
noremap <silent> <C-Right> :vertical resize -2<CR>
noremap <silent> <C-Up> :resize +2<CR>
noremap <silent> <C-Down> :resize -2<CR>

" No hlsearch
nmap <silent><SPACE>, :nohlsearch<CR>

" Split windows
nmap <silent>ss :split<CR>
nmap <silent>sv :vsplit<CR>

inoremap " ""<left>
inoremap ' ''<left>
inoremap ( ()<left>
inoremap [ []<left>
inoremap { {}<left>
inoremap {<CR> {<CR>}<ESC>O
inoremap {;<CR> {<CR>};<ESC>O

" -------------
" -- PLUGINS --
" -------------
call plug#begin()
" coloschemes
  Plug 'morhetz/gruvbox'
  Plug 'kyoz/purify', { 'rtp': 'vim' }

  Plug 'preservim/nerdtree'
  Plug 'neoclide/coc.nvim', {'branch': 'release'}
  Plug 'fatih/vim-go', { 'do': ':GoUpdateBinaries' }
call plug#end()

" ----------------
" -- COC-CONFIG --
" ----------------
function! CheckBackspace() abort
  let col = col('.') - 1
  return !col || getline('.')[col - 1]  =~# '\s'
endfunction

" TAB for completition
inoremap <silent><expr> <TAB>
      \ coc#pum#visible() ? coc#pum#next(1) :
      \ CheckBackspace() ? "\<Tab>" :
      \ coc#refresh()
inoremap <expr><S-TAB> coc#pum#visible() ? coc#pum#prev(1) : "\<C-h>"

" Make <CR> to accept selected completion item or notify coc.nvim to format
" <C-g>u breaks current undo, please make your own choice
inoremap <silent><expr> <CR> coc#pum#visible() ? coc#pum#confirm()
                              \: "\<C-g>u\<CR>\<c-r>=coc#on_enter()\<CR>"


" ---------------------
" -- NERDTREE-CONFIG --
" ---------------------
let NERDTreeMinimalUI=1
let NERDTreeShowHidden=1
let NERDTreeShowLineNumbers=1
let g:NERDTreeWinSize=38

" -----------------
" -- COLORSCHEME --
" -----------------
colorscheme purify
