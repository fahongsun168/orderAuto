#!/bin/bash

# 使用 PyInstaller 打包 CrawLabels.py 为单文件格式
pyinstaller --onefile CrawLabels.py

# 检查是否成功生成了可执行文件
if [ -f "dist/CrawLabels" ] || [ -f "dist/CrawLabels.exe" ]; then
    echo "Executable successfully created."

    # 删除生成的 .spec 文件
    rm -f CrawLabels.spec
    echo ".spec file removed."

    # 删除 build 目录
    rm -rf build
    echo "build directory removed."

    mkdir -p dist/config dist/cookiefile
    echo "dist/config&dist/cookiefile directory created"

    scp ../../config/config.properties dist/config
    echo "config.properties copied"

    scp ../../config/logging.conf dist/config
    echo "logging.conf copied"

    scp ../../cookiefile/hktvmall.txt dist/cookiefile
    echo "hktvmall.txt copied"

    mkdir -p dist/logs
    echo "logs directory created"

    # 定义要替换的原始路径和新路径
    ORIGINAL_PATH="\/Users\/trimniu\/Downloads\/"
    NEW_PATH=".\/logs\/"

    # 替换配置文件中的路径
    sed -i '' "s/$ORIGINAL_PATH/$NEW_PATH/g" ./dist/config/logging.conf
    echo "logging.conf log directory modified"
else
    echo "Executable creation failed. Check for errors in the output."
fi
