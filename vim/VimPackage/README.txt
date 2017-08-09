snippetmate not working?
    - check for .vimrc for overriding "imap <tab>..." 
    - if so disable them

smart semicolon
inoremap ;<cr> <end>;<cr>
inoremap .<cr> <end>.
inoremap ;;<cr> <down><end>;<cr>
inoremap ..<cr> <down><end>.


pathogen solve the program of vim plugins. In orignal vim, all plugins should
be installed in separate folders under ~vim. pathogen allows each plugin to be
in its own folder - as a bundle. 

vunder extends pathogen one step further. With vunder, you no longer need to
download the plugin manually - specify your plugin in .vimrc and run
"PluginInstall", then all plugin are installed automatically.
