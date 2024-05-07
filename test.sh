pip install --upgrade pip
cd utilities
recursive_install () { # Parameter 1 is the directory to install into the "python" directory
    if [ ! -d "python/$1" ]; then # if directory already exists then we don't need to do it again
        pip install -r "$1/requirements.txt"
        rsync -av --exclude-from="$1/exclude_list.txt" $1 python
        while IFS="" read -r line || [ -n "$line" ]
            do
            recursive_install "$line"
        done <"$1/utils_requirements.txt"
    fi
}
dir_name="tpds_bleh"
mkdir python
python3 -m venv create_layer
source create_layer/bin/activate
recursive_install $dir_name
cp -r create_layer/lib python/
file_name="$(cat $dir_name/version.txt).zip"
zip -r $file_name python
S3_key=$environment/layers/$dir_name/$file_name