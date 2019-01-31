# doc-cov 

doc-cov is a tool for measuring docstring coverage of Python project.

- Python versions >= 3.6 


## Quick start

1. Install doc-cov from pip.
2. Use `doccov PROJECT_PATH`

```
$ doccov tests/sample_project
---------   all    ---------
module       3 /   7 42.86%
```

## Options
### Target object
doc-cov can measure docstring coverage of functions, classes and modules.

#### functions (default, `-f`) 

```
$ doccov tests/sample_project -f
---------*coverage*---------
function     3 /   5 60.00%

```

#### classes `-c`

```
$ doccov tests/sample_project -c
---------*coverage*---------
class        2 /   2 100.00%

```

#### modules `-m`

```
$ doccov tests/sample_project -m
---------*coverage*---------
module       3 /   7 42.86%

```

### Output 

#### str (default, `--output str`)

```
$ doccov tests/sample_project -fmc --output str
---------*coverage*---------
function     3 /   5 60.00%
class        2 /   2 100.00%
module       3 /   7 42.86%
```

#### csv `--output csv`

```
$ doccov tests/sample_project -fmc --output csv
*coverage*,function,3,5,60.00%
*coverage*,class,2,2,100.00%
*coverage*,module,3,7,42.86%
```

### Target 
#### Print coverage of whole (default)

```
$ doccov tests/sample_project
---------*coverage*---------
module       3 /   7 42.86%
```  
#### Print all coverage of modules `--all`

```
$ docstring-coverage doccov tests/sample_project --all
---------module_fulldoc---------
module       1 /   1 100.00%
---------package_A ---------
module       1 /   1 100.00%
---------package_A.module_fulldoc---------
module       1 /   1 100.00%
---------package_B ---------
module       0 /   1 0.00%
---------package_B.module_shortdoc---------
module       0 /   1 0.00%
---------package_B.package_B_1---------
module       0 /   1 0.00%
---------package_B.package_B_1.module_nodoc---------
module       0 /   1 0.00%
---------*coverage*---------
module       3 /   7 42.86%

```
