Start the anaconda navigator
`/home/xmebhzero/anaconda3/bin/anaconda-navigator`

Create Conda Environment
```bash
conda create -n workshop_2nd numpy
```

Activate the new environment
```bash
conda activate workshop_2nd
```

Deactivate environment
```bash
conda deactivate
```

Delete conda environment
```bash
conda env remove --name example_env
```

Install dependencies (inside conda env)
```bash
conda install pandas
```

Exporting conda environment to conda server
```bash
conda env export > workshop_2nd.yml
```

Create new environment from exported environment
```bash
conda env create -f workshop_2nd.yml
```

Pypy environments
```bash
pyenv activate research-pypy
```