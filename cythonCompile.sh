BUILD_PATH="cython/"
BUILD_FLAG="$BUILD_PATH.compiled"
LIB_PATH="/usr/include/python"`python3 --version | grep -oP "3\.[0-9]{1,2}"`

rm -rf "$BUILD_PATH"
mkdir -p "$BUILD_PATH"

for file in `find . -name "*.py" -and -not -name "ScrabbleMain.py"`
do 
    echo "Compiling to c: $file"
    cython -3 "$file" -o "$BUILD_PATH`basename $file .py`.c"
done

cd "$BUILD_PATH"
for file in `find . -name "*.c"`
do 
    echo "Compiling to binary $file"
    gcc -O3 -fPIC -shared $file -I$LIB_PATH -o `basename $file .c`.so ; 
done
touch "__init__.py"
cd ..
