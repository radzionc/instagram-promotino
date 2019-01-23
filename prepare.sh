virtualenv venv
source venv/bin/activate
pip install git+https://github.com/timgrossmann/InstaPy.git
latest_version=$(wget https://chromedriver.storage.googleapis.com/LATEST_RELEASE -O -)
wget https://chromedriver.storage.googleapis.com/${latest_version}/chromedriver_linux64.zip
unzip chromedriver_linux64
assets_path=venv/lib/python3.7/site-packages/assets
mkdir $assets_path
chromedriver_path=$assets_path/chromedriver
mv chromedriver $chromedriver_path
chmod +x $chromedriver_path
chmod 755 $chromedriver_path
rm -rf chromedriver_linux64