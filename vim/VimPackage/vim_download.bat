REM "pathogen"
REM Install into the autoload folder
::git clone https://github.com/tpope/vim-pathogen.git
::mv pathogen.vim ~/vimfiles/autoload

REM "surround"
git clone https://github.com/tpope/vim-surround.git

REM "easymotion"
git clone https://github.com/Lokaltog/vim-easymotion.git

REM "syntastic"
git clone https://github.com/scrooloose/syntastic.git

REM "markdown syntax"
git clone https://github.com/plasticboy/vim-markdown

REM "sparkup"
git clone https://github.com/rstacruz/sparkup

REM "vim sparkup if sparkup not working (need to make a link of xml to html"
git clone https://github.com/tristen/vim-sparkup

REM "sinppet mate"
::git clone https://github.com/garbas/vim-snipmate.git
::git clone https://github.com/honza/vim-snippets.git
::git clone https://github.com/msanders/snipmate.vim.git 

REM "delimitmate
git clone https://github.com/Raimondi/delimitMate

REM "Markdown (if cygwin problem. set windows env CYGWIN=nodosfilewarning"
REM wget http://daringfireball.net/projects/downloads/Markdown_1.0.1.zip
curl http://daringfireball.net/projects/downloads/Markdown_1.0.1.zip -o markdown.zip

REM "ps1.vim
git clone https://github.com/PProvost/vim-ps1.git

REM "vim solarized"
git clone git://github.com/altercation/vim-colors-solarized.git

REM "type script syntax"
git clone https://github.com/leafgarland/typescript-vim.git 
