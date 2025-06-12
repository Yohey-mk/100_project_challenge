# install_mode.py
from argostranslate import package, translate
import os

available_packages = package.get_available_packages()
package.update_package_index()

for pkg in available_packages:
    if pkg.from_code == "en" and pkg.to_code == "ja":
        print("Downloading and installing mode:", pkg)
        download_path = pkg.download()
        package.install_from_path(download_path)
        break

else:
    print("No matching packge found.")