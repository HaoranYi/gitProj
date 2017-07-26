# Use conda to manage python package and python env.

## package management

go to https://anaconda.org to search package

```
    conda update conda
    conda list                   -- view packages for current env
    conda search beautifulsoup4  -- search for a package

    conda install --name test beautifulsoup4  -- install package, w.o name
                                              --  install to curr_env
    conda install --channel https://conda.ananconda.org/pandas bottleneck
                                              -- install from a channel
    conda remove --name test iopro         -- remove package from test env
```

## environment management
```
    conda create --name test YOUR_PROGRAM pkg1 pkg2
    conda info --envs  # list all env
    conda env list     # list all env

    activate test
    deactivate

    conda remove --name test --all   # remove test env
```

## share env with yaml
```
    conda env export > env.yaml
    conda env create -f env.yaml
```

## manage python
```
    conda create --name test python=3
```


## Jupyter notebook
```
    conda install jupyter
    jupyter notebook
```

1. run `setenv.bat` to add annaconda path.
2. run `r.bat` to start jupyter notebook.
